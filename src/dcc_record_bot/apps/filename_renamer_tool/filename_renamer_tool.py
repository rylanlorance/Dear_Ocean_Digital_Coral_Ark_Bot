from re import L
from uu import Error
import yaml 
import os
import re

class DigitalCoralArkFileRenamerTool():

    species_common_name_dict = {
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

    def __init__(self, input_dir: str, output_dir)  -> None:
        self.input_dir = input_dir # add validation
        self.output_dir = output_dir

        ## default values
        self.start2ing_record_id = None

        self.default_datetime = None
        self.default_location_id = None
        self.default_user_id = None
        self.default_species_id_1 = None
        self.default_species_id_2 = None
        self.default_tagger = None

        with open('src/dcc_record_bot/apps/filename_renamer_tool/filename_renamer_tool.yaml') as f1:
            self.config = yaml.safe_load(f1)

            if 'starting_image_id' not in self.config:
                print("error, no image id generated")
                        
            if self.config['location_id'] != "":
                self.default_location_id = self.config['location_id']
            
            if self.config['user_id'] != "":
                self.default_location_id = self.config['user_id']

        # self.config = yaml.safe_load(open("filename_renamer_tool.yaml"))
    
    def test_rename_files(self):
        print('lets rename our files')
        
        try: 
            for filename in os.listdir(self.input_dir):
                f = os.path.join(self.input_dir, filename)   
                if os.path.isfile(f):

                    if not self.config['contains_correct_species_id']:
                        self.validate_raw_filename_before_rename_attempt(filename)
                        species_ids = self.extract_species_id_from_unformatted_file_name(filename)
                        print('species_ids', species_ids)

        except Exception as e:
            print('error', e)

    def validate_raw_filename_before_rename_attempt(self, filename):
        illegal_strings = ['or'] # certain strings prevent file renamer tool from working
        for illegal_string in illegal_strings:
            if illegal_string in filename:
                raise Error("Filename cannot contain the value 'or', ignoring.")

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
                print('species common name', species_common_name)
                if species_common_name in self.species_common_name_dict:
                    species_id = self.species_common_name_dict[species_common_name]['species_id']
                    species_ids.append(species_id)
                else:
                    raise KeyError("Error: Species Common Name not found in species_dict. ")
     
        else:
            print("error! check config file.s")
            exit(1)

        return species_ids
        
        

        
        

        