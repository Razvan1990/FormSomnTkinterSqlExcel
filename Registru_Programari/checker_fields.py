import datetime
from datetime import datetime
import constants_programari


class CheckFields:

    def check_if_necessary_fields_completed(self, last_name, cnp, telephone_number, ):
        if telephone_number == "" or cnp == "" or last_name == "":
            return True
        return False

    def check_radiobutton_pressed(self, radiobutton_value):
        if radiobutton_value == "":
            return True
        return False

    def check_selected_date(self, date_selected):
        # get current date
        current_date = datetime.today()
        # convert today to string format
        current_date_string = current_date.strftime("%d-%m-%Y")
        # start comparing
        current_date_converted = datetime.strptime(current_date_string, "%d-%m-%Y")
        date_selected_converted = datetime.strptime(date_selected, "%d-%m-%Y")
        if current_date_converted > date_selected_converted:
            return True
        return False

    def get_cnp_errors(self, cnp):
        # in the sql_add function we will check if the option is different from 0
        message = ""
        option = 0
        if len(cnp) != 13:
            message = "CNP-UL INTRODUSE NU ARE 13 CIFRE!"
            option = 1
        elif not cnp.isdigit():
            message = "CNP-UL NU TREBUIE SA CONTINA LITERE!"
            option = 2
        elif cnp.startswith("3") or cnp.startswith("4") or cnp.startswith("0"):
            message = "CNP-UL INTRODUS NU EXISTA SAU APARTINE CUIVA NASCUT INAINTE DE 1900!"
            option = 3
        return message, option

    def get_telephone_number_errors(self, tel_number):
        message = ""
        option = 0
        if not tel_number.isdigit():
            option = 1
            message = "NUMARUL DE TELEFON NU TREBUIE SA CONTINA LITERE"
        return message, option

    def check_if_first_last_name_entered(self, first_name, last_name):
        message = ""
        option = 0
        if last_name == "" and first_name == "":
            message = "VA ROG COMPLETATI CAMPURILE DE PRENUME SI NUME"
            option = 1
        elif last_name == "":
            message = "VA ROG COMPLETATI NUMELE"
            option = 2
        elif first_name == "":
            message = "VA ROG COMPLETATI PRENUMELE"
            option = 3
        return option, message

    def check_cnp_complete(self, cnp):
        if cnp == "":
            return True
        return False

    def split_date(self, date_string):
        list_dates = date_string.split("-")
        return list_dates

    def convert_date(self, date_string):
        new_date = "D" + "_" + date_string.replace("-", "_")
        return new_date

    def reconvert_date(self, date_table_name):
        #this function is used to create the excel sheets with date and to sort list by dates
        original_date = date_table_name[2:].replace("_", "-")
        return original_date

    def get_hours_list(self):
        list_hours_results = []
        for element in constants_programari.STARTING_TABLE_DAY:
            list_hours_results.append(element[0])
        return list_hours_results





