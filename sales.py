from tkinter import *
import calendar
from babel.dates import format_date, parse_date, get_day_names, get_month_names
from babel.numbers import *
from tkcalendar import *
import datetime

# Reports
from sales_report import sales_report


def sales():
    top = Toplevel()
    top.title('Sales')
    top.iconbitmap('icon.ico')
    top.geometry("430x120")
    top.resizable(0,0)

    def from_date(event):
        global from_date_is
        w = event.widget
        date = w.get_date()
        from_date_is = '{}'.format(date)

    def to_date(event):
        global to_date_is
        w = event.widget
        date = w.get_date()
        to_date_is = '{}'.format(date)


    def print_sales_report():
        global from_date_is
        global to_date_is

        date_complete = str(datetime.datetime.now()).split(".")
        date_and_time = date_complete[0].split(" ")
        date = date_and_time[0]

        if from_date_is == "":
            from_date_is = date

        if to_date_is == "":
            to_date_is = date

        sales_report(from_date_is, to_date_is)


    from_label = Label(top, text="From Date:", font=("Roboto", 13))
    from_label.grid(row=0, column=0, padx=10, pady=10)

    From_Date = DateEntry(top)
    From_Date.grid(row=0, column=1, padx=10, pady=10)
    From_Date.bind("<<DateEntrySelected>>", from_date)

    to_label = Label(top, text="To Date:", font=("Roboto", 13))
    to_label.grid(row=0, column=2, padx=10, pady=10)

    To_Date = DateEntry(top)
    To_Date.grid(row=0, column=3, padx=10, pady=10)
    To_Date.bind("<<DateEntrySelected>>", to_date)

    global from_date_is
    from_date_is = ""

    global to_date_is
    to_date_is = ""

    generate_sales_report_button = Button(top, text="SALES REPORT", font=("Arial", 15, 'bold'), justify='center',
                                     cursor="hand1", command=print_sales_report)
    generate_sales_report_button.configure(foreground="white")
    generate_sales_report_button.configure(bg="black")
    generate_sales_report_button.grid(row=1, column=1, columnspan=2, padx=10, pady=10)