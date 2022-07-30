from tkinter import *
from sql_working import *


def lost_inventory():
    top = Toplevel()
    top.title('Lost or Damaged Inventory')
    top.iconbitmap('icon.ico')
    top.geometry("450x190")
    top.resizable(0, 0)

    def show_elements(x):
        inventory_name_label.config(fg="black")
        quantity_label.grid(row=2, column=0, padx=5, sticky='w')
        quantity.grid(row=2, column=1, padx=5, sticky='w')
        narration_label.grid(row=3, column=0, padx=5, sticky='w')
        narration.grid(row=3, column=1, padx=5, sticky='w')
        lost_quantity_button.place(x=175, y=135)
        quantity.delete(0, "end")
        narration.delete(0, "end")
        quantity.focus()



    def item_name(x):
        global variable2
        variable2 = StringVar(top)
        variable2.set("Select Item")
        global inventory_name_label
        inventory_name_label = Label(top, text="Item Name:", font=("Roboto", 15))
        inventory_name_label.grid(row=1, column=0, padx=5, sticky='w')
        global option_name
        option_name = OptionMenu(top, variable2, *fetch_item_names(str(variable.get())), command=show_elements)
        option_name.configure(cursor="hand1")
        option_name.grid(row=1, column=1, padx=5, sticky='ew')


    def lost_qunatity():
        global variable2
        try:
            if len(str(narration.get())) > 0 and isinstance(int(quantity.get()), int) and str(variable2.get()) != "Select Item":
                narration_label.config(fg="black")
                inventory_name_label.config(fg="black")
                quantity_label.config(fg="black")
                narration_label.config(fg="black")
                item = get_inventory_id(str(variable2.get()))
                entry_in_lost(str(item), int(quantity.get()), "D/L: " + str(narration.get()))
                debit_entry_in_inventory_status_lost_items(str(item), int(quantity.get()), "D/L: " + str(narration.get()), 0)
                quantity_label.grid_forget()
                quantity.grid_forget()
                narration_label.grid_forget()
                narration.grid_forget()
                lost_quantity_button.place_forget()
                option_name.grid_forget()
                inventory_name_label.grid_forget()
                variable.set("Select Type")
                variable2.set("Select Item")
            else:
                if len(str(narration.get())) < 1:
                    narration_label.config(fg="red")
                    inventory_name_label.config(fg="black")
                elif str(variable2.get()) != "Select Item":
                    narration_label.config(fg="black")
                    inventory_name_label.config(fg="red")



        except ValueError:
            quantity_label.config(fg="red")



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
        inventory_type_label = Label(top, text="Item Type:      ", font=("Roboto", 15))
        inventory_type_label.grid(row=0, column=0, padx=5, sticky='w')
        option.configure(cursor="hand1")
        option.grid(row=0, column=1, padx=5, sticky='ew')

        quantity_label = Label(top, text="Quantity:", font=("Roboto", 15))
        quantity_label.grid_forget()
        quantity = Entry(top, width=10, font=("Roboto", 15), bg='white')
        quantity.grid_forget()

        narration_label = Label(top, text="Narration:", font=("Roboto", 15))
        narration_label.grid_forget()
        narration = Entry(top, width=25, font=("Roboto", 15), bg='white')
        narration.grid_forget()

        lost_quantity_button = Button(top, text="Lost Quantity", font=("Arial", 15, 'bold'), justify='center', cursor="hand1", command=lost_qunatity)
        lost_quantity_button.configure(foreground="black")
        lost_quantity_button.configure(bg="light grey")
        lost_quantity_button.place_forget()
    except TypeError:
        inventory_type_label = Label(top, text="*** First Add Inventory By Going To ***\nAdd Inventory Option\n\nThen\n\n*** Add Quantity Of Inventory By ***\nGoing To Add Quantity Option", font=("Roboto", 15))
        inventory_type_label.place(x=40, y=7)