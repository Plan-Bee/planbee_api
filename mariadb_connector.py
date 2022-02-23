import mariadb
import sys
import os

from dotenv import load_dotenv

load_dotenv()  # use .env as environmental variables from OS


class MariaDBConnector(object):
    def __init__(self):
        try:
            conn = mariadb.connect(
                user=os.environ.get("MARIADB_USER"),
                password=os.environ.get("MARIADB_PASSWORD"),
                host=os.environ.get("MARIADB_HOST"),
                port=int(os.environ.get("MARIADB_PORT")),
                database=os.environ.get("MARIADB_DATABASE"),
            )
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

        self.cursor = conn.cursor()

    def get_honeypi_data(self):
        self.cursor.execute(
            "SELECT broodroom_temperature,outdoor_temperature FROM honeypi_data",
            ()
        )
        return self.cursor


def test():
    mariadb_connector_obj = MariaDBConnector()

    for (brood_room_temperature, outdoor_temperature) in mariadb_connector_obj.get_honeypi_data():
        print(f"brood_room_temperature: {brood_room_temperature}\n"
              f"outdoor_temperature:   {outdoor_temperature}")


if __name__ == '__main__':
    test()
