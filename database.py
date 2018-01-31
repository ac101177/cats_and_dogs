import sqlite3


class Database:
    def __init__(self, database_path):
        self.connect = sqlite3.connect(database_path)
        self.cursor = self.connect.cursor()

    def commit(self):
        self.connect.commit()

    def close(self):
        self.cursor.close()
        self.connect.close()

    def create_table(self, table_name, column_names, value_type, unique_columns=[]):

        table_input = 'create table if not exists ' + table_name + ' ( '
        for i, column in enumerate(column_names):
            if column == 'id':
                table_input += column + ' integer primary key' + ', '
            else:
                table_input += column + ' ' + value_type[i] + ', '
        if unique_columns:
            table_input += "unique( " + ",".join(unique_columns) + " ) "
        else:
            table_input = table_input[:-2]
        table_input += ")"

        self.cursor.execute(table_input)
        self.connect.commit()


    def insert_or_replace_into_table(self, table_name, column_names, item_values):
        insert_input = 'insert or replace into ' + table_name + ' ( ' + ",".join(column_names) + " ) values ( " + ",".join(["?"]*len(column_names)) + " )"
        self.cursor.execute(insert_input, tuple(item_values))
        row_id = self.cursor.lastrowid
        self.connect.commit()
        return row_id

    def delete_from_table(self, table_name, column_names, item_values):
        delete_input = "delete from "+ table_name +" where "+" and ".join([i+"=:"+i for i in column_names])
        self.cursor.execute(delete_input, dict(zip(column_names, item_values)))
        self.connect.commit()

    def check_if_table_is_nonempty(self, table_name):
        return self.cursor.execute("select exists (select * from "+ table_name + ")").fetchone()[0]

# return firstmatch for query to be tested later
    def fetch_first_match_for_table_query(self, table_name, column_names, item_values):
        query_input = 'select * from ' + table_name + ' where ' +" and ".join([i+"=:"+i for i in column_names])
        return self.cursor.execute(query_input, dict(zip(column_names, item_values))).fetchone()

# print all rows in a table ordered by column name to be tested later
    def print_all_rows_of_table(self, table_name):
        for i in self.cursor.execute('select * from ' + table_name).fetchall():
            print(i)
