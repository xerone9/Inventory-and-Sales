from tkinter import *
from sql_working import *


def edit_inventory():
    top = Toplevel()
    top.title('Change Price')
    top.iconbitmap('icon.ico')
    top.geometry("650x200")
    top.resizable(0, 0)


    def update():
        try:
            if isinstance(int(new_price.get()), int):
                inventory_id = get_inventory_id(str(variable2.get()))
                new_rate = new_price.get()
                edit_inventory_price(inventory_id, new_rate)

                variable.set("Select Type")
                variable2.set("Select Item")
                inventory_name_label.grid_forget()
                option_name.grid_forget()
                new_price_label.grid_forget()
                new_price_label.grid_forget()
                update_inventory_price_button.place_forget()
                new_price.grid_forget()


        except ValueError:
            new_price_label.config(fg="red")



    def price(x):
        new_price_label.grid(row=0, column=4, padx=7, pady=10, sticky='w')
        new_price.grid(row=0, column=5, padx=7, pady=10, sticky='w')
        update_inventory_price_button.place(x=250, y=100)
        new_price.focus()


    def item_name(x):
        global variable2
        variable2 = StringVar(top)
        variable2.set("Select Item")
        global inventory_name_label
        inventory_name_label = Label(top, text="Item Name:", font=("Roboto", 13))
        inventory_name_label.grid(row=0, column=2, padx=7, pady=10, sticky='w')
        global option_name
        option_name = OptionMenu(top, variable2, *fetch_item_names(str(variable.get())), command=price)
        option_name.configure(cursor="hand1")
        option_name.grid(row=0, column=3, pady=10, padx=7, sticky='ew')



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
        option.configure(cursor="hand1")
        option.grid(row=0, column=1, padx=7, pady=10, sticky='ew')

        inventory_type_label = Label(top, text="Item Type:", font=("Roboto", 13))
        inventory_type_label.grid(row=0, column=0, padx=7, pady=10, sticky='w')


        new_price_label = Label(top, text="New Price:", font=("Roboto", 13))
        new_price_label.grid_forget()
        new_price = Entry(top, width=4, font=("Roboto", 15), bg='white')
        new_price.grid_forget()

        update_inventory_price_button = Button(top, text="UPDATE", font=("Arial", 15, 'bold'), justify='center', cursor="hand1", command=update)
        update_inventory_price_button.configure(foreground="black")
        update_inventory_price_button.configure(bg="green")
        update_inventory_price_button.place_forget()
    except TypeError:
        empty_label = Label(top, text="*** First Add Inventory By Going To Add Inventory Option ***", font=("Roboto", 17))
        empty_label.place(x=20, y=55)
