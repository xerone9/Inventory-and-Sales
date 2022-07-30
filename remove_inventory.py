from tkinter import *
from sql_working import *

def remove_inventory():
    top = Toplevel()
    top.title('Remove Inventory')
    top.iconbitmap('icon.ico')
    top.geometry("490x150")
    top.resizable(0, 0)

    def remove():
        inventory_id = get_inventory_id(str(variable2.get()))
        delete_values_from_Inventory(str(inventory_id))
        inventory_name_label.grid_forget()
        remove_inventory_button.place_forget()
        option_name.grid_forget()
        variable.set("Select Type")
        variable2.set("Select Item")


    def display_button(x):
        remove_inventory_button.place(relx=0.50, rely=0.75, anchor=CENTER)


    def item_name(x):
        global variable2
        variable2 = StringVar(top)
        variable2.set("Select Item")
        global inventory_name_label
        inventory_name_label = Label(top, text="Item Name:", font=("Roboto", 13))
        inventory_name_label.grid(row=0, column=2, padx=5, pady=10, sticky='w')
        global option_name
        option_name = OptionMenu(top, variable2, *fetch_item_names(str(variable.get())), command=display_button)
        option_name.configure(cursor="hand1")
        option_name.grid(row=0, column=3, padx=5, pady=10, sticky='ew')

    variable = StringVar(top)
    item_types = []
    for types in fetch_inventory_types():
        if types != "Other":
            item_types.append(types)
    variable.set("Select Type")

    global variable2
    variable2 = StringVar(top)
    variable2.set("Select Item")

    try:
        option = OptionMenu(top, variable, *item_types, command=item_name)
        inventory_type_label = Label(top, text="Item Type:", font=("Roboto", 13))
        inventory_type_label.grid(row=0, column=0, padx=5, pady=10, sticky='w')
        option.configure(cursor="hand1")
        option.grid(row=0, column=1, padx=5, pady=10, sticky='ew')

        remove_inventory_button = Button(top, text="REMOVE", font=("Arial", 15, 'bold'), justify='center', cursor="hand1",
                                     command=remove)
        remove_inventory_button.configure(foreground="black")
        remove_inventory_button.configure(bg="red")
        remove_inventory_button.place_forget()
    except TypeError:
        empty_label = Label(top, text="*** First Add Inventory By Going To ***\nAdd Inventory Option", font=("Roboto", 15))
        empty_label.place(x=55, y=40)