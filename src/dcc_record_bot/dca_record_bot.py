import operator
import datetime
import re
import os
import config
import yaml
from .apps.dca_record_filename_format_validator import DigiArkFilenameFormatValidator
from .apps.filename_renamer_tool.filename_renamer_tool import DigitalCoralArkFileRenamerTool

class DigitalCoralArkRecordBot():    
    filename_format_validator = DigiArkFilenameFormatValidator()
    # file_renamer_tool = DigitalCoralArkFileRenamerTool()

    def __init__(self, input_dir: str, output_dir)  -> None:
        self.input_dir = input_dir # add validation
        self.output_dir = output_dir
        self.file_names_arr = self.generate_file_names_arr()


        
    def generate_file_names_arr(self):
        file_names = []

        for filename in os.listdir(self.input_dir):
            file_names.append(filename)

        return file_names