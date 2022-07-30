import re
import argparse
import os
import sys
import shutil
import time
import json 
 
file_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(file_dir + '/..')
helper_dir = os.path.abspath(root_dir + '/../..')   
sys.path.append(os.path.normpath(helper_dir)) 

from packages.util.LambdaHelper import LambdaHelper

parser = argparse.ArgumentParser()
parser.add_argument('--env-name', type=LambdaHelper.env_regex_type, default='dev')
parser.add_argument('--use-container', action='store_true')

args = vars(parser.parse_args())

start_time = time.time()

helper = LambdaHelper(root_dir=root_dir,args=args)

# handle setting environment for upload
helper.use_env( args['env_name'] if args['env_name'] else 'dev') 

build_dir = root_dir + '/.aws-sam/build'

# LambdaHelper.run_command(' '.join([
#     sys.executable,
#     root_dir + '/scripts/use_env.py {}'.format(args['env_name'])
# ]))

LambdaHelper.run_command(' '.join([
    'sam',
    'build',
    '--template',
    root_dir + '/template.yaml',
    '--build-dir',
    build_dir,
    '--use-container' if args['use_container'] else ''
]))

# LambdaHelper.run_command(' '.join([
#     sys.executable,
#     root_dir + '/scripts/use_env.py dev'
# ]))

build_dir_func = helper.get_build_dir_func()

print(build_dir_func)
if (os.path.exists(build_dir_func)):
    shutil.rmtree(build_dir_func)
# handle copy function to build/function
helper.copy_function_to(build_dir_func)

# # make archive function

# print('make_archive ' + build_dir_func + '.zip')
helper.make_archive(build_dir_func)

print('Elapsed time: {} seconds -- {}'.format(int(time.time() - start_time), os.path.realpath(__file__)))  # nopep8