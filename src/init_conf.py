import configparser
import sys


class InitConf:

    def __init__(self):
        self.notion_token = None
        self.calendar_name = None
        self.databases_id = []
        self.database_name = []

    def ask_notion_token(self):
        token = input("Paste your Notion integration token : ")
        assert token[:7] == "secret_", "token must begin with 'secret_'"
        assert len(token) == 50, "token size must be 50 characters"
        self.notion_token = token

    def ask_calendar_name(self):
        name = input("Enter the calendar name you want to sync : ")
        self.calendar_name = name

    def ask_databases(self):
        nb_calendar = int(input("How many databases would you like to sync ? "))
        for i in range(nb_calendar):
            db_name = input("Enter your database name : ")
            db_name = db_name.replace(" ", "_")
            db_token = input("Paste your database ID : ")
            assert len(db_token) == 32, "database ID must have a 32-length"
            self.database_name.append(db_name)
            self.databases_id.append(db_token)

    def write_config_file(self, path):
        config = configparser.ConfigParser()
        config['GLOBAL'] = {
            "NOTION_TOKEN": self.notion_token,
            "APPLE_CALENDAR": self.calendar_name
        }
        config['DATABASES'] = {
            name: id_ for (name, id_) in zip(self.database_name, self.databases_id)
        }
        with open(path, 'w') as configfile:
            config.write(configfile)

    def run(self, path):
        self.ask_notion_token()
        self.ask_calendar_name()
        self.ask_databases()
        self.write_config_file(path)


if __name__ == '__main__':
    path = sys.argv[1]
    try:
        InitConf().run(path)
    except Exception as e:
        print(e)
        sys.exit()






