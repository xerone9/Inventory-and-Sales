from tkinter import *
import tkinter as tk
from sql_working import *
from temporary_invoice_print_report import temporary_invioce_print


def items_to_deliver():
    top = Toplevel()
    top.title('Items To Be Delivered Today')
    top.iconbitmap('icon.ico')
    top.geometry("560x600")
    top.resizable(0, 0)

    empty = []

    for i in items_to_be_deliverd_today():
        empty.append(i)

    if len(empty) > 0:
        datex = str(datetime.datetime.now()).split(".")
        date_and_time = str(datex[0]).split(" ")
        date = date_and_time[0]

        frame = LabelFrame(top, text="Items To Be Deliverd Today", padx=10, pady=10)
        frame.grid(row=0, column=1, padx=10, pady=10)

        delivery_date_label = Label(frame, text="Delivery Date: " + str(date), font=("Roboto", 15))
        delivery_date_label.grid(row=0, column=1, padx=7)

        frame2 = LabelFrame(top, text="Invoices", padx=10, pady=10)
        frame2.grid(row=1, column=1, padx=10, pady=10)

        frame2.rowconfigure(0, weight=1)
        frame2.columnconfigure(0, weight=1)

        scroll_size = 0

        for item in items_to_be_deliverd_today():
            scroll_size += 1

        set_scroll_size = scroll_size * 30

        canvas = tk.Canvas(
            frame2, scrollregion="0 0 2000 " + str(set_scroll_size), width=500, height=430)
        canvas.grid(row=0, column=0, sticky=tk.NSEW)

        scroll = tk.Scrollbar(frame2, orient=tk.VERTICAL, command=canvas.yview)
        scroll.grid(row=0, column=1, sticky=tk.NS)
        canvas.config(yscrollcommand=scroll.set)

        frame = tk.LabelFrame(frame2, labelanchor=tk.N)

        row = 1
        for item in items_to_be_deliverd_today():
            invoice_number_label = Label(frame, text="Invoice Number: " + str(item[0]), font=("Roboto", 12))
            invoice_number_label.grid(row=row, column=1, padx=7, pady=2, sticky='w')
            customer_name_label = Label(frame, text="Name: " + str(item[1]), font=("Roboto", 12))
            customer_name_label.grid(row=row, column=3, padx=7, pady=2, sticky='w')
            print_invoice_button = Button(frame, text="PRINT", font=("Arial", 9, 'bold'), justify='center',
                                          cursor="hand1", command=lambda x=str(item[0]): temporary_invioce_print(x))
            print_invoice_button.configure(foreground="white")
            print_invoice_button.configure(bg="blue")
            print_invoice_button.grid(row=row, column=4, padx=7, pady=2)

            row += 1

        # Frame is now inserted into canvas via create_window method
        item = canvas.create_window((2, 2), anchor=tk.NW, window=frame)
    else:
        empty_label = Label(top, text="*** No Items To Deliver Today ***", font=("Roboto", 15))
        empty_label.place(x=120, y=120)

