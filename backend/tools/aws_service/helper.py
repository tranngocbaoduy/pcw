import os
import re
import sys
import shutil
import json
import subprocess
import glob
from datetime import datetime, date


class S3Helper(object):
    def __init__(self, root_dir, args):
        self.root_dir = root_dir
        self.args = args
        self.env_name = args["env_name"]
        self.profile = args["profile"] if args.get("profile") else "pcw-admin"
        self.project_name = args["project_name"] if args.get("project_name") else "pcw"

        # load config file
        self.config = self.get_config_file()

        pass

    def get_build_dir_func(self):
        return os.path.join(
            self.root_dir, os.path.splitext(self.config["function_zip_rpath"])[0]
        )

    def get_config_file(self):
        with open(os.path.join(self.root_dir, "config.json")) as f:
            config = json.load(f)
        return config

    def copy_zip_function_to(self, build_dir_func):
        shutil.copytree(
            os.path.join(self.root_dir, "function"),
            build_dir_func,
            ignore=shutil.ignore_patterns(".aws-sam", "node_modules"),
        )

    def copy_data_to(self, data_finished_dir):
        shutil.copytree(
            os.path.join(self.root_dir, "data/raw"),
            os.path.join(self.root_dir, data_finished_dir),
            ignore=shutil.ignore_patterns(".aws-sam", "node_modules"),
            dirs_exist_ok=True,
        )

    def remove_old_data(self):
        print("Remove old file")
        for domain_path in glob.glob(self.root_dir + "/data/raw/*"):
            if os.path.exists(domain_path):
                shutil.rmtree(domain_path, ignore_errors=True)

    def is_exist_data(self, page_item):
        dst_dir = os.path.join(
            self.root_dir, "data/goods", page_item["PK"], page_item["SK"]
        )
        if not os.path.exists(dst_dir):
            return False
        return True

    def write_handled_data(self, new_goods_item):
        today = str(date.today())
        dst_dir = os.path.join(
            self.root_dir,
            "data/pre-goods",
            today,
            new_goods_item["CATEGORY"],
            new_goods_item["PK"],
            new_goods_item["SK"],
        )

        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        else:
            return
        with open("{}/index.json".format(dst_dir), "w", encoding="utf-8") as f:
            json.dump(new_goods_item, f, ensure_ascii=False, indent=4)

    def use_env(self, env):
        env = env if env else self.env_name
        src_file = self.root_dir + "/function/.env.{}.local".format(env)
        if not os.path.exists(src_file):
            src_file = self.root_dir + "/function/.env.{}".format(env)
            pass
        shutil.copyfile(src_file, self.root_dir + "/function/.env")

    def build_function(self):
        print("Build zip file")
        command = " ".join(
            [
                sys.executable,
                os.path.join(self.root_dir, "build.py"),
                "--use-container" if self.args["use_container"] else "",
            ]
        )
        S3Helper.run_command(command)

    def make_archive(self, build_dir_func):
        shutil.make_archive(build_dir_func, "zip", build_dir_func)

    def upload_to_s3(self):
        print("Upload to S3")
        command = " ".join(
            [
                "aws",
                "s3",
                "cp",
                os.path.join(self.root_dir, self.config["function_zip_rpath"]),
                "s3://{}-{}-data-bucket/{}".format(
                    self.project_name,
                    self.env_name,
                    os.path.basename(self.config["function_name"]),
                ),
                "--profile={}".format(self.profile),
                "--recursive",
            ]
        )
        S3Helper.run_command(command)

    def remove_old_files(self):
        print("Remove old file")
        for domain_path in glob.glob(self.root_dir + "/function/*"):
            if os.path.exists(domain_path):
                shutil.rmtree(domain_path, ignore_errors=True)

    @staticmethod
    def copyfile(src, dst):
        print(
            "copyfile from {} to {}".format(os.path.abspath(src), os.path.abspath(dst))
        )
        dst_dir = os.path.dirname(dst)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        shutil.copyfile(src, dst)

    @staticmethod
    def env_regex_type(arg_value):
        pattern = r"^[a-zA-Z]{0,32}$"
        if not re.compile(pattern).match(arg_value):
            raise argparse.ArgumentTypeError(arg_value + "\nenv must match " + pattern)
        return arg_value

    @staticmethod
    def run_parallel(
        commands=[],
        batch_size=3,
        allow_errors=[],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ):
        outputs = []
        while len(commands) > 0:
            cmd_group = commands[:batch_size]
            commands = commands[batch_size:]
            ps = []
            for cmd in cmd_group:
                print("> " + cmd)
                p = subprocess.Popen(cmd, shell=True, stdout=stdout, stderr=stderr)
                ps.append(p)
            for p in ps:
                out, err = p.communicate()
                if out is not None:
                    print(out.decode("utf-8"))
                if err is not None:
                    print(err.decode("utf-8"))
                print(
                    '"{}" run finished with status: {}'.format(
                        cmd_group[ps.index(p)], p.returncode
                    )
                )
                outputs.append(out)
            exit_codes = [p.returncode for p in ps]
            for exit_code in exit_codes:
                if (exit_code != 0) & (exit_code not in allow_errors):
                    sys.exit(exit_code)
        return outputs

    @staticmethod
    def run_command(command, allow_errors=[]):
        print("> " + command)
        status = os.system(command)
        print('"{}" run finished with status: {}'.format(command, status))
        if (status != 0) & (status not in allow_errors):
            sys.exit(status)
