import re
import argparse
import os
import sys
import shutil


def env_regex_type(arg_value):
    pattern = r"^[a-zA-Z]{0,32}$"
    if not re.compile(pattern).match(arg_value):
        raise argparse.ArgumentTypeError(arg_value + "\nenv must match " + pattern)
    return arg_value


parser = argparse.ArgumentParser()
parser.add_argument("env", type=env_regex_type)

args = vars(parser.parse_args())

file_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(file_dir + "/..")


def run_command(command, allow_errors=[]):
    print("> " + command)
    status = os.system(command)
    print('"{}" run finished with status: {}'.format(command, status))
    if (status != 0) & (status not in allow_errors):
        sys.exit(status)


env_path = os.path.join(root_dir, ".env.{}".format(args["env"]))
if os.path.exists(env_path + ".local"):
    env_path = env_path + ".local"
    pass
shutil.copyfile(env_path, os.path.join(root_dir, ".env"))
