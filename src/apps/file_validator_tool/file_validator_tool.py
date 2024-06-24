from genericpath import isfile
import os
import datetime
import re

from src.apps.database_upload_tool.dca_record_bot import DigitalCoralArkRecordBot

class FilenameValidatorTool(DigitalCoralArkRecordBot):
    """I validate the filename format of input records. This typically happens before 
       we attempt to insert into the database. I do not validate the content of the fields 
       in the filename; rather, I only check for filename length and character types."""

    def __init__(self, input_dir) -> None:
        super().validate_directory_parameter(input_dir)
        self.input_dir = input_dir

        self.filenames = super().generate_filenames_from_input_file(self.input_dir)


    def generate_file_format_report(self):
        """Generates a file format report for multiple records."""
        num_files = len(self.filenames)

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
        
        print(f"Correct Files [{len(files_correct_format)}]:")
        print([i for i in files_correct_format])

        print(f"Incorrect Files [{len(files_incorrect_format)}]:")
        
        for filename, error in files_incorrect_format:
            print(f'[{filename}] {error}')
  
    def validate_filename_format(self, filename: str):
        """Validates filename format for all fields. Checks strength length and datetime. """
        file_name_parsed = re.split(r"\s|_|\.+", filename)
        
        # numbers of fields must equal 9
        if len(file_name_parsed) != 9:
            raise ValueError(
                f"filename format error: [{filename}]" "Incorrect number of fields."
            )
        
        # all fields must have the exact character length (i.e. species_id = 7)
        # except for the donor info.  
        file_name_excluding_donor_id = file_name_parsed[:-3]
        total_chars_in_filename_excluding_donor_id =  sum([len(i) for i in file_name_excluding_donor_id])

        if total_chars_in_filename_excluding_donor_id != 38:
            raise ValueError("Filename format error: [{}]. Aggregate length wrong. ")
  
        fn_dt = file_name_parsed[0]
        fn_loc_id = file_name_parsed[1]

        self.__validate_filename_format_dt(fn_dt)
        self.__validate_fn_format_loc_id(fn_loc_id)

    def __validate_filename_format_dt(self, dt):
        if not bool(datetime.datetime.strptime(dt, "%Y-%m-%d")):
            raise ValueError("Filename Date Format Error: Must be in %Y%m%d format.")
    
    def __validate_fn_format_loc_id(self, loc_id):
        if any(char.isdigit() for char in loc_id):
            raise ValueError("Filename Location Id Format Error: Must not contain digits.")
