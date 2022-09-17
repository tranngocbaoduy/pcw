import re
import argparse
import os
import sys
import shutil
import time
import json
import datetime
import boto3

# add directory to path 
file_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(file_dir + '/..')
sys.path.append(os.path.normpath(root_dir)) 

from utils.AWSHelper import AWSHelper

def init(args):
    if __name__ == '__main__':
        parser = argparse.ArgumentParser()
        parser.add_argument('env_name',
                            type=lambda x, pattern=r'^[a-z]{1,32}$': x if re.compile(pattern).match(x) else (_ for _ in ()).throw(argparse.ArgumentTypeError('must match ' + pattern)))
        parser.add_argument('--project-name', default='pcw')
        parser.add_argument('--profile', default='pcw-admin-us')
        parser.add_argument('--version', default=(datetime.datetime.utcnow().replace(microsecond=0).isoformat() + 'Z').replace(':', '_'))
        parser.add_argument('--only-template', action='store_true')
        parser.add_argument('--skip-build', action='store_true')

        args = vars(parser.parse_args())

    if (args['only_template']):
        args['skip_build'] = True

    global main_stack_name
    main_stack_name = '{}-{}'.format(args['project_name'], args['env_name'])

    global source_bucket_name
    source_bucket_name = '{}-source-bucket'.format(main_stack_name)

    # global tenants_bucket_name
    # tenants_bucket_name = '{}-tenants-bucket'.format(main_stack_name)

    global session
    session = boto3.Session(profile_name=args['profile'])

    return args


def main(args={}):
    args = init(args)

    start_time = time.time()

    if (not args['skip_build']):
        global source_bucket_local_dir
        source_bucket_local_dir = root_dir + '/build/.packages/{}'.format(args['env_name'])
        if (os.path.exists(source_bucket_local_dir)):
            shutil.rmtree(source_bucket_local_dir)



        packages_dir = root_dir + '/packages'
        package_dirnames = [item for item in os.listdir(packages_dir)
                            if item.endswith('-lambda')]
        # package_dirnames = []

        ignore_dirnames = ['util']

        for dirname in package_dirnames:
            if (dirname in ignore_dirnames):
                continue

            package_config_file = os.path.abspath(os.path.join(packages_dir,
                                                               dirname,
                                                               'scripts/config.json'))
            if not os.path.exists(package_config_file):
                print('"{}" is not exist'.format(package_config_file))
                continue
            with open(os.path.join(packages_dir, dirname, 'scripts/config.json')) as f:
                config = json.load(f)
                AWSHelper.copy_file(os.path.join(packages_dir, dirname, config['function_zip_rpath']),
                         os.path.join(source_bucket_local_dir, os.path.basename(config['function_zip_rpath']))) 

    # is_exists_tenants_bucket = False
    # try:
    #     session.client('s3').head_bucket(Bucket=tenants_bucket_name)
    #     is_exists_tenants_bucket = True
    # except:
    #     is_exists_tenants_bucket = False
    #     pass

    template_parameters_map = {
        'SourceBucketName': source_bucket_name,
        'LogBucketName': '{}-log-bucket'.format(main_stack_name),
        'DataBucketName': '{}-data-bucket'.format(main_stack_name)
    }
    # if (not is_exists_tenants_bucket):
    #     template_parameters_map['TenantsBucketName'] = tenants_bucket_name
    template_parameters_str = ' '.join(['{}={}'.format(key, template_parameters_map[key]) for key in template_parameters_map])

    AWSHelper.run_command(' '.join([
        "aws",
        "cloudformation",
        "deploy",
        "--template-file={}".format(os.path.join(root_dir, 'templates/source-bucket.template')),
        "--stack-name={}-{}-source-bucket".format(args['project_name'], args['env_name']),
        "--parameter-overrides",
        template_parameters_str,
        "--tags",
        "env={}".format(args['env_name']),
        "--profile={}".format(args['profile'])
    ]), [])

    if (not args['skip_build']):
        time.sleep(5)

        version = args['version']
        AWSHelper.run_command(' '.join([
            "aws",
            "s3",
            "cp",
            source_bucket_local_dir,
            's3://{}/packages/{}'.format(source_bucket_name, version),
            "--recursive",
            "--profile={}".format(args['profile'])
        ]))
        AWSHelper.run_command(' '.join([
            "aws",
            "s3",
            "cp",
            's3://{}/packages/{}'.format(source_bucket_name, version),
            's3://{}/packages/latest'.format(source_bucket_name),
            "--recursive",
            "--profile={}".format(args['profile'])
        ]))

    print('Elapsed time: {} seconds -- {}'.format(int(time.time() - start_time), os.path.realpath(__file__)))  # nopep8


if __name__ == '__main__':
    main()
