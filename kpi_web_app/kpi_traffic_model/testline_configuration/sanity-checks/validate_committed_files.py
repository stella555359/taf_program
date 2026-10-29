import os
import re
import sys
from pathlib import Path

from binaryornot.check import is_binary


class Check(object):
    def __init__(self, changed_files):
        self.changed_files = changed_files
        self.rc = None
        self.msg = ''

    def run(self):
        raise NotImplementedError


class CorrectFileNames(Check):
    def __init__(self, changed_files, pattern):
        self.pattern = pattern
        super(CorrectFileNames, self).__init__(changed_files)

    def is_incorrect(self, name):
        return re.match(self.pattern, name) is None

    def run(self):
        incorrect_names = list(filter(self.is_incorrect, self.changed_files))
        self.rc = 1 if incorrect_names else 0

        if self.rc:
            complaint = "File names should only contain characters, digits, dots, underscores or dashes.\n"
            details = "Incorrect file/directory name(s): '{}'".format("', '".join(incorrect_names))
            self.msg = complaint + details

        return self.rc


class EmptyFilesCheck(Check):

    def empty_files(self, paths):
        def is_empty_file(path):
            return os.path.getsize(path) == 0

        return list(filter(is_empty_file, paths))

    def run(self):
        existing_changed_files = filter(os.path.exists, self.changed_files)
        bad_paths = self.empty_files(existing_changed_files)
        self.rc = 1 if bad_paths else 0

        if self.rc:
            complaint = "Please do not commit empty files.\n"
            details = "Prohibited files:\n{}".format("\n".join(bad_paths))
            self.msg = complaint + details

        return self.rc


class ProhibitedFilesCheck(Check):
    TEST_LINE_PATTERN = r"([0-9]+)_([0-9]+)_([a-zA-Z0-9_]+)"
    LEGACY_QT_TEST_LINE_PATTERN = r"QT_(WRO|HZ|HGZ|TSR)_(TL|CLASS)\d+_\w+"
    NEW_QT_TEST_LINE_PATTERN = r"QT_(\w+)_[A-Z]+_?(\d+)(C|E)?"
    FILENAME_PATTERN = r"^[.a-zA-Z0-9_-]+$"
    ALLOWED_EXTENSIONS = [".yaml", ".yml", ".sce", ".sid", ".env", ".xml"]
    ADDITIONAL_ALLOWED_FILES_PATTERN = [
        r"^README.md$",
        r"^CONTRIBUTING.md$",
        r"^requirements.cfg$",
        r"^{tl}/__init__\.py$".format(tl=TEST_LINE_PATTERN),
        r"^{tl}/__init__\.py$".format(tl=LEGACY_QT_TEST_LINE_PATTERN),
        r"^{tl}/__init__\.py$".format(tl=NEW_QT_TEST_LINE_PATTERN),
        r"^\.gitignore$",
        r"^topology_validation_rules/.*",
        r"^common/.*\.py$",
    ]

    def filter_out_allowed_files(self, file_paths):
        """
        Filter out paths to files with allowed extensions
        """
        return [
            path
            for path in file_paths
            if not any(
                re.match(pattern, path) for pattern in self.ADDITIONAL_ALLOWED_FILES_PATTERN
            )
        ]

    def find_files_with_not_allowed_extensions(self, paths):
        """
        Filter out paths to files with allowed extensions
        """
        return [
            path for path in paths if os.path.splitext(path)[1] not in self.ALLOWED_EXTENSIONS
        ]

    def filter_directories(self, path):
        """
        Get all directories in path except root dir and check to filename pattern
        """
        drop_root_dir_and_filename = slice(1, -1)
        return all(
            re.match(self.FILENAME_PATTERN, directory)
            for directory in path[drop_root_dir_and_filename]
        )

    def find_not_allowed_files_and_directories(self, paths):
        """
        Filter out paths for which all checks are True (returned list contains files which do not match all patterns)

        Split the path, do the following separate checks:
        * test line match `test_line_pattern`
        * directories match `filename_pattern`
        * files match `filename_pattern`
        """

        def is_allowed(path):
            path, ext = os.path.splitext(path)
            path_as_list = path.split(os.sep)
            test_line_name_match = re.match(self.TEST_LINE_PATTERN, path_as_list[0])
            legacy_test_line_name_match = re.match(self.LEGACY_QT_TEST_LINE_PATTERN, path_as_list[0])
            new_test_line_name_match = re.match(self.NEW_QT_TEST_LINE_PATTERN, path_as_list[0])
            directories_match = self.filter_directories(path_as_list)
            filename_match = re.match(
                self.FILENAME_PATTERN, os.path.splitext(path_as_list[-1])[0]
            )

            if ((test_line_name_match or
                 legacy_test_line_name_match or
                 new_test_line_name_match) and directories_match and filename_match):
                return True
            return False

        return [path for path in paths if not is_allowed(path)]

    def run(self):
        existing_changed_files = [f for f in self.changed_files if os.path.exists(f)]
        files_to_be_checked = self.filter_out_allowed_files(existing_changed_files)
        wrong_paths = set(
            self.find_files_with_not_allowed_extensions(files_to_be_checked) +
            self.find_not_allowed_files_and_directories(files_to_be_checked)
        )

        self.rc = 1 if wrong_paths else 0
        if self.rc:
            complaint = (
                "Please do not commit any files that are not essential.\n"
                "The only file extensions allowed inside the test line "
                "configuration are: {}.\n".format(", ".join(self.ALLOWED_EXTENSIONS))
            )
            details = "Prohibited files (not allowed extensions or paths):\n{}".format("\n".join(wrong_paths))

            self.msg = complaint + details

        return self.rc


class BinaryOrLogFilesCheck(Check):
    ROBOT_FILE_NAMES = ("output.xml", "log.html", "report.html")
    IGNORED_FILE_NAMES = ("/COMMIT_MSG",)

    def _is_robot_file(self, path):
        filename = os.path.basename(path)
        return filename in self.ROBOT_FILE_NAMES

    def prohibited_files(self, paths):
        bad_paths = []

        for path in paths:
            if path in self.IGNORED_FILE_NAMES:
                continue
            elif is_binary(path) or self._is_robot_file(path):
                bad_paths.append(path)
        return bad_paths

    def run(self):
        existing_changed_files = filter(os.path.exists, self.changed_files)
        bad_paths = self.prohibited_files(existing_changed_files)
        self.rc = 1 if len(bad_paths) else 0

        if self.rc:
            complaint = (
                "Please do not add any binary files or RobotFramework logs. "
                "Most of the time it is unnecessary.\n"
                "If you really have to add a file that breaks this check, "
                "contact the repository maintainers first.\n"
            )
            details = "Prohibited files:\n{}".format("\n".join(bad_paths))
            self.msg = complaint + details

        return self.rc


class CommonDirSymlinkCheck(Check):
    def run(self):
        existing_changed_files = filter(os.path.exists, self.changed_files)
        bad_paths = []
        for path in existing_changed_files:
            if not self.is_common_dir_symlink(path):
                bad_paths.append(path)

        self.rc = 1 if bad_paths else 0

        if self.rc:
            complaint = (
                "The 'common' file in each TL directory should be a symlink to "
                "the common parts directory (../common).\n"
            )
            details = "'common' files that don't symlink to the common dir:\n{}".format(
                "\n".join(bad_paths)
            )
            self.msg = complaint + details

        return self.rc

    @staticmethod
    def is_common_dir_symlink(path):
        path = Path(path)
        if path.is_symlink() and path.resolve() == Path("./common").resolve():
            return True
        else:
            return False


def filter_out_common_symlink_paths(changed_files):
    common_dir_symlink_paths = []
    other_paths = []
    for path in changed_files:
        if os.path.basename(path) == "common":
            common_dir_symlink_paths.append(path)
        else:
            other_paths.append(path)
    return common_dir_symlink_paths, other_paths


def verify(changed_files):
    changed_files = changed_files.split("\n")
    changed_files = [f for f in changed_files if not f.endswith('.gitkeep')]

    common_symlink_paths, changed_files = filter_out_common_symlink_paths(changed_files)

    checks = (EmptyFilesCheck(changed_files),
              ProhibitedFilesCheck(changed_files),
              BinaryOrLogFilesCheck(changed_files),
              CorrectFileNames(changed_files, r"^[/.a-zA-Z0-9_-]*$"),
              CommonDirSymlinkCheck(common_symlink_paths),
    )
    for check in checks:
        check.run()
        if check.rc:
            print(check.msg)
            print('\n')

    if any([check.rc for check in checks]):
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    changed_files = sys.argv[1]
    verify(changed_files)
