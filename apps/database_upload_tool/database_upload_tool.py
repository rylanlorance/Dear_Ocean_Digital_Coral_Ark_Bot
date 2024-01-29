import sqlalchemy
from dca_record_bot import DigitalCoralArkRecordBot
from sqlalchemy import exc

import re

from middleware.models.record import Record

class DatabaseUploadTool(DigitalCoralArkRecordBot):
    class RecordFileAbstraction:
        def __init__(self, filename) -> None:
            fn_parsed = re.split(r"\s|_|\.+", filename)

            self.dt = fn_parsed[0]
            self.loc_id = fn_parsed[1]
            
            if fn_parsed[2] == "0000000":
                self.species_id_1 = None
            else:
                self.species_id_1 = fn_parsed[2]
            
            if fn_parsed[3] == "0000000":
                self.species_id_2 = None
            else:
                self.species_id_2 = fn_parsed[3]
            
            self.tagger_id = fn_parsed[4][3:5]
            self.id = fn_parsed[5]

            self.donor_last_name = fn_parsed[6]
            self.donor_first_initial = fn_parsed[7]
 
    def __init__(self, input_dir) -> None:
        super().validate_directory_parameter(input_dir)
        self.input_dir = input_dir

        self.filenames = super().generate_filenames_from_input_file(self.input_dir)

    def upload_files_to_database(self, safe_mode: bool):
        print(f"running upload script with safemode [{safe_mode}]")

        safe_files = []
        unsafe_files = []

        # Fix donor id dipshit

        for filename in self.filenames:
            print('filename', filename)
            try:
                self.upload_file_to_db(filename, safe_mode)
                safe_files.append(filename)

            except exc.SQLAlchemyError as e:
                unsafe_files.append((filename, e))

            except Exception as e:
                unsafe_files.append((filename, e))

        print('Upload Attempt Report')
        print(f'Files Marked As Safe [{len(safe_files)}]')
        print([filename for filename in safe_files])

        print(f'Files Marked As Not Safe [{len(unsafe_files)}]')
        for fn, error in unsafe_files:
            print(f"unsafe file [{fn}]")
            print("Error: ", error)
            print("-------------------------------------")


    def upload_file_to_db(self, filename: str, safe_mode: bool):
        record_abstract = self.RecordFileAbstraction(filename)
        print('record_abstract', vars(record_abstract))

        # validate species id
        species_dict = super().db_session.generate_species_dict_keyed_by_species_id()

        for i in [record_abstract.species_id_1, record_abstract.species_id_2]:
            if i:
                if i not in species_dict:
                    raise KeyError("Error! Species ID not in Species Table.")

        donor_id = super().db_session.retreive_donor_id_by_last_name(record_abstract.donor_last_name)

        # attempt to upload the file to the database
        record = Record(
            record_id=record_abstract.id,
            recorded_dt=record_abstract.dt,
            location_id=record_abstract.location_id,
            donor_id=record_abstract.donor_id,
            species_tag_1=record_abstract.species_id_1,
            species_tag_2=record_abstract.species_id_2,
            uploaded_dt="20240101",
            tagger_id=record_abstract.tagger_id
        )

        self.db_session.session.add(record)
        self.db_session.session.flush()

        if not safe_mode:
            self.db_session.session.commit()
            print('Database changes committed.')

