from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import Session
from .models.record import Record

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

        stmt = select(Record)
        
        for record in self.session.scalars(stmt):
            print('record', vars(record))

        # self.db_username = 
        # self.db_password = 
        # self.
