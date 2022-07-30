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
parser.add_argument('--profile', default='pcw-admin')
parser.add_argument('--template-filename', default='pcw.template')
parser.add_argument('--dynamodb-tables-template-filename', default='dynamodb-tables.template')
# parser.add_argument('--use-container', action='store_true')
# parser.add_argument('--skip-build', action='store_true')
# parser.add_argument('--skip-build-layer', action='store_true')
# parser.add_argument('--skip-deploy-source-bucket', action='store_true')
parser.add_argument('--detach-vpc', action='store_true')
# parser.add_argument('--update-function-code', action='store_true')
# parser.add_argument('--deploy-webapp', action='store_true')
# parser.add_argument('--only-template', action='store_true')
# parser.add_argument('--skip-default-layer', action='store_true')
# parser.add_argument('--update-default-layer', action='store_true')
parser.add_argument('--skip-version', action='store_true')
# parser.add_argument('--deploy-layer', action='store_true')
# parser.add_argument('--use-env-name-waf', action='store_true')
# parser.add_argument('--update-waf', action='store_true')

args = vars(parser.parse_args())
# if (args['only_template']):
#     args['skip_deploy_source_bucket'] = True
#     args['skip_default_layer'] = True
#     args['skip_version'] = True
# if (args['skip_deploy_source_bucket']):
#     args['skip_build'] = True
# if (args['skip_version'] and not args['only_template']):
#     args['update_function_code'] = True

# if (args['update_default_layer']):
#     args['skip_default_layer'] = False

env_type = 'dev' if not args['env_name'] in ['prod', 'staging', 'canary', 'prestaging'] else args['env_name']
# if (env_type != 'dev'):
#     args['update_waf'] = True

# # if not args['force']:
# #     def confirm(message):
# #         if (input(message + ' [Y/N]? ').lower().strip() != 'y'):
# #             sys.exit(0)

# #     if (args['env_name'] == 'prod' or args['env_name'] == 'staging' or args['env_name'] == 'canary'):
# #         confirm('Are you sure you want to continue deploy {}'.format(args['env_name']))
# #     branchname = re.compile('## (.*)\s').search(subprocess.check_output('git status -b -s', shell=True, cwd=root_dir).decode("utf-8")).group(1)
# #     if (args['env_name'] == 'prod' and not branchname.startswith('master') or
# #         args['env_name'] == 'staging' and not branchname.startswith('develop') or
# #             args['env_name'] == 'canary' and not (branchname.startswith('hotfix') or branchname.startswith('release'))):
# #         print('Invalid branch {} for deploy {}'.format(branchname, args['env_name']))
# #         confirm('Are you sure you want to continue deploy {} from branch {}'.format(args['env_name'], branchname))
 

start_time = time.time()

session = boto3.Session(profile_name=args['profile'])
cloudformation_client = session.client('cloudformation')
# apigateway_client = session.client('apigateway')
# lambda_client = session.client('lambda')
s3_client = session.client('s3')
# ssm_client = session.client('ssm')

main_stack_name = '{}-{}'.format(args['project_name'], args['env_name'])
source_bucket_name = '{}-source-bucket'.format(main_stack_name)

cur_version = ''
try:
    cur_stack_parameters = cloudformation_client.describe_stacks(StackName=main_stack_name)['Stacks'][0]['Parameters']
    cur_version = next((x for x in cur_stack_parameters if x['ParameterKey'] == 'Version'), {}).get('ParameterValue', '')
except:
    pass

# if (cur_version and cur_version < '2020-12-31T05_43_03.952Z'):
#     args['skip_deploy_source_bucket'] = False
#     args['skip_default_layer'] = False
#     args['skip_version'] = False

version = ''
if args['skip_version'] and cur_version:
    version = cur_version
else:
    version = (datetime.datetime.utcnow().replace(microsecond=0).isoformat() + 'Z').replace(':', '_')

# stripe.api_key = ssm_client.get_parameter(Name='{}-stripe-secret-key-secure'.format(env_type), WithDecryption=True)['Parameter']['Value']


# def get_latest_layer_version_arn(layer_name):
#     try:
#         return lambda_client.list_layer_versions(LayerName=layer_name)['LayerVersions'][0]['LayerVersionArn']
#     except:
#         return None


# def deploy_default_layer():
#     default_lambda_layer_nodejs12x_version_arn = ''
#     if (args['skip_default_layer']):
#         try:
#             default_lambda_layer_nodejs12x_version_arn = get_latest_layer_version_arn('{}-DefaultLambdaLayerNodejs12x'.format(main_stack_name))
#         except:
#             pass
#     if (not default_lambda_layer_nodejs12x_version_arn):
#         run_command(' '.join([
#             sys.executable,
#             os.path.abspath(os.path.join(root_dir, "../packages/default-lambda-layer/nodejs12.x/scripts/publish_layer_version.py")),
#             '--force',
#             args['env_name'],
#             '--project-name={}'.format(args['project_name']),
#             '--profile={}'.format(args['profile']),
#             '--skip-build' if args['skip_build_layer'] else ''
#         ]))
#         default_lambda_layer_nodejs12x_version_arn = lambda_client.list_layer_versions(LayerName='{}-DefaultLambdaLayerNodejs12x'.format(main_stack_name))['LayerVersions'][0]['LayerVersionArn']
#     return default_lambda_layer_nodejs12x_version_arn


# def get_ssm_parameter_name_version(name):
#     try:
#         parameter = ssm_client.get_parameter(Name=name)['Parameter']
#         return str(parameter['Name']) + ':' + str(parameter['Version'])
#     except:
#         return None


# def get_ssm_parameter_ref(name):
#     try:
#         parameter = ssm_client.get_parameter(Name=name)['Parameter']
#         return '{{resolve:ssm:' + str(parameter['Name']) + ':' + str(parameter['Version']) + '}}'
#     except:
#         return None


# # def get_template_parameter_layers_map():
# #     layers_map = {
# #         'DefaultLambdaLayerNodejs12xVersionArn': deploy_default_layer(),
# #         'LighthouseFunctionLayerVersionArn': get_latest_layer_version_arn('{}-LighthouseFunctionLayer'.format(main_stack_name)),
# #         'QualityFunctionLayerVersionArn': get_latest_layer_version_arn('{}-QualityFunctionLayer'.format(main_stack_name)),
# #         'SitemapGeneratorFunctionLayerVersionArn': get_latest_layer_version_arn('{}-SitemapGeneratorFunctionLayer'.format(main_stack_name)),
# #         'ThumbnailGeneratorFunctionLayerVersionArn': get_latest_layer_version_arn('{}-ThumbnailGeneratorFunctionLayer'.format(main_stack_name)),
# #         'LayoutImageDiffFunctionLayerVersionArn': get_latest_layer_version_arn('{}-LayoutImageDiffFunctionLayer'.format(main_stack_name)),
# #         'SpellingInconsistenciesFunctionLayerVersionArn': get_latest_layer_version_arn('{}-SpellingInconsistenciesFunctionLayer'.format(main_stack_name)),
# #     }
# #     return layers_map 

def get_web_acl_arn():
    waf_env_name = env_type if not args['use_env_name_waf'] else args['env_name']

    if (not args['update_waf']):
        try:
            waf_stack_outputs = cloudformation_client.describe_stacks(StackName='{}-{}-waf-regional'.format(args['project_name'], waf_env_name))['Stacks'][0]['Outputs']
            web_acl_arn = next((x for x in waf_stack_outputs if x['OutputKey'] == 'WebACLArn'), None)['OutputValue']
            return web_acl_arn
        except:
            pass

    deploy_waf.main({
        'force': True,
        'env_name': waf_env_name,
        'project_name': args['project_name'],
        'profile': args['profile'],
    })
    waf_stack_outputs = cloudformation_client.describe_stacks(StackName='{}-{}-waf-regional'.format(args['project_name'], waf_env_name))['Stacks'][0]['Outputs']
    web_acl_arn = next((x for x in waf_stack_outputs if x['OutputKey'] == 'WebACLArn'), None)['OutputValue']
    return web_acl_arn


def deploy_template(): 
    __version = 'lastest'
    template_parameters_map = {
        'EnvName': args['env_name'],
        'EnvType': env_type,
        'DynamodbTablesStackName': '{}-dynamodb-tables'.format(main_stack_name), 
        'SesRegion': 'us-east-1',
        'VpcEnabled': 'true' if not args['detach_vpc'] else 'false',
        'Version': __version, 
        # 'WebACLArn': get_web_acl_arn(),
        # **template_parameter_layers_map,
    } 
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

#     if (cur_version and cur_version < '2020-12-31T05_43_03.952Z'):
#         deploy_dynamodb_tables.main({
#             'force': True,
#             'env_name': args['env_name'],
#             'project_name': args['project_name'],
#             'profile': args['profile'],
#             'template_filename': args['dynamodb_tables_template_filename'],
#             'remove_invoices_table': True,
#         })
#         deploy_dynamodb_tables.main({
#             'force': True,
#             'env_name': args['env_name'],
#             'project_name': args['project_name'],
#             'profile': args['profile'],
#             'template_filename': args['dynamodb_tables_template_filename'],
#         })

#     print('Waiting for api deployment to be created..')
#     stack_outputs = cloudformation_client.describe_stacks(StackName=main_stack_name)['Stacks'][0]['Outputs']
#     rest_api_id = next((x for x in stack_outputs if x['OutputKey'] == 'RestApiId'), None)['OutputValue']
#     apigateway_client.create_deployment(restApiId=rest_api_id, stageName=args['env_name'])
#     print('Successfully created api deployment')

#     if (update_webhook_endpoint_id):
#         rest_api_base_url = next((x for x in stack_outputs if x['OutputKey'] == 'RestApiBaseUrl'), None)['OutputValue']
#         stripe.WebhookEndpoint.modify(
#             update_webhook_endpoint_id,
#             url=rest_api_base_url + '/webhook'
#         )


# if not args['skip_build']:
#     run_command(' '.join([
#         sys.executable,
#         root_dir + '/scripts/build_all_functions.py',
#         '--use-container' if args['use_container'] else ''
#     ]))

# # if not args['skip_deploy_source_bucket']:
# #     run_command(' '.join([
# #         sys.executable,
# #         root_dir + '/scripts/deploy_source_bucket.py',
# #         args['env_name'],
# #         '--project-name={}'.format(args['project_name']),
# #         '--profile={}'.format(args['profile']),
# #         '--version={}'.format(version)
# #     ]))
# # elif not args['skip_version']:
# #     run_command(' '.join([
# #         "aws",
# #         "s3",
# #         "cp",
# #         's3://{}-source-bucket/packages/latest'.format(main_stack_name),
# #         's3://{}-source-bucket/packages/{}'.format(main_stack_name, version),
# #         "--recursive",
# #         "--profile={}".format(args['profile'])
# #     ]))

# # template_parameter_layers_map = get_template_parameter_layers_map()
# # missing_layer_names = []
# # for key in template_parameter_layers_map:
# #     if (template_parameter_layers_map[key] is None):
# #         missing_layer_names.append(key.replace('VersionArn', ''))
# # if args['deploy_layer'] or missing_layer_names:
# #     run_command(' '.join([
# #         sys.executable,
# #         root_dir + '/scripts/publish_layer_version.py',
# #         '--force',
# #         args['env_name'],
# #         '--project-name={}'.format(args['project_name']),
# #         '--profile={}'.format(args['profile']),
# #         '--skip-update-function-code',
# #         '--only {}'.format(','.join(missing_layer_names)) if not args['deploy_layer'] else ''
# #     ]))
# #     template_parameter_layers_map = get_template_parameter_layers_map()

deploy_template()

# # if args['update_function_code']:
# #     run_command(' '.join([
# #         sys.executable,
# #         root_dir + "/scripts/update_function_code.py",
# #         '--force',
# #         args['env_name'],
# #         '--project-name={}'.format(args['project_name']),
# #         '--profile={}'.format(args['profile']),
# #         '--skip-build',
# #         '--skip-upload',
# #     ]))
 
# # if (env_type == 'dev'):
# #     run_command(' '.join([
# #         sys.executable,
# #         root_dir + "/scripts/update_webapp_env.py",
# #         args['env_name'],
# #         '--profile',
# #         args['profile']
# #     ]))
# # if (not cur_version):
# #     run_command(' '.join([
# #         'node',
# #         root_dir + '/patches/update-system-weighting-data.js',
# #         '--env_name',
# #         args['env_name'],
# #         '--profile',
# #         args['profile']
# #     ]))

# # if args['deploy_webapp']:
# #     run_command(' '.join([
# #         sys.executable,
# #         root_dir + '/scripts/deploy_webapp.py',
# #         '--force',
# #         args['env_name'],
# #         '--project-name={}'.format(args['project_name']),
# #         '--profile={}'.format(args['profile'])
# #     ]))


print('Elapsed time: {} seconds -- {}'.format(int(time.time() - start_time), os.path.realpath(__file__)))  # nopep8