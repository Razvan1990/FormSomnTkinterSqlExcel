import os
import sqlite3
import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
from datetime import datetime
from checker_fields import CheckFields
from checkers_sql import CheckSqlCommands
from sms_sender import SendSmsAppointment
from excel_writer import ExcelWriter
import constants_programari


class GuiApp:

    def __init__(self):
        self.pictures_folder = os.getcwd()
        self.checkers_fields = CheckFields()
        self.checkers_sql = CheckSqlCommands()
        self.sms_sender = SendSmsAppointment()
        self.excel_writer = ExcelWriter()

    '''
    ADD PART
    '''

    def cancel_appointment_add(self):
        root_appointments_addition.destroy()
        # self.create_main_gui()

    def add_appointment(self, name, cnp, telephone_number, selection_day):
        '''MAKE CHECKS'''
        # 1. check if fields are completed
        if self.checkers_fields.check_if_necessary_fields_completed(name, cnp, telephone_number):
            messagebox.showerror(parent=root_appointments_addition, title="DATE NECOMPLETATE",
                                 message="COMPLETATI DATELE OBLIGATORII!")
            return
            # 2. check cnp
        message_error_cnp, option_error_cnp = self.checkers_fields.get_cnp_errors(cnp)
        if option_error_cnp == 1:
            messagebox.showerror(parent=root_appointments_addition, title="CNP INVALID", message=message_error_cnp)
            return
        elif option_error_cnp == 2:
            messagebox.showerror(parent=root_appointments_addition, title="CNP INVALID", message=message_error_cnp)
            return
        elif option_error_cnp == 3:
            messagebox.showerror(parent=root_appointments_addition, title="CNP INVALID", message=message_error_cnp)
            return
            # 3. check telephone number
        message_error_telephone, option_error_telephone = self.checkers_fields.get_telephone_number_errors(
            telephone_number)
        if option_error_telephone != 0:
            messagebox.showerror(parent=root_appointments_addition, title="NUMAR INVALID",
                                 message=message_error_telephone)
            return
        '''SQL COMMAND'''
        database = os.path.join(constants_programari.DATABASE_FOLDER, constants_programari.NAME_DATABASE)
        connection = sqlite3.connect(database)
        my_cursor = connection.cursor()
        # we will practically do an update here as something is already completed
        table_name = self.checkers_fields.convert_date(selection_day)
        my_cursor.execute("""UPDATE """ + table_name + """ SET
        ORA=:hour_add,
        PRENUME=:first_name_add,
        NUME=:last_name_add,
        CNP=:cnp_add,
        TELEFON=:telephone_add WHERE oid=:id""",
                          # dummy dictionary
                          {
                              "hour_add": hour_entry.get(),
                              "first_name_add": first_name_entry_add.get().upper(),
                              "last_name_add": last_name_entry_add.get().upper(),
                              "cnp_add": cnp_entry_add.get(),
                              "telephone_add": telephone_entry_add.get(),
                              "id": list_appointment[0]
                          }
                          )
        connection.commit()
        connection.close()
        message_appointment = "Pacientul {} a fost programat la consult in data de {} in intervalul orar {}".format(
            name,
            selection_day,
            hour_entry.get())
        messagebox.showinfo(parent=root_appointments_addition, title="PROGRAMARE CU SUCCESS",
                            message=message_appointment)
        # send sms to recipient
        '''THIS PART IS WORKING BUT SMS CAN BE SENT JUST TO VERIFIED NUMBER(ME)'''
        # self.sms_sender.add_phone_to_list(telephone_number,first_name_entry_add.get(), name)
        # self.sms_sender.send_sms(telephone_number,selection_day,hour_entry.get())
        '''SECOND METHOD WORKS BETTER FROM SINCH'''
        # self.sms_sender.send_sms2(telephone_number,selection_day, hour_entry.get())
        root_appointments_addition.destroy()
        root_add_treeview.destroy()
        self.create_main_gui()

    def make_appointment_gui(self):

        # create global entries
        global root_appointments_addition
        global date_entry_label
        global hour_entry
        global first_name_entry_add
        global last_name_entry_add
        global cnp_entry_add
        global telephone_entry_add
        global list_appointment

        # check to see if selected hour is not for a completed appointment
        list_appointment = []
        for appointment in tree_appointments_add.selection():
            appointment_data = tree_appointments_add.item(appointment)
            appointment_list_values = appointment_data["values"]
            list_appointment = appointment_list_values
        # root_add_treeview.destroy()
        # 1. check to see if selected hour has not been completed
        if list_appointment[3] != "" or list_appointment[4] != "" or list_appointment[5] != "":
            messagebox.showerror("SLOT OCUPAT", "ACEAST INTERVAL ARE DEJA O PROGRAMARE")
            return
        # create frame
        root_appointments_addition = Tk()
        root_appointments_addition.title("PROGRAMARE")
        image_ico = os.path.join(self.pictures_folder, constants_programari.PICTURE_FOLDER,
                                 constants_programari.SOMN_ICO_IMAGE)
        root_appointments_addition.iconbitmap(image_ico)
        root_appointments_addition.geometry("600x500")
        root_appointments_addition["bg"] = "#5BBD2A"
        root_appointments_addition.resizable(NO, NO)
        frame_title = LabelFrame(root_appointments_addition, fg="#EEEBF3", bg="#5BBD2A", font=("Helvetica", 20, "bold"),
                                 bd=5,
                                 cursor="target", width=500, height=425, labelanchor="n", text="ADAUGARE PROGRAMARE",
                                 relief=tkinter.GROOVE)
        frame_title.grid(padx=42, pady=10, row=0, column=0, )  # put it in the middle
        frame_title.grid_rowconfigure(0, weight=1)
        frame_title.grid_columnconfigure(0, weight=1)
        '''CREATE ENTRIES AND LABELS'''
        # date
        date_entry_label = Label(frame_title, width=25, justify="center", font=("Comic Sans", 11, "bold italic"),
                                 cursor="target",
                                 bg="#5BBD2A", fg="#DA3B22", text=calendar_add.get_date())
        date_entry_label.place(x=220, y=30)
        # hour
        hour_entry = Entry(frame_title, width=25, justify="center", font=("Helvetica", 9, "bold"),
                           cursor="target",
                           bg="#D4E2D0")
        hour_entry.place(x=250, y=80)
        # first_name
        first_name_entry_add = Entry(frame_title, width=25, justify="center", font=("Helvetica", 9, "bold"),
                                     cursor="target",
                                     bg="#D4E2D0")
        first_name_entry_add.place(x=250, y=130)
        # last_name
        last_name_entry_add = Entry(frame_title, width=25, justify="center", font=("Helvetica", 9, "bold"),
                                    cursor="target",
                                    bg="#D4E2D0")
        last_name_entry_add.place(x=250, y=180)
        # cnp
        cnp_entry_add = Entry(frame_title, width=25, justify="center", font=("Helvetica", 9, "bold"),
                              cursor="target",
                              bg="#D4E2D0")
        cnp_entry_add.place(x=250, y=230)
        # telephone
        telephone_entry_add = Entry(frame_title, width=25, justify="center",
                                    font=("Helvetica", 9, "bold"),
                                    cursor="target",
                                    bg="#D4E2D0")
        telephone_entry_add.place(x=250, y=280)
        # LABELS
        date_label_add = Label(frame_title, text="DATA", justify="center",
                               font=("Comic Sans", 11, "bold italic"),
                               cursor="star", fg="#DA3B22", bg="#5BBD2A", )
        date_label_add.place(x=80, y=30)

        hour_label_add = Label(frame_title, text="ORA*", justify="center",
                               font=("Helvetica", 11, "bold"),
                               cursor="star", fg="#C6E744", bg="#5BBD2A", )
        hour_label_add.place(x=50, y=80)

        first_name_label_add = Label(frame_title, text="PRENUME", justify="center",
                                     font=("Helvetica", 11, "bold"),
                                     cursor="star", fg="#C6E744", bg="#5BBD2A", )
        first_name_label_add.place(x=50, y=130)

        last_name_label_add = Label(frame_title, text="NUME*", justify="center",
                                    font=("Helvetica", 11, "bold"),
                                    cursor="star", fg="#C6E744", bg="#5BBD2A", )
        last_name_label_add.place(x=50, y=180)

        cnp_label_add = Label(frame_title, text="CNP*", justify="center",
                              font=("Helvetica", 11, "bold"),
                              cursor="star", fg="#C6E744", bg="#5BBD2A", )
        cnp_label_add.place(x=50, y=230)

        telephone_label_add = Label(frame_title, text="TELEFON*", justify="center",
                                    font=("Helvetica", 11, "bold"),
                                    cursor="star", fg="#C6E744", bg="#5BBD2A", )
        telephone_label_add.place(x=50, y=280)
        # add buttons
        ok_button_update = Button(frame_title, text="PROGRAMEAZA", width=20, height=2, fg="#1E2729", bg="#248B48",
                                  font=("Helvetica", 9, "bold"),
                                  command=lambda: self.add_appointment(last_name_entry_add.get(),
                                                                       cnp_entry_add.get(),
                                                                       telephone_entry_add.get(),
                                                                       calendar_add.get_date()))
        cancel_button = Button(frame_title, text="CANCEL", width=20, height=2, fg="#1E2729", bg="#E8E7D8",
                               font=("Helvetica", 9, "bold"), command=self.cancel_appointment_add)
        ok_button_update.place(x=50, y=320)
        cancel_button.place(x=280, y=320)

        # MAKE THE HOUR ALREADY COMPLETED AND DISABLE ENTRY
        hour_entry.insert(0, list_appointment[1])
        hour_entry["state"] = tkinter.DISABLED

    def cancel_treeview_add(self):
        root_add_treeview.destroy()
        self.create_main_gui()

    def check_available_hours(self):
        # check if selected date is not in the past
        date_selected = calendar_add.get_date()
        if self.checkers_fields.check_selected_date(date_selected):
            messagebox.showerror("DATA INVALIDA", "DATA SELECTATA ESTE DIN TRECUT")
            return
        # check to see if the table already exists in the database
        # transform date with _ instead of -
        date_selected_new = self.checkers_fields.convert_date(date_selected)
        if not self.checkers_sql.check_if_table_exists(date_selected_new):
            # 1. first we create the table
            self.checkers_sql.create_table(date_selected_new)
            # 2. second we need to update the initial table with hours
            self.checkers_sql.create_initial_hours_for_table(date_selected_new)

        '''SQL COMMAND TO RETRIEVE DATA'''
        database = os.path.join(constants_programari.DATABASE_FOLDER, constants_programari.NAME_DATABASE)
        connection = sqlite3.connect(database)
        my_cursor = connection.cursor()
        my_cursor.execute("""SELECT oid, *FROM """ + date_selected_new)
        list_appointments = my_cursor.fetchall()
        '''
        CREATE GUI FOR TREEVIEW
        '''
        root_add.destroy()
        global root_add_treeview
        global tree_appointments_add
        # used to store the values for the make_appointment_gui function
        global record_update_tuple
        root_add_treeview = Tk()
        root_add_treeview.title("ADD")
        image_ico = os.path.join(self.pictures_folder, constants_programari.PICTURE_FOLDER,
                                 constants_programari.SOMN_ICO_IMAGE)
        root_add_treeview.iconbitmap(image_ico)
        root_add_treeview.geometry("900x600")
        root_add_treeview["bg"] = "#5BBD2A"
        root_add_treeview.resizable(NO, NO)
        root_add_treeview.protocol("WM_DELETE_WINDOW", self.cancel_x_button)
        # frame creation
        frame_treeview = LabelFrame(root_add_treeview, fg="#EEEBF3", bg="#5BBD2A", font=("Helvetica", 16, "bold"), bd=5,
                                    cursor="target", width=750, height=475, labelanchor="n",
                                    text="VIZUALIZARE PROGRAMARI " + date_selected,
                                    relief=tkinter.GROOVE)
        frame_treeview.grid(padx=70, pady=10, row=0, column=0, )  # put it in the middle
        frame_treeview.grid_rowconfigure(0, weight=1)
        frame_treeview.grid_columnconfigure(0, weight=1)
        # create treeview
        columns = ("ID", "ORA", "PRENUME", "NUME", "CNP", "TELEFON")
        tree_appointments_add = ttk.Treeview(frame_treeview, show='headings', columns=columns, height=16, )
        # ADD THE COLUMNS
        # define the headings
        tree_appointments_add.heading(0, text="ID", anchor=tkinter.CENTER)
        tree_appointments_add.heading(1, text="ORA", anchor=tkinter.CENTER)
        tree_appointments_add.heading(2, text="PRENUME", anchor=tkinter.CENTER)
        tree_appointments_add.heading(3, text="NUME", anchor=tkinter.CENTER)
        tree_appointments_add.heading(4, text="CNP", anchor=tkinter.CENTER)
        tree_appointments_add.heading(5, text="TELEFON", anchor=tkinter.CENTER)
        # redefine column dimensions
        tree_appointments_add.column("ID", width=25, )
        tree_appointments_add.column("ORA", width=125)
        tree_appointments_add.column("PRENUME", width=150, stretch=NO)
        tree_appointments_add.column("NUME", width=150, stretch=NO)
        tree_appointments_add.column("CNP", width=125, stretch=NO)
        tree_appointments_add.column("TELEFON", width=125, stretch=NO)
        tree_appointments_add.tag_configure("orow")
        # create a custom style
        style = ttk.Style(root_add_treeview)
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="#D4EE77", foreground="#C7651D", justify="center")
        style.configure("Treeview", background="#5B5F51", fieldbackground="#5B5F51", foreground="#F1F7E5",
                        font=("Helvetica", 10, "bold"))
        # change selection color
        style.map("Treeview", background=[("selected", "#A3D623")])
        # populate the list
        for appointment in list_appointments:
            record_update = list()
            record_update.append(str(appointment[0]))
            record_update.append(appointment[1])
            record_update.append(appointment[2])
            record_update.append(appointment[3])
            record_update.append(appointment[4])
            record_update.append(appointment[5])
            record_update_tuple = tuple(record_update)
            tree_appointments_add.insert('', tkinter.END, values=record_update_tuple)
        # put treeview on frame
        tree_appointments_add.place(x=18, y=20)
        # add buttons for cancel and delete
        cancel_button = Button(frame_treeview, text="CANCEL", width=40, height=2, fg="#1E2729", bg="#E8E7D8",
                               font=("Helvetica", 9, "bold"), command=self.cancel_treeview_add)
        cancel_button.place(x=230, y=385)
        tree_appointments_add.bind("<Double-Button-1>", lambda event: self.make_appointment_gui())
        root_add_treeview.mainloop()

    def cancel_form_add(self):
        root_add.destroy()
        self.create_main_gui()

    def create_add_gui(self):
        app_menu.destroy()
        # global variables
        global root_add
        global calendar_add

        root_add = Tk()
        root_add.title("ADD")
        image_ico = os.path.join(self.pictures_folder, constants_programari.PICTURE_FOLDER,
                                 constants_programari.SOMN_ICO_IMAGE)
        root_add.iconbitmap(image_ico)
        root_add.geometry("600x400")
        root_add["bg"] = "#5BBD2A"
        root_add.resizable(NO, NO)

        # root_add.protocol("WM_DELETE_WINDOW", self.cancel_x_button)
        # create first frame for title label
        frame_title = LabelFrame(root_add, fg="#EEEBF3", bg="#5BBD2A", font=("Helvetica", 15, "bold"), bd=5,
                                 cursor="target", width=500, height=350, labelanchor="n", text="ADAUGARE PROGRAMARE",
                                 relief=tkinter.GROOVE)
        frame_title.grid(padx=42, pady=10, row=0, column=0, )  # put it in the middle
        frame_title.grid_rowconfigure(0, weight=1)
        frame_title.grid_columnconfigure(0, weight=1)
        # Add calendar
        calendar_add = Calendar(frame_title, selectmode='day', date_pattern="DD-MM-YYYY", bd=2,
                                headersbackground="#EBFE8A",
                                headersforeground="#1E1F1C", selectbackground="#209DBF", selectforeground="#F26B18",
                                weekendbackground="#8D7B80", font=("Helvetica", 9, "bold"))
        calendar_add.place(x=200, y=30)
        calendar_label = Label(frame_title, text="DATA PROGRAMARE", justify="center", font=("Helvetica", 13, "bold"),
                               cursor="star", fg="#3D91C4", bg="#5BBD2A")
        calendar_label.place(x=20, y=100)
        # CREATE BUTTONS
        ok_button = Button(frame_title, text="DISPONIBILITATE", width=20, height=2, fg="#1E2729", bg="#248B48",
                           font=("Helvetica", 9, "bold"),
                           command=lambda: self.check_available_hours())
        cancel_button = Button(frame_title, text="CANCEL", width=20, height=2, fg="#1E2729", bg="#E8E7D8",
                               font=("Helvetica", 9, "bold"), command=self.cancel_form_add)
        ok_button.place(x=40, y=250)
        cancel_button.place(x=300, y=250)

    '''
    SEARCH PART
    '''

    def cancel_search_treeview(self):
        root_search_treeview.destroy()

    def get_appointments_dates_hours(self, option, first_name, last_name, cnp):
        '''
        Here we will get all the tables and traverse all the tables to get the records
        based on the search pattern
        :return: A listbox with all dates and respective hour when a patient  is programmed
        '''
        '''MAKE CHECKS'''
        # 1.check button is pressed
        if self.checkers_fields.check_radiobutton_pressed(option):
            messagebox.showerror("NICI O SELECTIE", "VA ROG SELECTATI O OPTIUNE DE CAUTARE")
            return
        # 2. check last and first name
        if option == "Nume":
            option_error, message_error = self.checkers_fields.check_if_first_last_name_entered(first_name, last_name)
            if option_error == 1:
                messagebox.showerror("CAMPURI NECOMPLETATE", message=message_error)
                return
            elif option_error == 2:
                messagebox.showerror("NUME NECOMPLETAT", message=message_error)
                return
            elif option_error == 3:
                messagebox.showerror("PRENUME NECOMPLETAT", message=message_error)
                return
        # 3. check cnp
        if option == "Cnp":
            if self.checkers_fields.check_cnp_complete(cnp):
                messagebox.showerror("CNP NECOMPLETAT", "VA ROG COMPLETATI CNP-UL")
                return
            cnp_message_error, cnp_option_error = self.checkers_fields.get_cnp_errors(cnp)
            if cnp_option_error == 1:
                messagebox.showerror("CNP INVALID", message=cnp_message_error)
                return
            elif cnp_option_error == 2:
                messagebox.showerror("CNP INVALID", message=cnp_message_error)
                return
            elif cnp_option_error == 3:
                messagebox.showerror("CNP INVALID", message=cnp_message_error)
                return
        '''SQL COMMAND'''
        # 1. FIRST WE NEED TO ITERATE AND TAKE ALL THE TABLES
        # a dictionary to have the results table hour pairs
        dict_results = {}
        database = os.path.join(os.getcwd(), constants_programari.DATABASE_FOLDER,
                                constants_programari.NAME_DATABASE)
        connection = sqlite3.connect(database)
        my_cursor = connection.cursor()
        sql_retrieve_table_command = """SELECT name FROM sqlite_schema WHERE type ='table' """
        my_cursor.execute(sql_retrieve_table_command)
        list_tables_sql = my_cursor.fetchall()
        # get list of tables from returned list of tuples
        list_tables_final = list()  # this list is needed to retrieve from sql
        for tuple_name in list_tables_sql:
            list_tables_final.append(tuple_name[0])
        # sort the list in order
        # transform list with date format
        list_tables_final_dates = list()
        for name_date in list_tables_final:
            date = self.checkers_fields.reconvert_date(name_date)
            list_tables_final_dates.append(date)
        # sort the list in chronological order
        list_tables_final_dates.sort(key=lambda data: datetime.strptime(data, "%d-%m-%Y"), reverse=True)
        # recreate tables in sorted order now by reverse engineering the reconvert(convert)
        list_tables_sql_sorted = list()
        for table in list_tables_final_dates:
            sorted_table = self.checkers_fields.convert_date(table)
            list_tables_sql_sorted.append(sorted_table)
        # now we need to iterate on every table and fetch the results from there
        for table_name in list_tables_sql_sorted:
            if option == "Nume":
                my_cursor.execute(
                    """SELECT ORA, NUME, CNP FROM """ + table_name + """ WHERE PRENUME=:first_name AND NUME=:last_name""",
                    # dummy dictionary
                    {
                        "first_name": first_name.upper(),
                        "last_name": last_name.upper()
                    }
                )
                list_results = my_cursor.fetchall()
                # put just lists with data available
                if len(list_results) != 0:
                    dict_results.update({table_name[2:]: list_results[0]})
            elif option == "Cnp":
                my_cursor.execute(
                    """SELECT ORA, NUME, CNP FROM """ + table_name + """ WHERE CNP=:cnp""",
                    # dummy dictionary
                    {
                        "cnp": cnp
                    }
                )
                list_results = my_cursor.fetchall()
                # put just lists with data available
                if len(list_results) != 0:
                    dict_results.update({table_name[2:]: list_results[0]})
        # check dictionary is not empty -> no valid appointment
        if len(dict_results) == 0:
            messagebox.showerror("PROGRAMARE INEXISTENTA", "NU EXISTA O PROGRAMARE CU ACESTE DATE")
            return
        '''CREATE GUI TO SHOW DATA'''
        global root_search_treeview
        root_search_treeview = Tk()
        root_search_treeview.title("SEARCH")
        image_ico = os.path.join(self.pictures_folder, constants_programari.PICTURE_FOLDER,
                                 constants_programari.SOMN_ICO_IMAGE)
        root_search_treeview.iconbitmap(image_ico)
        root_search_treeview.geometry("650x400")
        root_search_treeview["bg"] = "#32BBAD"
        root_search_treeview.resizable(NO, NO)
        root_search_treeview.protocol("WM_DELETE_WINDOW", self.cancel_x_button)
        # treeview creation
        frame_treeview = LabelFrame(root_search_treeview, fg="#EEEBF3", bg="#32BBAD", font=("Helvetica", 15, "bold"),
                                    bd=5,
                                    cursor="target", width=575, height=375, labelanchor="n",
                                    text=last_name.upper() + " " + cnp,
                                    relief=tkinter.GROOVE)  # it shows eithher the name or the cnp depending on what is selecting
        frame_treeview.grid(padx=40, pady=10, row=0, column=0, )  # put it in the middle
        frame_treeview.grid_rowconfigure(0, weight=1)
        frame_treeview.grid_columnconfigure(0, weight=1)
        # create tree to show appointments
        columns = ("DATA", "ORA", "NUME", "CNP")
        tree_searches = ttk.Treeview(frame_treeview, show='headings', columns=columns, height=13)
        # ADD THE COLUMNS
        # define the headings
        tree_searches.heading(0, text="DATA", anchor=tkinter.CENTER)
        tree_searches.heading(1, text="ORA", anchor=tkinter.CENTER)
        tree_searches.heading(2, text="NUME", anchor=tkinter.CENTER)
        tree_searches.heading(3, text="CNP", anchor=tkinter.CENTER)
        # redefine column dimensions
        tree_searches.column("DATA", width=100, stretch=NO)
        tree_searches.column("ORA", width=125, stretch=NO)
        tree_searches.column("NUME", width=125, stretch=NO)
        tree_searches.column("CNP", width=125, stretch=NO)
        tree_searches.tag_configure("orow")
        # create a custom style
        style = ttk.Style(root_search_treeview)
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="#D4EE77", foreground="#C7651D")
        # populate the list
        for key in dict_results:
            record_update = list()
            record_update.append(key.replace("_", "-"))
            record_update.append(dict_results[key][0])
            record_update.append(dict_results[key][1])
            record_update.append(dict_results[key][2])
            record_update_tuple_searches = tuple(record_update)
            tree_searches.insert('', tkinter.END, values=record_update_tuple_searches)
        tree_searches.place(x=35, y=10)
        # create a scrollbar
        my_scrollbar = Scrollbar(frame_treeview, orient=tkinter.VERTICAL, command=tree_searches.yview)
        tree_searches.configure(yscrollcommand=my_scrollbar.set)
        my_scrollbar.place(x=513, y=11, height=288)
        # add ok button to quit treeview
        ok_button = Button(frame_treeview, text="INCHIDERE REZULTATE", width=30, height=2, fg="#1E2729", bg="#E8E7D8",
                           font=("Helvetica", 9, "bold"), command=self.cancel_search_treeview)
        ok_button.place(x=170, y=302)

    def handle_radio_button_name(self, value_name, *args):
        # value_name = selection_option1
        if args[0] == value_name:
            # first we make the first and last name states enabled
            args[1]["state"] = tkinter.NORMAL
            args[2]["state"] = tkinter.NORMAL
            # delete cnp and make it disabled
            args[3]["state"] = tkinter.NORMAL
            args[3].delete(0, END)
            args[3]["state"] = tkinter.DISABLED

    def handle_radio_button_cnp(self, value_cnp, *args):
        # value_cnp = selection_option2
        if args[0] == value_cnp:
            # first we make the cnp enabled
            args[1]["state"] = tkinter.NORMAL
            # delete the first and last name and make them disabled
            args[2]["state"] = tkinter.NORMAL
            args[3]["state"] = tkinter.NORMAL
            args[2].delete(0, END)
            args[3].delete(0, END)
            # make them  disabled again
            args[2]["state"] = tkinter.DISABLED
            args[3]["state"] = tkinter.DISABLED

    def cancel_form_search(self):
        root_search.destroy()
        self.create_main_gui()

    def create_search_gui(self):
        app_menu.destroy()
        global root_search
        global radio_button_name
        global radio_button_cnp
        global first_name_entry_search
        global last_name_entry_search
        global cnp_entry_search
        global selection_search_option

        root_search = Tk()
        root_search.title("CAUTARE")
        image_ico = os.path.join(self.pictures_folder, constants_programari.PICTURE_FOLDER,
                                 constants_programari.SOMN_ICO_IMAGE)
        root_search.iconbitmap(image_ico)
        root_search.geometry("720x330")
        root_search["bg"] = "#32BBAD"
        root_search.resizable(NO, NO)
        root_search.protocol("WM_DELETE_WINDOW", self.cancel_x_button)
        # stringvars
        selection_search_option = StringVar()
        selection_option1 = "Nume"
        selection_option2 = "Cnp"
        frame_title = LabelFrame(root_search, fg="#EEEBF3", bg="#32BBAD", font=("Helvetica", 20, "bold"), bd=5,
                                 cursor="target", width=650, height=300, labelanchor="n", text="CAUTARE PACIENT",
                                 relief=tkinter.GROOVE)
        frame_title.grid(padx=30, pady=10, row=0, column=0, )  # put it in the middle
        frame_title.grid_rowconfigure(0, weight=1)
        frame_title.grid_columnconfigure(0, weight=1)
        # add frame for first and last name
        frame_first_last_name = LabelFrame(frame_title, fg="#EEEBF3", bg="#32BBAD", font=("Helvetica", 15, "bold"),
                                           bd=5,
                                           cursor="target", width=230, height=190, labelanchor="n",
                                           text="SELECTIE NUME",
                                           relief=tkinter.GROOVE)
        frame_first_last_name.place(x=20, y=10)
        first_name_entry_search = Entry(frame_first_last_name, width=18, justify="center",
                                        font=("Helvetica", 8, "bold"),
                                        cursor="target",
                                        bg="#9EEB8D", state=tkinter.DISABLED)
        first_name_entry_search.place(x=100, y=40)
        first_name_entry_label = Label(frame_first_last_name, text="PRENUME", justify="center",
                                       font=("Helvetica", 11, "bold"),
                                       cursor="star", fg="#5F6B78", bg="#32BBAD")
        first_name_entry_label.place(x=5, y=40)
        last_name_entry_search = Entry(frame_first_last_name, width=18, justify="center",
                                       font=("Helvetica", 8, "bold"),
                                       cursor="target",
                                       bg="#9EEB8D", state=tkinter.DISABLED)
        last_name_entry_search.place(x=100, y=100)
        last_name_entry_label = Label(frame_first_last_name, text="NUME", justify="center",
                                      font=("Helvetica", 11, "bold"),
                                      cursor="star", fg="#5F6B78", bg="#32BBAD")
        last_name_entry_label.place(x=5, y=100)
        # add cnp frame
        frame_cnp = LabelFrame(frame_title, fg="#EEEBF3", bg="#32BBAD", font=("Helvetica", 15, "bold"),
                               bd=5,
                               cursor="target", width=230, height=190, labelanchor="n",
                               text="SELECTIE CNP",
                               relief=tkinter.GROOVE)
        frame_cnp.place(x=270, y=10)
        cnp_entry_search = Entry(frame_cnp, width=20, justify="center",
                                 font=("Helvetica", 8, "bold"),
                                 cursor="target",
                                 bg="#9EEB8D", state=tkinter.DISABLED)
        cnp_entry_search.place(x=80, y=70)
        cnp_search_label = Label(frame_cnp, text="CNP", justify="center",
                                 font=("Helvetica", 11, "bold"),
                                 cursor="star", fg="#5F6B78", bg="#32BBAD")
        cnp_search_label.place(x=5, y=70)
        # create frame for checkbuttons
        check_frame = LabelFrame(frame_title, fg="#EEEBF3", bg="#32BBAD", font=("Helvetica", 15, "bold"),
                                 bd=5,
                                 cursor="target", width=100, height=190, labelanchor="n",
                                 text="CHECK",
                                 relief=tkinter.GROOVE)
        check_frame.place(x=520, y=10)
        # put radiobuttons
        radio_button_name = Radiobutton(check_frame, text="NAME", variable=selection_search_option,
                                        value=selection_option1,
                                        bd=5, font=("Helvetica", 11, "bold"),
                                        bg="#32BBAD", fg="#EEEBF3", selectcolor="black",
                                        command=lambda: self.handle_radio_button_name(selection_option1,
                                                                                      selection_search_option.get(),
                                                                                      first_name_entry_search,
                                                                                      last_name_entry_search,
                                                                                      cnp_entry_search))
        radio_button_name.place(x=5, y=30)
        radio_button_cnp = Radiobutton(check_frame, text="CNP", variable=selection_search_option,
                                       value=selection_option2,
                                       bd=5, font=("Helvetica", 11, "bold"),
                                       bg="#32BBAD", fg="#EEEBF3", selectcolor='black',
                                       command=lambda: self.handle_radio_button_cnp(selection_option2,
                                                                                    selection_search_option.get(),
                                                                                    cnp_entry_search,
                                                                                    first_name_entry_search,
                                                                                    last_name_entry_search))

        radio_button_cnp.place(x=5, y=100)
        # put ok and cancel buttons
        ok_button = Button(frame_title, text="VIZUALIZARE", width=30, height=2, fg="#1E2729", bg="#248B48",
                           font=("Helvetica", 9, "bold"),
                           command=lambda: self.get_appointments_dates_hours(selection_search_option.get(),
                                                                             first_name_entry_search.get(),
                                                                             last_name_entry_search.get(),
                                                                             cnp_entry_search.get()))
        cancel_button = Button(frame_title, text="CANCEL", width=30, height=2, fg="#1E2729", bg="#E8E7D8",
                               font=("Helvetica", 9, "bold"), command=self.cancel_form_search)
        ok_button.place(x=70, y=210)
        cancel_button.place(x=350, y=210)
        root_search.mainloop()

    '''
    DELETE PART
    '''

    def delete_appointment_sql(self, table_name):
        database = os.path.join(constants_programari.DATABASE_FOLDER, constants_programari.NAME_DATABASE)
        connection = sqlite3.connect(database)
        my_cursor = connection.cursor()
        # our delete method is in fact an update method because we want to maintain the ID and HOUR
        my_cursor.execute("""UPDATE """ + table_name + """ SET
        PRENUME=:first_name_delete,
        NUME=:last_name_delete,
        CNP=:cnp_delete,
        TELEFON=:telephone_delete WHERE oid=:id""",
                          # dummy dictionary
                          {
                              "first_name_delete": "",
                              "last_name_delete": "",
                              "cnp_delete": "",
                              "telephone_delete": "",
                              "id": list_appointment_delete[0]
                          }
                          )
        connection.commit()
        connection.close()
        message_delete = "Programarea pacientului {} de pe data de {} si ora {} a fost stearsa".format(
            list_appointment_delete[3], table_name[2:].replace("_", "-"), list_appointment_delete[1])
        messagebox.showinfo(parent=root_delete_appointment_gui, title="PROGRAMARE STEARSA", message=message_delete)
        root_delete_appointment_gui.destroy()
        root_delete_appointments.destroy()
        self.create_main_gui()

    def cancel_delete_record(self):
        root_delete_appointment_gui.destroy()

    def delete_appointment_gui(self, date_selected):
        global root_delete_appointment_gui
        global hour_entry_delete
        global first_name_entry_delete
        global last_name_entry_delete
        global cnp_entry_delete
        global telephone_entry_delete
        global list_appointment_delete
        '''CHECK FIRST IF AN EMPTY RECORD IS PRESSED'''
        list_appointment_delete = []
        for appointment in delete_appointments_treeview.selection():
            appointment_data = delete_appointments_treeview.item(appointment)
            appointment_list_values = appointment_data["values"]
            list_appointment_delete = appointment_list_values
        if list_appointment_delete[3] == "" or list_appointment_delete[4] == "":
            messagebox.showerror("SLOT GOL", "NU EXISTA O PROGRAMARE LA ACEST SLOT")
            return
        '''GET DATA FROM SQL COMMAND IN ORDER TO AVOID TELEPHONE BUG FROM TREEVIEW'''
        database = os.path.join(constants_programari.DATABASE_FOLDER, constants_programari.NAME_DATABASE)
        connection = sqlite3.connect(database)
        my_cursor = connection.cursor()
        my_cursor.execute("""SELECT * FROM """ + date_selected + """ WHERE oid=:id""",
                          # dummy dictionary
                          {
                              "id": list_appointment_delete[0]
                          }
                          )
        record_list = my_cursor.fetchall()
        root_delete_appointment_gui = Tk()
        root_delete_appointment_gui.title("STERGERE")
        image_ico = os.path.join(self.pictures_folder, constants_programari.PICTURE_FOLDER,
                                 constants_programari.SOMN_ICO_IMAGE)
        root_delete_appointment_gui.iconbitmap(image_ico)
        root_delete_appointment_gui.geometry("600x500")
        root_delete_appointment_gui["bg"] = "#BC6678"
        root_delete_appointment_gui.resizable(NO, NO)
        frame_title = LabelFrame(root_delete_appointment_gui, fg="#EEEBF3", bg="#BC6678",
                                 font=("Helvetica", 20, "bold"),
                                 bd=5,
                                 cursor="target", width=500, height=425, labelanchor="n", text="STERGERE PROGRAMARE",
                                 relief=tkinter.GROOVE)
        frame_title.grid(padx=42, pady=10, row=0, column=0, )  # put it in the middle
        frame_title.grid_rowconfigure(0, weight=1)
        frame_title.grid_columnconfigure(0, weight=1)
        '''CREATE ENTRIES AND LABELS'''
        # date
        date_entry_delete_label = Label(frame_title, width=25, justify="center", font=("Comic Sans", 11, "bold italic"),
                                        cursor="target",
                                        bg="#BC6678", fg="#27962D", text=date_selected[2:].replace("_", "-"))
        date_entry_delete_label.place(x=220, y=30)
        # hour
        hour_entry_delete = Entry(frame_title, width=25, justify="center", font=("Helvetica", 9, "bold"),
                                  cursor="target",
                                  bg="#D4E2D0")
        hour_entry_delete.place(x=250, y=80)
        # first_name
        first_name_entry_delete = Entry(frame_title, width=25, justify="center", font=("Helvetica", 9, "bold"),
                                        cursor="target",
                                        bg="#D4E2D0")
        first_name_entry_delete.place(x=250, y=130)
        # last_name
        last_name_entry_delete = Entry(frame_title, width=25, justify="center", font=("Helvetica", 9, "bold"),
                                       cursor="target",
                                       bg="#D4E2D0")
        last_name_entry_delete.place(x=250, y=180)
        # cnp
        cnp_entry_delete = Entry(frame_title, width=25, justify="center", font=("Helvetica", 9, "bold"),
                                 cursor="target",
                                 bg="#D4E2D0")
        cnp_entry_delete.place(x=250, y=230)
        # telephone
        telephone_entry_delete = Entry(frame_title, width=25, justify="center",
                                       font=("Helvetica", 9, "bold"),
                                       cursor="target",
                                       bg="#D4E2D0")
        telephone_entry_delete.place(x=250, y=280)
        # LABELS
        date_label_delete = Label(frame_title, text="DATA", justify="center",
                                  font=("Comic Sans", 11, "bold italic"),
                                  cursor="star", fg="#27962D", bg="#BC6678", )
        date_label_delete.place(x=80, y=30)

        hour_label_delete = Label(frame_title, text="ORA*", justify="center",
                                  font=("Helvetica", 11, "bold"),
                                  cursor="star", fg="#C6E744", bg="#BC6678", )
        hour_label_delete.place(x=50, y=80)

        first_name_label_delete = Label(frame_title, text="PRENUME", justify="center",
                                        font=("Helvetica", 11, "bold"),
                                        cursor="star", fg="#C6E744", bg="#BC6678", )
        first_name_label_delete.place(x=50, y=130)

        last_name_label_delete = Label(frame_title, text="NUME*", justify="center",
                                       font=("Helvetica", 11, "bold"),
                                       cursor="star", fg="#C6E744", bg="#BC6678", )
        last_name_label_delete.place(x=50, y=180)

        cnp_label_delete = Label(frame_title, text="CNP*", justify="center",
                                 font=("Helvetica", 11, "bold"),
                                 cursor="star", fg="#C6E744", bg="#BC6678", )
        cnp_label_delete.place(x=50, y=230)

        telephone_label_delete = Label(frame_title, text="TELEFON*", justify="center",
                                       font=("Helvetica", 11, "bold"),
                                       cursor="star", fg="#C6E744", bg="#BC6678", )
        telephone_label_delete.place(x=50, y=280)
        # add buttons
        ok_button_update = Button(frame_title, text="STERGERE", width=20, height=2, fg="#1E2729", bg="#248B48",
                                  font=("Helvetica", 9, "bold"),
                                  command=lambda: self.delete_appointment_sql(date_selected))
        cancel_button = Button(frame_title, text="CANCEL", width=20, height=2, fg="#1E2729", bg="#E8E7D8",
                               font=("Helvetica", 9, "bold"), command=self.cancel_delete_record)
        ok_button_update.place(x=50, y=320)
        cancel_button.place(x=280, y=320)

        # MAKE THE ENTRIES ALREADY COMPLETED AND DISABLE THEM
        hour_entry_delete.insert(0, record_list[0][0])
        hour_entry_delete["state"] = tkinter.DISABLED

        first_name_entry_delete.insert(0, record_list[0][1])
        first_name_entry_delete["state"] = tkinter.DISABLED

        last_name_entry_delete.insert(0, record_list[0][2])
        last_name_entry_delete["state"] = tkinter.DISABLED

        cnp_entry_delete.insert(0, record_list[0][3])
        cnp_entry_delete["state"] = tkinter.DISABLED

        telephone_entry_delete.insert(0, record_list[0][4])
        telephone_entry_delete["state"] = tkinter.DISABLED

    def view_results_day(self, date_selected, root_window):
        '''SQL SELECTION'''
        database = os.path.join(constants_programari.DATABASE_FOLDER, constants_programari.NAME_DATABASE)
        connection = sqlite3.connect(database)
        my_cursor = connection.cursor()
        my_cursor.execute("""SELECT oid, * FROM """ + date_selected)
        list_appointments = my_cursor.fetchall()
        connection.close()
        global delete_appointments_treeview
        # create the columns for the treeview
        columns = ("ID", "ORA", "PRENUME", "NUME", "CNP", "TELEFON")
        delete_appointments_treeview = ttk.Treeview(root_window, show='headings', columns=columns,
                                                    height=16, )
        # ADD THE COLUMNS
        # define the headings
        delete_appointments_treeview.heading(0, text="ID", anchor=tkinter.CENTER)
        delete_appointments_treeview.heading(1, text="ORA", anchor=tkinter.CENTER)
        delete_appointments_treeview.heading(2, text="PRENUME", anchor=tkinter.CENTER)
        delete_appointments_treeview.heading(3, text="NUME", anchor=tkinter.CENTER)
        delete_appointments_treeview.heading(4, text="CNP", anchor=tkinter.CENTER)
        delete_appointments_treeview.heading(5, text="TELEFON", anchor=tkinter.CENTER)
        # redefine column dimensions
        delete_appointments_treeview.column("ID", width=25, )
        delete_appointments_treeview.column("ORA", width=125)
        delete_appointments_treeview.column("PRENUME", width=150, stretch=NO)
        delete_appointments_treeview.column("NUME", width=150, stretch=NO)
        delete_appointments_treeview.column("CNP", width=125, stretch=NO)
        delete_appointments_treeview.column("TELEFON", width=125, stretch=NO)
        delete_appointments_treeview.tag_configure("orow")
        # create a custom style
        style = ttk.Style(root_window)
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="#D4EE77", foreground="#C7651D", justify="center")
        style.configure("Treeview", background="#5B5F51", fieldbackground="#5B5F51", foreground="#F1F7E5",
                        font=("Helvetica", 10, "bold"))
        # change selection color
        style.map("Treeview", background=[("selected", "#A3D623")])
        # populate the list
        for appointment in list_appointments:
            record_update = list()
            record_update.append(str(appointment[0]))
            record_update.append(appointment[1])
            record_update.append(appointment[2])
            record_update.append(appointment[3])
            record_update.append(str(appointment[4]))
            record_update.append(str(appointment[5]))
            record_update_tuple_delete = tuple(record_update)
            delete_appointments_treeview.insert('', tkinter.END, values=record_update_tuple_delete)
            # put treeview on frame
        delete_appointments_treeview.place(x=15, y=10)
        root_window["text"] = "PROGRAMARI: " + date_selected[2:].replace("_", "-")
        delete_appointments_treeview.bind("<Double-Button-1>", lambda event: self.delete_appointment_gui(date_selected))

    def cancel_form_delete(self):
        root_delete_appointments.destroy()
        self.create_main_gui()

    def create_delete_gui(self):
        global root_delete_appointments
        global date_delete
        app_menu.destroy()
        '''RETRIEVE ALL TABLES'''
        list_tables = self.checkers_sql.get_list_with_tables()
        # stringvar for date delete
        global date_delete_value
        root_delete_appointments = Tk()
        root_delete_appointments.title("DELETE")
        image_ico = os.path.join(self.pictures_folder, constants_programari.PICTURE_FOLDER,
                                 constants_programari.SOMN_ICO_IMAGE)
        root_delete_appointments.iconbitmap(image_ico)
        root_delete_appointments.geometry("1200x500")
        root_delete_appointments["bg"] = "#BC6678"
        root_delete_appointments.resizable(NO, NO)
        # stringvar to be defined after root creation
        date_delete_value = StringVar()
        # set the value of the option menu to the first chronological day of the list
        date_delete_value.set(list_tables[0])
        root_delete_appointments.protocol("WM_DELETE_WINDOW", self.cancel_x_button)
        # create frame for delete
        frame_title = LabelFrame(root_delete_appointments, fg="#EEEBF3", bg="#BC6678", font=("Helvetica", 25, "bold"),
                                 bd=5,
                                 cursor="target", width=1100, height=450, labelanchor="n", text="STERGERE PROGRAMARE",
                                 relief=tkinter.GROOVE)
        frame_title.grid(padx=32, pady=10, row=0, column=0, )  # put it in the middle
        frame_title.grid_rowconfigure(0, weight=1)
        frame_title.grid_columnconfigure(0, weight=1)
        # create a frame for datetime
        frame_date_delete = LabelFrame(frame_title, fg="#EEEBF3", bg="#BC6678", font=("Helvetica", 15, "bold"),
                                       bd=5,
                                       cursor="target", width=275, height=250, labelanchor=tkinter.N,
                                       text="SELECTIE ZI",
                                       relief=tkinter.GROOVE)
        frame_date_delete.grid(row=0, column=0, padx=10, pady=10, sticky=tkinter.EW)
        frame_date_delete.grid_rowconfigure(0, weight=1)
        frame_date_delete.grid_columnconfigure(0, weight=1)
        # add the option menu
        date_option_label = Label(frame_date_delete, text="ZIUA", justify="center",
                                  font=("Helvetica", 11, "bold"),
                                  cursor="star", fg="#C6CB3B", bg="#BC6678")
        date_option_label.place(x=5, y=50)
        date_delete = OptionMenu(frame_date_delete, date_delete_value, *list_tables)
        date_delete.config(bg="#BC6678", font=("Helvetica", 11, "bold"), fg="#C6CB3B",
                           width=18)
        date_delete.place(x=65, y=49)
        # add ok button in this frame
        ok_button = Button(frame_date_delete, text="VIZUALIZARE", width=20, height=2, fg="#1E2729", bg="#248B48",
                           font=("Helvetica", 9, "bold"),
                           command=lambda: self.view_results_day(date_delete_value.get(), frame_treeview_results))
        ok_button.place(x=55, y=130)
        # ok_button.place(relx=0.3, rely=0.7)
        # create frame for treeview results
        frame_treeview_results = LabelFrame(frame_title, fg="#EEEBF3", bg="#BC6678", font=("Helvetica", 15, "bold"),
                                            bd=5,
                                            cursor="target", width=750, height=400, labelanchor="n",
                                            text="PROGRAMARI:",
                                            relief=tkinter.GROOVE)
        frame_treeview_results.grid(padx=40, pady=10, row=0, column=1, )  # put it in the middle
        frame_treeview_results.grid_rowconfigure(0, weight=1)
        frame_treeview_results.grid_columnconfigure(0, weight=1)
        # add cancel button
        cancel_button = Button(frame_title, text="CANCEL", width=30, height=2, fg="#1E2729", bg="#E8E7D8",
                               font=("Helvetica", 9, "bold"), command=self.cancel_form_delete)
        cancel_button.place(x=35, y=360)
        root_delete_appointments.mainloop()

    """
    EDIT PART
    """

    def update_record(self, date_selected, new_day, new_hour, first_name, last_name, cnp, telephone_number):
        ''''
        a.FIRST WE DO THE GENERAL CHECKS
        '''
        # 1.check if everything is completed
        if self.checkers_fields.check_if_necessary_fields_completed(last_name, cnp, telephone_number):
            messagebox.showerror(parent=root_update_appointment_gui, title="DATE NECOMPLETATE",
                                 message="COMPLETATI DATELE OBLIGATORII")
            return
            # 2. check cnp
        message_error_cnp, option_error_cnp = self.checkers_fields.get_cnp_errors(cnp)
        if option_error_cnp == 1:
            messagebox.showerror(parent=root_update_appointment_gui, title="CNP INVALID", message=message_error_cnp)
            return
        elif option_error_cnp == 2:
            messagebox.showerror(parent=root_update_appointment_gui, title="CNP INVALID", message=message_error_cnp)
            return
        elif option_error_cnp == 3:
            messagebox.showerror(parent=root_update_appointment_gui, title="CNP INVALID", message=message_error_cnp)
            return
            # 3. check telephone number
        message_error_telephone, option_error_telephone = self.checkers_fields.get_telephone_number_errors(
            telephone_number)
        if option_error_telephone != 0:
            messagebox.showerror(parent=root_update_appointment_gui, title="NUMAR INVALID",
                                 message=message_error_telephone)
            return
        '''
        B. CHECK IF THERE IS AN UPDATE
        '''
        database = os.path.join(constants_programari.DATABASE_FOLDER, constants_programari.NAME_DATABASE)
        connection = sqlite3.connect(database)
        my_cursor = connection.cursor()
        my_cursor.execute("""SELECT * FROM """ + date_selected + """ WHERE oid=:id""",
                          # dummy dictionary
                          {
                              "id": list_appointment_update[0]
                          }
                          )
        record_list = my_cursor.fetchall()
        # get original list
        original_list = list()
        original_list.append(date_selected)
        original_list.append(record_list[0][0])
        original_list.append(record_list[0][1])
        original_list.append(record_list[0][2])
        original_list.append(record_list[0][3])
        original_list.append(record_list[0][4])
        # check new list
        update_list = list()
        new_day_string = new_day.strftime("%d-%m-%Y")
        new_day_converted = self.checkers_fields.convert_date(new_day_string)
        update_list.append(new_day_converted)
        update_list.append(new_hour)
        update_list.append(first_name)
        update_list.append(last_name)
        update_list.append(cnp)
        update_list.append(telephone_number)
        # check lists
        if self.checkers_sql.compare_list(original_list, update_list):
            messagebox.showerror(parent=root_update_appointment_gui, title="FARA MODIFICARI",
                                 message="NU A FOST EFECTUATA NICI O MODIFICARE LA PROGRAMARE")
            return
        '''
        C. CHECK FOR UPDATE ON DAY
            C1. NO DIFFERENCE ON DAY -> CHECK IF DIFFERENCE ON HOUR 
        '''
        if date_selected == new_day_converted:
            '''D. CHECK IF WE HAVE AN MODIFICATION ON THE HOUR'''
            if record_list[0][0] == new_hour:
                '''D1. In this case we will do just a simple update'''
                my_cursor.execute("""UPDATE """ + date_selected + """ SET
                       PRENUME=:first_name_update,
                       NUME=:last_name_update,
                       CNP=:cnp_update,
                       TELEFON=:telephone_update WHERE oid=:id""",
                                  # dummy dictionary
                                  {
                                      "first_name_update": first_name,
                                      "last_name_update": last_name,
                                      "cnp_update": cnp,
                                      "telephone_update": telephone_number,
                                      "id": list_appointment_update[0]
                                  }
                                  )
                connection.commit()
                connection.close()
                message_appointment_update = "Datele pacientului {} au fost modificate".format(
                    last_name)
                messagebox.showinfo(parent=root_update_appointment_gui, title="REPROGRAMARE",
                                    message=message_appointment_update)
                root_update_appointment_gui.destroy()
                root_update_gui.destroy()
                self.create_main_gui()
                return
            else:
                '''D2. In this case we will do a check to see if we already have something on the new hour
                 first do a delete of the current things appointment and then an update based on the new hour'''
                # check part
                my_cursor.execute("SELECT * FROM " + date_selected + " WHERE ORA='" + new_hour + "'")
                list_results_hour = my_cursor.fetchall()
                if list_results_hour[0][2] != "" or list_results_hour[0][3] != "":
                    messagebox.showerror(parent=root_update_appointment_gui, title="SLOT OCUPAT",
                                         message="ACEST SLOT ESTE DEJA REZERVAT")
                    return
                # delete part
                my_cursor.execute("""UPDATE """ + date_selected + """ SET
                        PRENUME=:first_name_update,
                        NUME=:last_name_update,
                        CNP=:cnp_update,
                        TELEFON=:telephone_update WHERE oid=:id""",
                                  # dummy dictionary
                                  {
                                      "first_name_update": "",
                                      "last_name_update": "",
                                      "cnp_update": "",
                                      "telephone_update": "",
                                      "id": list_appointment_update[0]
                                  }
                                  )
                connection.commit()
                connection.close()
                # now do the update with new hour
                database = os.path.join(constants_programari.DATABASE_FOLDER, constants_programari.NAME_DATABASE)
                connection = sqlite3.connect(database)
                my_cursor = connection.cursor()
                my_cursor.execute("""UPDATE """ + date_selected + """ SET
                                    PRENUME=:first_name_update,
                                    NUME=:last_name_update,
                                    CNP=:cnp_update,
                                    TELEFON=:telephone_update WHERE ORA=:new_hour""",
                                  # dummy dictionary
                                  {
                                      "first_name_update": first_name,
                                      "last_name_update": last_name,
                                      "cnp_update": cnp,
                                      "telephone_update": telephone_number,
                                      "new_hour": new_hour

                                  }
                                  )
                connection.commit()
                connection.close()
                message_appointment_update = "Pacientul {} a fost reprogramat in data de {} in intervalul orar {}".format(
                    last_name, date_selected[2:].replace("_", "-"), new_hour)
                messagebox.showinfo(parent=root_update_appointment_gui, title="REPROGRAMARE",
                                    message=message_appointment_update)
                # send sms to recipient
                '''THIS PART IS WORKING BUT SMS CAN BE SENT JUST TO VERIFIED NUMBER(ME)'''
                # self.sms_sender.add_phone_to_list(telephone_number,first_name_entry_add.get(), name)
                # self.sms_sender.send_sms(telephone_number,selection_day,hour_entry.get())
                '''SECOND METHOD WORKS BETTER FROM SINCH'''
                # self.sms_sender.send_sms2(telephone_number,selection_day, hour_entry.get())
                root_update_appointment_gui.destroy()
                root_update_gui.destroy()
                self.create_main_gui()
                return
        else:
            '''
            E. IN THIS CASE THE DAY HAS BEEN MODIFIED
            '''
            '''E1.We check first that the new day is not in the past'''
            if self.checkers_fields.check_selected_date(new_day_converted[2:].replace("_", "-")):
                messagebox.showerror(parent=root_update_appointment_gui, title="DATA IN TRECUT",
                                     message="DATA SELECTATA ESTE IN TRECUT")
                return
            '''E2. We first check to see if the new_day_converted exists in the list of tables'''
            # get list with all days -> tables
            sql_retrieve_table_command = """SELECT name FROM sqlite_schema WHERE type ='table' """
            my_cursor.execute(sql_retrieve_table_command)
            list_tables_sql = my_cursor.fetchall()
            list_known_tables = list()
            for tuple_name in list_tables_sql:
                list_known_tables.append(tuple_name[0])
            '''E3. Now we check if there is already a table with this date-> if so we check to see if the new chosen slot is ok'''
            if new_day_converted in list_known_tables:
                my_cursor.execute("SELECT * FROM " + new_day_converted + " WHERE ORA='" + new_hour + "'")
                list_results_day = my_cursor.fetchall()
                if list_results_day[0][2] != "" or list_results_day[0][3] != "":
                    messagebox.showerror(parent=root_update_appointment_gui, title="SLOT OCUPAT",
                                         message="ACEST SLOT ESTE DEJA REZERVAT")
                    return
                '''E4.DELETE APPOINTMENT FROM PREVIOUS DAY'''
                my_cursor.execute("""UPDATE """ + date_selected + """ SET
                                       PRENUME=:first_name_update,
                                       NUME=:last_name_update,
                                       CNP=:cnp_update,
                                       TELEFON=:telephone_update WHERE oid=:id""",
                                  # dummy dictionary
                                  {
                                      "first_name_update": "",
                                      "last_name_update": "",
                                      "cnp_update": "",
                                      "telephone_update": "",
                                      "id": list_appointment_update[0]
                                  }
                                  )
                connection.commit()
                connection.close()
                '''E5. AFTER THIS WE NEED TO JUST DO THE UPDATE ON THE NEW SELECTED DAY'''
                database = os.path.join(constants_programari.DATABASE_FOLDER, constants_programari.NAME_DATABASE)
                connection = sqlite3.connect(database)
                my_cursor = connection.cursor()
                my_cursor.execute("""UPDATE """ + new_day_converted + """ SET
                                                    PRENUME=:first_name_update,
                                                    NUME=:last_name_update,
                                                    CNP=:cnp_update,
                                                    TELEFON=:telephone_update WHERE ORA=:new_hour""",
                                  # dummy dictionary
                                  {
                                      "first_name_update": first_name,
                                      "last_name_update": last_name,
                                      "cnp_update": cnp,
                                      "telephone_update": telephone_number,
                                      "new_hour": new_hour

                                  }
                                  )
                connection.commit()
                connection.close()
                message_appointment_update = "Pacientul {} a fost reprogramat in data de {} in intervalul orar {}".format(
                    last_name, new_day_converted[2:].replace("_", "-"), new_hour)
                messagebox.showinfo(parent=root_update_appointment_gui, title="REPROGRAMARE",
                                    message=message_appointment_update)
                # send sms to recipient
                '''THIS PART IS WORKING BUT SMS CAN BE SENT JUST TO VERIFIED NUMBER(ME)'''
                # self.sms_sender.add_phone_to_list(telephone_number,first_name_entry_add.get(), name)
                # self.sms_sender.send_sms(telephone_number,selection_day,hour_entry.get())
                '''SECOND METHOD WORKS BETTER FROM SINCH'''
                # self.sms_sender.send_sms2(telephone_number,selection_day, hour_entry.get())
                root_update_appointment_gui.destroy()
                root_update_gui.destroy()
                self.create_main_gui()
                return
            else:
                '''
                F. IN THIS CASE WE WILL DO A BASIC UPDATE WITH A NEW TABLE CREATED
                '''
                '''F1. DELETE APPOINTMENT FROM PREVIOUS DAY'''
                my_cursor.execute("""UPDATE """ + date_selected + """ SET
                                                      PRENUME=:first_name_update,
                                                      NUME=:last_name_update,
                                                      CNP=:cnp_update,
                                                      TELEFON=:telephone_update WHERE oid=:id""",
                                  # dummy dictionary
                                  {
                                      "first_name_update": "",
                                      "last_name_update": "",
                                      "cnp_update": "",
                                      "telephone_update": "",
                                      "id": list_appointment_update[0]
                                  }
                                  )
                connection.commit()
                connection.close()
                '''F2. CREATE NEW TABLE WITH INITIAL HOURS'''
                self.checkers_sql.create_table(new_day_converted)
                self.checkers_sql.create_initial_hours_for_table(new_day_converted)
                '''F3. NOW WE DO AN ORDINARY UPDATE'''
                database = os.path.join(constants_programari.DATABASE_FOLDER, constants_programari.NAME_DATABASE)
                connection = sqlite3.connect(database)
                my_cursor = connection.cursor()
                my_cursor.execute("""UPDATE """ + new_day_converted + """ SET
                                                                   PRENUME=:first_name_update,
                                                                   NUME=:last_name_update,
                                                                   CNP=:cnp_update,
                                                                   TELEFON=:telephone_update WHERE ORA=:new_hour""",
                                  # dummy dictionary
                                  {
                                      "first_name_update": first_name,
                                      "last_name_update": last_name,
                                      "cnp_update": cnp,
                                      "telephone_update": telephone_number,
                                      "new_hour": new_hour

                                  }
                                  )
                connection.commit()
                connection.close()
                message_appointment_update = "Pacientul {} a fost reprogramat in data de {} in intervalul orar {}".format(
                    last_name, new_day_converted[2:].replace("_", "-"), new_hour)
                messagebox.showinfo(parent=root_update_appointment_gui, title="REPROGRAMARE",
                                    message=message_appointment_update)
                # send sms to recipient
                '''THIS PART IS WORKING BUT SMS CAN BE SENT JUST TO VERIFIED NUMBER(ME)'''
                # self.sms_sender.add_phone_to_list(telephone_number,first_name_entry_add.get(), name)
                # self.sms_sender.send_sms(telephone_number,selection_day,hour_entry.get())
                '''SECOND METHOD WORKS BETTER FROM SINCH'''
                # self.sms_sender.send_sms2(telephone_number,selection_day, hour_entry.get())
                root_update_appointment_gui.destroy()
                root_update_gui.destroy()
                self.create_main_gui()
                return


    def cancel_update_record(self):
        root_update_appointment_gui.destroy()

    def update_appointment_gui(self, date_selected):
        global root_update_appointment_gui
        global day_update_entry
        global hour_entry_update
        global first_name_entry_update
        global last_name_entry_update
        global cnp_entry_update
        global telephone_entry_update
        global list_appointment_update
        # stringvar
        global hour_entry_update_value
        '''CHECK FIRST IF AN EMPTY RECORD IS PRESSED'''
        list_appointment_update = []
        for appointment in update_appointments_treeview.selection():
            appointment_data = update_appointments_treeview.item(appointment)
            appointment_list_values = appointment_data["values"]
            list_appointment_update = appointment_list_values
        if list_appointment_update[3] == "" or list_appointment_update[4] == "":
            messagebox.showerror("SLOT GOL", "NU EXISTA O PROGRAMARE LA ACEST SLOT")
            return
        '''GET DATA FROM SQL COMMAND IN ORDER TO AVOID TELEPHONE BUG FROM TREEVIEW'''
        database = os.path.join(constants_programari.DATABASE_FOLDER, constants_programari.NAME_DATABASE)
        connection = sqlite3.connect(database)
        my_cursor = connection.cursor()
        my_cursor.execute("""SELECT * FROM """ + date_selected + """ WHERE oid=:id""",
                          # dummy dictionary
                          {
                              "id": list_appointment_update[0]
                          }
                          )
        record_list = my_cursor.fetchall()
        root_update_appointment_gui = Toplevel()
        root_update_appointment_gui.title("EDITARE")
        image_ico = os.path.join(self.pictures_folder, constants_programari.PICTURE_FOLDER,
                                 constants_programari.SOMN_ICO_IMAGE)
        root_update_appointment_gui.iconbitmap(image_ico)
        root_update_appointment_gui.geometry("600x500")
        root_update_appointment_gui["bg"] = "#0C79E7"
        root_update_appointment_gui.resizable(NO, NO)
        hour_entry_update_value = StringVar()
        hour_entry_update_value.set(record_list[0][0])
        frame_title = LabelFrame(root_update_appointment_gui, fg="#EEEBF3", bg="#0C79E7",
                                 font=("Helvetica", 20, "bold"),
                                 bd=5,
                                 cursor="target", width=500, height=425, labelanchor="n", text="EDITARE PROGRAMARE",
                                 relief=tkinter.GROOVE)
        frame_title.grid(padx=42, pady=10, row=0, column=0, )  # put it in the middle
        frame_title.grid_rowconfigure(0, weight=1)
        frame_title.grid_columnconfigure(0, weight=1)
        '''CREATE ENTRIES AND LABELS'''
        # Date
        # split date
        date_split = self.checkers_fields.split_date(date_selected[2:].replace("_", "-"))
        day_update_entry = DateEntry(frame_title, selectmode='day', date_pattern="DD-MM-YYYY", bd=2,
                                     headersbackground="#EBFE8A",
                                     headersforeground="#1E1F1C", selectbackground="#209DBF",
                                     selectforeground="#F26B18",
                                     weekendbackground="#8D7B80", font=("Helvetica", 9, "bold"), bg="#9EEB8D",
                                     day=int(date_split[0]), month=int(date_split[1]), year=int(date_split[2]))
        day_update_entry.place(x=250, y=30)
        # hour
        list_hours = self.checkers_fields.get_hours_list()
        hour_entry_update = OptionMenu(frame_title, hour_entry_update_value, *list_hours)
        hour_entry_update.config(bg="#0C79E7", font=("Helvetica", 9, "bold"), fg="#C4E028",
                                 width=22)
        hour_entry_update.place(x=250, y=80)
        # first_name
        first_name_entry_update = Entry(frame_title, width=25, justify="center", font=("Helvetica", 9, "bold"),
                                        cursor="target",
                                        bg="#D4E2D0")
        first_name_entry_update.place(x=250, y=130)
        # last_name
        last_name_entry_update = Entry(frame_title, width=25, justify="center", font=("Helvetica", 9, "bold"),
                                       cursor="target",
                                       bg="#D4E2D0")
        last_name_entry_update.place(x=250, y=180)
        # cnp
        cnp_entry_update = Entry(frame_title, width=25, justify="center", font=("Helvetica", 9, "bold"),
                                 cursor="target",
                                 bg="#D4E2D0")
        cnp_entry_update.place(x=250, y=230)
        # telephone
        telephone_entry_update = Entry(frame_title, width=25, justify="center",
                                       font=("Helvetica", 9, "bold"),
                                       cursor="target",
                                       bg="#D4E2D0")
        telephone_entry_update.place(x=250, y=280)
        # LABELS
        date_label_update = Label(frame_title, text="DATA*", justify="center",
                                  font=("Comic Sans", 11, "bold italic"),
                                  cursor="star", fg="#DA3B22", bg="#0C79E7", )
        date_label_update.place(x=50, y=30)

        hour_label_update = Label(frame_title, text="ORA*", justify="center",
                                  font=("Helvetica", 11, "bold"),
                                  cursor="star", fg="#C6E744", bg="#0C79E7", )
        hour_label_update.place(x=50, y=80)

        first_name_label_update = Label(frame_title, text="PRENUME", justify="center",
                                        font=("Helvetica", 11, "bold"),
                                        cursor="star", fg="#C6E744", bg="#0C79E7", )
        first_name_label_update.place(x=50, y=130)

        last_name_label_update = Label(frame_title, text="NUME*", justify="center",
                                       font=("Helvetica", 11, "bold"),
                                       cursor="star", fg="#C6E744", bg="#0C79E7", )
        last_name_label_update.place(x=50, y=180)

        cnp_label_update = Label(frame_title, text="CNP*", justify="center",
                                 font=("Helvetica", 11, "bold"),
                                 cursor="star", fg="#C6E744", bg="#0C79E7", )
        cnp_label_update.place(x=50, y=230)

        telephone_label_update = Label(frame_title, text="TELEFON*", justify="center",
                                       font=("Helvetica", 11, "bold"),
                                       cursor="star", fg="#C6E744", bg="#0C79E7", )
        telephone_label_update.place(x=50, y=280)
        # add buttons

        ok_button_update = Button(frame_title, text="UPDATARE", width=20, height=2, fg="#1E2729", bg="#248B48",
                                  font=("Helvetica", 9, "bold"),
                                  command=lambda: self.update_record(date_selected, day_update_entry.get_date(),
                                                                     hour_entry_update_value.get(),
                                                                     first_name_entry_update.get().upper(),
                                                                     last_name_entry_update.get().upper(),
                                                                     cnp_entry_update.get(),
                                                                     telephone_entry_update.get()))
        cancel_button = Button(frame_title, text="CANCEL", width=20, height=2, fg="#1E2729", bg="#E8E7D8",
                               font=("Helvetica", 9, "bold"), command=self.cancel_update_record)
        ok_button_update.place(x=50, y=320)
        cancel_button.place(x=280, y=320)

        # MAKE THE ENTRIES ALREADY COMPLETED

        first_name_entry_update.insert(0, record_list[0][1])

        last_name_entry_update.insert(0, record_list[0][2])

        cnp_entry_update.insert(0, record_list[0][3])

        telephone_entry_update.insert(0, record_list[0][4])

    def view_result_day_update(self, date_selected, root_window):
        '''SQL SELECTION'''
        database = os.path.join(constants_programari.DATABASE_FOLDER, constants_programari.NAME_DATABASE)
        connection = sqlite3.connect(database)
        my_cursor = connection.cursor()
        my_cursor.execute("""SELECT oid, * FROM """ + date_selected)
        list_appointments = my_cursor.fetchall()
        connection.close()
        global update_appointments_treeview
        # create the columns  for the treeview
        columns = ("ID", "ORA", "PRENUME", "NUME", "CNP", "TELEFON")
        update_appointments_treeview = ttk.Treeview(root_window, show='headings', columns=columns,
                                                    height=16, )
        # ADD THE COLUMNS
        # define the headings
        update_appointments_treeview.heading(0, text="ID", anchor=tkinter.CENTER)
        update_appointments_treeview.heading(1, text="ORA", anchor=tkinter.CENTER)
        update_appointments_treeview.heading(2, text="PRENUME", anchor=tkinter.CENTER)
        update_appointments_treeview.heading(3, text="NUME", anchor=tkinter.CENTER)
        update_appointments_treeview.heading(4, text="CNP", anchor=tkinter.CENTER)
        update_appointments_treeview.heading(5, text="TELEFON", anchor=tkinter.CENTER)
        # redefine column dimensions
        update_appointments_treeview.column("ID", width=25, )
        update_appointments_treeview.column("ORA", width=125)
        update_appointments_treeview.column("PRENUME", width=150, stretch=NO)
        update_appointments_treeview.column("NUME", width=150, stretch=NO)
        update_appointments_treeview.column("CNP", width=125, stretch=NO)
        update_appointments_treeview.column("TELEFON", width=125, stretch=NO)
        update_appointments_treeview.tag_configure("orow")
        # create a custom style
        style = ttk.Style(root_window)
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="#D4EE77", foreground="#C7651D", justify="center")
        style.configure("Treeview", background="#5B5F51", fieldbackground="#5B5F51", foreground="#F1F7E5",
                        font=("Helvetica", 10, "bold"))
        # change selection color
        style.map("Treeview", background=[("selected", "#A3D623")])
        # populate the list
        for appointment in list_appointments:
            record_update = list()
            record_update.append(str(appointment[0]))
            record_update.append(appointment[1])
            record_update.append(appointment[2])
            record_update.append(appointment[3])
            record_update.append(str(appointment[4]))
            record_update.append(str(appointment[5]))
            record_update_tuple_update = tuple(record_update)
            update_appointments_treeview.insert('', tkinter.END, values=record_update_tuple_update)
        # put treeview on frame
        update_appointments_treeview.place(x=15, y=10)
        root_window["text"] = "PROGRAMARI: " + date_selected[2:].replace("_", "-")
        update_appointments_treeview.bind("<Double-Button-1>", lambda event: self.update_appointment_gui(date_selected))

    def cancel_form_update(self):
        root_update_gui.destroy()
        self.create_main_gui()

    def create_update_gui(self):
        global root_update_gui
        global date_update
        app_menu.destroy()
        '''RETRIEVE ALL TABLES'''
        list_tables = self.checkers_sql.get_list_with_tables()
        # stringvar for date update
        global date_update_value
        root_update_gui = Tk()
        root_update_gui.title("UPDATE")
        image_ico = os.path.join(self.pictures_folder, constants_programari.PICTURE_FOLDER,
                                 constants_programari.SOMN_ICO_IMAGE)
        root_update_gui.iconbitmap(image_ico)
        root_update_gui.geometry("1200x500")
        root_update_gui["bg"] = "#0C79E7"
        root_update_gui.resizable(NO, NO)
        date_update_value = StringVar()
        # set the value of the option menu to the first chronological day of the list
        date_update_value.set(list_tables[0])
        root_update_gui.protocol("WM_DELETE_WINDOW", self.cancel_x_button)
        # create frame for update
        frame_title = LabelFrame(root_update_gui, fg="#EEEBF3", bg="#0C79E7", font=("Helvetica", 25, "bold"),
                                 bd=5,
                                 cursor="target", width=1100, height=450, labelanchor="n", text="EDITARE PROGRAMARE",
                                 relief=tkinter.GROOVE)
        frame_title.grid(padx=32, pady=10, row=0, column=0, )  # put it in the middle
        frame_title.grid_rowconfigure(0, weight=1)
        frame_title.grid_columnconfigure(0, weight=1)
        # create a frame for datetime
        frame_date_update = LabelFrame(frame_title, fg="#EEEBF3", bg="#0C79E7", font=("Helvetica", 15, "bold"),
                                       bd=5,
                                       cursor="target", width=275, height=250, labelanchor=tkinter.N,
                                       text="SELECTIE ZI",
                                       relief=tkinter.GROOVE)
        frame_date_update.grid(row=0, column=0, padx=10, pady=10, sticky=tkinter.EW)
        frame_date_update.grid_rowconfigure(0, weight=1)
        frame_date_update.grid_columnconfigure(0, weight=1)
        # add the option menu
        date_option_label = Label(frame_date_update, text="ZIUA", justify="center",
                                  font=("Helvetica", 11, "bold"),
                                  cursor="star", fg="#C6CB3B", bg="#0C79E7")
        date_option_label.place(x=5, y=50)
        date_update = OptionMenu(frame_date_update, date_update_value, *list_tables)
        date_update.config(bg="#0C79E7", font=("Helvetica", 11, "bold"), fg="#C6CB3B",
                           width=18)
        date_update.place(x=65, y=49)
        # add ok button in this frame
        ok_button = Button(frame_date_update, text="VIZUALIZARE", width=20, height=2, fg="#1E2729", bg="#248B48",
                           font=("Helvetica", 9, "bold"),
                           command=lambda: self.view_result_day_update(date_update_value.get(),
                                                                       frame_treeview_results_update))
        ok_button.place(x=55, y=130)
        # create frame for treeview results
        frame_treeview_results_update = LabelFrame(frame_title, fg="#EEEBF3", bg="#0C79E7",
                                                   font=("Helvetica", 15, "bold"),
                                                   bd=5,
                                                   cursor="target", width=750, height=400, labelanchor="n",
                                                   text="PROGRAMARI:",
                                                   relief=tkinter.GROOVE)
        frame_treeview_results_update.grid(padx=40, pady=10, row=0, column=1, )  # put it in the middle
        frame_treeview_results_update.grid_rowconfigure(0, weight=1)
        frame_treeview_results_update.grid_columnconfigure(0, weight=1)
        # add cancel button
        cancel_button = Button(frame_title, text="CANCEL", width=30, height=2, fg="#1E2729", bg="#E8E7D8",
                               font=("Helvetica", 9, "bold"), command=self.cancel_form_update)
        cancel_button.place(x=35, y=360)
        root_update_gui.mainloop()

    '''
    MENU PART
    '''

    def cancel_x_button(self):
        messagebox.showinfo("FOLOSITI OK OR CANCEL",
                            "Va rog sa apasati OK/CANCEL pentru a iesi din formular in meniul principal")
        pass

    def close_main_gui(self):
        app_menu.destroy()

    def create_main_gui(self):
        global app_menu
        app_menu = Tk()
        app_menu.title("MENU PROGRAMARI")
        image_canvas = os.path.join(self.pictures_folder, constants_programari.PICTURE_FOLDER,
                                    constants_programari.SOMN_IMAGE)
        image_ico = os.path.join(self.pictures_folder, constants_programari.PICTURE_FOLDER,
                                 constants_programari.SOMN_ICO_IMAGE)
        app_menu.iconbitmap(image_ico)
        app_menu.geometry("850x500")
        app_menu.resizable(NO, NO)
        app_menu["bg"] = "#E7D185"
        # create image
        image_canvas = PhotoImage(file=image_canvas)
        # create canvas
        canvas = Canvas(app_menu, height=400, width=450, bg="#E7D185", bd=10, relief=tkinter.GROOVE)
        canvas.place(x=350, y=10)
        canvas.create_image((222, 211), image=image_canvas)
        # create buttons and label
        name_label = Label(app_menu, text="REGISTRU PROGRAMARI", bg="#E7D185", fg="#EEEBF3", borderwidth=5,
                           font=("Helvetica", 19, "bold"), relief=tkinter.GROOVE,
                           justify="center", padx=5, pady=0)
        name_label.grid(row=0, column=0, sticky=tkinter.EW)
        name_label.place(relx=0.02, rely=0.02)
        add_button = Button(app_menu, fg="#EEEBF3", bg="#5BBD2A", font=("Helvetica", 9, "bold"), bd=4,
                            cursor="target", width=20, height=2, justify="center", text="ADAUGARE",
                            relief=tkinter.GROOVE, command=self.create_add_gui)
        select_button = Button(app_menu, fg="#EEEBF3", bg="#0C79E7", font=("Helvetica", 9, "bold"), bd=4,
                               cursor="target", width=20, height=2, justify="center", text="EDITARE",
                               relief=tkinter.GROOVE, command=self.create_update_gui)
        delete_button = Button(app_menu, fg="#EEEBF3", bg="#BC6678", font=("Helvetica", 9, "bold"), bd=4,
                               cursor="target", width=20, height=2, justify="center", text="STERGERE",
                               relief=tkinter.GROOVE, command=self.create_delete_gui)
        search_button = Button(app_menu, fg="#EEEBF3", bg="#32BBAD", font=("Helvetica", 9, "bold"), bd=4,
                               cursor="target", width=20, height=2, justify="center", text="CAUTARE PROGRAMARE",
                               relief=tkinter.GROOVE, command=self.create_search_gui)
        convert_excel_all = Button(app_menu, fg="#EEEBF3", bg="#F36D1C", font=("Helvetica", 9, "bold"), bd=4,
                                   cursor="target", width=20, height=2, justify="center",
                                   text="TRANSFER EXCEL DATE ",
                                   relief=tkinter.GROOVE, command=lambda: self.excel_writer.write_to_excel())
        cancel_button = Button(app_menu, fg="#EEEBF3", bg="#E10E3A", font=("Helvetica", 9, "bold"), bd=4,
                               cursor="target", width=66, height=2, justify="center", text="INCHIDERE",
                               relief=tkinter.GROOVE, command=self.close_main_gui)
        add_button.grid(row=1, column=0, padx=10, pady=5, ipady=15)
        add_button.place(relx=0.11, rely=0.13)
        select_button.grid(row=2, column=0, padx=10, pady=5, ipady=15)
        select_button.place(relx=0.11, rely=0.29)
        delete_button.grid(row=3, column=0, padx=10, pady=5, ipady=15)
        delete_button.place(relx=0.11, rely=0.45)
        search_button.grid(row=4, column=0, padx=10, pady=5, ipady=15)
        search_button.place(relx=0.11, rely=0.61)
        convert_excel_all.grid(row=5, column=0, padx=10, pady=5, ipady=15)
        convert_excel_all.place(relx=0.11, rely=0.78)
        cancel_button.grid(row=5, column=1, padx=(5, 0), pady=2)
        cancel_button.place(relx=0.41, rely=0.89)

        app_menu.mainloop()
