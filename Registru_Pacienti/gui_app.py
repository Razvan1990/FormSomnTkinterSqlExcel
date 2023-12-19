import os
import sqlite3
import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

from tkcalendar import Calendar, DateEntry

import constants_pacienti
from checker_fields import CheckFields
from checkers_sql import CheckSqlCommands
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
        root_add.resizable(NO, NO)
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
        # pressure
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
    DELETE PART
    '''

    def sql_delete(self, table_name, option, select_date, first_name, last_name, cnp):
        # args are first name and last name
        '''SQL COMMAND'''
        database = os.path.join(constants_pacienti.DATABASE_FOLDER, constants_pacienti.NAME_DATABASE)
        connection = sqlite3.connect(database)
        my_cursor = connection.cursor()
        # check selected option to see what queries to execute
        if option == "Data":
            my_cursor.execute("""DELETE FROM """ + table_name + """ WHERE DATA = :data""",
                              # dummy dictionary
                              {
                                  "data": select_date
                              })
        elif option == "Nume":
            my_cursor.execute(
                """DELETE FROM """ + table_name + """ WHERE PRENUME = :first_name AND NUME = :last_name""",
                # dummy dictionary
                {
                    "first_name": first_name.upper(),
                    "last_name": last_name.upper()
                })
        elif option == "Cnp":
            my_cursor.execute("""DELETE FROM """ + table_name + """ WHERE CNP = :cnp_value""",
                              # dummy dictionary
                              {
                                  "cnp_value": cnp
                              })
        connection.commit()
        if option == "Data":
            message_delete = "Pacientii din data de {} au fost stersi".format(select_date)
            messagebox.showinfo("PACIENT STERS", message=message_delete)
        elif option == "Nume":
            message_delete = "Pacientul {} {} a fost sters din baza de date".format(first_name, last_name)
            messagebox.showinfo("PACIENT STERS", message=message_delete)
        elif option == "Cnp":
            message_delete = "Pacientul cu cnp {} a fost sters din baza de date".format(cnp)
            messagebox.showinfo("PACIENT STERS", message=message_delete)
        root_delete_treeview.destroy()
        self.create_main_gui()

    def cancel_treeview_delete(self):
        root_delete_treeview.destroy()
        self.create_main_gui()

    def view_delete_records(self, table_name, option, select_date, first_name, last_name, cnp):
        '''MAKE CHECKS'''
        # 1.check button is pressed
        if self.checker_field.check_radiobutton_pressed(option):
            messagebox.showerror("NICI O SELECTIE", "VA ROG SELECTATI O OPTIUNE DE CAUTARE")
            return
        # 2. check if date is selected
        if option == "Data":
            if self.checker_field.check_if_date_selected(select_date):
                messagebox.showerror("DATA NESELECTATA", "VA ROG SELECTATI DATA")
                return
        # 3. check last and first name
        if option == "Nume":
            option_error, message_error = self.checker_field.check_if_first_last_name_entered(first_name, last_name)
            if option_error == 1:
                messagebox.showerror("CAMPURI NECOMPLETATE", message=message_error)
                return
            elif option_error == 2:
                messagebox.showerror("NUME NECOMPLETAT", message=message_error)
                return
            elif option_error == 3:
                messagebox.showerror("PRENUME NECOMPLETAT", message=message_error)
                return
        # 4. check cnp
        if option == "Cnp":
            if self.checker_field.check_cnp_complete(cnp):
                messagebox.showerror("CNP NECOMPLETAT", "VA ROG COMPLETATI CNP-UL")
                return
            cnp_message_error, cnp_option_error = self.checker_field.get_cnp_errors(cnp)
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
        database = os.path.join(constants_pacienti.DATABASE_FOLDER, constants_pacienti.NAME_DATABASE)
        connection = sqlite3.connect(database)
        my_cursor = connection.cursor()
        # check selected option to see what queries to execute
        if option == "Data":
            my_cursor.execute("""SELECT oid,* FROM """ + table_name + """ WHERE DATA=:data""",
                              # dummy dictionary
                              {
                                  "data": select_date
                              })
        elif option == "Nume":
            my_cursor.execute(
                """SELECT oid,* FROM """ + table_name + """ WHERE PRENUME=:first_name AND NUME=:last_name""",
                # dummy dictionary
                {
                    "first_name": first_name.upper(),
                    "last_name": last_name.upper()
                })
        elif option == "Cnp":
            my_cursor.execute("""SELECT oid,* FROM """ + table_name + """ WHERE CNP=:cnp_value""",
                              # dummy dictionary
                              {
                                  "cnp_value": cnp
                              })
        # get list of results and check if we have such records
        list_results = my_cursor.fetchall()
        if len(list_results) == 0:
            messagebox.showerror("PACIENT NEEXISTENT", "CAUTAREA NU A PRODUS NICI UN REZULTAT CU ACESTE CONDITII")
            return
        '''CREATE THE GUI WITH THE TREEVIEW OF RECORDS'''
        root_delete.destroy()
        global root_delete_treeview
        root_delete_treeview = Tk()
        root_delete_treeview.title("DELETE")
        image_ico = os.path.join(self.pictures_folder, constants_pacienti.PICTURE_FOLDER,
                                 constants_pacienti.SOMN_ICO_IMAGE)
        root_delete_treeview.iconbitmap(image_ico)
        root_delete_treeview.geometry("850x500")
        root_delete_treeview["bg"] = "#BC6678"
        root_delete_treeview.resizable(NO, NO)
        root_delete_treeview.protocol("WM_DELETE_WINDOW", self.cancel_x_button)
        # treeview creation
        frame_treeview = LabelFrame(root_delete_treeview, fg="#EEEBF3", bg="#BC6678", font=("Helvetica", 20, "bold"),
                                    bd=5,
                                    cursor="target", width=800, height=425, labelanchor="n", text="STERGERE PACIENT",
                                    relief=tkinter.GROOVE)
        frame_treeview.grid(padx=25, pady=10, row=0, column=0, )  # put it in the middle
        frame_treeview.grid_rowconfigure(0, weight=1)
        frame_treeview.grid_columnconfigure(0, weight=1)
        # create tree to show footballers
        columns = ("ID", "PRENUME", "NUME", "CNP", "APNEE", "TIP_APNEE", "PRESIUNE")
        tree_patients = ttk.Treeview(frame_treeview, show='headings', columns=columns, height=15, )
        # ADD THE COLUMNS
        # define the headings
        tree_patients.heading(0, text="ID", anchor=tkinter.W)
        tree_patients.heading(1, text="PRENUME", anchor=tkinter.W)
        tree_patients.heading(2, text="NUME", anchor=tkinter.W)
        tree_patients.heading(3, text="CNP", anchor=tkinter.W)
        tree_patients.heading(4, text="APNEE", anchor=tkinter.W)
        tree_patients.heading(5, text="TIP_APNEE", anchor=tkinter.W)
        tree_patients.heading(6, text="PRESIUNE", anchor=tkinter.W)
        # redefine column dimensions
        tree_patients.column("ID", width=25, )
        tree_patients.column("PRENUME", width=125, stretch=NO)
        tree_patients.column("NUME", width=125, stretch=NO)
        tree_patients.column("CNP", width=100, stretch=NO)
        tree_patients.column("APNEE", width=50, stretch=NO)
        tree_patients.column("TIP_APNEE", width=100, stretch=NO)
        tree_patients.column("PRESIUNE", width=125, stretch=NO)
        tree_patients.tag_configure("orow")
        # create a custom style
        style = ttk.Style(root_delete_treeview)
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="#D4EE77", foreground="#C7651D")
        # populate the list
        for record in list_results:
            record_update = list()
            record_update.append(str(record[0]))
            record_update.append(record[2])
            record_update.append(record[3])
            record_update.append(record[4])
            record_update.append(record[14])
            record_update.append(record[15])
            record_update.append(record[18])
            record_update_tuple = tuple(record_update)
            tree_patients.insert('', tkinter.END, values=record_update_tuple)
        # put the treeview on the frame
        tree_patients.place(x=60, y=10)
        # create a scrollbar
        my_scrollbar = Scrollbar(frame_treeview, orient=tkinter.VERTICAL, command=tree_patients.yview)
        tree_patients.configure(yscrollcommand=my_scrollbar.set)
        my_scrollbar.place(x=713, y=11, height=328)
        # add buttons for cancel and delete
        ok_button = Button(frame_treeview, text="DELETE", width=20, height=2, fg="#1E2729", bg="#248B48",
                           font=("Helvetica", 9, "bold"),
                           command=lambda: self.sql_delete(self.table_name, option, select_date, first_name, last_name,
                                                           cnp))
        cancel_button = Button(frame_treeview, text="CANCEL", width=20, height=2, fg="#1E2729", bg="#E8E7D8",
                               font=("Helvetica", 9, "bold"), command=self.cancel_treeview_delete)
        ok_button.place(x=150, y=343)
        cancel_button.place(x=480, y=343)

    def handle_radio_button_date(self, value_date, *args):
        # value_date = selection_option1
        if args[0] == value_date:
            # first we make the calendar available
            args[1]["state"] = tkinter.NORMAL
            # delete all other entries
            args[2]["state"] = tkinter.NORMAL
            args[3]["state"] = tkinter.NORMAL
            args[4]["state"] = tkinter.NORMAL
            args[2].delete(0, END)
            args[3].delete(0, END)
            args[4].delete(0, END)
            # make them  disabled again
            args[2]["state"] = tkinter.DISABLED
            args[3]["state"] = tkinter.DISABLED
            args[4]["state"] = tkinter.DISABLED

    def handle_radio_button_cnp(self, value_cnp, *args):
        # value_cnp = selection_option3
        if args[0] == value_cnp:
            # first we make the cnpo enabled
            args[1]["state"] = tkinter.NORMAL
            # reset calendar and make it disabled
            args[2]["state"] = tkinter.NORMAL
            args[2].delete(0, END)
            args[2]["state"] = tkinter.DISABLED
            # delete the first and last name and make them disabled
            args[3]["state"] = tkinter.NORMAL
            args[4]["state"] = tkinter.NORMAL
            args[3].delete(0, END)
            args[4].delete(0, END)
            # make them  disabled again
            args[3]["state"] = tkinter.DISABLED
            args[4]["state"] = tkinter.DISABLED

    def handle_radio_button_name(self, value_name, *args):
        # value_name = selection_option2
        if args[0] == value_name:
            # first we make the first and last name states enabled
            args[1]["state"] = tkinter.NORMAL
            args[2]["state"] = tkinter.NORMAL
            # delete the calendar date ane make it unavailable
            args[3]["state"] = tkinter.NORMAL
            args[3].delete(0, END)
            args[3]["state"] = tkinter.DISABLED
            # delete cnp and make it disabled
            args[4]["state"] = tkinter.NORMAL
            args[4].delete(0, END)
            args[4]["state"] = tkinter.DISABLED

    def cancel_form_delete(self):
        root_delete.destroy()
        self.create_main_gui()

    def create_delete_gui(self):
        global root_delete
        app_menu.destroy()
        # global variables
        global radio_button_date
        global radio_button_name
        global radio_button_cnp
        global calendar_entry
        global first_name_entry_delete
        global last_name_entry_delete
        global cnp_entry_delete
        global selection_option

        root_delete = Tk()
        root_delete.title("DELETE")
        image_ico = os.path.join(self.pictures_folder, constants_pacienti.PICTURE_FOLDER,
                                 constants_pacienti.SOMN_ICO_IMAGE)
        root_delete.iconbitmap(image_ico)
        root_delete.geometry("1020x330")
        root_delete["bg"] = "#BC6678"
        root_delete.resizable(NO, NO)
        root_delete.protocol("WM_DELETE_WINDOW", self.cancel_x_button)
        # stringvars
        selection_option = StringVar()
        # put values for radiobuttons
        selection_option1 = "Data"
        selection_option2 = "Nume"
        selection_option3 = "Cnp"
        frame_title = LabelFrame(root_delete, fg="#EEEBF3", bg="#BC6678", font=("Helvetica", 20, "bold"), bd=5,
                                 cursor="target", width=920, height=300, labelanchor="n", text="STERGERE PACIENT",
                                 relief=tkinter.GROOVE)
        frame_title.grid(padx=10, pady=10, row=0, column=0, )  # put it in the middle
        frame_title.grid_rowconfigure(0, weight=1)
        frame_title.grid_columnconfigure(0, weight=1)
        # add frame for date
        frame_date = LabelFrame(frame_title, fg="#EEEBF3", bg="#BC6678", font=("Helvetica", 15, "bold"),
                                bd=5,
                                cursor="target", width=230, height=200, labelanchor="n",
                                text="SELECTIE DATA",
                                relief=tkinter.GROOVE)
        frame_date.place(x=30, y=10)
        calendar_entry = DateEntry(frame_date, selectmode='day', date_pattern="DD-MM-YYYY", bd=2,
                                   headersbackground="#EBFE8A",
                                   headersforeground="#1E1F1C", selectbackground="#209DBF", selectforeground="#F26B18",
                                   weekendbackground="#8D7B80", font=("Helvetica", 9, "bold"), bg="#9EEB8D")
        calendar_entry.state(["disabled"])
        calendar_entry.place(x=80, y=20)
        calendar_entry_label = Label(frame_date, text="DATA", justify="center",
                                     font=("Helvetica", 11, "bold"),
                                     cursor="star", fg="#B9DBDA", bg="#BC6678")
        calendar_entry_label.place(x=20, y=20)
        # add frame for first and last name
        frame_first_last_name = LabelFrame(frame_title, fg="#EEEBF3", bg="#BC6678", font=("Helvetica", 15, "bold"),
                                           bd=5,
                                           cursor="target", width=230, height=200, labelanchor="n",
                                           text="SELECTIE NUME",
                                           relief=tkinter.GROOVE)
        frame_first_last_name.place(x=280, y=10)
        first_name_entry_delete = Entry(frame_first_last_name, width=18, justify="center",
                                        font=("Helvetica", 8, "bold"),
                                        cursor="target",
                                        bg="#9EEB8D", state=tkinter.DISABLED)
        first_name_entry_delete.place(x=100, y=40)
        first_name_label = Label(frame_first_last_name, text="PRENUME", justify="center",
                                 font=("Helvetica", 11, "bold"),
                                 cursor="star", fg="#B9DBDA", bg="#BC6678")
        first_name_label.place(x=5, y=40)
        last_name_entry_delete = Entry(frame_first_last_name, width=18, justify="center",
                                       font=("Helvetica", 8, "bold"),
                                       cursor="target",
                                       bg="#9EEB8D", state=tkinter.DISABLED)
        last_name_entry_delete.place(x=100, y=100)
        last_name_label = Label(frame_first_last_name, text="NUME", justify="center",
                                font=("Helvetica", 11, "bold"),
                                cursor="star", fg="#B9DBDA", bg="#BC6678")
        last_name_label.place(x=5, y=100)
        # add frame for cnp
        frame_cnp = LabelFrame(frame_title, fg="#EEEBF3", bg="#BC6678", font=("Helvetica", 15, "bold"),
                               bd=5,
                               cursor="target", width=230, height=200, labelanchor="n",
                               text="SELECTIE CNP",
                               relief=tkinter.GROOVE)
        frame_cnp.place(x=530, y=10)
        cnp_entry_delete = Entry(frame_cnp, width=20, justify="center",
                                 font=("Helvetica", 8, "bold"),
                                 cursor="target",
                                 bg="#9EEB8D", state=tkinter.DISABLED)
        cnp_entry_delete.place(x=80, y=60)
        cnp_label = Label(frame_cnp, text="CNP", justify="center",
                          font=("Helvetica", 11, "bold"),
                          cursor="star", fg="#B9DBDA", bg="#BC6678")
        cnp_label.place(x=5, y=60)
        # create frame for checkbuttons
        check_frame = LabelFrame(frame_title, fg="#EEEBF3", bg="#BC6678", font=("Helvetica", 15, "bold"),
                                 bd=5,
                                 cursor="target", width=100, height=200, labelanchor="n",
                                 text="CHECK",
                                 relief=tkinter.GROOVE)
        check_frame.place(x=780, y=10)
        # put radiobuttons
        radio_button_date = Radiobutton(check_frame, text="DATE", variable=selection_option,
                                        value=selection_option1,
                                        bd=5, font=("Helvetica", 11, "bold"),
                                        bg="#BC6678", fg="#EEEBF3", selectcolor="black",
                                        command=lambda: self.handle_radio_button_date(selection_option1,
                                                                                      selection_option.get(),
                                                                                      calendar_entry,
                                                                                      first_name_entry_delete,
                                                                                      last_name_entry_delete,
                                                                                      cnp_entry_delete))
        radio_button_date.place(x=5, y=20)
        radio_button_name = Radiobutton(check_frame, text="NUME", variable=selection_option,
                                        value=selection_option2,
                                        bd=5, font=("Helvetica", 11, "bold"),
                                        bg="#BC6678", fg="#EEEBF3", selectcolor='black',
                                        command=lambda: self.handle_radio_button_name(selection_option2,
                                                                                      selection_option.get(),
                                                                                      first_name_entry_delete,
                                                                                      last_name_entry_delete,
                                                                                      calendar_entry,
                                                                                      cnp_entry_delete))

        radio_button_name.place(x=5, y=70)
        radio_button_cnp = Radiobutton(check_frame, text="CNP", variable=selection_option,
                                       value=selection_option3,
                                       bd=5, font=("Helvetica", 11, "bold"),
                                       bg="#BC6678", fg="#EEEBF3", selectcolor='black',
                                       command=lambda: self.handle_radio_button_name(selection_option3,
                                                                                     selection_option.get(),
                                                                                     cnp_entry_delete,
                                                                                     calendar_entry,
                                                                                     first_name_entry_delete,
                                                                                     last_name_entry_delete))
        radio_button_cnp.place(x=5, y=120)
        # put ok and cancel buttons
        ok_button = Button(frame_title, text="VIZUALIZARE", width=30, height=2, fg="#1E2729", bg="#248B48",
                           font=("Helvetica", 9, "bold"),
                           command=lambda: self.view_delete_records(self.table_name, selection_option.get(),
                                                                    calendar_entry.get(), first_name_entry_delete.get(),
                                                                    last_name_entry_delete.get(),
                                                                    cnp_entry_delete.get()))
        cancel_button = Button(frame_title, text="CANCEL", width=30, height=2, fg="#1E2729", bg="#E8E7D8",
                               font=("Helvetica", 9, "bold"), command=self.cancel_form_delete)
        ok_button.place(x=150, y=215)
        cancel_button.place(x=500, y=215)

    '''
    EDIT PART
    '''

    def cancel_treeview_edit(self):
        root_edit_treeview.destroy()
        self.create_main_gui()

    def cancel_update(self):
        root_update.destroy()
        self.create_main_gui()

    def sql_update(self, table_name, cnp_upd, cal_date_upd, last_name_upd, telephone_number_upd,
                   *args):
        database = os.path.join(constants_pacienti.DATABASE_FOLDER, constants_pacienti.NAME_DATABASE)
        connection = sqlite3.connect(database)
        my_cursor = connection.cursor()
        # 1 .check if mandatory fields are completed
        if self.checker_field.check_if_necessary_fields_completed(cal_date_upd, cnp_upd, last_name_upd, ):
            messagebox.showerror("CAMPURI NECOMPLETATE", "CAMPURI OBLIGATORII(*) NECOMPLETATE!")
            return
            # 3. check cnp validity
        message_error, option = self.checker_field.get_cnp_errors(cnp_upd)
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
        message_error, option = self.checker_field.get_telephone_number_errors(telephone_number_upd)
        if option == 1 and len(telephone_number_upd) != 0:
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
            messagebox.showerror("BOLI CUNOSCUTE NECOMPLETAT",
                                 "COMPLETATI DACA PACIENTUL ARE BOLI CUNOSCUTE SAU NU")
            return
        '''
        CHECK IF WE HAVE DIFFERENCE TO EXECUTE THE UPDATE
        '''
        list_modifications = list()
        list_modifications.append(cal_update.get_date())
        list_modifications.append(first_name_entry_update.get().upper())
        list_modifications.append(last_name_entry_update.get().upper())
        list_modifications.append(str(cnp_entry_update.get()))
        list_modifications.append(str(telephone_number_entry_update.get()))
        list_modifications.append(address_entry_street_update.get().upper())
        list_modifications.append(address_entry_locality_update.get().upper())
        list_modifications.append(judet_value_update.get().upper())
        list_modifications.append(has_insurance_value_general_update.get())
        list_modifications.append(asigurare_value_update.get())
        list_modifications.append(has_doctor_ticket_value_general_update.get())
        list_modifications.append(ticket_number_update.get().upper())
        # in order to get without an extra space we use end-1c(character)
        list_modifications.append(anamneza_update.get("1.0", "end-1c").upper())
        list_modifications.append(has_apnea_value_general_update.get())
        list_modifications.append(apnea_type_value_update.get().upper())
        list_modifications.append(mask_type_value_update.get().upper())
        list_modifications.append(compliance_update.get().upper())
        list_modifications.append(pressure_update.get().upper())
        list_modifications.append(has_disease_value_general_update.get())
        list_modifications.append(disease_section_update.get("1.0", "end-1c").upper())
        list_modifications.append(recommendation_section_update.get("1.0", "end-1c").upper())

        print(list_record_entries)
        print(list_modifications)
        # make the comparison
        if self.checker_sql.compare_list(list_record_entries[0], list_modifications):
            messagebox.showerror("FARA MODIFICARI", "NU EXISTA MODIFICARI LA DATE")
            return

        # SQL PART

        my_cursor.execute("""UPDATE """ + table_name + """ SET
                            DATA =:calendar_update,
                            PRENUME=:first_name_upd,
                            NUME=:last_name_upd,
                            CNP=:cnp_upd,
                            TELEFON=:telephone_upd,
                            STRADA=:address_street_upd,
                            LOCALITATE=:address_locality_upd,
                            JUDET=:address_region_upd,
                            ASIGURARE=:insurance_val_upd,
                            TIP_ASIGURARE=:insurance_type_upd,
                            BILET_TRIMITERE=:ticket_val_upd,
                            NUMAR_BILET=:ticket_number_upd,
                            ANAMNEZA=:anamneza_upd,
                            APNEE=:apnea_val_upd,
                            TIP_APNEE=:apnea_type_upd,
                            TIP_MASCA=:mask_type_upd,
                            COMPLIANTA=:compliance_upd,
                            PRESIUNE=:pressure_upd,
                            BOLI_CUNOSCUTE=:disease_val_upd,
                            BOLI=:disease_types_upd,
                            RECOMANDARE=:recommendation_upd WHERE oid=:id""",

                          # dummy dictionary
                          {
                              "calendar_update": cal_update.get_date(),
                              "first_name_upd": first_name_entry_update.get().upper(),
                              "last_name_upd": last_name_entry_update.get().upper(),
                              "cnp_upd": str(cnp_entry_update.get()),
                              "telephone_upd": str(telephone_number_entry_update.get()),
                              "address_street_upd": address_entry_street_update.get().upper(),
                              "address_locality_upd":address_entry_locality_update.get().upper(),
                              "address_region_upd": judet_value_update.get().upper(),
                              "insurance_val_upd": has_insurance_value_general_update.get(),
                              "insurance_type_upd": asigurare_value_update.get(),
                              "ticket_val_upd": has_doctor_ticket_value_general_update.get(),
                              "ticket_number_upd": ticket_number_update.get().upper(),
                              "anamneza_upd": anamneza_update.get("1.0", "end-1c").upper(),
                              "apnea_val_upd": has_apnea_value_general_update.get(),
                              "apnea_type_upd": apnea_type_value_update.get().upper(),
                              "mask_type_upd": mask_type_value_update.get().upper(),
                              "compliance_upd": compliance_update.get().upper(),
                              "pressure_upd": pressure_update.get().upper(),
                              "disease_val_upd": has_disease_value_general_update.get(),
                              "disease_types_upd": disease_section_update.get("1.0", "end-1c").upper(),
                              "recommendation_upd": recommendation_section_update.get("1.0", "end-1c").upper(),
                              "id": list_record[0]
                          }
                          )
        connection.commit()
        message_update = "DATELE PACIENTULUI {} AVAND CNP {} SI CONSULTAT IN DATA DE {} AU FOST MODIFICATE".format(
            last_name_entry_update.get().upper(), str(cnp_entry_update.get()), cal_update.get_date())
        messagebox.showinfo("DATE MODIFICATE", message=message_update)
        my_cursor.close()
        connection.close()
        root_update.destroy()
        self.create_main_gui()

    def open_entry(self, table_name, event):
        '''
        :return: A window like in ADD with the information for the patient
        '''

        '''
        FIRST WE NEED TO INTEROGATE THE DATABASE TO OBTAIN ALL INFORMATION FOR THAT RECORD
        '''
        # use a global to already have a list that contains the original fields for the patient
        global list_record
        global list_record_entries
        database = os.path.join(constants_pacienti.DATABASE_FOLDER, constants_pacienti.NAME_DATABASE)
        connection = sqlite3.connect(database)
        my_cursor = connection.cursor()
        list_record = []
        # we need the first value of the treeview -> the id of the treeview
        for patient in tree_patients_edit.selection():
            patient_data = tree_patients_edit.item(patient)
            record = patient_data["values"]
            list_record = record
        # now use the record for sql command
        my_cursor.execute(
            """SELECT * FROM """ + table_name + """ WHERE oid =:id""",
            # dummy dictionary
            {
                "id": list_record[0]
            })
        list_record_entries = my_cursor.fetchall()
        """
        SECOND WE NEED TO RE - CREATE A WINDOW LIKE IN ADD
        """

        root_edit_treeview.destroy()
        global root_update
        global cal_update
        global first_name_entry_update
        global last_name_entry_update
        global cnp_entry_update
        global telephone_number_entry_update
        global address_entry_street_update
        global address_entry_locality_update
        global address_region_menu_update
        global has_insurance_yes_update  # checkButton
        global has_insurance_no_update  # checkButton
        global insurance_type_update
        # medical info
        global doctor_ticket_yes_update  # bilet trimitere
        global doctor_ticket_no_update  # bilet trimitere
        global ticket_number_update
        global has_apnea_update  # checkButton
        global has_apnea_yes_update
        global has_apnea_no_update
        global apnea_type_update
        global mask_type_update
        global compliance_update
        global pressure_update
        global has_diseases_yes_update
        global has_diseases_no_update
        # textareas
        global anamneza_update
        global disease_section_update
        global recommendation_section_update
        # stringvars
        global has_insurance_value_yes_update
        global has_insurance_value_no_update
        global has_insurance_value_general_update
        global has_doctor_ticket_value_yes_update
        global has_doctor_ticket_value_no_update
        global has_doctor_ticket_value_general_update
        global judet_value_update
        global asigurare_value_update
        global has_apnea_value_yes_update
        global has_apnea_value_no_update
        global has_apnea_value_general_update
        global apnea_type_value_update
        global mask_type_value_update
        global has_disease_value_yes_update
        global has_disease_value_no_update
        global has_disease_value_general_update

        root_update = Tk()
        root_update.title("UPDATE")
        image_ico = os.path.join(self.pictures_folder, constants_pacienti.PICTURE_FOLDER,
                                 constants_pacienti.SOMN_ICO_IMAGE)
        root_update.iconbitmap(image_ico)
        root_update.geometry("1200x900")
        root_update["bg"] = "#2092B0"
        root_update.resizable(NO, NO)
        # stringvar variables
        judet_value_update = StringVar()
        judet_value_update.set(list_record_entries[0][7])
        has_insurance_value_yes_update = StringVar()
        has_insurance_value_no_update = StringVar()
        has_insurance_value_general_update = StringVar()
        # set the insurance_general_value
        has_insurance_value_general_update.set(list_record_entries[0][8])
        asigurare_value_update = StringVar()
        asigurare_value_update.set(list_record_entries[0][9])
        has_doctor_ticket_value_yes_update = StringVar()
        has_doctor_ticket_value_no_update = StringVar()
        has_doctor_ticket_value_general_update = StringVar()
        # set the ticket_general value
        has_doctor_ticket_value_general_update.set(list_record_entries[0][10])
        has_apnea_value_yes_update = StringVar()
        has_apnea_value_no_update = StringVar()
        has_apnea_value_general_update = StringVar()
        # set apnea general value
        has_apnea_value_general_update.set(list_record_entries[0][13])
        # set the apnea_general value
        apnea_type_value_update = StringVar()
        apnea_type_value_update.set(list_record_entries[0][14])
        # set the mask value
        mask_type_value_update = StringVar()
        mask_type_value_update.set(list_record_entries[0][15])
        has_disease_value_yes_update = StringVar()
        has_disease_value_no_update = StringVar()
        has_disease_value_general_update = StringVar()
        # set known disease general
        has_disease_value_general_update.set(list_record_entries[0][18])

        # root_update.protocol("WM_DELETE_WINDOW", self.cancel_x_button)
        # create first frame for title label
        frame_title = LabelFrame(root_update, fg="#EEEBF3", bg="#2092B0", font=("Helvetica", 25, "bold"), bd=5,
                                 cursor="target", width=1100, height=850, labelanchor="n", text="MODIFICARE PACIENT",
                                 relief=tkinter.GROOVE)
        frame_title.grid(padx=42, pady=10, row=0, column=0, )  # put it in the middle
        frame_title.grid_rowconfigure(0, weight=1)
        frame_title.grid_columnconfigure(0, weight=1)

        # create frame for personal settings
        frame_personal_info = LabelFrame(frame_title, fg="#EEEBF3", bg="#2092B0", font=("Helvetica", 15, "bold"),
                                         bd=5,
                                         cursor="target", width=350, height=800, labelanchor=tkinter.N,
                                         text="DATE PERSONALE",
                                         relief=tkinter.GROOVE)
        frame_personal_info.grid(padx=10, pady=10, row=0, column=0, sticky=tkinter.EW)  # put it in the middle
        frame_personal_info.grid_rowconfigure(0, weight=1)
        frame_personal_info.grid_columnconfigure(0, weight=1)

        # first add the calendar and set the date
        list_date = self.checker_field.split_date(list_record_entries[0][0])
        cal_update = Calendar(frame_personal_info, selectmode='day', date_pattern="DD-MM-YYYY", bd=2,
                              headersbackground="#EBFE8A", year=int(list_date[2]), month=int(list_date[1]),
                              day=int(list_date[0]),
                              headersforeground="#1E1F1C", selectbackground="#209DBF", selectforeground="#F26B18",
                              weekendbackground="#8D7B80", font=("Helvetica", 9, "bold"))
        cal_update.grid(row=0, column=1, pady=(5, 5))
        calendar_label_update = Label(frame_personal_info, text="DATA*", justify="center",
                                      font=("Helvetica", 11, "bold"),
                                      cursor="star", fg="#C6E744", bg="#2092B0")
        calendar_label_update.grid(row=0, column=0, padx=5, pady=(5, 5))
        '''add entries and label'''
        # first name
        first_name_entry_update = Entry(frame_personal_info, width=25, justify="center", font=("Helvetica", 9, "bold"),
                                        cursor="target",
                                        bg="#D4E2D0")
        first_name_entry_update.grid(row=1, column=1, pady=(5, 5))
        first_name_label_update = Label(frame_personal_info, text="PRENUME", justify="center",
                                        font=("Helvetica", 11, "bold"),
                                        cursor="star", fg="#C6E744", bg="#2092B0")
        first_name_label_update.grid(row=1, column=0, padx=5, pady=(5, 5))
        # last name
        last_name_entry_update = Entry(frame_personal_info, width=25, justify="center", font=("Helvetica", 9, "bold"),
                                       cursor="target",
                                       bg="#D4E2D0")
        last_name_entry_update.grid(row=2, column=1, pady=(5, 5))
        last_name_label_update = Label(frame_personal_info, text="NUME*", justify="center",
                                       font=("Helvetica", 11, "bold"),
                                       cursor="star", fg="#C6E744", bg="#2092B0")
        last_name_label_update.grid(row=2, column=0, padx=5, pady=(5, 5))
        # cnp
        cnp_entry_update = Entry(frame_personal_info, width=25, justify="center", font=("Helvetica", 9, "bold"),
                                 cursor="target",
                                 bg="#D4E2D0")
        cnp_entry_update.grid(row=3, column=1, pady=(5, 5))
        cnp_label_update = Label(frame_personal_info, text="CNP*", justify="center", font=("Helvetica", 11, "bold"),
                                 cursor="star", fg="#C6E744", bg="#2092B0", )
        cnp_label_update.grid(row=3, column=0, padx=5, pady=(5, 5))
        # telephone
        telephone_number_entry_update = Entry(frame_personal_info, width=25, justify="center",
                                              font=("Helvetica", 9, "bold"),
                                              cursor="target",
                                              bg="#D4E2D0")
        telephone_number_entry_update.grid(row=4, column=1, pady=(5, 5))
        telephone_number_label_update = Label(frame_personal_info, text="TELEFON", justify="center",
                                              font=("Helvetica", 11, "bold"),
                                              cursor="star", fg="#C6E744", bg="#2092B0")
        telephone_number_label_update.grid(row=4, column=0, padx=5, pady=(5, 5))
        # create a frame label for the address
        address_frame_label_update = LabelFrame(frame_personal_info, fg="#EEEBF3", bg="#2092B0",
                                                font=("Helvetica", 13, "bold"), bd=5,
                                                cursor="target", labelanchor="n", text="ADRESA", width=315, height=200,
                                                relief=tkinter.GROOVE)
        address_frame_label_update.grid(row=5, column=0, columnspan=2)  # put it in the middle
        address_frame_label_update.grid_rowconfigure(0, weight=1)
        address_frame_label_update.grid_columnconfigure(0, weight=1)
        # street_name
        address_label_street_update = Label(address_frame_label_update, text="STRADA", justify="center",
                                            font=("Helvetica", 11, "bold"),
                                            cursor="star", fg="#C6E744", bg="#2092B0")
        address_label_street_update.grid(row=0, column=0, padx=5, pady=(5, 5))
        address_entry_street_update = Entry(address_frame_label_update, width=23, justify="center",
                                            font=("Helvetica", 9, "bold"),
                                            cursor="target",
                                            bg="#D4E2D0")
        address_entry_street_update.grid(row=0, column=1, padx=5, pady=(5, 5))
        # locality_name
        address_locality_label_update = Label(address_frame_label_update, text="LOCALITATE", justify="center",
                                              font=("Helvetica", 11, "bold"),
                                              cursor="star", fg="#C6E744", bg="#2092B0")
        address_locality_label_update.grid(row=1, column=0, padx=5, pady=(5, 5))
        address_entry_locality_update = Entry(address_frame_label_update, width=23, justify="center",
                                              font=("Helvetica", 9, "bold"),
                                              cursor="target",
                                              bg="#D4E2D0")
        address_entry_locality_update.grid(row=1, column=1, padx=5, pady=(5, 5))
        # region name
        address_region_label_update = Label(address_frame_label_update, text="JUDET*", justify="center",
                                            font=("Helvetica", 11, "bold"),
                                            cursor="star", fg="#C6E744", bg="#2092B0")
        address_region_label_update.grid(row=2, column=0, padx=5, pady=(5, 5))
        address_region_menu_update = OptionMenu(address_frame_label_update, judet_value_update,
                                                *constants_pacienti.REGION_LIST, )
        address_region_menu_update.config(bg="#07A52D", font=("Helvetica", 11, "bold"), fg="#DEFFE6", width=16)
        address_region_menu_update.grid(row=2, column=1, padx=5, pady=(5, 5))
        # insurance part
        has_insurance_yes_update = Checkbutton(frame_personal_info, text="YES", variable=has_insurance_value_yes_update,
                                               onvalue="YES", offvalue="", bg="#2092B0",
                                               command=lambda: self.handle_insurance_buton_yes(
                                                   has_insurance_value_yes_update,
                                                   has_insurance_value_general_update,
                                                   insurance_type_update,
                                                   has_insurance_no_update))
        has_insurance_yes_update.grid(row=6, column=1, padx=5, pady=(5, 5))
        has_insurance_yes_update.place(relx=0.4, rely=0.87)
        has_insurance_yes_update.deselect()
        has_insurance_no_update = Checkbutton(frame_personal_info, text="NO", variable=has_insurance_value_no_update,
                                              onvalue="NO", offvalue="", bg="#2092B0",
                                              command=lambda: self.handle_insurance_buton_no(
                                                  has_insurance_value_no_update,
                                                  has_insurance_value_general_update,
                                                  asigurare_value_update,
                                                  insurance_type_update,
                                                  has_insurance_yes_update))
        has_insurance_no_update.grid(row=6, column=2, padx=5, pady=(5, 5))
        has_insurance_no_update.place(relx=0.77, rely=0.87)
        has_insurance_no_update.deselect()
        # check what is the value of the insurance
        if has_insurance_value_general_update.get() == "YES":
            has_insurance_yes_update.select()
        else:
            has_insurance_no_update.select()
        insurance_label = Label(frame_personal_info, text="ASIGURARE*", justify="center",
                                font=("Helvetica", 11, "bold"),
                                cursor="star", fg="#C6E744", bg="#2092B0")
        insurance_label.grid(row=6, column=0, padx=5, pady=(15, 5))
        # type_insurance
        insurance_type_label_update = Label(frame_personal_info, text="TIP ASIGURARE", justify="center",
                                            font=("Helvetica", 11, "bold"),
                                            cursor="star", fg="#C6E744", bg="#2092B0")
        insurance_type_label_update.grid(row=7, column=0, padx=5, pady=(5, 5))
        insurance_type_update = OptionMenu(frame_personal_info, asigurare_value_update,
                                           *constants_pacienti.INSURANCE_LIST, )
        insurance_type_update.config(bg="#07A52D", font=("Helvetica", 11, "bold"), fg="#DEFFE6",
                                     width=18)
        insurance_type_update.grid(row=7, column=1, padx=5, pady=(5, 5), )
        '''
        FRAME PATIENT STATISTICS
        '''
        frame_patient_medical_update = LabelFrame(frame_title, fg="#EEEBF3", bg="#2092B0",
                                                  font=("Helvetica", 15, "bold"),
                                                  bd=5,
                                                  cursor="target", width=700, height=800, labelanchor="n",
                                                  text="DATE MEDICALE",
                                                  relief=tkinter.GROOVE)
        frame_patient_medical_update.grid(padx=10, pady=10, row=0, column=1, )  # put it in the middle
        frame_patient_medical_update.grid_rowconfigure(0, weight=1)
        frame_patient_medical_update.grid_columnconfigure(0, weight=1)
        # doctor ticket part
        doctor_ticket_label_update = Label(frame_patient_medical_update, text="BILET TRIMITERE*", justify="center",
                                           font=("Helvetica", 11, "bold"),
                                           cursor="star", fg="#C6E744", bg="#2092B0")
        doctor_ticket_label_update.place(x=40, y=30)
        doctor_ticket_yes_update = Checkbutton(frame_patient_medical_update, text="YES",
                                               variable=has_doctor_ticket_value_yes_update,
                                               onvalue="YES", offvalue="", bg="#2092B0",
                                               command=lambda: self.handle_ticket_medical_yes(
                                                   has_doctor_ticket_value_yes_update,
                                                   has_doctor_ticket_value_general_update,
                                                   ticket_number_update,
                                                   doctor_ticket_no_update))
        doctor_ticket_yes_update.place(x=195, y=30)
        doctor_ticket_yes_update.deselect()
        doctor_ticket_no_update = Checkbutton(frame_patient_medical_update, text="NO",
                                              variable=has_doctor_ticket_value_no_update,
                                              onvalue="NO", offvalue="", bg="#2092B0",
                                              command=lambda: self.handle_ticket_medical_no(
                                                  has_doctor_ticket_value_no_update,
                                                  has_doctor_ticket_value_general_update,
                                                  ticket_number_update,
                                                  doctor_ticket_yes_update))
        doctor_ticket_no_update.place(x=320, y=30)
        doctor_ticket_no_update.deselect()
        # check what is the value of the medical ticket
        if has_doctor_ticket_value_general_update.get() == "YES":
            doctor_ticket_yes_update.select()
        else:
            doctor_ticket_no_update.select()
        ticket_number_label_update = Label(frame_patient_medical_update, text="COD BILET", justify="center",
                                           font=("Helvetica", 11, "bold"),
                                           cursor="star", fg="#C6E744", bg="#2092B0")
        ticket_number_label_update.place(x=40, y=70)
        ticket_number_update = Entry(frame_patient_medical_update, width=23, justify="center",
                                     font=("Helvetica", 9, "bold"),
                                     cursor="target", bg="#D4E2D0")
        ticket_number_update.place(x=200, y=70)
        # anamneza
        anamneza_label_update = Label(frame_patient_medical_update, text="ANAMNEZA", justify="center",
                                      font=("Helvetica", 11, "bold"),
                                      cursor="star", fg="#C6E744", bg="#2092B0")
        anamneza_label_update.place(x=40, y=150)
        anamneza_update = Text(frame_patient_medical_update, width=65, height=10, font=("Helvetica", 9, "bold"),
                               cursor="target", bd=4, bg="#C8E6F0", relief=GROOVE, wrap=WORD, highlightcolor="#907AFB",
                               highlightbackground="#907AFB")
        anamneza_update.place(x=200, y=110)
        my_scrollbar_update = Scrollbar(frame_patient_medical_update, orient=tkinter.VERTICAL,
                                        command=anamneza_update.yview, )
        anamneza_update.configure(yscrollcommand=my_scrollbar_update.set, )
        my_scrollbar_update.place(x=660, y=110, height=160)
        '''apnea part'''
        frame_apnea_update = LabelFrame(frame_patient_medical_update, fg="#EEEBF3", bg="#2092B0",
                                        font=("Helvetica", 13, "bold"),
                                        bd=5,
                                        cursor="target", width=640, height=170, labelanchor="n",
                                        text="APNEE",
                                        relief=tkinter.GROOVE)
        frame_apnea_update.place(x=40, y=270)
        # apnea buttons
        has_apnea_label_update = Label(frame_apnea_update, text="APNEE*", justify="center",
                                       font=("Helvetica", 11, "bold"),
                                       cursor="star", fg="#C6E744", bg="#2092B0")
        has_apnea_label_update.place(x=190, y=10)
        has_apnea_yes_update = Checkbutton(frame_apnea_update, text="YES", variable=has_apnea_value_yes_update,
                                           onvalue="YES", offvalue="", bg="#2092B0",
                                           command=lambda: self.handle_apnea_buton_yes(has_apnea_value_yes_update,
                                                                                       has_apnea_value_general_update,
                                                                                       apnea_type_update,
                                                                                       mask_type_update,
                                                                                       compliance_update,
                                                                                       pressure_update,
                                                                                       has_apnea_no_update))
        has_apnea_yes_update.place(x=265, y=10)
        has_apnea_yes_update.deselect()
        has_apnea_no_update = Checkbutton(frame_apnea_update, text="NO", variable=has_apnea_value_no_update,
                                          onvalue="NO", offvalue="", bg="#2092B0",
                                          command=lambda: self.handle_apnea_buton_no(has_apnea_value_no_update,
                                                                                     has_apnea_value_general_update,
                                                                                     apnea_type_update,
                                                                                     apnea_type_value_update,
                                                                                     mask_type_update,
                                                                                     mask_type_value_update,
                                                                                     compliance_update,
                                                                                     pressure_update,
                                                                                     has_apnea_yes_update))
        has_apnea_no_update.place(x=375, y=10)
        has_apnea_no_update.deselect()
        # check what is the value of the apnea
        if has_apnea_value_general_update.get() == "YES":
            has_apnea_yes_update.select()
        else:
            has_apnea_no_update.select()
        # apnea type
        label_apnea_type_update = Label(frame_apnea_update, text="TIP APNEE", justify="center",
                                        font=("Helvetica", 11, "bold"),
                                        cursor="star", fg="#C6E744", bg="#2092B0")
        label_apnea_type_update.place(x=30, y=50)
        apnea_type_update = OptionMenu(frame_apnea_update, apnea_type_value_update, *constants_pacienti.APNEA_TYPE, )
        apnea_type_update.config(bg="#07A52D", font=("Helvetica", 11, "bold"), fg="#DEFFE6", width=16,
                                 )
        apnea_type_update.place(x=120, y=48)
        # mask type
        label_mask_type_update = Label(frame_apnea_update, text="TIP MASCA", justify="center",
                                       font=("Helvetica", 11, "bold"),
                                       cursor="star", fg="#C6E744", bg="#2092B0", )
        label_mask_type_update.place(x=30, y=100)
        mask_type_update = OptionMenu(frame_apnea_update, mask_type_value_update, *constants_pacienti.MASK_TYPE, )
        mask_type_update.config(bg="#07A52D", font=("Helvetica", 11, "bold"), fg="#DEFFE6", width=16,
                                )
        mask_type_update.place(x=120, y=96)
        # compliance
        label_compliance_update = Label(frame_apnea_update, text="COMPLIANTA", justify="center",
                                        font=("Helvetica", 11, "bold"),
                                        cursor="star", fg="#C6E744", bg="#2092B0")
        label_compliance_update.place(x=340, y=50)
        compliance_update = Entry(frame_apnea_update, width=23, justify="center", font=("Helvetica", 9, "bold"),
                                  cursor="target", bg="#D4E2D0", )
        compliance_update.place(x=450, y=50)
        # pressure
        label_pressure_update = Label(frame_apnea_update, text="PRESIUNE", justify="center",
                                      font=("Helvetica", 11, "bold"),
                                      cursor="star", fg="#C6E744", bg="#2092B0")
        label_pressure_update.place(x=340, y=100)
        pressure_update = Entry(frame_apnea_update, width=23, justify="center", font=("Helvetica", 9, "bold"),
                                cursor="target", bg="#D4E2D0", )
        pressure_update.place(x=450, y=100)
        # known diseases
        diseases_label_update = Label(frame_patient_medical_update, text="BOLI CUNOSCUTE*", justify="center",
                                      font=("Helvetica", 11, "bold"),
                                      cursor="star", fg="#C6E744", bg="#2092B0")
        diseases_label_update.place(x=40, y=480)
        has_diseases_yes_update = Checkbutton(frame_patient_medical_update, text="YES",
                                              variable=has_disease_value_yes_update,
                                              onvalue="YES", offvalue="", bg="#2092B0",
                                              command=lambda: self.handle_disease_buton_yes(
                                                  has_disease_value_yes_update,
                                                  has_disease_value_general_update,
                                                  disease_section_update,
                                                  has_diseases_no_update))
        has_diseases_yes_update.place(x=195, y=480)
        has_diseases_yes_update.deselect()
        has_diseases_no_update = Checkbutton(frame_patient_medical_update, text="NO",
                                             variable=has_disease_value_no_update,
                                             onvalue="NO", offvalue="", bg="#2092B0",
                                             command=lambda: self.handle_disease_buton_no(has_disease_value_no_update,
                                                                                          has_disease_value_general_update,
                                                                                          disease_section_update,
                                                                                          has_diseases_yes_update))
        has_diseases_no_update.place(x=250, y=480)
        has_diseases_no_update.deselect()
        # check the value of the disease_general value
        if has_disease_value_general_update.get() == "YES":
            has_diseases_yes_update.select()
        else:
            has_diseases_no_update.select()
        disease_section_update = Text(frame_patient_medical_update, width=46, height=7, font=("Helvetica", 9, "bold"),
                                      cursor="target", bd=4, bg="#C8E6F0", relief=GROOVE, wrap=WORD,
                                      highlightcolor="#907AFB",
                                      highlightbackground="#907AFB", )
        disease_section_update.place(x=330, y=480)
        my_scrollbar_disease_update = Scrollbar(frame_patient_medical_update, orient=tkinter.VERTICAL,
                                                command=disease_section_update.yview, )
        disease_section_update.configure(yscrollcommand=my_scrollbar_disease_update.set, )
        my_scrollbar_disease_update.place(x=660, y=480, height=117)
        # recommendation part
        recommendation_label_update = Label(frame_patient_medical_update, text="RECOMANDARE", justify="center",
                                            font=("Helvetica", 11, "bold"),
                                            cursor="star", fg="#C6E744", bg="#2092B0")
        recommendation_label_update.place(x=40, y=630)
        recommendation_section_update = Text(frame_patient_medical_update, width=65, height=8.3,
                                             font=("Helvetica", 9, "bold"),
                                             cursor="target", bd=4, bg="#C8E6F0", relief=GROOVE, wrap=WORD,
                                             highlightcolor="#907AFB",
                                             highlightbackground="#907AFB")
        recommendation_section_update.place(x=200, y=630)
        my_scrollbar_recommendation_update = Scrollbar(frame_patient_medical_update, orient=tkinter.VERTICAL,
                                                       command=recommendation_section_update.yview, )
        recommendation_section_update.configure(yscrollcommand=my_scrollbar_recommendation_update.set, )
        my_scrollbar_recommendation_update.place(x=660, y=630, height=130)

        # buttons
        ok_button_update = Button(root_update, text="UPDATE", width=20, height=2, fg="#1E2729", bg="#248B48",
                                  font=("Helvetica", 9, "bold"),
                                  command=lambda: self.sql_update(self.table_name, cnp_entry_update.get(),
                                                                  cal_update.get_date(),
                                                                  last_name_entry_update.get(),
                                                                  telephone_number_entry_update.get(),
                                                                  has_insurance_value_yes_update.get(),
                                                                  has_insurance_value_no_update.get(),
                                                                  has_doctor_ticket_value_yes_update.get(),
                                                                  has_doctor_ticket_value_no_update.get(),
                                                                  has_apnea_value_yes_update.get(),
                                                                  has_apnea_value_no_update.get(),
                                                                  has_disease_value_yes_update.get(),
                                                                  has_disease_value_no_update.get())
                                  )
        ok_button_update.place(x=70, y=817)
        cancel_button = Button(root_update, text="CANCEL", width=20, height=2, fg="#1E2729", bg="#E8E7D8",
                               font=("Helvetica", 9, "bold"), command=self.cancel_update)
        cancel_button.place(x=290, y=817)

        '''
        INSERT THE VALUES INTO LABELS
        '''
        first_name_entry_update.insert(0, list_record_entries[0][1])
        last_name_entry_update.insert(0, list_record_entries[0][2])
        cnp_entry_update.insert(0, list_record_entries[0][3])
        telephone_number_entry_update.insert(0, list_record_entries[0][4])
        address_entry_street_update.insert(0, list_record_entries[0][5])
        address_entry_locality_update.insert(0, list_record_entries[0][6])
        ticket_number_update.insert(0, list_record_entries[0][11])
        anamneza_update.insert("1.0", list_record_entries[0][12])
        compliance_update.insert(0, list_record_entries[0][16])
        pressure_update.insert(0, list_record_entries[0][17])
        disease_section_update.insert("1.0", list_record_entries[0][19])
        recommendation_section_update.insert("1.0", list_record_entries[0][20])

        ''''
        CREATE CUSTOM LABELS FOR DATE/NAME/CNP
        '''
        full_name = list_record_entries[0][1] + " " + list_record_entries[0][2]
        name_label_custom = Label(root_update, text=full_name, justify="center",
                                  font=("Comic Sans", 15, "bold italic"),
                                  cursor="star", fg="#E6E785", bg="#2092B0")
        cnp_label_custom = Label(root_update, text=list_record_entries[0][3], justify="center",
                                 font=("Comic Sans", 15, "bold italic"),
                                 cursor="star", fg="#E6E785", bg="#2092B0")
        date_label_custom = Label(root_update, text=list_record_entries[0][0], justify="center",
                                  font=("Comic Sans", 15, "bold italic"),
                                  cursor="star", fg="#E6E785", bg="#2092B0")
        name_label_custom.place(x=70, y=40)
        cnp_label_custom.place(x=70, y=80)
        date_label_custom.place(x=70, y=120)

    def view_edit_records(self, table_name, option, select_date, first_name, last_name, cnp):
        '''MAKE CHECKS'''
        # 1.check button is pressed
        if self.checker_field.check_radiobutton_pressed(option):
            messagebox.showerror("NICI O SELECTIE", "VA ROG SELECTATI O OPTIUNE DE CAUTARE")
            return
        # 2. check if date is selected
        if option == "Data":
            if self.checker_field.check_if_date_selected(select_date):
                messagebox.showerror("DATA NESELECTATA", "VA ROG SELECTATI DATA")
                return
        # 3. check last and first name
        if option == "Nume":
            option_error, message_error = self.checker_field.check_if_first_last_name_entered(first_name, last_name)
            if option_error == 1:
                messagebox.showerror("CAMPURI NECOMPLETATE", message=message_error)
                return
            elif option_error == 2:
                messagebox.showerror("NUME NECOMPLETAT", message=message_error)
                return
            elif option_error == 3:
                messagebox.showerror("PRENUME NECOMPLETAT", message=message_error)
                return
        # 4. check cnp
        if option == "Cnp":
            if self.checker_field.check_cnp_complete(cnp):
                messagebox.showerror("CNP NECOMPLETAT", "VA ROG COMPLETATI CNP-UL")
                return
            cnp_message_error, cnp_option_error = self.checker_field.get_cnp_errors(cnp)
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
        database = os.path.join(constants_pacienti.DATABASE_FOLDER, constants_pacienti.NAME_DATABASE)
        connection = sqlite3.connect(database)
        my_cursor = connection.cursor()
        # check selected option to see what queries to execute
        if option == "Data":
            my_cursor.execute("""SELECT oid, *FROM """ + table_name + """ WHERE DATA =:data""",
                              # dummy dictionary
                              {
                                  "data": select_date
                              })
        elif option == "Nume":
            my_cursor.execute(
                """
            SELECT oid, *FROM """ + table_name + """ WHERE PRENUME =:first_name AND NUME =:last_name""",
                # dummy dictionary
                {
                    "first_name": first_name.upper(),
                    "last_name": last_name.upper()
                })
        elif option == "Cnp":
            my_cursor.execute("""
            SELECT oid, *FROM """ + table_name + """ WHERE CNP =:cnp_value""",
                              # dummy dictionary
                              {
                                  "cnp_value": cnp
                              })
        # get list of results and check if we have such records
        list_results = my_cursor.fetchall()
        if len(list_results) == 0:
            messagebox.showerror("PACIENT NEEXISTENT", "CAUTAREA NU A PRODUS NICI UN REZULTAT CU ACESTE CONDITII")
            return
        '''CREATE THE GUI WITH THE TREEVIEW OF RECORDS'''
        root_edit.destroy()
        global root_edit_treeview
        global tree_patients_edit
        root_edit_treeview = Tk()
        root_edit_treeview.title("EDIT/UPDATE")
        image_ico = os.path.join(self.pictures_folder, constants_pacienti.PICTURE_FOLDER,
                                 constants_pacienti.SOMN_ICO_IMAGE)
        root_edit_treeview.iconbitmap(image_ico)
        root_edit_treeview.geometry("850x500")
        root_edit_treeview["bg"] = "#2092B0"
        root_edit_treeview.resizable(NO, NO)
        root_edit_treeview.protocol("WM_DELETE_WINDOW", self.cancel_x_button)
        # treeview creation
        frame_treeview = LabelFrame(root_edit_treeview, fg="#EEEBF3", bg="#2092B0", font=("Helvetica", 20, "bold"),
                                    bd=5,
                                    cursor="target", width=800, height=425, labelanchor="n",
                                    text="VIZUALIZARE/EDITARE PACIENT",
                                    relief=tkinter.GROOVE)
        frame_treeview.grid(padx=25, pady=10, row=0, column=0, )  # put it in the middle
        frame_treeview.grid_rowconfigure(0, weight=1)
        frame_treeview.grid_columnconfigure(0, weight=1)
        # create tree to show footballers
        columns = ("ID", "DATA", "PRENUME", "NUME", "CNP", "APNEE", "TIP_APNEE", "PRESIUNE")
        tree_patients_edit = ttk.Treeview(frame_treeview, show='headings', columns=columns, height=15, )
        # ADD THE COLUMNS
        # define the headings
        tree_patients_edit.heading(0, text="ID", anchor=tkinter.W)
        tree_patients_edit.heading(1, text="DATA", anchor=tkinter.W)
        tree_patients_edit.heading(2, text="PRENUME", anchor=tkinter.W)
        tree_patients_edit.heading(3, text="NUME", anchor=tkinter.W)
        tree_patients_edit.heading(4, text="CNP", anchor=tkinter.W)
        tree_patients_edit.heading(5, text="APNEE", anchor=tkinter.W)
        tree_patients_edit.heading(6, text="TIP_APNEE", anchor=tkinter.W)
        tree_patients_edit.heading(7, text="PRESIUNE", anchor=tkinter.W)
        # redefine column dimensions
        tree_patients_edit.column("ID", width=25, )
        tree_patients_edit.column("DATA", width=75)
        tree_patients_edit.column("PRENUME", width=125, stretch=NO)
        tree_patients_edit.column("NUME", width=125, stretch=NO)
        tree_patients_edit.column("CNP", width=100, stretch=NO)
        tree_patients_edit.column("APNEE", width=50, stretch=NO)
        tree_patients_edit.column("TIP_APNEE", width=100, stretch=NO)
        tree_patients_edit.column("PRESIUNE", width=125, stretch=NO)
        tree_patients_edit.tag_configure("orow")
        # create a custom style
        style = ttk.Style(root_edit_treeview)
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="#D4EE77", foreground="#C7651D")
        # populate the list
        for record in list_results:
            record_update = list()
            record_update.append(str(record[0]))
            record_update.append(record[1])
            record_update.append(record[2])
            record_update.append(record[3])
            record_update.append(record[4])
            record_update.append(record[14])
            record_update.append(record[15])
            record_update.append(record[18])
            record_update_tuple = tuple(record_update)
            tree_patients_edit.insert('', tkinter.END, values=record_update_tuple)
        # put the treeview on the frame
        tree_patients_edit.place(x=20, y=10)
        # create a scrollbar
        my_scrollbar = Scrollbar(frame_treeview, orient=tkinter.VERTICAL, command=tree_patients_edit.yview)
        tree_patients_edit.configure(yscrollcommand=my_scrollbar.set)
        my_scrollbar.place(x=748, y=11, height=328)
        # add button for cancel
        cancel_button = Button(frame_treeview, text="CANCEL", width=40, height=2, fg="#1E2729", bg="#E8E7D8",
                               font=("Helvetica", 9, "bold"), command=self.cancel_treeview_edit)
        cancel_button.place(x=250, y=343)
        # add bind function to treeview
        # todo open_entry_button
        tree_patients_edit.bind("<Double-Button-1>", lambda event: self.open_entry(self.table_name, event))

    def cancel_form_edit(self):
        root_edit.destroy()
        self.create_main_gui()

    def create_edit_gui(self):
        global root_edit
        app_menu.destroy()
        # global variables
        global radio_button_date_edit
        global radio_button_name_edit
        global radio_button_cnp_edit
        global calendar_entry_edit
        global first_name_entry_edit
        global last_name_entry_edit
        global cnp_entry_edit
        global selection_option_edit

        root_edit = Tk()
        root_edit.title("VIEW/UPDATE")
        image_ico = os.path.join(self.pictures_folder, constants_pacienti.PICTURE_FOLDER,
                                 constants_pacienti.SOMN_ICO_IMAGE)
        root_edit.iconbitmap(image_ico)
        root_edit.geometry("1020x330")
        root_edit["bg"] = "#2092B0"
        root_edit.resizable(NO, NO)
        root_edit.protocol("WM_DELETE_WINDOW", self.cancel_x_button)
        # stringvars
        selection_option_edit = StringVar()
        # put values for radiobuttons
        selection_option1_edit = "Data"
        selection_option2_edit = "Nume"
        selection_option3_edit = "Cnp"
        frame_title = LabelFrame(root_edit, fg="#EEEBF3", bg="#2092B0", font=("Helvetica", 20, "bold"), bd=5,
                                 cursor="target", width=920, height=300, labelanchor="n", text="EDITARE PACIENT",
                                 relief=tkinter.GROOVE)
        frame_title.grid(padx=10, pady=10, row=0, column=0, )  # put it in the middle
        frame_title.grid_rowconfigure(0, weight=1)
        frame_title.grid_columnconfigure(0, weight=1)
        # add frame for date
        frame_date = LabelFrame(frame_title, fg="#EEEBF3", bg="#2092B0", font=("Helvetica", 15, "bold"),
                                bd=5,
                                cursor="target", width=230, height=200, labelanchor="n",
                                text="SELECTIE DATA",
                                relief=tkinter.GROOVE)
        frame_date.place(x=30, y=10)
        calendar_entry_edit = DateEntry(frame_date, selectmode='day', date_pattern="DD-MM-YYYY", bd=2,
                                        headersbackground="#EBFE8A",
                                        headersforeground="#1E1F1C", selectbackground="#209DBF",
                                        selectforeground="#F26B18",
                                        weekendbackground="#8D7B80", font=("Helvetica", 9, "bold"), bg="#9EEB8D")
        calendar_entry_edit.state(["disabled"])
        calendar_entry_edit.place(x=80, y=20)
        calendar_entry_label = Label(frame_date, text="DATA", justify="center",
                                     font=("Helvetica", 11, "bold"),
                                     cursor="star", fg="#B9DBDA", bg="#2092B0")
        calendar_entry_label.place(x=20, y=20)
        # add frame for first and last name
        frame_first_last_name = LabelFrame(frame_title, fg="#EEEBF3", bg="#2092B0", font=("Helvetica", 15, "bold"),
                                           bd=5,
                                           cursor="target", width=230, height=200, labelanchor="n",
                                           text="SELECTIE NUME",
                                           relief=tkinter.GROOVE)
        frame_first_last_name.place(x=280, y=10)
        first_name_entry_edit = Entry(frame_first_last_name, width=18, justify="center",
                                      font=("Helvetica", 8, "bold"),
                                      cursor="target",
                                      bg="#9EEB8D", state=tkinter.DISABLED)
        first_name_entry_edit.place(x=100, y=40)
        first_name_label = Label(frame_first_last_name, text="PRENUME", justify="center",
                                 font=("Helvetica", 11, "bold"),
                                 cursor="star", fg="#B9DBDA", bg="#2092B0")
        first_name_label.place(x=5, y=40)
        last_name_entry_edit = Entry(frame_first_last_name, width=18, justify="center",
                                     font=("Helvetica", 8, "bold"),
                                     cursor="target",
                                     bg="#9EEB8D", state=tkinter.DISABLED)
        last_name_entry_edit.place(x=100, y=100)
        last_name_label = Label(frame_first_last_name, text="NUME", justify="center",
                                font=("Helvetica", 11, "bold"),
                                cursor="star", fg="#B9DBDA", bg="#2092B0")
        last_name_label.place(x=5, y=100)
        # add frame for cnp
        frame_cnp = LabelFrame(frame_title, fg="#EEEBF3", bg="#2092B0", font=("Helvetica", 15, "bold"),
                               bd=5,
                               cursor="target", width=230, height=200, labelanchor="n",
                               text="SELECTIE CNP",
                               relief=tkinter.GROOVE)
        frame_cnp.place(x=530, y=10)
        cnp_entry_edit = Entry(frame_cnp, width=20, justify="center",
                               font=("Helvetica", 8, "bold"),
                               cursor="target",
                               bg="#9EEB8D", state=tkinter.DISABLED)
        cnp_entry_edit.place(x=80, y=60)
        cnp_label = Label(frame_cnp, text="CNP", justify="center",
                          font=("Helvetica", 11, "bold"),
                          cursor="star", fg="#B9DBDA", bg="#2092B0")
        cnp_label.place(x=5, y=60)
        # create frame for checkbuttons
        check_frame = LabelFrame(frame_title, fg="#EEEBF3", bg="#2092B0", font=("Helvetica", 15, "bold"),
                                 bd=5,
                                 cursor="target", width=100, height=200, labelanchor="n",
                                 text="CHECK",
                                 relief=tkinter.GROOVE)
        check_frame.place(x=780, y=10)
        # put radiobuttons
        radio_button_date_edit = Radiobutton(check_frame, text="DATE", variable=selection_option_edit,
                                             value=selection_option1_edit,
                                             bd=5, font=("Helvetica", 11, "bold"),
                                             bg="#2092B0", fg="#EEEBF3", selectcolor="black",
                                             command=lambda: self.handle_radio_button_date(selection_option1_edit,
                                                                                           selection_option_edit.get(),
                                                                                           calendar_entry_edit,
                                                                                           first_name_entry_edit,
                                                                                           last_name_entry_edit,
                                                                                           cnp_entry_edit))
        radio_button_date_edit.place(x=5, y=20)
        radio_button_name_edit = Radiobutton(check_frame, text="NUME", variable=selection_option_edit,
                                             value=selection_option2_edit,
                                             bd=5, font=("Helvetica", 11, "bold"),
                                             bg="#2092B0", fg="#EEEBF3", selectcolor='black',
                                             command=lambda: self.handle_radio_button_name(selection_option2_edit,
                                                                                           selection_option_edit.get(),
                                                                                           first_name_entry_edit,
                                                                                           last_name_entry_edit,
                                                                                           calendar_entry_edit,
                                                                                           cnp_entry_edit))

        radio_button_name_edit.place(x=5, y=70)
        radio_button_cnp_edit = Radiobutton(check_frame, text="CNP", variable=selection_option_edit,
                                            value=selection_option3_edit,
                                            bd=5, font=("Helvetica", 11, "bold"),
                                            bg="#2092B0", fg="#EEEBF3", selectcolor='black',
                                            command=lambda: self.handle_radio_button_name(selection_option3_edit,
                                                                                          selection_option_edit.get(),
                                                                                          cnp_entry_edit,
                                                                                          calendar_entry_edit,
                                                                                          first_name_entry_edit,
                                                                                          last_name_entry_edit))
        radio_button_cnp_edit.place(x=5, y=120)
        # put ok and cancel buttons
        ok_button = Button(frame_title, text="VIZUALIZARE", width=30, height=2, fg="#1E2729", bg="#248B48",
                           font=("Helvetica", 9, "bold"),
                           command=lambda: self.view_edit_records(self.table_name, selection_option_edit.get(),
                                                                  calendar_entry_edit.get(),
                                                                  first_name_entry_edit.get(),
                                                                  last_name_entry_edit.get(),
                                                                  cnp_entry_edit.get()))
        cancel_button = Button(frame_title, text="CANCEL", width=30, height=2, fg="#1E2729", bg="#E8E7D8",
                               font=("Helvetica", 9, "bold"), command=self.cancel_form_edit)
        ok_button.place(x=150, y=215)
        cancel_button.place(x=500, y=215)

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
        app_menu.resizable(NO, NO)
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
                               relief=tkinter.GROOVE, command=self.create_edit_gui)
        delete_button = Button(app_menu, fg="#EEEBF3", bg="#BC6678", font=("Helvetica", 9, "bold"), bd=4,
                               cursor="target", width=20, height=2, justify="center", text="STERGERE",
                               relief=tkinter.GROOVE, command=self.create_delete_gui)
        convert_excel_all = Button(app_menu, fg="#EEEBF3", bg="#F36D1C", font=("Helvetica", 9, "bold"), bd=4,
                                   cursor="target", width=20, height=2, justify="center",
                                   text="TRANSFER EXCEL DATE ",
                                   relief=tkinter.GROOVE, command=lambda: self.writer.write_to_excel(self.table_name))

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
