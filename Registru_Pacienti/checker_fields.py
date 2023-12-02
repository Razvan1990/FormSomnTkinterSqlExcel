import datetime
from datetime import datetime


class CheckFields:

    def check_if_necessary_fields_completed(self, date, cnp, last_name, ):
        if date == "" or cnp == "" or last_name == "":
            return True
        return False

    def check_selected_date(self, date_selected):
        # get current date
        current_date = datetime.date.today()
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
        global message
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
        global message
        message = ""
        option = 0
        # the only check to do is just to see if there are numbers
        if not tel_number.isdigit():
            option = 1
            message = "NUMARUL DE TELEFON NU TREBUIE SA CONTINA LITERE"
        return message, option

    def check_buttons_selected(self, button1_value, button2_value):
        if button1_value == "" and button2_value == "":
            return True
        return False
