import importlib
import os
import sys
from pathlib import Path

from ute_testline_configuration.loader import Loader


changed_files_string = sys.argv[1]
changed_files = changed_files_string.split()
config_files = [f for f in changed_files if f.endswith('__init__.py')]

repo_root = Path(__file__).parent / ".."
sys.path.insert(0, str(repo_root.absolute()))


def validate(path):
    config = import_by_path(path)
    if hasattr(config, 'UTE_CONFIG'):
        print('>>> Validating UTE configuration: {}'.format(path))
        validate_ute_config(config)
        print('[OK]\n')
    else:
        print('Not a UTE configuration file\n')
    sys.modules.pop('__init__')


def validate_ute_config(config):
    loader = Loader()
    try:
        loader.validate_config_module(config)
    except Exception as e:
        print(e)  # ConfigNotValid error with msg "Errors found in testline configuration."
        exit(1)


def _import(module_name):
    try:
        return importlib.reload(__import__(module_name, fromlist=()))
    except ImportError as e:
        print(e)
        print('Could not import configuration file')
        exit(1)


def import_by_path(path):
    module_dir, module_file = os.path.split(os.path.abspath(path))
    print('module_dir: {}\nmodule_file: {}'.format(module_dir, module_file))
    sys.path.insert(0, module_dir)
    try:
        return _import(module_name='__init__')
    finally:
        sys.path.remove(module_dir)


if not config_files:
    print('[OK] No test line configuration files to validate')
    exit(0)

for cfg in config_files:
    if os.path.exists(cfg):
        validate(cfg)
    # else it means the configuration is being deleted
