import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import os
from PIL import Image, ImageTk
import constants_pacienti
from tkcalendar import Calendar
from checkers_sql import CheckSqlCommands
from checker_fields import CheckFields
from excel_writer import ExcelWriter


class GuiApp:

    def __init__(self):
        self.table_name = "Patient_registry"
        self.pictures_folder = os.path.dirname(os.getcwd())
        self.checker_sql = CheckSqlCommands()
        self.checker_field = CheckFields()
        self.writer = ExcelWriter()

    def cancel_x_button(self):
        messagebox.showinfo("FOLOSITI OK OR CANCEL",
                            "Va rog sa apasati OK/CANCEL pentru a iesi din formular in meniul principal")
        pass

    '''ADD MENU PART'''

    def check_if_buttons_are_selected(self, buton_no, buton_yes):
        if buton_yes.get() == "" and buton_no == "":
            return False
        return True

    def check_data_buton(self):
        if cal.get_date() == "":
            return True
        return False

    def handle_insurance_buton_no(self, *args):
        if args[0].get() == "NO":
            # in this way the value will be NO for the general and optionmenu is non_general
            args[1].set("NO")
            args[2].set("NON-APLICABIL")
            args[3].config(state=tkinter.DISABLED)
            args[4].deselect()

    def handle_insurance_buton_yes(self, *args):
        if args[0].get() == "YES":
            # in this way the value will be YES for the general and optionmenu is non_general
            args[1].set("YES")
            args[2].config(state=tkinter.NORMAL)
            args[3].deselect()

    def handle_ticket_medical_yes(self, *args):
        if args[0].get() == "YES":
            args[1].set("YES")
            args[2]["state"] = tkinter.NORMAL
            args[2].delete(0, END)
            args[3].deselect()

    def handle_ticket_medical_no(self, *args):
        if args[0].get() == "NO":
            args[1].set("NO")
            args[2].delete(0, END)
            args[2]["state"] = tkinter.NORMAL
            args[2].insert(0, "NON-APLICABIL")
            args[2]["state"] = tkinter.DISABLED
            args[3].deselect()

    def handle_apnea_buton_yes(self, *args):
        if args[0].get() == "YES":
            args[1].set("YES")
            args[2].config(state=tkinter.NORMAL)
            args[3].config(state=tkinter.NORMAL)
            args[4]["state"] = tkinter.NORMAL
            args[5]["state"] = tkinter.NORMAL
            args[4].delete(0, END)
            args[5].delete(0, END)
            args[6].deselect()

    def handle_apnea_buton_no(self, *args):
        if args[0].get() == "NO":
            args[1].set("NO")
            args[2].config(state=tkinter.NORMAL)
            args[3].set("NON-APLICABIL")
            args[2].config(state=tkinter.DISABLED)
            args[4].config(state=tkinter.NORMAL)
            args[5].set("NON-APLICABIL")
            args[4].config(state=tkinter.DISABLED)
            args[6].delete(0, END)
            args[7].delete(0, END)
            args[6]["state"] = tkinter.NORMAL
            args[7]["state"] = tkinter.NORMAL
            args[6].insert(0, "NON-APLICABIL")
            args[7].insert(0, "NON-APLICABIL")
            args[6]["state"] = tkinter.DISABLED
            args[7]["state"] = tkinter.DISABLED
            args[8].deselect()

    def handle_disease_buton_yes(self, *args):
        if args[0].get() == "YES":
            args[1].set("YES")
            args[2]["state"] = tkinter.NORMAL
            args[2].delete("1.0", END)
            args[3].deselect()

    def handle_disease_buton_no(self, *args):
        if args[0].get() == "NO":
            args[1].set("NO")
            args[2]["state"] = tkinter.NORMAL
            args[2].delete("1.0", END)
            args[2].insert("1.0", "NON-APLICABIL")
            args[2]["state"] = tkinter.DISABLED
            args[3].deselect()

    def cancel_form_add(self):
        root_add.destroy()
        self.create_main_gui()

    def clear_form_add(self):
        # we will clear everything from the form to the initial state
        # Personal stuff
        cal.selection_clear()
        first_name_entry.delete(0, END)
        last_name_entry.delete(0, END)
        cnp_entry.delete(0, END)
        telephone_number_entry.delete(0, END)
        address_entry_street.delete(0, END)
        address_entry_locality.delete(0, END)
        judet_value.set("SV-Suceava")
        has_insurance_yes.deselect()
        has_insurance_no.deselect()
        asigurare_value.set("NON-APLICABIL")
        insurance_type.config(state=tkinter.DISABLED)
        # Medical stuff
        doctor_ticket_yes.deselect()
        doctor_ticket_no.deselect()
        ticket_number.delete(0, END)
        ticket_number["state"] = tkinter.DISABLED
        anamneza.delete("1.0", END)
        has_apnea_yes.deselect()
        has_apnea_no.deselect()
        apnea_type_value.set("NON-APLICABIL")
        apnea_type.config(state=tkinter.DISABLED)
        mask_type_value.set("NON-APLICABIL")
        mask_type.config(state=tkinter.DISABLED)
        compliance.delete(0, END)
        compliance["state"] = tkinter.DISABLED
        pressure.delete(0, END)
        pressure["state"] = tkinter.DISABLED
        has_diseases_yes.deselect()
        has_diseases_no.deselect()
        disease_section.delete("1.0", END)
        disease_section["state"] = tkinter.DISABLED
        recommendation_section.delete("1.0", END)

    def sql_add(self, table_name, cnp, selection_date, last_name, telephone_number, *args):  # args are the checkbuttons
        database = os.path.join(constants_pacienti.DATABASE_FOLDER, constants_pacienti.NAME_DATABASE)
        connection = sqlite3.connect(database)
        my_cursor = connection.cursor()
        # check if table exists and if not create it
        if not self.checker_sql.check_if_table_exists(table_name):
            self.checker_sql.create_table(table_name)
        # first we need to make the checks
        # 1 .check if mandatory fields are completed
        if self.checker_field.check_if_necessary_fields_completed(selection_date, cnp, last_name):
            messagebox.showerror("CAMPURI NECOMPLETATE", "CAMPURI OBLIGATORII(*) NECOMPLETATE!")
            return
        if self.checker_sql.check_if_table_has_one_record(table_name):
            if self.checker_sql.check_for_duplicate_same_day(table_name, cnp, selection_date):
                messagebox.showerror("PACIENT DUPLICAT", "PACIENTUL DEJA A FOST ADAUGAT IN ACEASTA ZI!")
                return
        # 3. check cnp validity
        message_error, option = self.checker_field.get_cnp_errors(cnp)
        if option == 1:
            messagebox.showerror("CNP INVALID", message=message_error)
            return
        elif option == 2:
            messagebox.showerror("CNP INVALID", message=message_error)
            return
        elif option == 3:
            messagebox.showerror("CNP INVALID", message=message_error)
            return
        # 4.check telephone validity
        message_error, option = self.checker_field.get_telephone_number_errors(telephone_number)
        if option == 1 and len(telephone_number) != 0:
            messagebox.showerror("TELEFON INVALID", message=message_error)
            return
            # 5. check if at least one checkbutton is selected:
        if self.checker_field.check_buttons_selected(args[0], args[1]):
            messagebox.showerror("ASIGURARE NECOMPLETAT", "COMPLETATI DACA PACIENTUL E ASIGURAT SAU NU")
            return
        if self.checker_field.check_buttons_selected(args[2], args[3]):
            messagebox.showerror("BILET TRIMITERE NECOMPLETAT",
                                 "COMPLETATI DACA PACIENTUL ARE SAU NU BILET DE TRIMITERE")
            return
        if self.checker_field.check_buttons_selected(args[4], args[5]):
            messagebox.showerror("APNEE NECOMPLETAT", "COMPLETATI DACA PACIENTUL SUFERA DE APNEE SAU NU")
            return
        if self.checker_field.check_buttons_selected(args[6], args[7]):
            messagebox.showerror("BOLI CUNOSCUTE NECOMPLETAT", "COMPLETATI DACA PACIENTUL ARE BOLI CUNOSCUTE SAU NU")
            return
        # SQL PART
        # compute address name
        my_cursor.execute("""INSERT INTO """ + table_name + """ VALUES (
                                         :DATA,
                                         :PRENUME,
                                         :NUME,
                                         :CNP,
                                         :TELEFON,
                                         :STRADA,
                                         :LOCALITATE,
                                         :JUDET,
                                         :ASIGURARE,
                                         :TIP_ASIGURARE,
                                         :BILET_TRIMITERE,
                                         :NUMAR_BILET,
                                         :ANAMNEZA,
                                         :APNEE,
                                         :TIP_APNEE,
                                         :TIP_MASCA,
                                         :COMPLIANTA,
                                         :PRESIUNE,
                                         :BOLI_CUNOSCUTE,
                                         :BOLI,
                                         :RECOMANDARE)""",
                          # dummy dictionary
                          {
                              "DATA": cal.get_date(),
                              "PRENUME": first_name_entry.get().upper(),
                              "NUME": last_name_entry.get().upper(),
                              "CNP": str(cnp_entry.get()),
                              "TELEFON": str(telephone_number_entry.get()),
                              "STRADA": address_entry_street.get().upper(),
                              "LOCALITATE": address_entry_locality.get().upper(),
                              "JUDET": judet_value.get().upper(),
                              "ASIGURARE": has_insurance_value_general.get().upper(),
                              "TIP_ASIGURARE": asigurare_value.get(),
                              "BILET_TRIMITERE": has_doctor_ticket_value_general.get().upper(),
                              "NUMAR_BILET": ticket_number.get().upper(),
                              "ANAMNEZA": anamneza.get("1.0", END).upper(),
                              "APNEE": has_apnea_value_general.get().upper(),
                              "TIP_APNEE": apnea_type_value.get(),
                              "TIP_MASCA": mask_type_value.get(),
                              "COMPLIANTA": compliance.get().upper(),
                              "PRESIUNE": pressure.get().upper(),
                              "BOLI_CUNOSCUTE": has_disease_value_general.get().upper(),
                              "BOLI": disease_section.get("1.0", END).upper(),
                              "RECOMANDARE": recommendation_section.get("1.0", END).upper()
                          }
                          )
        connection.commit()
        connection.close()
        message_add = " Pacientul {} {} a fost adaugat in registru pe data de {}".format(first_name_entry.get(),
                                                                                         last_name_entry.get(),
                                                                                         cal.get_date())
        messagebox.showinfo("ADAUGARE", message_add)
        root_add.destroy()
        self.create_main_gui()

    def create_add_gui(self):
        app_menu.destroy()
        # personal data
        global root_add
        global cal
        global first_name_entry
        global last_name_entry
        global cnp_entry
        global telephone_number_entry
        global address_entry_street
        global address_entry_locality
        global address_region_menu
        global has_insurance_yes  # checkButton
        global has_insurance_no  # checkButton
        global insurance_type
        # medical info
        global doctor_ticket_yes  # bilet trimitere
        global doctor_ticket_no  # bilet trimitere
        global ticket_number
        global has_apnea  # checkButton
        global has_apnea_yes
        global has_apnea_no
        global apnea_type
        global mask_type
        global compliance
        global pressure
        global has_diseases_yes
        global has_diseases_no
        # textareas
        global anamneza
        global disease_section
        global recommendation_section
        # stringvars
        global has_insurance_value_yes
        global has_insurance_value_no
        global has_insurance_value_general
        global has_doctor_ticket_value_yes
        global has_doctor_ticket_value_no
        global has_doctor_ticket_value_general
        global judet_value
        global asigurare_value
        global has_apnea_value_yes
        global has_apnea_value_no
        global has_apnea_value_general
        global apnea_type_value
        global mask_type_value
        global has_disease_value_yes
        global has_disease_value_no
        global has_disease_value_general

        root_add = Tk()
        root_add.title("ADD")
        image_ico = os.path.join(self.pictures_folder, constants_pacienti.PICTURE_FOLDER,
                                 constants_pacienti.SOMN_ICO_IMAGE)
        root_add.iconbitmap(image_ico)
        root_add.geometry("1200x900")
        root_add["bg"] = "#5BBD2A"
        root_add.resizable(0, 0)
        # stringvar variables
        judet_value = StringVar()
        judet_value.set("SV-Suceava")
        has_insurance_value_yes = StringVar()
        has_insurance_value_no = StringVar()
        has_insurance_value_general = StringVar()
        asigurare_value = StringVar()
        asigurare_value.set("NON-APLICABIL")
        has_doctor_ticket_value_yes = StringVar()
        has_doctor_ticket_value_no = StringVar()
        has_doctor_ticket_value_general = StringVar()
        has_apnea_value_yes = StringVar()
        has_apnea_value_no = StringVar()
        has_apnea_value_general = StringVar()
        has_disease_value_yes = StringVar()
        has_disease_value_no = StringVar()
        has_disease_value_general = StringVar()
        apnea_type_value = StringVar()
        apnea_type_value.set("NON-APLICABIL")
        mask_type_value = StringVar()
        mask_type_value.set("NON-APLICABIL")

        root_add.protocol("WM_DELETE_WINDOW", self.cancel_x_button)
        # create first frame for title label
        frame_title = LabelFrame(root_add, fg="#EEEBF3", bg="#5BBD2A", font=("Helvetica", 25, "bold"), bd=5,
                                 cursor="target", width=1100, height=850, labelanchor="n", text="ADAUGARE PACIENT",
                                 relief=tkinter.GROOVE)
        frame_title.grid(padx=42, pady=10, row=0, column=0, )  # put it in the middle
        frame_title.grid_rowconfigure(0, weight=1)
        frame_title.grid_columnconfigure(0, weight=1)

        # create frame for personal settings
        frame_personal_info = LabelFrame(frame_title, fg="#EEEBF3", bg="#5BBD2A", font=("Helvetica", 15, "bold"),
                                         bd=5,
                                         cursor="target", width=350, height=800, labelanchor=tkinter.N,
                                         text="DATE PERSONALE",
                                         relief=tkinter.GROOVE)
        frame_personal_info.grid(padx=10, pady=10, row=0, column=0, sticky=tkinter.EW)  # put it in the middle
        frame_personal_info.grid_rowconfigure(0, weight=1)
        frame_personal_info.grid_columnconfigure(0, weight=1)

        # first add the calendar
        cal = Calendar(frame_personal_info, selectmode='day', date_pattern="DD-MM-YYYY", bd=2,
                       headersbackground="#EBFE8A",
                       headersforeground="#1E1F1C", selectbackground="#209DBF", selectforeground="#F26B18",
                       weekendbackground="#8D7B80", font=("Helvetica", 9, "bold"))
        cal.grid(row=0, column=1, pady=(5, 5))
        calendar_label = Label(frame_personal_info, text="DATA*", justify="center", font=("Helvetica", 11, "bold"),
                               cursor="star", fg="#3D91C4", bg="#5BBD2A")
        calendar_label.grid(row=0, column=0, padx=5, pady=(5, 5))
        '''add entries and label'''
        # first name
        first_name_entry = Entry(frame_personal_info, width=25, justify="center", font=("Helvetica", 9, "bold"),
                                 cursor="target",
                                 bg="#D4E2D0")
        first_name_entry.grid(row=1, column=1, pady=(5, 5))
        first_name_label = Label(frame_personal_info, text="PRENUME", justify="center",
                                 font=("Helvetica", 11, "bold"),
                                 cursor="star", fg="#3D91C4", bg="#5BBD2A")
        first_name_label.grid(row=1, column=0, padx=5, pady=(5, 5))
        # last name
        last_name_entry = Entry(frame_personal_info, width=25, justify="center", font=("Helvetica", 9, "bold"),
                                cursor="target",
                                bg="#D4E2D0")
        last_name_entry.grid(row=2, column=1, pady=(5, 5))

        last_name_label = Label(frame_personal_info, text="NUME*", justify="center", font=("Helvetica", 11, "bold"),
                                cursor="star", fg="#3D91C4", bg="#5BBD2A")
        last_name_label.grid(row=2, column=0, padx=5, pady=(5, 5))
        # cnp
        cnp_entry = Entry(frame_personal_info, width=25, justify="center", font=("Helvetica", 9, "bold"),
                          cursor="target",
                          bg="#D4E2D0")
        cnp_entry.grid(row=3, column=1, pady=(5, 5))
        cnp_label = Label(frame_personal_info, text="CNP*", justify="center", font=("Helvetica", 11, "bold"),
                          cursor="star", fg="#3D91C4", bg="#5BBD2A", )
        cnp_label.grid(row=3, column=0, padx=5, pady=(5, 5))
        # telephone
        telephone_number_entry = Entry(frame_personal_info, width=25, justify="center",
                                       font=("Helvetica", 9, "bold"),
                                       cursor="target",
                                       bg="#D4E2D0")
        telephone_number_entry.grid(row=4, column=1, pady=(5, 5))
        telephone_number_label = Label(frame_personal_info, text="TELEFON", justify="center",
                                       font=("Helvetica", 11, "bold"),
                                       cursor="star", fg="#3D91C4", bg="#5BBD2A")
        telephone_number_label.grid(row=4, column=0, padx=5, pady=(5, 5))

        # create a frame label for the address
        address_frame_label = LabelFrame(frame_personal_info, fg="#EEEBF3", bg="#5BBD2A",
                                         font=("Helvetica", 13, "bold"), bd=5,
                                         cursor="target", labelanchor="n", text="ADRESA", width=315, height=200,
                                         relief=tkinter.GROOVE)
        address_frame_label.grid(row=5, column=0, columnspan=2)  # put it in the middle
        address_frame_label.grid_rowconfigure(0, weight=1)
        address_frame_label.grid_columnconfigure(0, weight=1)
        # street_name
        address_label_street = Label(address_frame_label, text="STRADA", justify="center",
                                     font=("Helvetica", 11, "bold"),
                                     cursor="star", fg="#3D91C4", bg="#5BBD2A")
        address_label_street.grid(row=0, column=0, padx=5, pady=(5, 5))
        address_entry_street = Entry(address_frame_label, width=23, justify="center", font=("Helvetica", 9, "bold"),
                                     cursor="target",
                                     bg="#D4E2D0")
        address_entry_street.grid(row=0, column=1, padx=5, pady=(5, 5))
        # locality_name
        address_locality_label = Label(address_frame_label, text="LOCALITATE", justify="center",
                                       font=("Helvetica", 11, "bold"),
                                       cursor="star", fg="#3D91C4", bg="#5BBD2A")
        address_locality_label.grid(row=1, column=0, padx=5, pady=(5, 5))
        address_entry_locality = Entry(address_frame_label, width=23, justify="center",
                                       font=("Helvetica", 9, "bold"),
                                       cursor="target",
                                       bg="#D4E2D0")
        address_entry_locality.grid(row=1, column=1, padx=5, pady=(5, 5))
        # region name
        address_region_label = Label(address_frame_label, text="JUDET*", justify="center",
                                     font=("Helvetica", 11, "bold"),
                                     cursor="star", fg="#3D91C4", bg="#5BBD2A")
        address_region_label.grid(row=2, column=0, padx=5, pady=(5, 5))
        address_region_menu = OptionMenu(address_frame_label, judet_value, *constants_pacienti.REGION_LIST, )
        address_region_menu.config(bg="#07A52D", font=("Helvetica", 11, "bold"), fg="#DEFFE6", width=16)
        address_region_menu.grid(row=2, column=1, padx=5, pady=(5, 5))
        # insurance part
        has_insurance_yes = Checkbutton(frame_personal_info, text="YES", variable=has_insurance_value_yes,
                                        onvalue="YES", offvalue="", bg="#5BBD2A",
                                        command=lambda: self.handle_insurance_buton_yes(has_insurance_value_yes,
                                                                                        has_insurance_value_general,
                                                                                        insurance_type,
                                                                                        has_insurance_no))
        has_insurance_yes.grid(row=6, column=1, padx=5, pady=(5, 5))
        has_insurance_yes.place(relx=0.4, rely=0.87)
        has_insurance_yes.deselect()
        has_insurance_no = Checkbutton(frame_personal_info, text="NO", variable=has_insurance_value_no,
                                       onvalue="NO", offvalue="", bg="#5BBD2A",
                                       command=lambda: self.handle_insurance_buton_no(has_insurance_value_no,
                                                                                      has_insurance_value_general,
                                                                                      asigurare_value,
                                                                                      insurance_type,
                                                                                      has_insurance_yes))
        has_insurance_no.grid(row=6, column=2, padx=5, pady=(5, 5))
        has_insurance_no.place(relx=0.77, rely=0.87)
        has_insurance_no.deselect()
        insurance_label = Label(frame_personal_info, text="ASIGURARE*", justify="center",
                                font=("Helvetica", 11, "bold"),
                                cursor="star", fg="#3D91C4", bg="#5BBD2A")
        insurance_label.grid(row=6, column=0, padx=5, pady=(15, 5))
        # type_insurance
        insurance_type_label = Label(frame_personal_info, text="TIP ASIGURARE", justify="center",
                                     font=("Helvetica", 11, "bold"),
                                     cursor="star", fg="#3D91C4", bg="#5BBD2A")
        insurance_type_label.grid(row=7, column=0, padx=5, pady=(5, 5))
        insurance_type = OptionMenu(frame_personal_info, asigurare_value, *constants_pacienti.INSURANCE_LIST, )
        insurance_type.config(bg="#07A52D", font=("Helvetica", 11, "bold"), fg="#DEFFE6", state=tkinter.DISABLED,
                              width=18)
        insurance_type.grid(row=7, column=1, padx=5, pady=(5, 5), )

        '''
        FRAME PATIENT STATISTICS
        '''
        frame_patient_medical = LabelFrame(frame_title, fg="#EEEBF3", bg="#5BBD2A", font=("Helvetica", 15, "bold"),
                                           bd=5,
                                           cursor="target", width=700, height=800, labelanchor="n",
                                           text="DATE MEDICALE",
                                           relief=tkinter.GROOVE)
        frame_patient_medical.grid(padx=10, pady=10, row=0, column=1, )  # put it in the middle
        frame_patient_medical.grid_rowconfigure(0, weight=1)
        frame_patient_medical.grid_columnconfigure(0, weight=1)
        # doctor ticket part
        doctor_ticket_label = Label(frame_patient_medical, text="BILET TRIMITERE*", justify="center",
                                    font=("Helvetica", 11, "bold"),
                                    cursor="star", fg="#3D91C4", bg="#5BBD2A")
        doctor_ticket_label.place(x=40, y=30)
        doctor_ticket_yes = Checkbutton(frame_patient_medical, text="YES", variable=has_doctor_ticket_value_yes,
                                        onvalue="YES", offvalue="", bg="#5BBD2A",
                                        command=lambda: self.handle_ticket_medical_yes(has_doctor_ticket_value_yes,
                                                                                       has_doctor_ticket_value_general,
                                                                                       ticket_number,
                                                                                       doctor_ticket_no))
        doctor_ticket_yes.place(x=195, y=30)
        doctor_ticket_yes.deselect()
        doctor_ticket_no = Checkbutton(frame_patient_medical, text="NO", variable=has_doctor_ticket_value_no,
                                       onvalue="NO", offvalue="", bg="#5BBD2A",
                                       command=lambda: self.handle_ticket_medical_no(has_doctor_ticket_value_no,
                                                                                     has_doctor_ticket_value_general,
                                                                                     ticket_number,
                                                                                     doctor_ticket_yes))
        doctor_ticket_no.place(x=320, y=30)
        doctor_ticket_no.deselect()
        ticket_number_label = Label(frame_patient_medical, text="COD BILET", justify="center",
                                    font=("Helvetica", 11, "bold"),
                                    cursor="star", fg="#3D91C4", bg="#5BBD2A")
        ticket_number_label.place(x=40, y=70)
        ticket_number = Entry(frame_patient_medical, width=23, justify="center", font=("Helvetica", 9, "bold"),
                              cursor="target", bg="#D4E2D0", state=tkinter.DISABLED)
        ticket_number.place(x=200, y=70)
        # anamneza
        anamneza_label = Label(frame_patient_medical, text="ANAMNEZA", justify="center",
                               font=("Helvetica", 11, "bold"),
                               cursor="star", fg="#3D91C4", bg="#5BBD2A")
        anamneza_label.place(x=40, y=150)
        anamneza = Text(frame_patient_medical, width=65, height=10, font=("Helvetica", 9, "bold"),
                        cursor="target", bd=4, bg="#C8E6F0", relief=GROOVE, wrap=WORD, highlightcolor="#907AFB",
                        highlightbackground="#907AFB")
        anamneza.place(x=200, y=110)
        my_scrollbar = Scrollbar(frame_patient_medical, orient=tkinter.VERTICAL, command=anamneza.yview, )
        anamneza.configure(yscrollcommand=my_scrollbar.set, )
        my_scrollbar.place(x=660, y=110, height=160)
        '''apnea part'''
        frame_apnea = LabelFrame(frame_patient_medical, fg="#EEEBF3", bg="#5BBD2A", font=("Helvetica", 13, "bold"),
                                 bd=5,
                                 cursor="target", width=640, height=170, labelanchor="n",
                                 text="APNEE",
                                 relief=tkinter.GROOVE)
        frame_apnea.place(x=40, y=270)
        # apnea buttons
        has_apnea_label = Label(frame_apnea, text="APNEE*", justify="center",
                                font=("Helvetica", 11, "bold"),
                                cursor="star", fg="#3D91C4", bg="#5BBD2A")
        has_apnea_label.place(x=190, y=10)
        has_apnea_yes = Checkbutton(frame_apnea, text="YES", variable=has_apnea_value_yes,
                                    onvalue="YES", offvalue="", bg="#5BBD2A",
                                    command=lambda: self.handle_apnea_buton_yes(has_apnea_value_yes,
                                                                                has_apnea_value_general, apnea_type,
                                                                                mask_type, compliance, pressure,
                                                                                has_apnea_no))
        has_apnea_yes.place(x=265, y=10)
        has_apnea_yes.deselect()
        has_apnea_no = Checkbutton(frame_apnea, text="NO", variable=has_apnea_value_no,
                                   onvalue="NO", offvalue="", bg="#5BBD2A",
                                   command=lambda: self.handle_apnea_buton_no(has_apnea_value_no,
                                                                              has_apnea_value_general, apnea_type,
                                                                              apnea_type_value,
                                                                              mask_type, mask_type_value,
                                                                              compliance,
                                                                              pressure,
                                                                              has_apnea_yes))
        has_apnea_no.place(x=375, y=10)
        has_apnea_no.deselect()
        # apnea type
        label_apnea_type = Label(frame_apnea, text="TIP APNEE", justify="center",
                                 font=("Helvetica", 11, "bold"),
                                 cursor="star", fg="#3D91C4", bg="#5BBD2A")
        label_apnea_type.place(x=30, y=50)
        apnea_type = OptionMenu(frame_apnea, apnea_type_value, *constants_pacienti.APNEA_TYPE, )
        apnea_type.config(bg="#07A52D", font=("Helvetica", 11, "bold"), fg="#DEFFE6", width=16,
                          state=tkinter.DISABLED)
        apnea_type.place(x=120, y=48)
        # mask type
        label_mask_type = Label(frame_apnea, text="TIP MASCA", justify="center",
                                font=("Helvetica", 11, "bold"),
                                cursor="star", fg="#3D91C4", bg="#5BBD2A", )
        label_mask_type.place(x=30, y=100)
        mask_type = OptionMenu(frame_apnea, mask_type_value, *constants_pacienti.MASK_TYPE, )
        mask_type.config(bg="#07A52D", font=("Helvetica", 11, "bold"), fg="#DEFFE6", width=16,
                         state=tkinter.DISABLED)
        mask_type.place(x=120, y=96)
        # compliance
        label_compliance = Label(frame_apnea, text="COMPLIANTA", justify="center",
                                 font=("Helvetica", 11, "bold"),
                                 cursor="star", fg="#3D91C4", bg="#5BBD2A")
        label_compliance.place(x=340, y=50)
        compliance = Entry(frame_apnea, width=23, justify="center", font=("Helvetica", 9, "bold"),
                           cursor="target", bg="#D4E2D0", state=tkinter.DISABLED)
        compliance.place(x=450, y=50)
        # presiune
        label_pressure = Label(frame_apnea, text="PRESIUNE", justify="center",
                               font=("Helvetica", 11, "bold"),
                               cursor="star", fg="#3D91C4", bg="#5BBD2A")
        label_pressure.place(x=340, y=100)
        pressure = Entry(frame_apnea, width=23, justify="center", font=("Helvetica", 9, "bold"),
                         cursor="target", bg="#D4E2D0", state=tkinter.DISABLED)
        pressure.place(x=450, y=100)

        # known diseases
        diseases_label = Label(frame_patient_medical, text="BOLI CUNOSCUTE*", justify="center",
                               font=("Helvetica", 11, "bold"),
                               cursor="star", fg="#3D91C4", bg="#5BBD2A")
        diseases_label.place(x=40, y=480)
        has_diseases_yes = Checkbutton(frame_patient_medical, text="YES", variable=has_disease_value_yes,
                                       onvalue="YES", offvalue="", bg="#5BBD2A",
                                       command=lambda: self.handle_disease_buton_yes(has_disease_value_yes,
                                                                                     has_disease_value_general,
                                                                                     disease_section,
                                                                                     has_diseases_no))
        has_diseases_yes.place(x=195, y=480)
        has_diseases_no = Checkbutton(frame_patient_medical, text="NO", variable=has_disease_value_no,
                                      onvalue="NO", offvalue="", bg="#5BBD2A",
                                      command=lambda: self.handle_disease_buton_no(has_disease_value_no,
                                                                                   has_disease_value_general,
                                                                                   disease_section,
                                                                                   has_diseases_yes))
        has_diseases_no.place(x=250, y=480)
        disease_section = Text(frame_patient_medical, width=46, height=7, font=("Helvetica", 9, "bold"),
                               cursor="target", bd=4, bg="#C8E6F0", relief=GROOVE, wrap=WORD,
                               highlightcolor="#907AFB",
                               highlightbackground="#907AFB", state=tkinter.DISABLED)
        disease_section.place(x=330, y=480)
        my_scrollbar_disease = Scrollbar(frame_patient_medical, orient=tkinter.VERTICAL,
                                         command=disease_section.yview, )
        disease_section.configure(yscrollcommand=my_scrollbar_disease.set, )
        my_scrollbar_disease.place(x=660, y=480, height=117)
        # recommendation part
        recommendation_label = Label(frame_patient_medical, text="RECOMANDARE", justify="center",
                                     font=("Helvetica", 11, "bold"),
                                     cursor="star", fg="#3D91C4", bg="#5BBD2A")
        recommendation_label.place(x=40, y=630)
        recommendation_section = Text(frame_patient_medical, width=65, height=8.3, font=("Helvetica", 9, "bold"),
                                      cursor="target", bd=4, bg="#C8E6F0", relief=GROOVE, wrap=WORD,
                                      highlightcolor="#907AFB",
                                      highlightbackground="#907AFB")
        recommendation_section.place(x=200, y=630)
        my_scrollbar_recommendation = Scrollbar(frame_patient_medical, orient=tkinter.VERTICAL,
                                                command=recommendation_section.yview, )
        recommendation_section.configure(yscrollcommand=my_scrollbar_recommendation.set, )
        my_scrollbar_recommendation.place(x=660, y=630, height=130)
        # buttons
        ok_button = Button(root_add, text="SAVE", width=15, height=2, fg="#1E2729", bg="#248B48",
                           font=("Helvetica", 9, "bold"),
                           command=lambda: self.sql_add(self.table_name, cnp_entry.get(), cal.get_date(),
                                                        last_name_entry.get(), telephone_number_entry.get(),
                                                        has_insurance_value_yes.get(), has_insurance_value_no.get(),
                                                        has_doctor_ticket_value_yes.get(),
                                                        has_doctor_ticket_value_no.get(),
                                                        has_apnea_value_yes.get(), has_apnea_value_no.get(),
                                                        has_disease_value_yes.get(),
                                                        has_disease_value_no.get())
                           )
        ok_button.place(x=60, y=817)
        clear_button = Button(root_add, text="CLEAR", width=15, height=2, fg="#1E2729", bg="#F0FCFB",
                              font=("Helvetica", 9, "bold"),
                              command=self.clear_form_add)
        clear_button.place(x=200, y=817)
        cancel_button = Button(root_add, text="CANCEL", width=15, height=2, fg="#1E2729", bg="#E8E7D8",
                               font=("Helvetica", 9, "bold"), command=self.cancel_form_add)
        cancel_button.place(x=340, y=817)

        root_add.mainloop()

    '''
    Main gui creation
    Using canvas to put picture
    '''

    '''APP MENU PART'''

    def close_main_gui(self):
        app_menu.destroy()

    def create_main_gui(self):
        global app_menu
        app_menu = Tk()
        app_menu.title("MENU PACIENTI SOMN")
        image_canvas = os.path.join(self.pictures_folder, constants_pacienti.PICTURE_FOLDER,
                                    constants_pacienti.SOMN_IMAGE)
        image_ico = os.path.join(self.pictures_folder, constants_pacienti.PICTURE_FOLDER,
                                 constants_pacienti.SOMN_ICO_IMAGE)
        app_menu.iconbitmap(image_ico)
        app_menu.geometry("850x500")
        app_menu.resizable(0, 0)
        app_menu["bg"] = "#36EBCA"
        # create image
        image_canvas = PhotoImage(file=image_canvas)
        # create canvas
        canvas = Canvas(app_menu, height=400, width=450, bg="#36EBCA", bd=10, relief=tkinter.GROOVE)
        canvas.place(x=350, y=10)
        canvas.create_image((222, 211), image=image_canvas)
        # create buttons and label
        name_label = Label(app_menu, text="REGISTRU PACIENTI", bg="#36EBCA", fg="#EEEBF3", borderwidth=5,
                           font=("Helvetica", 25, "bold"), relief=tkinter.GROOVE,
                           justify="center", padx=5, pady=0)
        name_label.grid(row=0, column=0, sticky=tkinter.EW)
        name_label.place(relx=0.0, rely=0.02)
        add_button = Button(app_menu, fg="#EEEBF3", bg="#5BBD2A", font=("Helvetica", 9, "bold"), bd=4,
                            cursor="target", width=20, height=2, justify="center", text="ADAUGARE",
                            relief=tkinter.GROOVE, command=self.create_add_gui)
        select_button = Button(app_menu, fg="#EEEBF3", bg="#2092B0", font=("Helvetica", 9, "bold"), bd=4,
                               cursor="target", width=20, height=2, justify="center", text="VIZUALIZARE/EDITARE",
                               relief=tkinter.GROOVE)
        # command=self.open_edit)
        delete_button = Button(app_menu, fg="#EEEBF3", bg="#C9334F", font=("Helvetica", 9, "bold"), bd=4,
                               cursor="target", width=20, height=2, justify="center", text="STERGERE",
                               relief=tkinter.GROOVE)
        # command=self.open_delete)
        convert_excel_all = Button(app_menu, fg="#EEEBF3", bg="#F36D1C", font=("Helvetica", 9, "bold"), bd=4,
                                   cursor="target", width=20, height=2, justify="center",
                                   text="TRANSFER EXCEL DATE ",
                                   relief=tkinter.GROOVE,command=lambda:self.writer.write_to_excel(self.table_name))

        cancel_button = Button(app_menu, fg="#EEEBF3", bg="#C9334F", font=("Helvetica", 9, "bold"), bd=4,
                               cursor="target", width=66, height=2, justify="center", text="INCHIDERE",
                               relief=tkinter.GROOVE, command=self.close_main_gui)
        # command=self.open_delete)
        # command=self.open_delete)
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
