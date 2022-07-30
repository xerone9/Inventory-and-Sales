from tkinter import *
import tkinter as tk
from sql_working import *
from temporary_invoice_print_report import temporary_invioce_print


def viwe_invoice():
    top = Toplevel()
    top.title('View Invoices')
    top.iconbitmap('icon.ico')
    top.geometry("680x600")
    top.resizable(0, 0)


    def get_invoices(x):
        global frame2
        frame2.destroy()

        frame2 = LabelFrame(top, text="Invoices", padx=10, pady=10)
        frame2.grid(row=1, column=1, padx=10)

        frame2.rowconfigure(0, weight=1)
        frame2.columnconfigure(0, weight=1)

        scroll_size = 0

        for item in get_invoices_of_customers(str(variable.get())):
            scroll_size += 1

        set_scroll_size = scroll_size * 28

        # scrollregion is also essential when using scrollbars
        canvas = tk.Canvas(
            frame2, scrollregion="0 0 2000 " + str(set_scroll_size), width=620, height=430)
        canvas.grid(row=0, column=0, sticky=tk.NSEW)

        scroll = tk.Scrollbar(frame2, orient=tk.VERTICAL, command=canvas.yview)
        scroll.grid(row=0, column=1, sticky=tk.NS)
        canvas.config(yscrollcommand=scroll.set)

        # I've used a labelframe instead of frame so button are neatly collected and named
        frame = tk.LabelFrame(frame2, labelanchor=tk.N)

        # Note I've placed buttons in frame


        row = 1
        for item in get_invoices_of_customers(str(variable.get())):
            invoice_number_label = Label(frame, text="Invoice Number: " + str(item[0]), font=("Roboto", 12))
            invoice_number_label.grid(row=row, column=1, padx=7, pady=2, sticky='w')
            date_label = Label(frame, text="Date: " + str(item[1]), font=("Roboto", 12))
            date_label.grid(row=row, column=2, padx=7, pady=2)
            customer_name_label = Label(frame, text="Name: " + str(item[2]), font=("Roboto", 12))
            customer_name_label.grid(row=row, column=3, padx=7, pady=2)

            print_invoice_button = Button(frame, text="PRINT", font=("Arial", 9, 'bold'), justify='center',
                                          cursor="hand1", command=lambda x=str(item[0]): temporary_invioce_print(x))
            print_invoice_button.configure(foreground="white")
            print_invoice_button.configure(bg="blue")
            print_invoice_button.grid(row=row, column=4, padx=7, pady=2)



            row += 1

        # Frame is now inserted into canvas via create_window method
        item = canvas.create_window((2, 2), anchor=tk.NW, window=frame)







            # select_invoice_label = Label(frame2, text="Invoice Number:", font=("Roboto", 10))
            # select_invoice_label.grid(row=0, column=2, padx=7)



    try:
        frame = LabelFrame(top, text="Customers", padx=10, pady=10)
        frame.grid(row=0, column=1, padx=10, pady=10)

        variable = StringVar(top)
        customers = []
        for types in get_customers_from_invoices():
            if types[1] not in customers:
                customers.append(types[1])
        variable.set("Select Cusotmer")

        option = OptionMenu(frame, variable, *customers, command=get_invoices)
        option.configure(cursor="hand1")
        option.grid(row=0, column=1, padx=7)


        global frame2
        frame2 = LabelFrame(top, text="Invoices", padx=10, pady=10)
        frame2.grid(row=1, column=1, padx=10)

    except TypeError:
        empty_label = Label(top, text="*** There Are No Invoices ****", font=("Roboto", 15))
        empty_label.place(x=200, y=180)








