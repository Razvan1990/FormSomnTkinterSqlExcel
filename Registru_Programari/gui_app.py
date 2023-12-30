import os
import sqlite3
import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import Calendar
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
        message_appointment = "Pacientul {} a fost programat la consult in data de {} in intervalul orar {}".format(name,
                                                                                                        selection_day,
                                                                                                        hour_entry.get())
        messagebox.showinfo(parent=root_appointments_addition, title="PROGRAMARE CU SUCCESS", message=message_appointment)
        #send sms to recipient
        '''THIS PART IS WORKING BUT SMS CAN BE SENT JUST TO VERIFIED NUMBER(ME)'''
        #self.sms_sender.add_phone_to_list(telephone_number,first_name_entry_add.get(), name)
        #self.sms_sender.send_sms(telephone_number,selection_day,hour_entry.get())
        '''SECOND METHOD WORKS BETTER FROM SINCH'''
        #self.sms_sender.send_sms2(telephone_number,selection_day, hour_entry.get())
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
        # root_edit_treeview.protocol("WM_DELETE_WINDOW", self.cancel_x_button)
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
        select_button = Button(app_menu, fg="#EEEBF3", bg="#2092B0", font=("Helvetica", 9, "bold"), bd=4,
                               cursor="target", width=20, height=2, justify="center", text="EDITARE",
                               relief=tkinter.GROOVE, )  # command=self.create_edit_gui)
        delete_button = Button(app_menu, fg="#EEEBF3", bg="#BC6678", font=("Helvetica", 9, "bold"), bd=4,
                               cursor="target", width=20, height=2, justify="center", text="STERGERE",
                               relief=tkinter.GROOVE, )  # command=self.create_delete_gui)
        convert_excel_all = Button(app_menu, fg="#EEEBF3", bg="#F36D1C", font=("Helvetica", 9, "bold"), bd=4,
                                   cursor="target", width=20, height=2, justify="center",
                                   text="TRANSFER EXCEL DATE ",
                                   relief=tkinter.GROOVE,   command=lambda: self.excel_writer.write_to_excel())

        cancel_button = Button(app_menu, fg="#EEEBF3", bg="#E10E3A", font=("Helvetica", 9, "bold"), bd=4,
                               cursor="target", width=66, height=2, justify="center", text="INCHIDERE",
                               relief=tkinter.GROOVE, command=self.close_main_gui)
        add_button.grid(row=1, column=0, padx=10, pady=5, ipady=15)
        add_button.place(relx=0.11, rely=0.15)
        select_button.grid(row=2, column=0, padx=10, pady=5, ipady=15)
        select_button.place(relx=0.11, rely=0.36)
        delete_button.grid(row=3, column=0, padx=10, pady=5, ipady=15)
        delete_button.place(relx=0.11, rely=0.57)
        convert_excel_all.grid(row=4, column=0, padx=10, pady=5, ipady=15)
        convert_excel_all.place(relx=0.11, rely=0.78)
        cancel_button.grid(row=5, column=1, padx=(5, 0), pady=2)
        cancel_button.place(relx=0.41, rely=0.89)

        app_menu.mainloop()
