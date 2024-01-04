import datetime
from re import L
from uu import Error
import yaml 
import os
import re
from datetime import datetime
import pathlib
import shutil

class DigitalCoralArkFileRenamerTool():
    hard_coded_species_common_name_dict = {
        "bluestripe_butterflyfish": {
            'species_common_name': 'bluestripe butterflyfish',
            'species_id': 'BLUEBTR',
            'family': 'chaetodontidae',
            'species': 'fremblii'
        },
           "thompsons_butterflyfish": {
            'species_common_name': "thompson's butterflyfish",
            'species_id': 'THOMBTR',
            'family': 'chaetodontidae',
            'species': 'thompsoni'
        },
        "lined_butterflyfish": {
            'species_common_name': "lined butterflyfish",
            'species_id': 'LINEBTR',
            'family': 'chaetodontidae',
            'species': 'lineolatus'
        },
        'fourspot_butterflyfish': {
            'species_common_name': 'fourspot butterflyfish',
            'species_id': 'FOURBTR',
            'family': 'blah blah',
            'species': 'blahblah' 
        },
        
    }

    def __init__(self, input_dir: str, output_dir:str)  -> None:
        self.input_dir = input_dir # add validation
        self.output_dir = output_dir

        ## default values
        self.start2ing_record_id = None

        self.default_datetime = None
        self.default_location_id = None
        self.default_user_id = None
        self.default_species_id_1 = None
        self.default_species_id_2 = None
        self.default_tagger_id = None

        with open('src/dcc_record_bot/apps/filename_renamer_tool/filename_renamer_tool.yaml') as f1:
            self.config = yaml.safe_load(f1)
            print(self.config)

            if 'starting_image_id' not in self.config:
                print("error, no image id generated")
                        
            if self.config['location_id'] != "":
                self.default_location_id = self.config['location_id']
            
            if self.config['user_id'] != "":
                self.default_user_id = self.config['user_id']
            
            if self.config['tagger_id'] != "":
                self.default_tagger_id = self.config['tagger_id']

        # self.config = yaml.safe_load(open("filename_renamer_tool.yaml"))
    
    def rename_files(self):
        if not self.test_rename_files():
            print("Error. Cannot copy files. Test rename failed. ")
            exit(-1)
            
        else:
            print("Test Rename Completed Successfully...continuing with rename")
        
        ctr = self.config['starting_image_id']

        for filename_1 in os.listdir(self.input_dir):
            f_1 = os.path.join(self.input_dir, filename_1)   
            if os.path.isfile(f_1):
                filename_1_extension = pathlib.Path(f_1).suffix

                self.validate_raw_filename_before_rename_attempt(filename_1)
                species_ids = self.extract_species_id_from_unformatted_file_name(filename_1)
                record_dt = self.extract_record_datetime_from_unformatted_file_name(filename_1)


                ## create a new file string
                filename_2_record_id =  '{:>06d}'.format(ctr)
                filename_2_datetime =  record_dt.strftime("%Y%m%d")
                filename_2_loc_id = self.default_location_id

                filename_2 = filename_2_record_id + '_' 
                filename_2 += filename_2_datetime + '_'
                filename_2 += filename_2_loc_id + "_"

                if len(species_ids) == 1:
                    filename_2 += species_ids[0] + "_"
                    filename_2 += '0000000' + "_"
                
                else:   
                    filename_2 += species_ids[0] + "_"
                    filename_2 += species_ids[1] + "_"

                filename_2 += f"TAG{self.default_tagger_id}"

                filename_2 += filename_1_extension
            
                f_2 = os.path.join(self.output_dir, filename_2)   

                print('f2', f_2)

                shutil.copyfile(f_1, f_2)

                ctr+=1


    def test_rename_files(self):
        print(f"""Testing files for the Digital Coral Ark File Renamer Tool
reading from directory: [{self.input_dir}]
            """)
        errors = 0

        for filename in os.listdir(self.input_dir):
            print(f"Testing File...[{filename}]")
            try:
                f = os.path.join(self.input_dir, filename)   
                if os.path.isfile(f):
                    if not self.config['contains_correct_species_id']:
                        self.validate_raw_filename_before_rename_attempt(filename)
                        self.extract_species_id_from_unformatted_file_name(filename)
                        self.extract_record_datetime_from_unformatted_file_name(filename)
                        print(u'\u2713')


            except Exception as e:
                print("Error: File not valid for Filename Renamer Tool.")
                print(e)
                errors+=1
        
        if errors > 0:
            return False
        
        else:
            print("Test Complete!")
            return True

    def validate_raw_filename_before_rename_attempt(self, filename):
        illegal_strings = ['or'] # certain strings prevent file renamer tool from working
        for illegal_string in illegal_strings:
            if illegal_string in filename:
                raise Error("Filename cannot contain the value 'or', ignoring.")
    
    def extract_record_datetime_from_unformatted_file_name(self, filename):
        file_name_parsed = re.split(r"\s|_|\.+", filename)
        
        ## find the datetime, which is most likely value with eight values and all numeric
        potential_dt_field = 0

        for field in file_name_parsed:
            if len(field) == 8:
                if field.isnumeric():
                    potential_dt_field = field
        
        if not potential_dt_field:
            raise ValueError("Error with filename: No datetime provided.")
        
        if not bool(datetime.strptime(potential_dt_field, "%Y%m%d")):
            raise ValueError("Filename Date Format Error: Must be in %y%m%d format.")

        return datetime.strptime(potential_dt_field, "%Y%m%d")

    def extract_species_id_from_unformatted_file_name(self, filename):   
        species_ids = []

        species_common_names = []   

        if self.config['common_name_location'] == 'first_four_words':
            file_name_parsed = re.split(r"\s|_|\.+", filename)

            filename_species_1_common_name = (file_name_parsed[0] + "_" + file_name_parsed[1]).lower()
            species_common_names.append(filename_species_1_common_name)

            if 'and' in file_name_parsed:
                file_name_parsed.remove('and')
                filename_species_2_common_name = (file_name_parsed[2] + "_" + file_name_parsed[3]).lower()
                species_common_names.append(filename_species_2_common_name)

            for species_common_name in species_common_names:
                if species_common_name in self.hard_coded_species_common_name_dict:
                    species_id = self.hard_coded_species_common_name_dict[species_common_name]['species_id']
                    species_ids.append(species_id)
                else:
                    raise KeyError(f"Error: Species Common Name not found in species_dict. Incorrect File: [{filename}]")
     
        else:
            print("error! check config file.s")
            exit(1)

        return species_ids
        
        