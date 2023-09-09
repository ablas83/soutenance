import psycopg2
import pandas as pd


def connection_database():
    conn_db = psycopg2.connect(
        host="ec2-34-247-16-250.eu-west-1.compute.amazonaws.com",
        database="d1fqoktf0gl90p",
        user="xpfxvuvcndvbve",
        password="43b5e0de771549a5cb3117f84603628575b85328a0aecd350b017dcbf4534ddb",
    )
    return conn_db


def get_data_to_df(data_name, db, file_path):
    if data_name == "Diabet inde":
        sql_query = "SELECT * FROM diabete_inde;"
        cursor = db.cursor()
        cursor.execute(sql_query)
        data = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(data, columns=columns)

    elif data_name == "Vin":
        sql_query = "SELECT * FROM vin;"
        cursor = db.cursor()
        cursor.execute(sql_query)
        data = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(data, columns=columns)

    else:

        # Lire le fichier CSV en DataFrame
        df = pd.read_csv(file_path, sep=",")

    return df
