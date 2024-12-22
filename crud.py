import sqlite3

class CRUD:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.connection.row_factory = sqlite3.Row  # Удобно для дебага
        self.cursor = self.connection.cursor()

    def get_total_income(self):
        try:
            query = "SELECT SUM(price) AS total_income FROM Услуги"
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            return result['total_income'] if result['total_income'] is not None else 0
        except Exception as e:
            print(f"Error calculating total income: {e}")
            return 0

    def get_total_expenses(self):
        try:
            query = "SELECT SUM(cost) AS total_expenses FROM Материал"
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            return result['total_expenses'] if result['total_expenses'] is not None else 0
        except Exception as e:
            print(f"Error calculating total expenses: {e}")
            return 0

    def get_material_balance(self):
        try:
            query = """
            SELECT SUM(purchased) - SUM(used) AS material_balance FROM Материал
            """
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            return result['material_balance'] if result['material_balance'] is not None else 0
        except Exception as e:
            print(f"Error calculating material balance: {e}")
            return 0

    def read_records(self, table_name):
        try:
            query = f"SELECT * FROM {table_name}"
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error reading records from {table_name}: {e}")
            return []

    def read_record_by_id(self, table_name, record_id):
        try:
            query = f"SELECT * FROM {table_name} WHERE id = ?"
            self.cursor.execute(query, (record_id,))
            return self.cursor.fetchone()
        except Exception as e:
            print(f"Error reading record with ID {record_id} from {table_name}: {e}")
            return None

    def add_record(self, table_name, record):
        placeholders = ', '.join(['?'] * len(record))
        try:
            query = f"INSERT INTO {table_name} VALUES ({placeholders})"
            self.cursor.execute(query, record)
            self.connection.commit()
        except Exception as e:
            print(f"Error adding record to {table_name}: {e}")

    def update_record(self, table_name, record, record_id):
        set_clause = ', '.join([f"{col} = ?" for col in record.keys()])
        try:
            query = f"UPDATE {table_name} SET {set_clause} WHERE id = ?"
            self.cursor.execute(query, (*record.values(), record_id))
            self.connection.commit()
            print(f"Record with ID {record_id} updated successfully.")
        except Exception as e:
            print(f"Error updating record in {table_name}: {e}")

    def delete_record(self, table_name, record_id):
        try:
            query = f"DELETE FROM {table_name} WHERE id = ?"
            self.cursor.execute(query, (record_id,))
            self.connection.commit()
            print(f"Record with ID {record_id} deleted successfully.")
        except Exception as e:
            print(f"Error deleting record from {table_name}: {e}")

    def __del__(self):
        self.connection.close()
