import os.path
import sys

changed_files_string = sys.argv[1]
changed_files = changed_files_string.split()

MODIFICATION_LIMIT = 5

IGNORED_NAMES = ("sanity-checks", "topology_validation_rules", "")


def get_modified_test_lines(paths):
    test_lines = set([path.split('/')[0] for path in changed_files if '/' in path])
    return test_lines - set(IGNORED_NAMES)


modified_test_lines = get_modified_test_lines(changed_files)
exit_code = 1 if len(modified_test_lines) > MODIFICATION_LIMIT else 0

if exit_code != 0:
    complaint = (
        "WARNING: Modifying more than {} test line configs should be approved by a Code Guard!".format(MODIFICATION_LIMIT)
    )
    print(complaint)
    print("Modifications in {} test lines:\n{}".format(len(modified_test_lines), "\n".join(sorted(modified_test_lines))))

exit(exit_code)
