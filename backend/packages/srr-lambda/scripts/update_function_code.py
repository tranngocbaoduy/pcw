import re
import argparse
import os
import sys
import time 
import json

file_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(file_dir + '/..')
helper_dir = os.path.abspath(root_dir + '/../..')   
sys.path.append(os.path.normpath(helper_dir)) 

from packages.util.LambdaHelper import LambdaHelper

parser = argparse.ArgumentParser()
parser.add_argument('--force', action='store_true')
parser.add_argument('env_name', type=LambdaHelper.env_regex_type)
parser.add_argument('--project-name', default='pcw')
parser.add_argument('--profile', default='pcw-admin-us')
parser.add_argument('--use-container', action='store_true')
parser.add_argument('--skip-build', action='store_true')
parser.add_argument('--skip-upload', action='store_true')

args = vars(parser.parse_args())  
start_time = time.time() 

print(args)
helper = LambdaHelper(root_dir=root_dir,args=args) 

if not args['skip_build']:
    helper.build_function()

if not args['skip_upload']: 
    helper.upload_to_s3()

helper.update_function_code()
    
print('Elapsed time: {} seconds -- {}'.format(int(time.time() - start_time), os.path.realpath(__file__)))  # nopep8