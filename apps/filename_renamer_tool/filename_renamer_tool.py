"""TODO"""

from datetime import datetime
from multiprocessing import Value
import os
import pathlib
import re
import shutil
import sys
from time import clock_getres
import yaml

from dca_record_bot import DigitalCoralArkRecordBot

# some of the common names are unknown, so we skip them.
known_unknown_common_names = [
    ["Ladyfish", "or"],
    ["Bonefish", "‘ō’io"],
    ["Bonefish", 'ʻŌʻio'],
    ["Baby", "Sergeants"]
]

class FileRenameTool(DigitalCoralArkRecordBot):
    """TODO"""

    def __init__(self, input_dir: str, output_dir: str) -> None:
        super().validate_directory_parameter(input_dir)
        super().validate_output_directory_parameter(output_dir)

        self.input_dir = input_dir
        self.output_dir = output_dir

        config_relative_path = "./apps/filename_renamer_tool/config.yaml"

        if not os.path.isfile(config_relative_path):
            print("config.yaml not found.")
            sys.exit(1)

        with open(config_relative_path, "+r", encoding="UTF-8") as config_file:
            config = yaml.safe_load(config_file)

        # Read in default values from config file.
        self.default_record_starting_record_id = config["starting_image_id"]
        self.default_record_location_id = config["location_id"]
        self.default_donor_info = config["donor_info"]
        self.default_record_tagger_id = config["tagger_id"]

        self.config_datetime_field_index = config["datetime_field_index"]
        self.config_codebook_field_index_setting = config[
            "codebook_field_index_setting"
        ]

        dca_codebook = super().db_session.generate_dca_codebook_object()

    def rename_files(self, safe_mode: bool):
        """TODO:"""

        print(
            f"""Digital Coral Ark: File Rename Tool
Performing Rename tool on the following input directory
[{self.input_dir}]
and output directory
[{self.output_dir}]
with safe mode set to [{safe_mode}]
"""
        )

        errors = 0

        ctr = self.default_record_starting_record_id

        for filename_1 in os.listdir(self.input_dir):
            if not filename_1.startswith('.'):
                try:
                    f_1 = os.path.join(self.input_dir, filename_1)
                    if os.path.isfile(f_1):
                        if os.path.isfile(f_1):
                            print(f"Evaluating [{filename_1}]...")
                            filename_1 = self.cleanup_raw_filenames_before_rename(filename_1)
                            f_1_parsed = re.split(r"\s|_|\.+", filename_1)
                            
                            if self.is_codebook_common_name_known_unknown(f_1_parsed):
                                print("Common name is considered 'known unknown', skipping... ")
                                print("\u2713")

                                continue
                            
                            self.validate_raw_filenames_before_rename(f_1_parsed)

                            record_dt = (
                                self.extract_record_datetime_from_unformatted_file_name(
                                    f_1_parsed
                                )
                            )

                            codebook_ids = (
                                self.extract_codebook_ids_from_unformatted_file_name(
                                    f_1_parsed
                                )
                            )
                            fn_1_ext = pathlib.Path(f_1).suffix

                            fn_2 = self.generate_filename_2_based_on_extracted_values(
                                ctr, record_dt, codebook_ids, fn_1_ext
                            )

                            if safe_mode:
                                print(f"Filename 2 Name: {fn_2}")
                                print("\u2713")

                            if not safe_mode:
                                print(f"Creating file [{fn_2}]...")

                                f_2 = os.path.join(self.output_dir, fn_2)

                                shutil.copyfile(f_1, f_2)

                            ctr += 1

                except Exception as e:
                    print("Error: File not valid for Filename Renamer Tool.")
                    print(e)
                    errors += 1

        return True if not errors else False

    def generate_filename_2_based_on_extracted_values(
        self,
        record_id: int,
        record_dt: datetime,
        species_ids: list,
        filename_1_extension: str,
    ):
        f2_datetime = record_dt.strftime("%Y-%m-%d")
        f2_loc_id = self.default_record_location_id
        f2_record_id = "{:>06d}".format(record_id)
        f2_donor_name = self.default_donor_info
        f2_tagger_id = f"TAG{self.default_record_tagger_id}"

        fn_2 = f"{f2_datetime}_{f2_loc_id}_"

        if len(species_ids) == 0:
            fn_2 += "0000000_0000000"

        elif len(species_ids) == 1:
            fn_2 += species_ids[0] + "_"
            fn_2 += "0000000" + "_"

        elif len(species_ids) == 2:
            fn_2 += species_ids[0] + "_"
            fn_2 += species_ids[1] + "_"

        else:
            print("Error: Species ID Misconfigured.")
            exit(-1)

        fn_2 += f"{f2_tagger_id}_"
        fn_2 += f"{f2_record_id}_"
        fn_2 += f"{f2_donor_name}"

        fn_2 += filename_1_extension.lower()

        return fn_2

    def cleanup_raw_filenames_before_rename(self, fn: str):
        return fn.replace("'", '')

    def is_codebook_common_name_known_unknown(self, fn_1_parsed: list):
        search_subset = fn_1_parsed[0:2]
        print(search_subset)

        if search_subset in known_unknown_common_names:
            return True
        else:
            return False


    def validate_raw_filenames_before_rename(self, fn_parsed: list):
        """TODO"""
        illegal_strings = ["or"]

        common_elements = set(illegal_strings) & set(fn_parsed)

        if common_elements:
            raise ValueError("Filename contains illegal value")

    def extract_record_datetime_from_unformatted_file_name(self, fn_parsed: list):
        """TODO"""
        # print('extracting!')
        # print('fn_parsed', fn_parsed)
        for potential_dt_field in fn_parsed:
            # print(potential_dt_field)
            try:
                record_dt = datetime.strptime(potential_dt_field, "%Y%m%d")
                return record_dt

            except Exception:
                pass
        
        raise ValueError("Filename Date Format Error: Could not find a valid date in %y%m%d format.")
        

    def extract_codebook_ids_from_unformatted_file_name(self, fn_parsed: list):
        """TODO"""
        codebook_ids = []

        codebook_common_names = []

        dca_codebook_keyed_by_common_name = (
            super().db_session.generate_dca_codebook_object()
        )

        if self.config_codebook_field_index_setting == "first_four_words":
            potential_common_names = []
            
            fn_codebook_id_1_common_name_1 = (fn_parsed[0] + "_" + fn_parsed[1]).lower()
            fn_codebook_id_1_common_name_2 = (fn_parsed[0] + "_" + fn_parsed[1] + '_' + fn_parsed[2]).lower()

            potential_common_names.append(fn_codebook_id_1_common_name_1)
            potential_common_names.append(fn_codebook_id_1_common_name_2)

            if set(potential_common_names) & set(dca_codebook_keyed_by_common_name["species"]):
                for potential_common_name in potential_common_names:
                    if potential_common_name in dca_codebook_keyed_by_common_name["species"]:
                        species_id = dca_codebook_keyed_by_common_name["species"][
                            potential_common_name
                        ].species_id

                        codebook_ids.append(species_id)

            else:
                raise KeyError(
                    f"Error: Codebook Common Name not found in dca codebook"
                    f"Incorrect File: [{fn_parsed}]"
                )

        # if self.config_species_field_setting == "first_four_words":
        #     filename_species_1_common_name = (fn_parsed[0] + "_" + fn_parsed[1]).lower()
        #     species_common_names.append(filename_species_1_common_name)

        # if "and" in fn_parsed:
        #     fn_parsed.remove("and")
        #     filename_species_2_common_name = (
        #         fn_parsed[2] + "_" + fn_parsed[3]
        #     ).lower()
        #     species_common_names.append(filename_species_2_common_name)

        # for species_common_name in species_common_names:
        #     if species_common_name in self.hard_coded_species_common_name_dict:
        #         species_id = self.hard_coded_species_common_name_dict[
        #             species_common_name
        #         ]["species_id"]
        #         species_ids.append(species_id)
        #     else:
        #         raise KeyError(
        #             f"Error: Species Common Name not found in species_dict"
        #             f"Incorrect File: [{fn_parsed}]"
        #         )

        else:
            print("Error: Species config setting not specified.")
            sys.exit(-1)

        return codebook_ids
