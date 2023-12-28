import yaml 

class DigitalCoralArkFileRenamerTool():
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
            config = yaml.safe_load(f1)

            if 'starting_image_id' not in config:
                print("error, no image id generated")
                        
            if config['location_id'] != "":
                self.default_location_id = config['location_id']
            
            if config['user_id'] != "":
                self.default_location_id = config['user_id']

        # self.config = yaml.safe_load(open("filename_renamer_tool.yaml"))
    
    def test_rename_files(self):
        print('lets rename our files')


    



    # def extract_species_id_from_unformatted_file_name():
        

        
        

        