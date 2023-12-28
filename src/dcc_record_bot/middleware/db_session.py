from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import Session

from .models.record import Record
from .models.species import Species

import yaml

class DCADatabaseSession():
    def __init__(self) -> None:
        with open('src/dcc_record_bot/middleware/middleware_config.yaml') as f1:
            config = yaml.safe_load(f1)

            self.db_host = config['DB_HOST']
            self.db_user_id = config['DB_USER_ID']
            self.db_password = config['DB_PASSWORD']

        url = (
            f'postgresql://{self.db_user_id}:'
            f'{self.db_password}'
            f'@{self.db_host}/dca_dev'
        )
        
        engine = create_engine(url)   

        self.session = Session(engine)

        # stmt = select(Record)
        
        # for record in self.session.scalars(stmt):
        #     print('record', vars(record))

        # self.db_username = 
        # self.db_password = 
        # self.
    
    def generate_species_dict_keyed_by_species_id(self):        
        stmt = select(Species)

        species_dict = {}

        for species in self.session.scalars(stmt):
            print(vars(species))

            species_dict[species.species_id] = species

        return species_dict
        
    # def get_all_species_ids(self):
    #     print('getting species_ids')


    # def get_all_species_common_names(self):
    #     print('getting species_common_names')

    # def find_tag_id_based_on_filename(self):
    #     print('finding tag id')
