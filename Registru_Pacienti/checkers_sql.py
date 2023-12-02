import os
import constants_pacienti
import sqlite3


class CheckSqlCommands():
    '''
    Here we check all sql things in order for the app to not throw errors
    '''

    def check_if_table_exists(self, table_name):
        # connecting to database
        database = os.path.join(os.getcwd(), constants_pacienti.DATABASE_FOLDER, constants_pacienti.NAME_DATABASE)
        connection = sqlite3.connect(database)
        my_cursor = connection.cursor()
        # sql statement to check
        my_cursor.execute(
            """SELECT count(*) from sqlite_master  WHERE type ="table" AND name =?"""
            , (table_name,))
        # check the results
        if my_cursor.fetchone()[0] == 1:
            result = True
        else:
            result = False
        my_cursor.close()
        connection.close()
        return result

    # selection_date will be used as string because it will be done through a calendar
    def check_for_duplicate_same_day(self, table_name, cnp, selection_date):
        database = os.path.join(os.getcwd(), constants_pacienti.DATABASE_FOLDER, constants_pacienti.NAME_DATABASE)
        connection = sqlite3.connect(database)
        my_cursor = connection.cursor()
        my_cursor.execute(
            """SELECT * from """ + table_name + """ WHERE CNP = """ + "'" + cnp + "'" + """ AND DATA= """ + "'" + selection_date + "'")
        #print(my_cursor.fetchall())
        list_records = my_cursor.fetchall()
        if len(list_records) > 0:
            result = True
        else:
            result = False
        my_cursor.close()
        connection.close()
        return result

    def get_original_list(self, table_name, cnp, last_name):
        database = os.path.join(os.getcwd(), constants_pacienti.DATABASE_FOLDER, constants_pacienti.NAME_DATABASE)
        connection = sqlite3.connect(database)
        my_cursor = connection.cursor()
        my_cursor.execute("SELECT * from " + table_name + " WHERE cnp = " + cnp + "AND last_name= " + last_name)
        result = my_cursor.fetchall()
        my_cursor.close()
        connection.close()
        return result

    def create_table(self, table_name):
        database = os.path.join(constants_pacienti.DATABASE_FOLDER, constants_pacienti.NAME_DATABASE)
        connection = sqlite3.connect(database)
        my_cursor = connection.cursor()
        # sql query to create table
        my_cursor.execute(
            """CREATE TABLE """ + table_name + """
            (DATA text, PRENUME text, NUME text, CNP text, TELEFON text, STRADA text,LOCALITATE text,
            JUDET text, ASIGURARE text,TIP_ASIGURARE text,BILET_TRIMITERE text, NUMAR_BILET text, ANAMNEZA text,
             APNEE text, TIP_APNEE text, TIP_MASCA text, COMPLIANTA text, PRESIUNE text, BOLI_CUNOSCUTE text, BOLI text,
             RECOMANDARE text);""")
        connection.commit()
        connection.close()

    def check_if_table_has_one_record(self, table_name):
        database = os.path.join(constants_pacienti.DATABASE_FOLDER, constants_pacienti.NAME_DATABASE)
        connection = sqlite3.connect(database)
        my_cursor = connection.cursor()
        my_cursor.execute("SELECT COUNT (*) FROM " + table_name)
        nr_records = my_cursor.fetchall()
        print(nr_records)
        if nr_records[0][0] > 0:
            return True
        return False

    def compute_address_excel(self, street_name, locality_name, region_name):
        return street_name + "," + locality_name + "," + region_name
