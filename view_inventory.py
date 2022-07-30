from tkinter import *
from sql_working import *
from tkinter import ttk
import datetime

def view_inventory():
    date = str(datetime.datetime.now()).split(".")
    date_is = date[0].split(" ")
    top = Toplevel()
    top.title('View Inventory')
    top.iconbitmap('icon.ico')
    top.geometry("575x400")
    top.resizable(0, 0)

    inventory_Register_label = Label(top, text="INVENTORY REGISTER", font=("Roboto", 25))
    inventory_Register_label.place(relx=0.85, rely=0.14, anchor="se")

    inventory_Date_label = Label(top, text="Dated: " + str(date_is[0]), font=("Roboto", 15), fg="Blue")
    inventory_Date_label.place(relx=0.62, rely=0.20, anchor="se")

    frame = Frame(top)
    frame.place(x=20, rely=0.25)

    inventory_stock = ttk.Treeview(frame, height=10, style="mystyle.Treeview")
    inventory_stock['columns'] = ("Item Type", "Item Name", "Rate", "Item Quantity", "In Stock")
    inventory_stock.column("#0", minwidth=25, width=40)
    inventory_stock.column("Item Type", anchor=W, width=130)
    inventory_stock.column("Item Name", anchor=W, width=130)
    inventory_stock.column("Rate", anchor=W, width=45)
    inventory_stock.column("Item Quantity", anchor=CENTER, width=100)
    inventory_stock.column("In Stock", anchor=CENTER, width=75)

    inventory_stock.heading("#0", text="S. No", anchor=W)
    inventory_stock.heading("Item Type", text="Item Type", anchor=W)
    inventory_stock.heading("Item Name", text="Item Name", anchor=W)
    inventory_stock.heading("Rate", text="Rate", anchor=W)
    inventory_stock.heading("Item Quantity", text="Item Quantity", anchor=CENTER)
    inventory_stock.heading("In Stock", text="In Stock", anchor=CENTER)

    inventory_stock.pack(side='left', fill='y')

    scrollbar = Scrollbar(frame, orient="vertical", command=inventory_stock.yview)
    scrollbar.pack(side="right", fill="y")
    inventory_stock.configure(yscrollcommand=scrollbar.set)

    # my_tree.insert(parent="", index='end', iid=0, text="1", values=("Usman Mustafa Khawar", "Basic Programming", "03:00 To 06:00", "RM-05"))


    count = 0
    list = []
    for value in inventory_Register():
        if value[0] + "-" + value[1] not in list:
            list.append(value[0] + "-" + value[1])

    list.sort()

    items = []
    for value in list:
        breaking_items = str(value).split("-")
        items.append(breaking_items[1])

    for value in items:
        inventory_type = get_inventory_type(str(get_inventory_id(str(value))))
        inventory_name = value
        inventory_rate = get_inventory_rate(str(get_inventory_id(str(value))))
        inventory_total_quantity = get_total_quantity(get_inventory_id(str(value)))
        inventory_available_quantity = get_current_quantity(get_inventory_id(str(value)))

        inventory_stock.insert(parent="", index='end', iid=count, text=count + 1,
                               values=(str(inventory_type), str(inventory_name), str(inventory_rate), str(inventory_total_quantity), str(inventory_available_quantity)))
        count += 1

