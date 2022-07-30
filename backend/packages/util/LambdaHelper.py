import os
import re
import sys
import shutil
import json
import subprocess

class LambdaHelper(object):

    def __init__(self, root_dir, args):
        self.root_dir = root_dir 
        self.args = args
        self.env_name = args['env_name']
        self.profile = args['profile'] if args.get('profile') else 'pcw-admin'
        self.project_name = args['project_name'] if args.get('project_name') else 'pcw'

        # load config file
        self.config = self.get_config_file()

        pass
 
    def get_build_dir_func(self):
        return os.path.join(self.root_dir, os.path.splitext(self.config['function_zip_rpath'])[0])

    def get_config_file(self):
        with open(os.path.join(self.root_dir, 'scripts/config.json')) as f:
            config = json.load(f)
        return config 

    def copy_function_to(self,build_dir_func):
        shutil.copytree(os.path.join(self.root_dir, 'function'), 
                build_dir_func, ignore=shutil.ignore_patterns('.aws-sam', 'node_modules'))

    def use_env(self, env):  
        env = env if env else self.env_name
        src_file = self.root_dir + '/function/.env.{}.local'.format(env)
        if not os.path.exists(src_file):
            src_file = self.root_dir + '/function/.env.{}'.format(env)
            pass
        shutil.copyfile(src_file, self.root_dir + '/function/.env')  

    def build_function(self):
        command = ' '.join([
            sys.executable,
            os.path.join(self.root_dir, "scripts/build.py"),
            '--use-container' if self.args['use_container'] else ''
        ])
        LambdaHelper.run_command(command)

    def make_archive(self, build_dir_func): 
        for function_name in self.config['function_names']:
            zip_dir_upload = os.path.join(build_dir_func, function_name)
            zip_dir_local = os.path.join(build_dir_func, self.get_local_name_function(function_name)) 
            if (os.path.isdir(zip_dir_local)):  
                shutil.make_archive(zip_dir_upload, 'zip', zip_dir_local)

    def get_local_name_function(self, name):
        return name.lower().replace('function','')

    def upload_to_s3(self):
        for function_name in self.config['function_names']:
            command = ' '.join([
                "aws",
                "s3",
                "cp",
                os.path.join(self.root_dir, self.config['function_zip_rpath'] + function_name + '.zip'),
                "s3://{}-{}-source-bucket/packages/lastest/{}".format(
                    self.project_name, self.env_name, os.path.basename(self.config['function_zip_rpath'] + function_name + '.zip')),
                "--profile={}".format(self.profile)
            ])
            LambdaHelper.run_command(command)

    def update_function_code(self):
        commands = []
        for function_name in self.config['function_names']:
            commands.append(' '.join([
                "aws",
                "lambda",
                "update-function-code",
                "--function-name={}-{}-{}".format(
                    self.project_name, self.env_name, function_name),
                "--s3-bucket={}-{}-source-bucket".format(
                    self.project_name, self.env_name),
                "--s3-key=packages/lastest/{}".format(os.path.basename(self.config['function_zip_rpath'] + function_name + '.zip')),
                "--profile={}".format(self.profile)
            ]))
        LambdaHelper.run_parallel(commands)

    @staticmethod
    def copyfile(src, dst):
        print('copyfile from {} to {}'.format(
            os.path.abspath(src), os.path.abspath(dst)))
        dst_dir = os.path.dirname(dst)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        shutil.copyfile(src, dst)

    @staticmethod
    def env_regex_type(arg_value):
        pattern = r"^[a-zA-Z]{0,32}$"
        if not re.compile(pattern).match(arg_value):
            raise argparse.ArgumentTypeError(
                arg_value + '\nenv must match ' + pattern)
        return arg_value    

    @staticmethod
    def run_parallel(commands=[], batch_size=3, allow_errors=[], stdout=subprocess.PIPE, stderr=subprocess.PIPE):
        outputs = []
        while len(commands) > 0:
            cmd_group = commands[:batch_size]
            commands = commands[batch_size:]
            ps = []
            for cmd in cmd_group:
                print('> ' + cmd)
                p = subprocess.Popen(cmd, shell=True, stdout=stdout, stderr=stderr)
                ps.append(p)
            for p in ps:
                out, err = p.communicate()
                if (out is not None):
                    print(out.decode('utf-8'))
                if (err is not None):
                    print(err.decode('utf-8'))
                print('"{}" run finished with status: {}'.format(
                    cmd_group[ps.index(p)], p.returncode))
                outputs.append(out)
            exit_codes = [p.returncode for p in ps]
            for exit_code in exit_codes:
                if ((exit_code != 0) & (exit_code not in allow_errors)):
                    sys.exit(exit_code)
        return outputs

    @staticmethod
    def run_command(command, allow_errors=[]):
        print('> ' + command)
        status = os.system(command)
        print('"{}" run finished with status: {}'.format(command, status))
        if ((status != 0) & (status not in allow_errors)):
            sys.exit(status)
