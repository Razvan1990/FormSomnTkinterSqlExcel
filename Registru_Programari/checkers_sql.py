import os
import constants_programari
import sqlite3


class CheckSqlCommands:

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
