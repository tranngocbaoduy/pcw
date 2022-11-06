import os
import sys
import shutil
import json
import time
import subprocess


class AWSHelper:
    @staticmethod
    def run_command(command, allow_errors=[]):
        print("> " + command)
        status = os.system(command)
        print('"{}" run finished with status: {}'.format(command, status))
        if (status != 0) & (status not in allow_errors):
            sys.exit(status)

    @staticmethod
    def copy_file(src, dst):
        dst_dir = os.path.dirname(dst)
        if not os.path.isdir(dst_dir):
            os.makedirs(dst_dir)
        if os.path.exists(dst_dir):
            shutil.rmtree(dst_dir)
        if os.path.isdir(src):
            shutil.copytree(src, dst)

    @staticmethod
    def get_stack_outputs(stack_name, profile="pcw-admin"):
        command = " ".join(
            [
                "aws",
                "cloudformation",
                "describe-stacks",
                "--stack-name={}".format(stack_name),
                "--query",
                '"Stacks[0].Outputs"',
                "--output",
                "json",
                "--profile={}".format(profile),
            ]
        )
        print("> " + command)
        outputs = json.loads(
            subprocess.check_output(command, shell=True).decode("utf-8")
        )
        result = {}
        for ouput in outputs:
            result[ouput["OutputKey"]] = ouput["OutputValue"]
        print(json.dumps(result, indent=2))
        return result
