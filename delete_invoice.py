from tkinter import *
from tkinter import ttk
import tkinter as tk
from sql_working import *
import os


def delete_invoice():
    top = Toplevel()
    top.title('Delete Invoices')
    top.iconbitmap('icon.ico')
    top.geometry("680x500")
    top.resizable(0, 0)

    def delete_and_destroy(x):
        company_name = ""
        try:
            f = open("enter_company_name.ini", "r")
            for y in f:
                name = str(y)
                if "Name" in name:
                    company_name = name.split(" = ")[1] + " - "
            f.close()
        except FileNotFoundError:
            company_name = "RUBICK-.org"


        customer_name = get_customer_name_from_invoices(x)
        delete_location = os.path.expanduser('~/Documents/' + company_name + 'Invoices/' + customer_name + ' (' + str(x) + ').pdf')
        os.remove(delete_location)
        delete_invoice_from_data(x)

        top.destroy()

    empty = []
    for i in get_customers_from_invoices():
        if i[2] != "Item Received Back":
            empty.append(i)

    if len(empty) > 0:
        frame2 = LabelFrame(top, text="Invoices", padx=10, pady=10)
        frame2.grid(row=1, column=1, padx=10, pady=10)

        frame2.rowconfigure(0, weight=1)
        frame2.columnconfigure(0, weight=1)

        scroll_size = 0

        for item in get_customers_from_invoices():
            if item[2] != "Item Received Back":
                scroll_size += 1

        set_scroll_size = scroll_size * 30

        canvas = tk.Canvas(
            frame2, scrollregion="0 0 2000 " + str(set_scroll_size), width=620, height=430)
        canvas.grid(row=0, column=0, sticky=tk.NSEW)

        scroll = tk.Scrollbar(frame2, orient=tk.VERTICAL, command=canvas.yview)
        scroll.grid(row=0, column=1, sticky=tk.NS)
        canvas.config(yscrollcommand=scroll.set)

        frame = tk.LabelFrame(frame2, labelanchor=tk.N)


        row = 1
        for item in get_customers_from_invoices():
            if item[2] != "Item Received Back":
                invoice_number_label = Label(frame, text="Invoice Number: " + str(item[0]), font=("Roboto", 12))
                invoice_number_label.grid(row=row, column=1, padx=7, pady=2, sticky='w')
                date_label = Label(frame, text="Date: " + str(item[3]), font=("Roboto", 12))
                date_label.grid(row=row, column=2, padx=7, pady=2)
                customer_name_label = Label(frame, text="Name: " + str(item[1]), font=("Roboto", 12))
                customer_name_label.grid(row=row, column=3, padx=7, pady=2, sticky='w')

                delete_invoice_button = Button(frame, text="DELETE", font=("Arial", 9, 'bold'), justify='center',
                                              cursor="hand1", command=lambda x=str(item[0]): delete_and_destroy(x))
                delete_invoice_button.configure(foreground="white")
                delete_invoice_button.configure(bg="RED")
                delete_invoice_button.grid(row=row, column=4, padx=7, pady=2)

                row += 1

        item = canvas.create_window((2, 2), anchor=tk.NW, window=frame)
    else:
        empty_label = Label(top, text="*** There Are no Invoices To Delete ***", font=("Roboto", 20))
        empty_label.place(x=75, y=150)
