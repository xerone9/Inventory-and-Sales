from tkinter import *
from tkinter import ttk
from sql_working import *


def receive_back_inventory():
    top = Toplevel()
    top.title('Receive Back Item')
    top.iconbitmap('icon.ico')
    top.geometry("500x450")

    def destroy_option_menu():
        try:
            option2.destroy()
        except NameError:
            pass


    def receive_back():
        global invoice_no_is
        received_back_inventory(invoice_no_is, str(variable.get()))
        top.destroy()




    def get_sub_invoice(x):
        select_invoice_label.config(text="Invoice Number: " + str(variable2.get()))
        destroy_option_menu()
        get_sub_invoice_no = str(select_invoice_label.cget("text")).split(": ")
        global invoice_no_is
        invoice_no_is = str(get_sub_invoice_no[1])
        sub_date = ""
        for value in get_Item_Given_of_invoice_no_from_inventory_ledger(str(get_sub_invoice_no[1])):
            sub_date = value[2]
        date.config(text="Dated: " + str(sub_date))
        date.grid(row=0, column=3, padx=7)
        inventory_stock_given.delete(*inventory_stock_given.get_children())

        item_given = get_Item_Given_of_invoice_no_from_inventory_ledger(str(get_sub_invoice_no[1]))

        count = 0

        for items in item_given:
            inventory_stock_given.insert(parent="", index='end', iid=count, text=count + 1,
                                   values=(items[2], items[0], items[1]))
            count += 1



    def get_invoices(x):
        global variable2
        variable2 = StringVar(top)
        invoices = []
        for invoice in get_Item_Given_Invoices_of_customer(str(variable.get())):
            invoices.append(invoice[0])
        variable2.set("Select Invoice")

        if len(invoices) > 1:
            global option2
            option2 = OptionMenu(frame, variable2, *invoices, command=get_sub_invoice)
            select_invoice_label.config(text="Invoice Number:")
            option2.configure(cursor="hand1")
            option2.grid(row=0, column=3, padx=7)
            date.grid_remove()
        else:
            destroy_option_menu()
            invoice_no = 0
            get_date = ""
            for item in get_Item_Given_Invoices_of_customer(str(variable.get())):
                invoice_no = item[0]
                get_date = item[1]
            select_invoice_label.config(text="Invoice Number: " + str(invoice_no))
            global invoice_no_is
            invoice_no_is = str(invoice_no)
            date.config(text="Dated: " + str(get_date))
            date.grid(row=0, column=3, padx=7)
            inventory_stock_given.delete(*inventory_stock_given.get_children())

            item_given = get_Item_Given_of_invoice_no_from_inventory_ledger(str(invoice_no))

            count = 0

            for items in item_given:
                inventory_stock_given.insert(parent="", index='end', iid=count, text=count + 1,
                                             values=(items[2], items[0], items[1]))
                count += 1


    frame = LabelFrame(top, text="Orders", padx=10, pady=10)
    frame.place(x=15, y=15)

    variable = StringVar(top)
    customers = []
    for types in get_Item_Given_Invoices():
        if types[3] not in customers:
            customers.append(types[3])
    variable.set("Select Cusotmer")

    try:
        option = OptionMenu(frame, variable, *customers, command=get_invoices)
        option.configure(cursor="hand1")
        option.grid(row=0, column=1, padx=7)

        select_invoice_label = Label(frame, text="Invoice Number:", font=("Roboto", 10))
        select_invoice_label.grid(row=0, column=2, padx=7)

        date = Label(frame, text="Invoice Number:", font=("Roboto", 10))
        date.grid_remove()

        frame2 = LabelFrame(top, text="Items Given", padx=10, pady=10)
        frame2.place(x=30, y=100)


        inventory_stock_given = ttk.Treeview(frame2, height=10, style="mystyle.Treeview")
        inventory_stock_given['columns'] = ("Item Date", "Item Name", "Item Quantity")
        inventory_stock_given.column("#0", minwidth=25, width=40)
        inventory_stock_given.column("Item Date", anchor=W, width=100)
        inventory_stock_given.column("Item Name", anchor=W, width=100)
        inventory_stock_given.column("Item Quantity", anchor=CENTER, width=120)

        inventory_stock_given.heading("#0", text="S. No", anchor=W)
        inventory_stock_given.heading("Item Date", text="Item Date", anchor=W)
        inventory_stock_given.heading("Item Name", text="Item Name", anchor=W)
        inventory_stock_given.heading("Item Quantity", text="Item Quantity", anchor=CENTER)

        inventory_stock_given.pack(side='left', fill='y')

        scrollbar = Scrollbar(frame2, orient="vertical", command=inventory_stock_given.yview)
        scrollbar.pack(side="right", fill="y")
        inventory_stock_given.configure(yscrollcommand=scrollbar.set)

        receive_back_button = Button(top, text="RECEIVE BACK", font=("Arial", 10, 'bold'), justify='center', cursor="hand1", command=receive_back)
        receive_back_button.configure(foreground="black")
        receive_back_button.configure(bg="light grey")
        receive_back_button.pack(side = "bottom", pady=35)

        global invoice_no_is
        invoice_no_is = 0
    except TypeError:
        select_invoice_label = Label(top, text="*** NOTHING TO RECEIVE BACK ***", font=("helvetica", 20))
        select_invoice_label.place(x=20, rely=0.3)





