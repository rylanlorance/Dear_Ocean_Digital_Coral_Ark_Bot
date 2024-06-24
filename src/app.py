import os
from apps.database_upload_tool.database_upload_tool import DatabaseUploadTool
from apps.file_validator_tool.file_validator_tool import FilenameValidatorTool

from apps.filename_renamer_tool.filename_renamer_tool import FileRenameTool
import config

import argparse

# from src.dcc_record_bot.dca_record_bot import DigitalCoralArkRecordBot
# from src.dcc_ record_bot.apps.filename_renamer_tool.filename_renamer_tool import DigitalCoralArkFileRenamerTool
# # from file_rename_bot.file_rename_bot import FileRenameBot
# # from dak_archive_bot.dak_archive_bot import DigitalArkArchiveBot


def cmd_rename_files(args):
    file_rename_tool = FileRenameTool(
        input_dir=args.input_dir, output_dir=args.output_dir
    )

    if args.safe_mode == "on":
        file_rename_tool.rename_files(safe_mode=True)

    else:
        file_rename_tool.rename_files(safe_mode=False)

def cmd_validate_files(args):
    file_validator_tool = FilenameValidatorTool(args.input_dir)
    file_validator_tool.generate_file_format_report()

def cmd_upload_files(args):
    database_upload_tool = DatabaseUploadTool(args.input_dir)

    if args.safe_mode == "on":
        database_upload_tool.upload_files_to_database(safe_mode=True)
    else:
        database_upload_tool.upload_files_to_database(safe_mode=False)

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(help="")

parser_rename_files = subparsers.add_parser(
    "rename", help="Tool used to rename files, must be preconfigured."
)
parser_rename_files.add_argument("input_dir", type=str)
parser_rename_files.add_argument("output_dir", type=str)
parser_rename_files.add_argument('--safe-mode', type=str, default="on")
parser_rename_files.set_defaults(func=cmd_rename_files)

parser_validate_files = subparsers.add_parser(
    "validate", help="Tool for validating filename formats"
)
parser_validate_files.add_argument("input_dir", type=str)
parser_validate_files.set_defaults(func=cmd_validate_files)

parser_upload_files = subparsers.add_parser(
    "upload", help="Tool used to upload records to the database."
)
parser_upload_files.add_argument("input_dir", type=str)
parser_upload_files.add_argument('--safe-mode', type=str, default="on")
parser_upload_files.set_defaults(func=cmd_upload_files)

args = parser.parse_args()
args.func(args)


# if __name__ == "__main__":
#     # Initialize all tools
