import mariadb
import sys
import os
import json

from dotenv import load_dotenv

load_dotenv()  # use .env as environmental variables from OS


class MariaDBConnector(object):
    def __init__(self):
        try:
            self.conn = mariadb.connect(
                user=os.environ.get("MARIADB_USER"),
                password=os.environ.get("MARIADB_PASSWORD"),
                host=os.environ.get("MARIADB_HOST"),
                port=int(os.environ.get("MARIADB_PORT")),
                database=os.environ.get("MARIADB_DATABASE"),
            )
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

        self.cursor = self.conn.cursor()

    def get_honeypi_data(self, start_date="", end_date=""):
        if start_date != "" and end_date != "":
            self.cursor.execute(
                "SELECT * "
                "FROM honeypi_data "
                "WHERE timestamp BETWEEN ? AND ? "
                "ORDER BY timestamp DESC "
                "LIMIT 100 ",
                (start_date, end_date)
            )
        else:
            self.cursor.execute(
                "SELECT * "
                "FROM honeypi_data "
                "ORDER BY timestamp DESC "
                "LIMIT 100 ",
                ()
            )
        row_headers = [x[0] for x in self.cursor.description]  # this will extract row headers
        results = self.cursor.fetchall()
        json_data = []
        for result in results:
            json_data.append(dict(zip(row_headers, result)))

        return json_data

    def close_connection(self):
        self.conn.close()


def test():
    mariadb_connector_obj = MariaDBConnector()

    for (brood_room_temperature, outdoor_temperature) in mariadb_connector_obj.get_honeypi_data():
        print(f"brood_room_temperature: {brood_room_temperature}\n"
              f"outdoor_temperature:   {outdoor_temperature}")


if __name__ == '__main__':
    test()
