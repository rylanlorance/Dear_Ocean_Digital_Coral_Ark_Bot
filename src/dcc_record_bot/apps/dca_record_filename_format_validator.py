import re
import datetime


class DigiArkFilenameFormatValidator:
    def generate_filename_format_report_from_filenames(self, filenames: list):
        number_of_files = len(filenames)
        files_correct_format = []
        files_incorrect_format = []

        for filename in filenames:
            try:
                res = self.validate_filename_format_for_one_file(filename)

                if res:
                    files_correct_format.append(filename)

            except Exception as e:
                files_incorrect_format.append(
                    (filename, e)
                )

        print(
            f"""Dear Ocean Digital Coral Ark
Filename Format Validator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
validating [{number_of_files}] files
"""
        )

        print("Correct Files: ")
        for filename in files_correct_format:
            print(filename)
        
        print('Incorrect Files: ')        
        for filename, error in files_incorrect_format:
            print(f'[{filename}] {error}')

        percent_of_files_correctly_formatted = len(files_correct_format) / number_of_files
        print(f"Percent of files in directory with correct formatting: [{percent_of_files_correctly_formatted}]")

             
    def validate_filename_format_for_one_file(self, filename: str):
        file_name_parsed = re.split(r"\s|_|\.+", filename)

        filename_id = file_name_parsed[0]
        filename_dt = file_name_parsed[1]
        filename_loc_id = file_name_parsed[2]
        filename_user_id = [file_name_parsed[3], file_name_parsed[4]]

        try:
            if len(file_name_parsed) != 10:
                raise ValueError(
                    f"filename format error: [{filename}]" "Incorrect number of fields."
                )

            self.validate_filename_format_file_id(filename_id)
            self.validate_filename_format_dt(filename_dt)
            self.validate_filename_format_location_id(filename_loc_id)
            return True

        except Exception as e:
            print("error!", e)
            raise e

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
