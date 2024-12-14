import sqlite3

class CRUD:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def read_records(self, table_name):
        query = f"SELECT * FROM {table_name}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def add_record(self, table_name, record):
        placeholders = ', '.join(['?'] * len(record))
        query = f"INSERT INTO {table_name} VALUES ({placeholders})"
        self.cursor.execute(query, record)
        self.connection.commit()

    def update_record(self, table_name, record, record_id):
        set_clause = ', '.join([f"{col} = ?" for col in record.keys()])
        query = f"UPDATE {table_name} SET {set_clause} WHERE id = ?"
        self.cursor.execute(query, (*record.values(), record_id))
        self.connection.commit()

    def delete_record(self, table_name, record_id):
        query = f"DELETE FROM {table_name} WHERE id = ?"
        self.cursor.execute(query, (record_id,))
        self.connection.commit()

    def __del__(self):
        self.connection.close()