"""
Script prepares a regex pattern for Black so that it checks only specific files.

For example for $CHANGED_FILES list
.gitlab-ci.yml
2_16_CLOUD853/__init__.py
7_16_UTE5GCLOUD1/__init__.py
sanity-checks/mypy.sh
sanity-checks/ute_config.py

it will produce the following pattern:

2_16_CLOUD853/__init__.py$|7_16_UTE5GCLOUD1/__init__.py$

"""

import sys


changed_files_string = sys.argv[1]
changed_files = changed_files_string.split()
pattern = "|".join([f + "$" for f in changed_files if f.endswith("__init__.py")])
print(pattern)
