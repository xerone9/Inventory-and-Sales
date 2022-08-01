from tkinter import *
from sql_working import *
from tkinter import ttk


def add_inventory():
    def splash_screen(error):
        splash_root = Toplevel()
        splash_root.title('Error')
        splash_root.iconbitmap('icon.ico')
        splash_root.geometry("750x100")
        splash_root.resizable(0, 0)
        error = Label(splash_root, text=str(error), padx=10, pady=10, fg="red", font=("Roboto", 15))
        error.place(x=10, y=10)


    top = Toplevel()
    top.title('Add Inventory')
    top.geometry("600x570")
    top.iconbitmap('icon.ico')
    top.resizable(0, 0)

    def other_type(x):
        other = str(variable.get())
        if other == "Other":
            inventory_type2.grid(row=2, column=1, padx=10, pady=2, sticky='w')
            inventory_type2_label.grid(row=2, column=0, padx=10, pady=2, sticky='w')
            inventory_type2.delete(0, "end")
        else:
            inventory_type2_label.grid_remove()
            inventory_type2.grid_remove()
            inventory_type2.delete(0, "end")
            inventory_type2.insert(0, other)

    def save():
        global option
        try:
            inventory_rate_label.config(fg="black")
            if len(str(inventory_name.get())) > 0 and len(str(inventory_rate.get())) and str(variable.get()) != "Select Type" and isinstance(int(inventory_rate.get()), int):
                if str(variable.get()) == "Other":
                    if len(str(inventory_type2.get())) < 1:
                        inventory_type2_label.config(fg="red")
                    else:
                        if validate_item_type(inventory_type2.get()):
                            error = '*** "' + str(inventory_type2.get()) + '" is already in item types. Select it in "Item Types" options ***'
                            splash_screen(error)
                        elif validate_item_name(inventory_name.get()):
                            error = '*** "' + str(inventory_name.get()) + '" is already in item Names. You can not add it again ***'
                            splash_screen(error)
                        else:
                            entry_in_inventory(inventory_type2.get(), inventory_name.get(), inventory_rate.get())
                            inventory_name.delete(0, "end")
                            inventory_rate.delete(0, "end")
                            variable.set(fetch_inventory_types()[1])
                            inventory_type2.delete(0, "end")
                            inventory_type2_label.grid_remove()
                            inventory_type2.grid_remove()
                            variable.set("Select Type")
                            inventory_type_label.config(fg="black")
                            inventory_type2_label.config(fg="black")
                            inventory_rate_label.config(fg="black")
                            inventory_name_label.config(fg="black")
                            option.destroy()
                            option = OptionMenu(item_details, variable, *fetch_inventory_types(), command=other_type)
                            option.configure(cursor="hand1")
                            option.grid(row=1, column=1, padx=10, pady=2, sticky='w')

                            my_tree.delete(*my_tree.get_children())

                            teacher_list = fetch_inventory()
                            count = 0

                            for value in teacher_list:
                                my_tree.insert(parent="", index='end', iid=count, text=count + 1,
                                               values=(value[0], value[1], value[2]))
                                count += 1
                            inventory_name.focus()

                else:
                    if validate_item_name(inventory_name.get()):
                        error = '*** "' + str(inventory_name.get()) + '" is already in item Names. You can not add it again ***'
                        splash_screen(error)
                    else:
                        entry_in_inventory(inventory_type2.get(), inventory_name.get(), inventory_rate.get())
                        inventory_name.delete(0, "end")
                        inventory_rate.delete(0, "end")
                        variable.set(fetch_inventory_types()[1])
                        inventory_type2.delete(0, "end")
                        inventory_type2_label.grid_remove()
                        inventory_type2.grid_remove()
                        variable.set("Select Type")
                        inventory_type_label.config(fg="black")
                        inventory_type2_label.config(fg="black")
                        inventory_rate_label.config(fg="black")
                        inventory_name_label.config(fg="black")
                        option.destroy()
                        option = OptionMenu(item_details, variable, *fetch_inventory_types(), command=other_type)
                        option.configure(cursor="hand1")
                        option.grid(row=1, column=1, padx=10, pady=2, sticky='w')

                        my_tree.delete(*my_tree.get_children())

                        teacher_list = fetch_inventory()
                        count = 0

                        for value in teacher_list:
                            my_tree.insert(parent="", index='end', iid=count, text=count + 1,
                                           values=(value[0], value[1], value[2]))
                            count += 1
                        inventory_name.focus()
            else:
                if str(variable.get()) == "Select Type":
                    inventory_type_label.config(fg="red")
                else:
                    inventory_type_label.config(fg="black")

                if len(str(inventory_name.get())) < 1:
                    inventory_name_label.config(fg="red")
                else:
                    inventory_name_label.config(fg="black")

                if len(str(inventory_type2.get())) < 1:
                    inventory_type2_label.config(fg="red")
                else:
                    inventory_type2_label.config(fg="black")

                if len(str(inventory_rate.get())) < 1:
                    inventory_rate_label.config(fg="red")
                else:
                    inventory_rate_label.config(fg="black")

                if isinstance(inventory_rate.get(), int):
                    inventory_rate_label.config(fg="black")
                else:
                    inventory_rate_label.config(fg="red")
        except ValueError:
            inventory_rate_label.config(fg="red")


    variable = StringVar(top)
    variable.set("Select Type")

    item_details = LabelFrame(top, text="New Item Details", padx=10, pady=10)
    item_details.grid(row=0, column=0, pady=15, padx=10)
    inventory_name_label = Label(item_details, text="Item Name:", font=("Roboto", 15))
    inventory_name_label.grid(row=0, column=0, padx=10, pady=2, sticky='w')
    inventory_name = Entry(item_details, width=25, font=("Roboto", 15), bg='white')
    inventory_name.grid(row=0, column=1, padx=10, pady=2, sticky='w')

    inventory_type_label = Label(item_details, text="Item Type:", font=("Roboto", 15))
    inventory_type_label.grid(row=1, column=0, padx=10, pady=2, sticky='w')
    global option
    option = OptionMenu(item_details, variable, *fetch_inventory_types(), command=other_type)
    option.configure(cursor="hand1")
    option.grid(row=1, column=1, padx=10, pady=2, sticky='w')

    inventory_type2_label = Label(item_details, text="Name Type:", font=("Roboto", 15))
    inventory_type2_label.place_forget()
    inventory_type2 = Entry(item_details, width=25, font=("Roboto", 15), bg='white')
    inventory_type2.place_forget()
    inventory_type2.insert(0, str(variable.get()))

    inventory_rate_label = Label(item_details, text="Item Rate:", font=("Roboto", 15))
    inventory_rate_label.grid(row=3, column=0, padx=10, pady=2, sticky='w')
    inventory_rate = Entry(item_details, width=25, font=("Roboto", 15), bg='white')
    inventory_rate.grid(row=3, column=1, padx=10, pady=2, sticky='w')

    add_inventory_button = Button(item_details, text="S A V E", font=("Arial", 15, 'bold'), justify='center', cursor="hand1", command=save)
    add_inventory_button.configure(foreground="black")
    add_inventory_button.configure(bg="light grey")
    # startButton.place(x=100, y=208)
    add_inventory_button.grid(row=4, column=0, columnspan=2, padx=10, pady=7)

    available_items = LabelFrame(top, text="Items Currently In Database", padx=10, pady=10)
    available_items.grid(row=1, column=0, pady=15, padx=10)

    frame = Frame(available_items)
    frame.grid(row=0, column=0, pady=0, padx=5)

    my_tree = ttk.Treeview(frame, height=10, style="mystyle.Treeview")
    my_tree['columns'] = ("Item Type", "Item Name", "Item Rate")
    my_tree.column("#0", minwidth=25, width=75)
    my_tree.column("Item Type", anchor=W, width=150)
    my_tree.column("Item Name", anchor=W, width=150)
    my_tree.column("Item Rate", anchor=CENTER, width=120)

    my_tree.heading("#0", text="S. No", anchor=W)
    my_tree.heading("Item Type", text="Item Type", anchor=W)
    my_tree.heading("Item Name", text="Item Name", anchor=W)
    my_tree.heading("Item Rate", text="Item Rate", anchor=CENTER)

    my_tree.pack(side='left', fill='y')

    scrollbar = Scrollbar(frame, orient="vertical", command=my_tree.yview)
    scrollbar.pack(side="right", fill="y")
    my_tree.configure(yscrollcommand=scrollbar.set)

    # my_tree.insert(parent="", index='end', iid=0, text="1", values=("Usman Mustafa Khawar", "Basic Programming", "03:00 To 06:00", "RM-05"))

    teacher_list = fetch_inventory()
    count = 0

    for value in teacher_list:
        my_tree.insert(parent="", index='end', iid=count, text=count + 1,
                                values=(value[0], value[1], value[2]))
        count += 1

