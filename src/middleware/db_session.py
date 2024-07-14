from sqlite3 import DatabaseError
from sqlalchemy import Select, create_engine
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import MultipleResultsFound

from middleware.models.donor import Donor

from .models.record import Record
from .models.species import Species

import yaml

class DCADatabaseSession():
    def __init__(self) -> None:
        with open('src/middleware/middleware_config.yaml') as f1:
            config = yaml.safe_load(f1)

            self.__db_host = config['DB_HOST']
            self.__db_user_id = config['DB_USER_ID']
            self.__db_password = config['DB_PASSWORD']
            self.__port = config['PORT']
        url = (
            f'postgresql://{self.__db_user_id}:'
            f'{self.__db_password}'
            f'@{self.__db_host},{self.__port}/dca_dev_working'
        )
        
        self.engine = create_engine(url)   

        self.__session = Session(self.engine)

    def test_db_connection(self):
        try:
            conn = self.engine.connect()
            conn.close()
            print('db connection working')

        except Exception as e:
            print('Error! Database connection not working.')



    def generate_dca_codebook_object(self):
        dca_codebook = {
            'species': {},
            'families': {}
        }
        stmt = select(Species)

        for species in self.__session.scalars(stmt):
            species_str = species.common_name.lower().replace(' ', '_').replace("'", '')
            dca_codebook['species'][species_str] = species

        return dca_codebook

    def generate_species_dict_keyed_by_species_id(self):        
        stmt = select(Species)

        species_dict = {}

        for species in self.__session.scalars(stmt):
            species_dict[species.species_id] = species

        return species_dict
    
    def retrieve_donor_id_by_last_name(self, lastname: str):
        """Queries donor table based on last name"""

        stmt = Select(Donor).where(Donor.last_name==lastname)

        result = self.__session.execute(stmt)

        try:
            donor_res = result.scalar_one_or_none()
            if not donor_res:
                raise DatabaseError
            else:
                return donor_res.donor_id

        except MultipleResultsFound:
            print("Error: Multiple donor ids matched for lastname")

    def upload_record_to_db(self, record: Record, safe_mode: bool):
        self.__session.add(record)
        self.__session.flush()

        if not safe_mode:
            self.__session.commit()
            
    
