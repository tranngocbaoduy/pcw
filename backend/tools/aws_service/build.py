import re
import argparse
import os
import sys
import shutil
import time
import json
import glob

file_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(file_dir + "/../..")
sys.path.append(os.path.normpath(root_dir))

from tools.aws_service.helper import S3Helper

parser = argparse.ArgumentParser()
parser.add_argument("--env-name", type=S3Helper.env_regex_type, default="dev")
parser.add_argument("--use-container", action="store_true")

args = vars(parser.parse_args())

start_time = time.time()

helper = S3Helper(root_dir=root_dir + "/tools/aws_service", args=args)

# handle setting environment for upload
helper.use_env(args["env_name"] if args["env_name"] else "dev")

build_dir_func = helper.get_build_dir_func()
if os.path.exists(build_dir_func):
    shutil.rmtree(build_dir_func)

# handle copy function to build/function
helper.copy_zip_function_to(build_dir_func)

# make archive function
for domain_path in glob.glob(build_dir_func + "/*"):
    for url_path in glob.glob(domain_path + "/*"):
        for version_path in glob.glob(url_path + "/*"):
            helper.make_archive(version_path)
            if os.path.exists(version_path):
                shutil.rmtree(version_path, ignore_errors=True)


print(
    "Elapsed time: {} seconds -- {}".format(
        int(time.time() - start_time), os.path.realpath(__file__)
    )
)  # nopep8
