import operator
import datetime
import re
import os
import config
import yaml
# from .apps.dca_record_filename_format_validator import DigiArkFilenameFormatValidator
# from .apps.filename_renamer_tool.filename_renamer_tool import DigitalCoralArkFileRenamerTool

class DigitalCoralArkRecordBot():    
    # filename_format_validator = DigiArkFilenameFormatValidator()
    # file_renamer_tool = DigitalCoralArkFileRenamerTool()

    # def __init__(self)  -> None:
    #     # self.input_dir = input_dir # add validation
    #     # self.output_dir = output_dir
    #     # self.file_names_arr = self.generate_file_names_arr()


    def validate_directory_parameter(self, directory):
        if not os.path.isdir(directory):
            print("Error: Directory not found", directory)
            exit(-1)

    def validate_output_directory_parameter(self, directory):
       self.validate_directory_parameter(directory)
       
       if not os.listdir(directory):
        # empty directory
        return
       
       else:
          print("Error: Output directory not empty")
          exit(-1)
    
