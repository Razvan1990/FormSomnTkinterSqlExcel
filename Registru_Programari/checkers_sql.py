import os
import constants_programari
import sqlite3
from datetime import datetime
from checker_fields import CheckFields


class CheckSqlCommands:

    def __init__(self):
        self.checker = CheckFields()

    def check_if_table_exists(self, table_name):
        # connecting to database
        database = os.path.join(os.getcwd(), constants_programari.DATABASE_FOLDER, constants_programari.NAME_DATABASE)
        connection = sqlite3.connect(database)
        my_cursor = connection.cursor()
        # sql statement to check
        my_cursor.execute(
            """SELECT count(*) from sqlite_master  WHERE type ="table" AND name =?""", (table_name,))
        # check the results
        if my_cursor.fetchone()[0] == 1:
            result = True
        else:
            result = False
        my_cursor.close()
        connection.close()
        return result

    def create_table(self, table_name):
        # table name will be in fact the day
        # we just need the hour
        database = os.path.join(constants_programari.DATABASE_FOLDER, constants_programari.NAME_DATABASE)
        connection = sqlite3.connect(database)
        my_cursor = connection.cursor()
        # sql query to create table
        my_cursor.execute(
            """CREATE TABLE """ + table_name + """ (ORA text, PRENUME text, NUME text, CNP text, TELEFON text);"""
        )
        connection.commit()
        connection.close()

    def create_initial_hours_for_table(self, table_name):
        '''

        :param table_name:
        :return: here we will update the table by inserting the hours for programming
        '''
        database = os.path.join(constants_programari.DATABASE_FOLDER, constants_programari.NAME_DATABASE)
        connection = sqlite3.connect(database)
        my_cursor = connection.cursor()
        # sql query to insert the hours
        sql = """INSERT INTO """ + table_name + """ (ORA,PRENUME,NUME,CNP,TELEFON) VALUES (?,?,?,?,?)"""
        my_cursor.executemany(sql, constants_programari.STARTING_TABLE_DAY)
        connection.commit()
        connection.close()

    def get_list_with_tables(self):
        database = os.path.join(constants_programari.DATABASE_FOLDER, constants_programari.NAME_DATABASE)
        connection = sqlite3.connect(database)
        my_cursor = connection.cursor()
        sql_retrieve_table_command = """SELECT name FROM sqlite_schema WHERE type ='table' """
        my_cursor.execute(sql_retrieve_table_command)
        list_tables_sql = my_cursor.fetchall()
        # get list of tables from returned list of tuples
        list_tables_final = list()  # this list is needed to retrieve from sql
        for tuple_name in list_tables_sql:
            list_tables_final.append(tuple_name[0])
        # transform list with date format
        list_tables_final_dates = list()
        for name_date in list_tables_final:
            date = self.checker.reconvert_date(name_date)
            list_tables_final_dates.append(date)
        # sort the list in cronological order
        list_tables_final_dates.sort(key=lambda data: datetime.strptime(data, "%d-%m-%Y"), reverse=True)
        # recreate tables in sorted order now by reverse engineering the reconvert(convert)
        list_tables_sql_sorted = list()
        for table in list_tables_final_dates:
            sorted_table = self.checker.convert_date(table)
            list_tables_sql_sorted.append(sorted_table)
        return list_tables_sql_sorted

    def compare_list(self, original_list, updated_list):
        for i in range(0, len(original_list)):
            if original_list[i] != updated_list[i]:
                return False
        return True



