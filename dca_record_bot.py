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


    def validate_directory_parameter(self, dir):
        if not os.path.isdir(dir):
            print("Error: Directory not found", dir)
            exit(-1)

    def validate_output_directory_parameter(self, dir):
       self.validate_directory_parameter(dir)
       
       if not os.listdir(dir):
        # empty directory
        return
       
       else:
          print("Error: Output directory not empty")
          exit(-1)
    
    def generate_filenames_from_input_file(self, dir):
            filenames = []

            for filename in os.listdir(dir):
                f = os.path.join(dir)
                if os.path.isfile(f):
                    filenames.append(filename)

            return filenames