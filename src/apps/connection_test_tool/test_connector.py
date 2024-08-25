
from middleware.db_session import DCADatabaseSession

class DatabaseTestTool(DCADatabaseSession):
    def __init__(self):
        super().__init__()


    def print_names_of_species(self):
        super().test_db_connection()
