from database.conect_db import ConnectDB
import pandas as pd

class BaseControl:
    def __init__(self):
        self.conn = ConnectDB().getConection()
        self.cursor = self.conn.cursor()
        self.table = None

    def insert(self, data):
        try:
            column_insert = ",".join(list(data.keys()))
            values_insert = tuple(data.values())
            sql = "INSERT INTO {2}({0}) VALUES ({1})".format(column_insert, ', '.join(['?'] * len(list(data.keys()))), self.table)
            self.cursor.execute(sql, values_insert)
            self.conn.commit()
        except:
            print("Insert Data Fail.")

    def insert_data_from_df(self, df):
        try:
            df.to_sql(self.table, self.conn, if_exists='append', index=False)
            # self.conn.close()
        except:
            print("Insert Data From Datrframe Fail.")

    def get_df_from_db(self):
        QUERY = "SELECT * FROM {}".format(self.table)
        df = pd.read_sql_query(QUERY, self.conn)
        return df