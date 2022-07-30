from tkinter import *
from sql_working import *
import datetime
from quick_estimate_report import quick_estimate_report
from tkinter import ttk
from tkcalendar import *

def quick_estimate():
    top = Toplevel()
    top.title('Quick Estimate')
    top.iconbitmap('icon.ico')
    top.geometry("700x520")
    top.resizable(0,0)

    def getdata():
        global items_cart
        global total_label
        x = inventory_stock.selection()
        y = inventory_stock.item(x)['values']
        delete_value = ""
        for items in y:
            delete_value += str(items) + "*"

        removing_total = str(delete_value).split("*")
        actual_values = removing_total[0] + "*" + removing_total[1] + "*" + removing_total[3] + "*" + removing_total[2] + "*" + removing_total[4]
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

    def print_invoice():
        global items_cart

        quick_estimate_report(items_cart)
        top.destroy()


    def send_to_invoices_table():
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
        for_days_label.config(fg="black")
        enter_quantity_label.config(fg="black")
        try:
            int(enter_quantity.get())
            int(for_days.get())
            items_cart.append(str(get_inventory_type(str(item_id))) + "*" + str(get_inventory_name(str(item_id))) + "*" + str(enter_quantity.get()) + "*" + str(item_rate) + "*" + str(for_days.get()))
        except ValueError:
            pass
        try:
            int(enter_quantity.get())
        except ValueError:
            enter_quantity_label.config(fg="red")
        try:
            int(for_days.get())
        except ValueError:
            for_days_label.config(fg="red")


        count = 0
        total = 0

        inventory_stock.delete(*inventory_stock.get_children())

        if len(items_cart) > 0:
            for items in items_cart:
                item = str(items).split("*")
                current_total = int(item[2]) * int(item[3]) * int(item[4])
                total += int(item[2]) * int(item[3]) * int(item[4])
                inventory_stock.insert(parent="", index='end', iid=count, text=count + 1,
                                       values=(str(item[0]), str(item[1]), str(item[3]), str(item[2]), str(item[4]), str(current_total)))
                count += 1

            frame4 = LabelFrame(top, text="Grand Total: ", padx=10, pady=10)
            frame4.place(x=480, y=420)

            global total_label
            total_label = Label(frame4, text="Rs. " + "{:,}".format(total), font=("Roboto", 10, "bold"))
            total_label.pack()

            generate_invoice_button.configure(command=print_invoice)
            generate_invoice_button.place(x=240, y=428)

            delete_items_button.configure(command=getdata)
            delete_items_button.place(x=50, y=428)

    def enter_quantity_function(x):
        current_quantity = get_current_quantity(get_inventory_id(str(variable2.get())))
        current_stock_label.config(text="Current Quanity: " + str(current_quantity))
        current_stock_label.grid(row=1, column=2, padx=8)
        enter_quantity_label.grid(row=1, column=3)
        enter_quantity.grid(row=1, column=4, padx=7)

        add_quantity_button = Button(frame2, text="ADD", font=("Arial", 10, 'bold'), justify='center', cursor="hand1", command=send_to_invoices_table)
        add_quantity_button.configure(foreground="black")
        add_quantity_button.configure(bg="light grey")
        add_quantity_button.grid(row=1, column=5)

    def item_name(x):
        global variable2
        variable2 = StringVar(top)
        variable2.set("Select Item")
        option_name = OptionMenu(frame2, variable2, *fetch_item_names(str(variable.get())), command=enter_quantity_function)
        option_name.configure(cursor="hand1")
        option_name.grid(row=1, column=1, padx=2, sticky='ew')

    try:
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

        frame2 = LabelFrame(top, text="Select Inventory Quantity", padx=10, pady=10)
        frame2.place(x=15, y=15)
        option = OptionMenu(frame2, variable, *item_types, command=item_name)

        for_days_label = Label(frame2, text="No. Of Days:", font=("Roboto", 10, "bold"))
        for_days_label.grid(row=0, column=0, padx=7)
        for_days = Entry(frame2, width=4, font=("Roboto", 15), bg='white')
        for_days.insert(0, "1")
        for_days.grid(row=0, column=1, padx=1, pady=5)

        option = OptionMenu(frame2, variable, *item_types, command=item_name)
        option.configure(cursor="hand1")
        option.grid(row=1, column=0, padx=7, sticky='ew')

        current_stock_label = Label(frame2, text="", font=("Roboto", 10))
        current_stock_label.place_forget()

        enter_quantity_label = Label(frame2, text="Enter Quantity:", font=("Roboto", 10, "bold"))
        enter_quantity_label.place_forget()
        enter_quantity = Entry(frame2, width=4, font=("Roboto", 15), bg='white')
        enter_quantity.place_forget()

        frame3 = LabelFrame(top, text="Raw Estimate", padx=10, pady=10)
        frame3.place(x=15, y=140)

        inventory_stock = ttk.Treeview(frame3, height=10, style="mystyle.Treeview")
        inventory_stock['columns'] = ("Item Type", "Item Name", "Rate", "Item Quantity", "For Days", "Total")
        inventory_stock.column("#0", minwidth=25, width=40)
        inventory_stock.column("Item Type", anchor=W, width=130)
        inventory_stock.column("Item Name", anchor=W, width=130)
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

    except TypeError:
        empty_label = Label(top, text="*** First Add Inventory By Going To ***\nAdd Inventory Option\n\nThen\n\n*** Add Quantity Of Inventory By ***\nGoing To Add Quantity Option", font=("Roboto", 15))
        empty_label.place(x=120, y=120)






