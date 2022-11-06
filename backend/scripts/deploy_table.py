import re
import argparse
import os
import sys
import time
import boto3

file_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(file_dir + "/..")
sys.path.append(os.path.normpath(root_dir))

from utils.AWSHelper import AWSHelper


def init(args):
    if __name__ == "__main__":
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "env_name",
            type=lambda x, pattern=r"^[a-z]{1,32}$": x
            if re.compile(pattern).match(x)
            else (_ for _ in ()).throw(
                argparse.ArgumentTypeError("must match " + pattern)
            ),
        )
        parser.add_argument("--project-name", default="pcw")
        parser.add_argument("--profile", default="pcw-admin")
        parser.add_argument("--template-filename", default="dynamodb-tables.template")

        args = vars(parser.parse_args())

    global template_file
    template_file = root_dir + "/templates/" + args["template_filename"]

    global main_stack_name
    main_stack_name = "{}-{}".format(args["project_name"], args["env_name"])

    global session
    session = boto3.Session(profile_name=args["profile"])

    global cur_version
    cur_version = ""
    try:
        cur_stack_parameters = session.client("cloudformation").describe_stacks(
            StackName=main_stack_name
        )["Stacks"][0]["Parameters"]
        cur_version = next(
            (x for x in cur_stack_parameters if x["ParameterKey"] == "Version"), {}
        ).get("ParameterValue", "")
    except:
        pass

    return args


def main(args={}):
    args = init(args)

    start_time = time.time()

    template_parameters_map = {
        "CategoryTableName": "{}-CATEGORY".format(main_stack_name),
        "ProductTableName": "{}-PRODUCT".format(main_stack_name),
        "UserTableName": "{}-USER".format(main_stack_name),
    }

    AWSHelper.run_command(
        " ".join(
            [
                "aws",
                "cloudformation",
                "deploy",
                "--template-file={}".format(template_file),
                "--stack-name={}-dynamodb-tables".format(main_stack_name),
                "--parameter-overrides",
                " ".join(
                    [
                        "{}={}".format(key, template_parameters_map[key])
                        for key in template_parameters_map
                    ]
                ),
                "--tags",
                "env={}".format(args["env_name"]),
                "--profile={}".format(args["profile"]),
            ]
        )
    )

    print(
        "Elapsed time: {} seconds -- {}".format(
            int(time.time() - start_time), os.path.realpath(__file__)
        )
    )  # nopep8


if __name__ == "__main__":
    main()
