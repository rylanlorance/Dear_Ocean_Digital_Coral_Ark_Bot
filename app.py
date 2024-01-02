import os

from apps.filename_renamer_tool.filename_renamer_tool import FileRenameTool
import config

import argparse

# from src.dcc_record_bot.dca_record_bot import DigitalCoralArkRecordBot
# from src.dcc_ record_bot.apps.filename_renamer_tool.filename_renamer_tool import DigitalCoralArkFileRenamerTool
# # from file_rename_bot.file_rename_bot import FileRenameBot
# # from dak_archive_bot.dak_archive_bot import DigitalArkArchiveBot

# from src.dcc_record_bot.middleware.db_session import DCADatabaseSession


def cmd_rename_files(args):
    file_rename_tool = FileRenameTool(
        input_dir=args.input_dir, output_dir=args.output_dir
    )
    
    file_rename_tool.rename_files(safe_mode=True)


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(help="")

parser_rename_files = subparsers.add_parser(
    "rename", help="Tool used to rename files, must be preconfigured."
)
parser_rename_files.add_argument("input_dir", type=str)
parser_rename_files.add_argument("output_dir", type=str)
parser_rename_files.set_defaults(func=cmd_rename_files)

args = parser.parse_args()
args.func(args)

# if __name__ == "__main__":
#     # Initialize all tools
