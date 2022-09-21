import argparse
import datetime
import json
import os
import re
import subprocess
import sys
import time

import boto3 

# import deploy_dynamodb_tables
# import deploy_waf

file_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(file_dir + '/..')
sys.path.append(os.path.normpath(root_dir)) 

from utils.AWSHelper import AWSHelper

parser = argparse.ArgumentParser()
parser.add_argument('--force', action='store_true')
parser.add_argument('env_name',
                    type=lambda x, pattern=r'^[a-z]{1,32}$': x if re.compile(pattern).match(x) else (_ for _ in ()).throw(argparse.ArgumentTypeError('must match ' + pattern)))
parser.add_argument('--project-name', default='pcw')
parser.add_argument('--profile', default='pcw-admin-us')
parser.add_argument('--template-filename', default='pcw-us.template')  
parser.add_argument('--detach-vpc', action='store_true') 
parser.add_argument('--skip-version', action='store_true') 

args = vars(parser.parse_args()) 
env_type = 'dev' if not args['env_name'] in ['prod', 'staging', 'canary', 'prestaging'] else args['env_name']

start_time = time.time() 

session = boto3.Session(profile_name=args['profile'])
cloudformation_client = session.client('cloudformation') 
s3_client = session.client('s3') 

main_stack_name = '{}-{}'.format(args['project_name'], args['env_name'])
source_bucket_name = '{}-source-bucket'.format(main_stack_name)
 
cur_version = ''
try:
    cur_stack_parameters = cloudformation_client.describe_stacks(StackName=main_stack_name)['Stacks'][0]['Parameters']
    cur_version = next((x for x in cur_stack_parameters if x['ParameterKey'] == 'Version'), {}).get('ParameterValue', '')
except:
    pass 

version = ''
if args['skip_version'] and cur_version:
    version = cur_version
else:
    version = (datetime.datetime.utcnow().replace(microsecond=0).isoformat() + 'Z').replace(':', '_')

def deploy_template(): 
    __version = 'latest'
    template_parameters_map = {
        'EnvName': args['env_name'],
        'EnvType': env_type, 
        'SesRegion': 'us-east-1',
        'VpcEnabled': 'true' if not args['detach_vpc'] else 'false',
        'Version': __version, 
        'StageName': 'dev',  
    } 
    print('deploy_template', template_parameters_map)
    template_parameters_str = ' '.join(['{}={}'.format(key, template_parameters_map[key]) for key in template_parameters_map])
    ans = s3_client.put_object(Bucket=source_bucket_name, Key='template-parameters/{}/main.json'.format(version), Body=json.dumps(template_parameters_map, indent=2))
    
    AWSHelper.run_command(' '.join([
        "aws",
        "cloudformation",
        "deploy",
        "--template-file={}".format(root_dir + '/templates/' + args['template_filename']),
        "--s3-bucket={}-{}-source-bucket".format(args['project_name'], args['env_name']),  # nopep8
        "--s3-prefix=templates/main/{}".format(version),
        "--stack-name={}".format(main_stack_name),
        "--parameter-overrides",
        template_parameters_str,
        "--capabilities=CAPABILITY_IAM",
        "--tags",
        "env={}".format(args['env_name']),
        '--profile={}'.format(args['profile'])
    ]))
 
deploy_template()
 

print('Elapsed time: {} seconds -- {}'.format(int(time.time() - start_time), os.path.realpath(__file__)))  # nopep8