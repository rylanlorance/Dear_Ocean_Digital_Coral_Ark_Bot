"""TODO"""
from datetime import datetime
import os
import pathlib
import re
import shutil
import sys
import yaml

from dca_record_bot import DigitalCoralArkRecordBot


class FileRenameTool(DigitalCoralArkRecordBot):
    """TODO"""

    hard_coded_species_common_name_dict = {
        "bluestripe_butterflyfish": {
            "species_common_name": "bluestripe butterflyfish",
            "species_id": "BLUEBTR",
            "family": "chaetodontidae",
            "species": "fremblii",
        },
        "thompsons_butterflyfish": {
            "species_common_name": "thompson's butterflyfish",
            "species_id": "THOMBTR",
            "family": "chaetodontidae",
            "species": "thompsoni",
        },
        "lined_butterflyfish": {
            "species_common_name": "lined butterflyfish",
            "species_id": "LINEBTR",
            "family": "chaetodontidae",
            "species": "lineolatus",
        },
        "fourspot_butterflyfish": {
            "species_common_name": "fourspot butterflyfish",
            "species_id": "FOURBTR",
            "family": "blah blah",
            "species": "blahblah",
        },
    }

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
        self.default_donor_id = config["donor_id"]
        self.default_record_tagger_id = config["tagger_id"]

        self.config_datetime_field_index = config["datetime_field_index"]
        self.config_species_field_setting = config["species_field_index_setting"]

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
            try:
                f_1 = os.path.join(self.input_dir, filename_1)
                if os.path.isfile(f_1):
                    if os.path.isfile(f_1):
                        print(f"Evaluating [{filename_1}]...")
                        f_1_parsed = re.split(r"\s|_|\.+", filename_1)
                        self.validate_raw_filenames_before_rename(f_1_parsed)
                        record_dt = (
                            self.extract_record_datetime_from_unformatted_file_name(
                                f_1_parsed
                            )
                        )
                        species_ids = (
                            self.extract_species_ids_from_unformatted_file_name(
                                f_1_parsed
                            )
                        )

                        if safe_mode:
                            print("\u2713")

                        if not safe_mode:
                            fn_1_ext = pathlib.Path(f_1).suffix

                            fn_2 = self.generate_filename_2_based_on_extracted_values(
                                ctr, record_dt, species_ids, fn_1_ext
                            )

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
        f2_record_id = "{:>06d}".format(record_id)
        f2_datetime = record_dt.strftime("%Y%m%d")
        f2_loc_id = self.default_record_location_id
        f2_donor_id = self.default_donor_id

        fn_2 = f2_record_id + "_"
        fn_2 += f2_datetime + "_"
        fn_2 += f2_loc_id + "_"
        fn_2 += f2_donor_id + "_"

        if len(species_ids) == 1:
            fn_2 += species_ids[0] + "_"
            fn_2 += "0000000" + "_"

        else:
            fn_2 += species_ids[0] + "_"
            fn_2 += species_ids[1] + "_"

        fn_2 += f"TAG{self.default_record_tagger_id}"

        fn_2 += filename_1_extension.lower()

        return fn_2

    def validate_raw_filenames_before_rename(self, fn_parsed: list):
        """TODO"""
        illegal_strings = ["or"]

        common_elements = set(illegal_strings) & set(fn_parsed)

        if common_elements:
            raise ValueError("Filename contains illegal value")

    def extract_record_datetime_from_unformatted_file_name(self, fn_parsed: list):
        """TODO"""
        dt_field_right_index = self.config_datetime_field_index
        potential_dt_field = fn_parsed[dt_field_right_index]

        if not bool(datetime.strptime(potential_dt_field, "%Y%m%d")):
            raise ValueError("Filename Date Format Error: Must be in %y%m%d format.")

        return datetime.strptime(potential_dt_field, "%Y%m%d")

    def extract_species_ids_from_unformatted_file_name(self, fn_parsed: list):
        """TODO"""
        species_ids = []
        species_common_names = []

        if self.config_species_field_setting == "first_four_words":
            filename_species_1_common_name = (fn_parsed[0] + "_" + fn_parsed[1]).lower()
            species_common_names.append(filename_species_1_common_name)

            if "and" in fn_parsed:
                fn_parsed.remove("and")
                filename_species_2_common_name = (
                    fn_parsed[2] + "_" + fn_parsed[3]
                ).lower()
                species_common_names.append(filename_species_2_common_name)
            for species_common_name in species_common_names:
                if species_common_name in self.hard_coded_species_common_name_dict:
                    species_id = self.hard_coded_species_common_name_dict[
                        species_common_name
                    ]["species_id"]
                    species_ids.append(species_id)
                else:
                    raise KeyError(
                        f"Error: Species Common Name not found in species_dict"
                        f"Incorrect File: [{fn_parsed}]"
                    )

        else:
            print("Error: Species config setting not specified.")
            sys.exit(-1)

        return species_ids
