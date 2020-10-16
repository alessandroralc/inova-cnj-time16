from dotenv import load_dotenv
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
load_dotenv()

from app import application
from src.persistencia.database import db


migrate = Migrate(application, db)
manager = Manager(application)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':    
    manager.run()  
