from tkinter import *
from sql_working import *
import datetime
from generate_invoice_report import generate_invioce_report
from tkinter import ttk
from tkcalendar import *


def generate_invoice():
    def splash_screen(error):
        splash_root = Toplevel()
        splash_root.title('Error')
        splash_root.iconbitmap('icon.ico')
        splash_root.geometry("750x100")
        splash_root.resizable(0, 0)
        error = Label(splash_root, text=str(error), padx=10, pady=10, fg="red", font=("Roboto", 15))
        error.place(x=10, y=10)


    top = Toplevel()
    top.title('Generate Invoice')
    top.iconbitmap('icon.ico')
    top.geometry("700x700")
    top.resizable(0, 0)

    def getdata():
        global items_cart
        global total_label
        x = inventory_stock.selection()
        y = inventory_stock.item(x)['values']
        delete_value = ""
        for items in y:
            delete_value += str(items) + "*"

        removing_total = str(delete_value).split("*")
        actual_values = removing_total[0] + "*" + removing_total[1] + "*" + removing_total[3] + "*" + removing_total[
            2] + "*" + removing_total[4]
        if actual_values in items_cart:
            items_cart.remove(actual_values)

            inventory_stock.delete(*inventory_stock.get_children())
            count = 0
            total = 0

            for items in items_cart:
                item = str(items).split("*")
                current_total = int(item[2]) * int(item[3]) * int(item[4])
                total += int(item[2]) * int(item[3]) * int(item[4])
                inventory_stock.insert(parent="", index='end', iid=count, text=count + 1,
                                       values=(str(item[0]), str(item[1]), str(item[2]), str(item[3]), str(item[4]),
                                               str(current_total)))
                count += 1

            total_label.config(text="Rs. " + "{:,}".format(total))

        if len(items_cart) < 1:
            generate_invoice_button.place_forget()
            delete_items_button.place_forget()

            customer_name.grid(row=0, column=1, sticky='w', columnspan=3, padx=0)
            customer_contact_no.grid(row=1, column=1, sticky='w', padx=0)
            customer_nic_no.grid(row=1, column=3, sticky='w')
            delivery_date_is.grid(row=2, column=1, sticky='w')
            no_days.grid(row=2, column=3, sticky='w')
            delivery_address.grid(row=3, column=1, columnspan=3, sticky='w')

            customer_name_lock_label.grid_remove()
            customer_contact_no_lock_label.grid_remove()
            customer_nic_no_lock_label.grid_remove()
            delivery_date_lock_label.grid_remove()
            no_days_lock_label.grid_remove()
            delivery_address_lock_label.grid_remove()

    def from_date(event):
        w = event.widget
        date = w.get_date()
        global the_delivery_date
        the_delivery_date = '{}'.format(date)

    def print_invoice():
        datex = str(datetime.datetime.now()).split(".")
        date_and_time = str(datex[0]).split(" ")
        date = date_and_time[0]
        global items_cart
        for item in items_cart:
            items = item.split("*")
            debit_entry_in_inventory_status(str(get_inventory_id(items[1])), str(items[2]), str(customer_name.get()),
                                            str(int(get_last_invoice_No()) + 1))
            try:
                delivery_date = str(the_delivery_date)
            except NameError:
                delivery_date = date
            entry_in_inventory_ledger(str(int(get_last_invoice_No()) + 1), customer_name.get(),
                                      customer_contact_no.get(), str(delivery_date), delivery_address.get(),
                                      str(get_inventory_id(items[1])), str(items[2]), str(items[3]),
                                      customer_nic_no.get(), no_days.get())

        if len(list) < 1:
            entry_in_invoices(customer_name.get(), str(discount.get()))
            list.append(customer_name.get())
        else:
            pass
        store_discount_on_invoice(str(int(get_last_invoice_No()) + 1), discount.get())
        generate_invioce_report(str(get_last_invoice_No()))
        top.destroy()

    def send_to_invoices_table():
        if len(str(customer_name.get())) > 0 and len(str(customer_contact_no.get())) > 0 and len(
                str(customer_nic_no.get())) > 0 and len(str(no_days.get())) > 0 and len(
                str(delivery_address.get())) > 0 and len(str(enter_quantity.get())) > 0:
            if (int(current_quantity) - int(enter_quantity.get())) < 0:
                error = "Entered Quantity is Greater The Available Quantity Please Check"
                splash_screen(error)
            else:
                global the_delivery_date
                date_complete = str(datetime.datetime.now()).split(".")
                date_and_time = date_complete[0].split(" ")
                date = date_and_time[0]
                try:
                    delivery_date = str(the_delivery_date)
                except NameError:
                    delivery_date = date

                global items_cart
                item_id = get_inventory_id(str(variable2.get()))
                item_rate = get_inventory_rate(str(item_id))
                enter_quantity_label.config(fg="black")
                no_days_label.config(fg="black")
                try:
                    int(enter_quantity.get())
                    int(no_days.get())
                    items_cart.append(
                        str(get_inventory_type(str(item_id))) + "*" + str(get_inventory_name(str(item_id))) + "*" + str(
                            enter_quantity.get()) + "*" + str(item_rate) + "*" + str(no_days.get()))
                except ValueError:
                    pass
                try:
                    int(enter_quantity.get())
                except ValueError:
                    enter_quantity_label.config(fg="red")

                try:
                    int(no_days.get())
                except ValueError:
                    no_days_label.config(fg="red")

                count = 0
                total = 0

                inventory_stock.delete(*inventory_stock.get_children())
                if len(items_cart) > 0:
                    enter_quantity_label.config(fg="black")
                    no_days_label.config(fg="black")
                    for items in items_cart:
                        item = str(items).split("*")
                        current_total = int(item[2]) * int(item[3]) * int(item[4])
                        total += int(item[2]) * int(item[3]) * int(item[4])
                        inventory_stock.insert(parent="", index='end', iid=count, text=count + 1,
                                               values=(str(item[0]), str(item[1]), str(item[3]), str(item[2]), str(item[4]),
                                                       str(current_total)))
                        count += 1

                    frame4 = LabelFrame(top, text="Grand Total: ", padx=10, pady=10)
                    frame4.place(x=480, y=550)

                    global total_label
                    total_label = Label(frame4, text="Rs. " + "{:,}".format(total), font=("Roboto", 10, "bold"))
                    total_label.pack()

                    generate_invoice_button.configure(command=print_invoice)
                    generate_invoice_button.place(x=400, y=640)

                    delete_items_button.configure(command=getdata)
                    delete_items_button.place(x=60, y=640)

                    discount_label.place(x=260, y=565)
                    discount.place(x=380, y=565)

                    customer_name.grid_remove()
                    customer_contact_no.grid_remove()
                    customer_nic_no.grid_remove()
                    delivery_date_is.grid_remove()
                    no_days.grid_remove()
                    delivery_address.grid_remove()

                    customer_name_lock_label.config(text=str(customer_name.get()))
                    customer_name_lock_label.grid(row=0, column=1, sticky='w', columnspan=3, padx=0)

                    customer_contact_no_lock_label.config(text=str(customer_contact_no.get()))
                    customer_contact_no_lock_label.grid(row=1, column=1, sticky='w', padx=0)

                    customer_nic_no_lock_label.config(text=str(customer_nic_no.get()))
                    customer_nic_no_lock_label.grid(row=1, column=3, sticky='w')

                    delivery_date_lock_label.config(text=str(delivery_date))
                    delivery_date_lock_label.grid(row=2, column=1, sticky='w')

                    no_days_lock_label.config(text=str(no_days.get()))
                    no_days_lock_label.grid(row=2, column=3, sticky='w')

                    address = str(delivery_address.get())
                    if len(address) > 70:
                        address = address[:70] + "-\n" + address[70:]
                        delivery_address_label.grid_remove()
                        delivery_address_lock_label.config(text=str(address), justify='left', fg="green")
                        delivery_address_lock_label.grid(row=3, column=0, columnspan=4, sticky='w')
                    else:
                        address = str(delivery_address.get())
                        delivery_address_label.grid(row=3, column=0, sticky='w')
                        delivery_address_lock_label.config(text=str(address))
                        delivery_address_lock_label.grid(row=3, column=1, columnspan=3, sticky='w')
        else:
            customer_name_label.config(fg="red")
            customer_contact_no_label.config(fg="red")
            customer_nic_no_label.config(fg="red")
            no_days_label.config(fg="red")
            delivery_address_label.config(fg="red")
            enter_quantity_label.config(fg="red")
            if len(str(customer_name.get())) > 0:
                customer_name_label.config(fg="black")
            if len(str(customer_contact_no.get())) > 0:
                customer_contact_no_label.config(fg="black")
            if len(str(customer_nic_no.get())) > 0:
                customer_nic_no_label.config(fg="black")
            if len(str(no_days.get())) > 0:
                no_days_label.config(fg="black")
            if len(str(delivery_address.get())) > 0:
                delivery_address_label.config(fg="black")
            if len(str(enter_quantity.get())) > 0:
                enter_quantity_label.config(fg="red")

    def enter_quantity_function(x):
        global current_quantity
        current_quantity = get_current_quantity(get_inventory_id(str(variable2.get())))
        current_stock_label.config(text="Current Quanity: " + str(current_quantity))
        current_stock_label.grid(row=0, column=2, padx=8)
        enter_quantity_label.grid(row=0, column=3)
        enter_quantity.grid(row=0, column=4, padx=7)

        add_quantity_button = Button(frame2, text="ADD", font=("Arial", 10, 'bold'), justify='center', cursor="hand1",
                                     command=send_to_invoices_table)
        add_quantity_button.configure(foreground="black")
        add_quantity_button.configure(bg="light grey")
        add_quantity_button.grid(row=0, column=5)

    def item_name(x):
        global variable2
        variable2 = StringVar(top)
        variable2.set("Select Item")
        option_name = OptionMenu(frame2, variable2, *fetch_item_names(str(variable.get())),
                                 command=enter_quantity_function)
        option_name.configure(cursor="hand1")
        option_name.grid(row=0, column=1, padx=2, sticky='ew')

    variable = StringVar(top)
    item_types = []
    for types in fetch_inventory_types():
        if types != "Other":
            item_types.append(types)
    variable.set("Select Type")

    global variable2
    variable2 = StringVar(top)
    variable2.set("Select Item")

    list = []

    frame = LabelFrame(top, text="Customer Details", padx=10, pady=10)
    frame2 = LabelFrame(top, text="Select Inventory Quantity", padx=10, pady=10)
    try:
        option = OptionMenu(frame2, variable, *item_types, command=item_name)
        frame.place(x=15, y=15)

        customer_name_label = Label(frame, text="Customer Name:", font=("Roboto", 15))
        customer_name_label.grid(row=0, column=0, sticky='w', padx=0)
        customer_name = Entry(frame, width=44, font=("Roboto", 15), bg='white')
        customer_name.grid(row=0, column=1, sticky='w', columnspan=3, padx=0)

        customer_contact_no_label = Label(frame, text="Contact No:", font=("Roboto", 15))
        customer_contact_no_label.grid(row=1, column=0, sticky='w')
        customer_contact_no = Entry(frame, width=18, font=("Roboto", 15), bg='white')
        customer_contact_no.grid(row=1, column=1, sticky='w', padx=0)

        customer_nic_no_label = Label(frame, text="NIC:", font=("Roboto", 15))
        customer_nic_no_label.grid(row=1, column=2, sticky="w", padx=9)
        customer_nic_no = Entry(frame, width=19, font=("Roboto", 15), bg='white')
        customer_nic_no.grid(row=1, column=3, sticky='w')

        delivery_date_label = Label(frame, text="Delivery Date:", font=("Roboto", 15))
        delivery_date_label.grid(row=2, column=0, sticky='w')
        delivery_date_is = DateEntry(frame)
        delivery_date_is.grid(row=2, column=1, sticky='w')
        delivery_date_is.bind("<<DateEntrySelected>>", from_date)

        no_days_label = Label(frame, text="Days:", font=("Roboto", 15))
        no_days_label.grid(row=2, column=2, sticky='w', padx=9)
        no_days = Entry(frame, width=3, font=("Roboto", 15), bg='white')
        no_days.grid(row=2, column=3, sticky='w')
        no_days.insert(0, "1")

        delivery_address_label = Label(frame, text="Delivery Address:", font=("Roboto", 15))
        delivery_address_label.grid(row=3, column=0, sticky='w')
        delivery_address = Entry(frame, width=44, font=("Roboto", 15), bg='white')
        delivery_address.grid(row=3, column=1, columnspan=3, sticky='w')

        frame2 = LabelFrame(top, text="Select Inventory Quantity", padx=10, pady=10)
        frame2.place(x=15, y=200)

        option = OptionMenu(frame2, variable, *item_types, command=item_name)
        option.configure(cursor="hand1")
        option.grid(row=0, column=0, padx=7, sticky='ew')

        current_stock_label = Label(frame2, text="", font=("Roboto", 10))
        current_stock_label.place_forget()

        enter_quantity_label = Label(frame2, text="Enter Quantity:", font=("Roboto", 10, "bold"))
        enter_quantity_label.place_forget()
        enter_quantity = Entry(frame2, width=4, font=("Roboto", 15), bg='white')
        enter_quantity.place_forget()

        last_invoice_no = str(int(get_last_invoice_No()) + 1)

        frame3 = LabelFrame(top, text="Current Invoice :   " + last_invoice_no + "  ", padx=10, pady=10)
        frame3.place(x=15, y=280)

        inventory_stock = ttk.Treeview(frame3, height=10, style="mystyle.Treeview")
        inventory_stock['columns'] = ("Item Type", "Item Name", "Rate", "Item Quantity", "For Days", "Total")
        inventory_stock.column("#0", minwidth=25, width=40)
        inventory_stock.column("Item Type", anchor=W, width=135)
        inventory_stock.column("Item Name", anchor=W, width=135)
        inventory_stock.column("Rate", anchor=W, width=50)
        inventory_stock.column("Item Quantity", anchor=CENTER, width=100)
        inventory_stock.column("For Days", anchor=W, width=60)
        inventory_stock.column("Total", anchor=CENTER, width=100)

        inventory_stock.heading("#0", text="S. No", anchor=W)
        inventory_stock.heading("Item Type", text="Item Type", anchor=W)
        inventory_stock.heading("Item Name", text="Item Name", anchor=W)
        inventory_stock.heading("Rate", text="Rate", anchor=W)
        inventory_stock.heading("Item Quantity", text="Item Quantity", anchor=CENTER)
        inventory_stock.heading("For Days", text="For Days", anchor=W)
        inventory_stock.heading("Total", text="Total", anchor=CENTER)

        inventory_stock.pack(side='left', fill='y')

        scrollbar = Scrollbar(frame3, orient="vertical", command=inventory_stock.yview)
        scrollbar.pack(side="right", fill="y")
        inventory_stock.configure(yscrollcommand=scrollbar.set)

        discount_label = Label(top, text="Discount:", font=("Roboto", 20))
        discount_label.place_forget()
        discount = Entry(top, width=5, font=("Roboto", 20), bg='white', fg='blue')
        discount.insert(0, "0")
        discount.place_forget()

        generate_invoice_button = Button(top, text="Generate Invoice", font=("Arial", 15, 'bold'), cursor="hand1")
        generate_invoice_button.configure(foreground="white")
        generate_invoice_button.configure(bg="blue")
        generate_invoice_button.place_forget()

        delete_items_button = Button(top, text="DELETE ITEM", font=("Arial", 15, 'bold'), justify='center',
                                     cursor="hand1")
        delete_items_button.configure(foreground="white")
        delete_items_button.configure(bg="red")
        delete_items_button.place_forget()

        global items_cart
        items_cart = []

        customer_name_lock_label = Label(frame, text="Customer Name:", font=("Roboto", 15), fg="blue")
        customer_name_lock_label.grid_remove()

        customer_contact_no_lock_label = Label(frame, text="Contact No:", font=("Roboto", 15), fg="blue")
        customer_contact_no_lock_label.grid_remove()

        customer_nic_no_lock_label = Label(frame, text="NIC:", font=("Roboto", 15), fg="blue")
        customer_nic_no_lock_label.grid_remove()

        delivery_date_lock_label = Label(frame, text="Delivery Date:", font=("Roboto", 15), fg="blue")
        delivery_date_lock_label.grid_remove()

        no_days_lock_label = Label(frame, text="Days:", font=("Roboto", 15), fg="blue")
        no_days_lock_label.grid_remove()

        delivery_address_lock_label = Label(frame, text="Delivery Address:", font=("Roboto", 15), fg="blue")
        delivery_address_lock_label.grid_remove()
    except TypeError:
        empty_label = Label(top,
                            text="*** First Add Inventory By Going To ***\nAdd Inventory Option\n\nThen\n\n*** Add Quantity Of Inventory By ***\nGoing To Add Quantity Option",
                            font=("Roboto", 15))
        empty_label.place(x=180, y=220)
