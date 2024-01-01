import os
import config
from src.dcc_record_bot.dca_record_bot import DigitalCoralArkRecordBot
from src.dcc_record_bot.apps.filename_renamer_tool.filename_renamer_tool import DigitalCoralArkFileRenamerTool
# from file_rename_bot.file_rename_bot import FileRenameBot
# from dak_archive_bot.dak_archive_bot import DigitalArkArchiveBot

from src.dcc_record_bot.middleware.db_session import DCADatabaseSession

if __name__ == "__main__":
    try:
        if not os.path.isdir(config.INPUT_FILE_DIR):
            raise FileNotFoundError

        if not os.path.isdir(config.OUTPUT_FILE_DIR):
            raise FileNotFoundError
        
        beagle = DigitalCoralArkRecordBot(config.INPUT_FILE_DIR, config.OUTPUT_FILE_DIR)

    
        ## validate one file

        # filenames = []

        # for filename in os.listdir(config.INPUT_FILE_DIR):
        #     f = os.path.join(config.INPUT_FILE_DIR, filename)   
        #     if os.path.isfile(f):
        #         filenames.append(filename)

        # beagle.filename_format_validator.validate_filename_format_for_one_file("000001_20170101_KEA_Roberts.Anka_SADDLE_RETICUL_TAGRL_ADDRL.jpg")
        # beagle.filename_format_validator.generate_filename_format_report_from_filenames(filenames)

        # print(vars(dakBot))
        

        # my_file_rename_bot = FileRenameBot(config.INPUT_FILE_DIR, config.OUTPUT_FILE_DIR)
        # print(vars(my_file_rename_bot))
        
        # # validate filenames
        # my_file_rename_bot.super.validate_file_format()


        ## initialize database
        session = DCADatabaseSession()
        session.generate_species_dict_keyed_by_species_id()

        ## Rename a file
        file_renamer_tool = DigitalCoralArkFileRenamerTool(config.INPUT_FILE_DIR, config.OUTPUT_FILE_DIR)
        file_renamer_tool.test_rename_files()

    except FileNotFoundError:
        print("Input File not found", FileNotFoundError)

    except Exception as e:
        print(e)