from gui_app import GuiApp
from tkinter import *
from tkcalendar import Calendar
import os


def run_app_programari():
    app_runner = GuiApp()
    app_runner.create_main_gui()


if __name__ == "__main__":
   run_app_programari()
   # root = Tk()
   #
   # # Set geometry
   # root.geometry("400x400")
   #
   # # Add Calendar
   # cal = Calendar(root, selectmode='day', date_pattern="DD-MM-YYYY")
   # cal.pack(pady=20)
   #
   #
   # def grad_date():
   #     date.config(text="Selected Date is: " + cal.get_date())
   #     print(type(cal.get_date()))
   #
   #
   # # Add Button and Label
   # Button(root, text="Get Date",
   #        command=grad_date).pack(pady=20)
   #
   # date = Label(root, text="")
   # date.pack(pady=20)
   #
   # # Execute Tkinter
   # root.mainloop()

