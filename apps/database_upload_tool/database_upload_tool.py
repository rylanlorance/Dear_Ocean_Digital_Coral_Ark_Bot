
from dca_record_bot import DigitalCoralArkRecordBot

class DatabaseUploadTool(DigitalCoralArkRecordBot):
    def __init__(self, input_dir) -> None:
        super().validate_directory_parameter(input_dir)
        self.input_dir = input_dir

        self.filenames = super().generate_filenames_from_input_file(self.input_dir)
        

    def upload_files_to_database(self, safe_mode: bool):
        print(f"running upload script with safemode [{safe_mode}]")

        
    