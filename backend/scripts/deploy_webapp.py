import re
import argparse
import os
import sys
import shutil
import time
import subprocess
import json
import boto3
import datetime

file_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(file_dir + '/..')
sys.path.append(os.path.normpath(root_dir)) 

from utils.AWSHelper import AWSHelper
 
parser = argparse.ArgumentParser()
parser.add_argument('--force', action='store_true')
parser.add_argument('env_name',
                    type=lambda x, pattern=r'^[a-z]{1,32}$': x if re.compile(pattern).match(x) else (_ for _ in ()).throw(argparse.ArgumentTypeError('must match ' + pattern)))
parser.add_argument('--project-name', default='pcw')
parser.add_argument('--profile', default='pcw-admin')
parser.add_argument('--skip-build', action='store_true')
parser.add_argument('--skip-upload', action='store_true')
# parser.add_argument('--use-env-name-waf', action='store_true')
# parser.add_argument('--skip-basic-auth', action='store_true')
# parser.add_argument('--maintenance', action='store_true')
parser.add_argument('--only-template', action='store_true')

args = vars(parser.parse_args())
if (args['only_template']):
    args['skip_upload'] = True
# if (args['env_name'] == 'prod'):
    # args['skip_basic_auth'] = True
if (args['skip_upload']):
    args['skip_build'] = True

env_type = 'dev' if not args['env_name'] in ['prod', 'staging', 'canary', 'prestaging'] else args['env_name']

file_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(file_dir + '/..')


# if not args['force']:
#     def confirm(message):
#         try:
#             if (raw_input(message + ' [Y/N]? ').lower().strip() != 'y'):
#                 sys.exit(0)
#         except NameError:
#             if (input(message + ' [Y/N]? ').lower().strip() != 'y'):
#                 sys.exit(0)
#             pass

#     if (args['env_name'] == 'prod' or args['env_name'] == 'staging' or args['env_name'] == 'canary'):
#         confirm('Are you sure you want to continue deploy {}'.format(args['env_name']))
#     branchname = re.compile('## (.*)\s').search(subprocess.check_output('git status -b -s', shell=True, cwd=root_dir).decode("utf-8")).group(1)
#     if (args['env_name'] == 'prod' and not branchname.startswith('master') or
#         args['env_name'] == 'staging' and not branchname.startswith('develop') or
#             args['env_name'] == 'canary' and not (branchname.startswith('hotfix') or branchname.startswith('release'))):
#         print('Invalid branch {} for deploy {}'.format(branchname, args['env_name']))
#         confirm('Are you sure you want to continue deploy {} from branch {}'.format(args['env_name'], branchname))



start_time = time.time()

session = boto3.Session(profile_name=args['profile'])
cloudformation_client = session.client('cloudformation')
s3_client = session.client('s3')
cloudfront_client = session.client('cloudfront')

main_stack_name = '{}-{}'.format(args['project_name'], args['env_name']) 
source_bucket_name = '{}-source-bucket'.format(main_stack_name) 

webapp_dir = os.path.abspath(root_dir + '/../web-app')
webapp_bucket_name = '{}-webapp-bucket'.format(main_stack_name)
webapp_bucket_local_dir = os.path.join(root_dir, 'build/webapp-bucket/{}'.format(args['env_name']))
dist_dir = webapp_dir + '/dist'
# maintenance_html_path = os.path.join(dist_dir, 'maintenance/index.html')
print('webapp_bucket_local_dir',webapp_bucket_local_dir)
cur_stack_parameters = None
cur_stack_outputs = None
cur_version = ''
rest_api_base_url = ''

try:
    cur_stack_parameters = cloudformation_client.describe_stacks(StackName=main_stack_name)['Stacks'][0]['Parameters']
    cur_version = next((x for x in cur_stack_parameters if x['ParameterKey'] == 'Version'), {}).get('ParameterValue', '')
    cur_stack_outputs = cloudformation_client.describe_stacks(StackName=main_stack_name)['Stacks'][0]['Outputs']
    rest_api_base_url = next(item['OutputValue'] for item in cur_stack_outputs if item['OutputKey'] == 'RestApiBaseUrl')
except:
    pass

version = cur_version + '.' + (datetime.datetime.utcnow().replace(microsecond=0).isoformat() + 'Z').replace(':', '_')

if not args['skip_build']:
#     AWSHelper.run_command(' '.join([
#         sys.executable,
#         root_dir + "/scripts/update_webapp_env.py",
#         args['env_name'],
#         '--env=production',
#         '--profile',
#         args['profile']
#     ]))
    
#     # Run generate personal agreement pdf script
#     # personal_agreement_script_filename = os.path.join(root_dir, 'scripts/js/generate_personal_agreement_pdf.js')
#     # AWSHelper.run_command(' '.join([
#     #     "node",
#     #     personal_agreement_script_filename,
#     #     "--env_name={}".format(args['env_name'])
#     # ]))

    AWSHelper.run_command(' '.join([
        "npm",
        "run",
        "build",
        "--prefix",
        webapp_dir
    ]))

#     with open(maintenance_html_path, encoding='utf-8') as f:
#         s = f.read()
#         s = s.replace("VUE_APP_API_BASE_URL", rest_api_base_url)
#     with open(maintenance_html_path, "w", encoding='utf-8') as f:
#         f.write(s)

#     shutil.copy2(dist_dir + '/file/landing_page.html', dist_dir + '/lp')
#     shutil.copy2(dist_dir + '/index.html', dist_dir + '/sys-admin')


def upload_webapp():
    AWSHelper.copy_file(dist_dir, webapp_bucket_local_dir)

    AWSHelper.run_command(' '.join([
        "aws",
        "s3",
        "cp",
        webapp_bucket_local_dir,
        "s3://" + source_bucket_name + '/webapp/' + version,
        "--recursive",
        "--cache-control max-age=0",
        "--profile={}".format(args['profile'])
    ])) 
    AWSHelper.run_command(' '.join([
        "aws",
        "s3",
        "rm",
        "s3://" + webapp_bucket_name,
        "--recursive",
        "--profile={}".format(args['profile'])
    ]))
    AWSHelper.run_command(' '.join([
        "aws",
        "s3",
        "cp",
        "s3://" + source_bucket_name + '/webapp/' + version,
        "s3://" + webapp_bucket_name,
        "--recursive",
        "--profile={}".format(args['profile'])
    ]))


# def update_file_metadata():
#     lp_source_key = 'webapp/' + version + '/lp'
#     print('lp_source_key', lp_source_key)
#     s3_client.copy_object(Key=lp_source_key, Bucket=source_bucket_name,
#                           ContentType='text/html',
#                           CopySource={"Bucket": source_bucket_name, "Key": lp_source_key},
#                           MetadataDirective="REPLACE")
#     sys_admin_source_key = 'webapp/' + version + '/sys-admin'
#     s3_client.copy_object(Key=sys_admin_source_key, Bucket=source_bucket_name,
#                           ContentType='text/html',
#                           CopySource={"Bucket": source_bucket_name, "Key": sys_admin_source_key},
#                           MetadataDirective="REPLACE")


is_bucket_exists = False
try:
    s3_client.head_bucket(Bucket=webapp_bucket_name)
    is_bucket_exists = True
except:
    pass

if not args['skip_upload'] and is_bucket_exists:
    upload_webapp()

# waf_env_name = env_type if not args['use_env_name_waf'] else args['env_name']
# waf_stack_name = '{}-{}-waf-cloudfront'.format(args['project_name'], waf_env_name)
web_acl_arn = ''
try:
    waf_stack_outputs = session.client('cloudformation', region_name='ap-southeast-1').describe_stacks(StackName=waf_stack_name)['Stacks'][0]['Outputs']
    web_acl_arn = next((x for x in waf_stack_outputs if x['OutputKey'] == 'WebACLArn'), None)['OutputValue']
except:
    pass
  
AWSHelper.run_command(' '.join([
    "aws",
    "cloudformation",
    "deploy",
    "--template-file={}".format(os.path.join(root_dir, 'templates/webapp-bucket.template')),
    "--stack-name={}-{}-webapp-bucket".format(args['project_name'], args['env_name']),
    "--parameter-overrides",
    "EnvName={}".format(args['env_name']),
    "EnvType={}".format(env_type),
    "WebappBucketName={}".format(webapp_bucket_name),
    "WebACLArn={}".format(web_acl_arn),
    # "BasicAuthFunctionVersionArn={}".format(basic_auth_version_arn),
    # "MaintenanceState={}".format('ENABLED' if args['maintenance'] else 'DISABLED'),
    "--tags",
    "env={}".format(args['env_name']),
    "--profile={}".format(args['profile'])
]), [])

if not args['skip_upload'] and not is_bucket_exists:
    time.sleep(15)
    upload_webapp()

print('Elapsed time: {} seconds -- {}'.format(int(time.time() - start_time), os.path.realpath(__file__)))  
