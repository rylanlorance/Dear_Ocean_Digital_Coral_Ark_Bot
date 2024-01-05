from genericpath import isfile
import os
import datetime
import re

from dca_record_bot import DigitalCoralArkRecordBot


class FilenameValidatorTool(DigitalCoralArkRecordBot):
    """TODO"""

    def __init__(self, input_dir) -> None:
        super().validate_directory_parameter(input_dir)
        self.input_dir = input_dir

        self.filenames = super().generate_filenames_from_input_file(self.input_dir)


    def generate_file_format_report(self):
        num_files = len(self.filenames)

        """TODO"""
        print(
            f"""Digital Coral Ark
Filename Validator Tool
~~~~~~~~~~~~~~~~~~~~~~~~
validating [{num_files}] files."""
        )

        files_correct_format = []
        files_incorrect_format = []

        for filename in self.filenames:
            try:
                self.validate_filename_format(filename)
                files_correct_format.append(filename)

            except Exception as e:
                files_incorrect_format.append(
                    (filename, e)
                )
        
        print("Correct Files: ")
        print([i for i in files_correct_format])

        print('Incorrect Files: ')
        
        for filename, error in files_incorrect_format:
            print(f'[{filename}] {error}')
  


    def validate_filename_format(self, filename: str):
        """TODO"""
        file_name_parsed = re.split(r"\s|_|\.+", filename)

        filename_id = file_name_parsed[0]
        filename_dt = file_name_parsed[1]
        filename_loc_id = file_name_parsed[2]
        filename_user_id = [file_name_parsed[3], file_name_parsed[4]]
        
        if len(file_name_parsed) != 7:
            raise ValueError(
                f"filename format error: [{filename}]" "Incorrect number of fields."
            )
        
        self.validate_filename_format_file_id(filename_id)
        self.validate_filename_format_dt(filename_dt)
        self.validate_filename_format_location_id(filename_loc_id)

    def validate_filename_format_file_id(self, file_id):
        if len(file_id) != 6:
            raise ValueError("Filename_ID_Error. Incorrect number of values.")

        if not file_id.isnumeric():
            raise ValueError("Filename_ID_Error. Filename_id can only contain digits.")

    def validate_filename_format_dt(self, dt):
        if not bool(datetime.datetime.strptime(dt, "%Y%m%d")):
            raise ValueError("Filename Date Format Error: Must be in %Y%m%d format.")

    def validate_filename_format_location_id(self, loc_id):
        if len(loc_id) != 3:
            raise ValueError(
                "Filename Location Id Format Error: Must be 3 characters long."
            )
