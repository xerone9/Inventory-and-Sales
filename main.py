import webbrowser

from tkinter import *
from add_inventory import add_inventory
from add_quantity import add_quantity
from view_inventory import view_inventory
from remove_inventory import remove_inventory
from edit_inventory import edit_inventory
from receive_back_inventory import receive_back_inventory
from lost_damaged_inventory import lost_inventory
from view_invoices import viwe_invoice
from delete_invoice import delete_invoice
from all_orders import all_orders
from completed_orders import completed_orders
from quick_estimate import quick_estimate
from items_to_deliver import items_to_deliver
from generate_invoice import generate_invoice
from sales import sales

# Reports
from view_inventory_report import view_inventory_report
from availabe_inventory_report import available_inventory_report
from damaged_inventory_report import damaged_inventory_report
from overall_inventory_report import overall_inventory_report
from given_item_report import given_item_report



def callback(url):
    webbrowser.open_new(url)
    webbrowser.open_new("https://github.com/xerone9")


root = Tk()
root.resizable(0,0)
root.iconbitmap('icon.ico')

bg = PhotoImage(file="backgroud.png")

# Show image using label
label1 = Label(root, image=bg)
label1.place(x=0, y=0)

company_name = ""
try:
    f = open("enter_company_name.ini", "r")
    for x in f:
      name = str(x)
      if "Name" in name:
          company_name = name.split(" = ")[1]
    f.close()
except FileNotFoundError:
    company_name = "softwares.rubick.org"
root.title(str(company_name))
root.geometry("910x607")

my_menu = Menu(root)
root.config(menu=my_menu)

inventory_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Inventory", menu=inventory_menu)
inventory_menu.add_command(label="View Inventory", command=view_inventory)
inventory_menu.add_command(label="Add Inventory", command=add_inventory)
inventory_menu.add_command(label="Add Quantity To Inventory", command=add_quantity)
inventory_menu.add_command(label="Change Price", command=edit_inventory)
inventory_menu.add_command(label="Remove Inventory", command=remove_inventory)
inventory_menu.add_command(label="Receive Back Inventory", command=receive_back_inventory)
inventory_menu.add_command(label="Damaged/Lost Inventory", command=lost_inventory)

generate_invoice_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Invoice", menu=generate_invoice_menu)
generate_invoice_menu.add_command(label="Generate Invoice", command=generate_invoice)
generate_invoice_menu.add_command(label="View Invoices", command=viwe_invoice)
generate_invoice_menu.add_command(label="Delete Invoice", command=delete_invoice)

reports_menu = Menu(my_menu, tearoff=0)
order_sub_menu = Menu(reports_menu, tearoff=0)
inventory_sub_menu = Menu(reports_menu, tearoff=0)
my_menu.add_cascade(label="Reports", menu=reports_menu)
reports_menu.add_cascade(label="Inventory", menu=inventory_sub_menu)
inventory_sub_menu.add_command(label="Total Inventory", command=view_inventory_report)
inventory_sub_menu.add_command(label="Available Inventory", command=available_inventory_report)
inventory_sub_menu.add_command(label="Damaged Inventory", command=damaged_inventory_report)
inventory_sub_menu.add_command(label="Overall Inventory", command=overall_inventory_report)
reports_menu.add_cascade(label="Orders", menu=order_sub_menu)
order_sub_menu.add_command(label='All Orders', command=all_orders)
order_sub_menu.add_command(label='Completed Order', command=completed_orders)
order_sub_menu.add_command(label='Awaiting Return Orders', command=given_item_report)
reports_menu.add_cascade(label="Sales", command=sales)

daily_work_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Daily Work", menu=daily_work_menu)
daily_work_menu.add_cascade(label="Quick Estimate", command=quick_estimate)
daily_work_menu.add_cascade(label="Items To Be Delivered Today", command=items_to_deliver)


footer = Label(root, text="softwares.rubick.org", font=(14), cursor="hand2")
footer.bind("<Button-1>", lambda e: callback("http://softwares.rubick.org"))
footer.configure(foreground="white")
footer.configure(bg="black")
footer.pack(side=BOTTOM)

root.mainloop()
