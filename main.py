from src.Database import Database
import os
from datetime import datetime
import logging
from configparser import ConfigParser

if __name__ == "__main__":
    start_datetime = datetime.now()
    cwd = os.path.dirname(os.path.abspath(__file__))
    log_file = os.path.join(cwd,'logs',f"{start_datetime.strftime('%Y-%m-%dT%H:%M:%S')}.log")
    # Remove all handlers associated with the root logger object.
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logging.basicConfig(filename=log_file, level=logging.INFO)

    log_files = os.listdir(os.path.join(cwd,'logs'))
    def file_today(file,date):
        file_day = int(file.split('T')[0].split('-')[-1])
        return file_day != date.day
    to_remove = list(filter(lambda f : file_today(f,start_datetime),log_files))
    for f in to_remove:
        os.remove(os.path.join(cwd,'logs',f))
        
    conf = ConfigParser()
    conf.read('config.ini')
    notion_token = conf['GLOBAL']['NOTION_TOKEN']
    apple_calendar = conf['GLOBAL']['APPLE_CALENDAR']
    for key,database_id in conf['DATABASES'].items():
        logging.info(f"Start database {key}")
        db = Database(database_id,notion_token,apple_calendar,folder=os.path.join(cwd,'databases'))
        db.run()
        logging.info(f"End database {key}")

