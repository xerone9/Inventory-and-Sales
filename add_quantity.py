from tkinter import *
from sql_working import *


def add_quantity():
    top = Toplevel()
    top.title('Add Quantity')
    top.iconbitmap('icon.ico')
    top.geometry("300x200")
    top.resizable(0, 0)

    def item_name(x):
        inventory_type_label.config(fg="black")
        global variable2
        variable2 = StringVar(top)
        variable2.set("Select Item")
        global inventory_name_label
        inventory_name_label = Label(top, text="Item Name:", font=("Roboto", 15))
        inventory_name_label.grid(row=1, column=0, padx=10, pady=3, sticky='w')
        global option_name
        option_name = OptionMenu(top, variable2, *fetch_item_names(str(variable.get())))
        option_name.configure(cursor="hand1")
        option_name.grid(row=1, column=1, padx=10, pady=3, sticky='ew')

    def add_qunatity():
        global variable2
        global inventory_name_label
        global option_name
        try:
            if str(variable.get()) != "Select Type" and isinstance(int(quantity.get()), int):
                if str(variable2.get()) != "Select Item":
                    quantity_label.config(fg="black")
                    inventory_name_label.config(fg="black")
                    inventory_type_label.config(fg="black")
                    item = get_inventory_id(str(variable2.get()))
                    entry_in_inventory_status(item, int(quantity.get()), 0)
                    quantity.delete(0, "end")
                    variable.set("Select Type")
                    variable2.set("Select Item")
                    quantity.focus()
                else:
                    inventory_name_label.config(fg="red")

            else:
                if len(quantity.get()) < 1:
                    quantity_label.config(fg="red")
                else:
                    quantity_label.config(fg="black")

                if str(variable.get()) == "Select Type":
                    inventory_type_label.config(fg="red")
                else:
                    inventory_type_label.config(fg="black")

                if str(variable2.get()) == "Select Item":
                    inventory_name_label.config(fg="red")
                else:
                    inventory_name_label.config(fg="black")
        except ValueError:
            quantity_label.config(fg="red")





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


        option = OptionMenu(top, variable, *item_types, command=item_name)

        inventory_type_label = Label(top, text="Item Type:", font=("Roboto", 15))
        inventory_type_label.grid(row=0, column=0,padx=10, pady=3, sticky='w')
        option.configure(cursor="hand1")
        option.grid(row=0, column=1, padx=10, pady=3, sticky='w')

        quantity_label = Label(top, text="Quantity:", font=("Roboto", 15))
        quantity_label.grid(row=2, column=0, padx=10, pady=3, sticky='w')
        quantity = Entry(top, width=10, font=("Roboto", 15), bg='white')
        quantity.grid(row=2, column=1, padx=10, pady=3, sticky='w')

        add_quantity_button = Button(top, text="ADD Quantity", font=("Arial", 15, 'bold'), justify='center', cursor="hand1", command=add_qunatity)
        add_quantity_button.configure(foreground="black")
        add_quantity_button.configure(bg="light grey")
        add_quantity_button.grid(row=3, column=0, columnspan=2, pady=20)

        global inventory_name_label
        inventory_name_label = Label(top, text="Item Name:", font=("Roboto", 15))
        inventory_name_label.grid_forget()


    except TypeError:
        empty_label = Label(top, text="*** First Add Inventory By ***\nGoing To Add Inventory\nOption",
                            font=("Roboto", 15))
        empty_label.place(x=20, y=50)

