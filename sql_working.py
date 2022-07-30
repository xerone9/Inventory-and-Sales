import sqlite3
import datetime


def entry_in_inventory(type, item, rate):
    datex = str(datetime.datetime.now()).split(".")
    date_and_time = str(datex[0]).split(" ")
    date = date_and_time[0]
    time = date_and_time[1]
    inventory_id = 0
    conn = sqlite3.connect("data.db")

    c = conn.cursor()

    fetch_values = c.execute("SELECT Inventoryid, oid FROM Inventory")

    for value in fetch_values:
        if value is None:
            pass
        else:
            if inventory_id < int(value[0]):
                inventory_id = int(value[0])

    c.execute("INSERT INTO Inventory VALUES (:Date, :Item_Type, :Item_Name, :Rate, :Inventoryid, :Time)",
              {
                  'Date': date,
                  'Item_Type': type,
                  'Item_Name': item,
                  'Rate': rate,
                  'Inventoryid': inventory_id + 1,
                  'Time': time

              })

    conn.commit()
    conn.close()


def fetch_inventory_types():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    item_type = []

    fetch_values = c.execute("SELECT Item_Type, oid FROM Inventory")

    for value in fetch_values:
        if value[0] not in item_type:
            item_type.append(value[0])
    item_type.append("Other")
    return item_type

    conn.commit()
    conn.close()


def fetch_customer_details_from_inventory_ledger(invoice):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    date_complete = str(datetime.datetime.now()).split(".")
    date_and_time = date_complete[0].split(" ")
    date = date_and_time[0]

    customer = []

    fetch_values = c.execute(
        "SELECT Customer_Name, Customer_Contact_No, Customer_Delivery_Date, Customer_Address, Date, NIC FROM Inventory_Ledger WHERE Invoice_id=" + str(
            invoice))

    for value in fetch_values:
        if value[0] not in customer:
            customer.append(value[0])
        if value[1] not in customer:
            customer.append(value[1])
        if value[2] not in customer:
            customer.append(value[2])
        if value[3] not in customer:
            customer.append(value[3])
        if value[4] not in customer:
            customer.append(value[4])
        if value[5] not in customer:
            customer.append(value[5])

    if len(customer) < 6:
        customer.insert(4, str(date))

    return customer

    conn.commit()
    conn.close()


def fetch_item_names(category):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    item_names = []
    fetch_values = c.execute("SELECT Item_Name, oid FROM Inventory WHERE Item_Type='" + category + "'")

    for items in fetch_values:
        item_names.append(items[0])

    return item_names

    conn.commit()
    conn.close()


def delete_values_from_time_table():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    c.execute("DELETE FROM Inventory_Status WHERE Inventory_ID=" + str(9))

    conn.commit()
    conn.close()


def delete_values_from_Inventory(inventory_id):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    c.execute("DELETE FROM Inventory WHERE Inventoryid=" + str(inventory_id))
    c.execute("DELETE FROM Inventory_Status WHERE Inventory_ID=" + str(inventory_id))

    conn.commit()
    conn.close()


def fetch_inventory():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    fetch_values = c.execute("SELECT Item_Type, Item_name, Rate FROM Inventory ORDER BY Item_Type")

    return fetch_values

    conn.commit()
    conn.close()


def get_inventory_id(item_name):
    inventory_id = 0
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    fetch_items = c.execute("SELECT Item_name, Inventoryid FROM Inventory")

    for items in fetch_items:
        if items[0] == item_name:
            inventory_id = int(items[1])

    return inventory_id

    conn.commit()
    conn.close()


def get_inventory_name(id):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    item_name = c.execute("SELECT Item_name, Inventoryid FROM Inventory WHERE Inventoryid=" + id)
    name = ""

    for i in item_name:
        name = i[0]

    return name

    conn.commit()
    conn.close()


def get_inventory_type(item_type):
    of_type = " "
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    fetch_items = c.execute("SELECT Item_Type, Inventoryid FROM Inventory")

    for items in fetch_items:
        if items[1] == item_type:
            of_type = str(items[0])

    return of_type

    conn.commit()
    conn.close()


def get_inventory_rate(item_id):
    item_rate = 0
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    fetch_items = c.execute("SELECT Rate, Inventoryid FROM Inventory")

    for items in fetch_items:
        if items[1] == item_id:
            item_rate = int(items[0])

    return item_rate

    conn.commit()
    conn.close()


def entry_in_inventory_status(item, quantity, invoice):
    date = str(datetime.datetime.now()).split(".")
    date_time = date[0].split(" ")

    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    c.execute(
        "INSERT INTO Inventory_Status VALUES (:Date, :Inventory_ID, :Item_Added, :Item_Removed, :Narration, :Time, :Invoice_id)",
        {
            'Date': date_time[0],
            'Inventory_ID': int(item),
            'Item_Added': int(quantity),
            'Item_Removed': "",
            'Narration': "Purchased",
            'Time': date_time[1],
            'Invoice_id': invoice

        })

    conn.commit()
    conn.close()


def debit_entry_in_inventory_status(item, quantity, name, invoice):
    date = str(datetime.datetime.now()).split(".")
    date_time = date[0].split(" ")

    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    c.execute(
        "INSERT INTO Inventory_Status VALUES (:Date, :Inventory_ID, :Item_Added, :Item_Removed, :Narration, :Time, :Invoice_id)",
        {
            'Date': date_time[0],
            'Inventory_ID': int(item),
            'Item_Added': "",
            'Item_Removed': int(quantity),
            'Narration': "For Customer " + name,
            'Time': date_time[1],
            'Invoice_id': invoice

        })

    conn.commit()
    conn.close()


def debit_entry_in_inventory_status_lost_items(item, quantity, narration, invoice_no):
    date = str(datetime.datetime.now()).split(".")
    date_time = date[0].split(" ")

    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    c.execute(
        "INSERT INTO Inventory_Status VALUES (:Date, :Inventory_ID, :Item_Added, :Item_Removed, :Narration, :Time, :Invoice_id)",
        {
            'Date': date_time[0],
            'Inventory_ID': int(item),
            'Item_Added': "",
            'Item_Removed': int(quantity),
            'Narration': narration,
            'Time': date_time[1],
            'Invoice_id': invoice_no

        })

    conn.commit()
    conn.close()


def inventory_Register():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    stock = c.execute("""
    SELECT Item_Type, Item_Name, Rate, Item_Added, Item_Removed
    FROM Inventory LEFT JOIN Inventory_Status ON Inventory.Inventoryid = Inventory_Status.Inventory_ID
""")

    return stock

    conn.commit()
    conn.close()


def current_invoice(invoice_no):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    stock = c.execute("""
    SELECT Item_Type, Inventory.Item_Name, Item_Rate, Item_Quantity, Item_Total, NIC, For_Days
    FROM Inventory_Ledger JOIN Inventory ON Inventory_Ledger.Item_Name = Inventory.Inventoryid
    WHERE Invoice_id=""" + str(invoice_no) + " ORDER BY Item_Type")

    return stock

    conn.commit()
    conn.close()


def get_last_invoice_No():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    last_invoice_no = 0
    stock = c.execute("""
    SELECT Invoice_id, oid FROM Invoices
    """)

    for invoices in stock:
        last_invoice_no = invoices[0]

    return last_invoice_no

    conn.commit()
    conn.close()


def edit_inventory_price(inventory_id, rate):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    c.execute("""UPDATE Inventory SET                            
                        Rate = :Rate

                        WHERE Inventoryid = :Inventoryid""",
              {
                  'Rate': int(rate),
                  'Inventoryid': int(inventory_id)
              })

    conn.commit()
    conn.close()


def entry_in_inventory_ledger(invoice_id, name, contact, delivery, address, item, quantity, rate, nic, days):
    date_complete = str(datetime.datetime.now()).split(".")
    date_and_time = date_complete[0].split(" ")
    date = date_and_time[0]
    time = date_and_time[1]
    conn = sqlite3.connect("data.db")

    c = conn.cursor()

    c.execute(
        "INSERT INTO Inventory_Ledger VALUES (:Date, :Time, :Invoice_id, :Customer_Name, :Customer_Contact_No, :Customer_Delivery_Date, :Customer_Address, :Item_Name, :Item_Quantity, :Item_Rate, :Item_Total, :NIC, :For_Days)",
        {
            'Date': date,
            'Time': time,
            'Invoice_id': invoice_id,
            'Customer_Name': name,
            'Customer_Contact_No': contact,
            'Customer_Delivery_Date': delivery,
            'Customer_Address': address,
            'Item_Name': item,
            'Item_Quantity': quantity,
            'Item_Rate': rate,
            'Item_Total': int(quantity) * (int(rate) * int(days)),
            'NIC': str(nic),
            'For_Days': int(days),

        })

    conn.commit()
    conn.close()


def entry_in_invoices(name, discount):
    datex = str(datetime.datetime.now()).split(".")
    date_and_time = str(datex[0]).split(" ")
    date = date_and_time[0]
    time = date_and_time[1]
    inventory_id = 0
    conn = sqlite3.connect("data.db")

    c = conn.cursor()

    fetch_values = c.execute("SELECT Invoice_id, oid FROM Invoices")

    for value in fetch_values:
        if value is None:
            pass
        else:
            if inventory_id < int(value[0]):
                inventory_id = int(value[0])

    c.execute("INSERT INTO Invoices VALUES (:Invoice_id, :Date, :Time, :Customer_Name, :Order_Status, :Discount)",
              {
                  'Invoice_id': inventory_id + 1,
                  'Date': date,
                  'Time': time,
                  'Customer_Name': name,
                  'Order_Status': "Item Given",
                  'Discount': discount
              })

    conn.commit()
    conn.close()


def entry_in_lost(item, quantity, narration):
    datex = str(datetime.datetime.now()).split(".")
    date_and_time = str(datex[0]).split(" ")
    date = date_and_time[0]
    time = date_and_time[1]
    conn = sqlite3.connect("data.db")

    c = conn.cursor()

    c.execute("INSERT INTO Lost_Items VALUES (:Date, :Time, :Item_Name, :Item_Quantity, :Narration)",
              {
                  'Date': date,
                  'Time': time,
                  'Item_Name': item,
                  'Item_Quantity': quantity,
                  'Narration': narration
              })

    conn.commit()
    conn.close()


def fetch_lost_items(item):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    quantity_lost = 0

    fetch = c.execute("select Inventory_ID, Item_Removed FROM Inventory_Status where Inventory_ID=" + str(
        item) + " AND Narration like '%D/L: %'")

    for value in fetch:
        quantity_lost += int(value[1])

    return quantity_lost

    conn.commit()
    conn.close()


def get_current_quantity(inventory_id):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    quantity = 0

    fetch_items = c.execute(
        "SELECT Inventory_ID, Item_Added, Item_Removed FROM Inventory_Status WHERE Inventory_ID=" + str(inventory_id))

    for items in fetch_items:

        if items[1] == "":
            add = 0
        else:
            add = int(items[1])
        if items[2] == "":
            remove = 0
        else:
            remove = int(items[2])
        quantity += add - remove

    return quantity

    conn.commit()
    conn.close()


def get_total_quantity(inventory_id):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    fetch_items = c.execute("SELECT Item_Added, Narration FROM Inventory_Status WHERE Inventory_ID=" + str(
        inventory_id) + " AND Narration='Purchased'")

    total_quantity = 0

    for value in fetch_items:
        total_quantity += int(value[0])

    return total_quantity - int(fetch_lost_items(inventory_id))

    conn.commit()
    conn.close()


def get_Item_Given_Invoices():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    fetch = c.execute("""SELECT Invoice_id, Date, Time, Customer_Name FROM Invoices WHERE Order_Status='Item Given' """)

    return fetch

    conn.commit()
    conn.close()


def get_customer_name_from_invoices(invoice_no):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    fetch = c.execute("""SELECT Invoice_id, Customer_Name FROM Invoices WHERE Invoice_id=""" + str(invoice_no))

    customer_name = ""

    for items in fetch:
        customer_name = items[1]

    return customer_name

    conn.commit()
    conn.close()


def get_invoices_of_customers(customer):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    fetch = c.execute(
        """SELECT Invoice_id, Date, Customer_Name FROM Invoices WHERE Customer_Name='""" + str(customer) + "'")

    return fetch

    conn.commit()
    conn.close()


def get_customers_from_invoices():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    fetch = c.execute("""SELECT Invoice_id, Customer_Name, Order_Status, Date FROM Invoices""")

    return fetch

    conn.commit()
    conn.close()


def get_Item_Given_Invoices_of_customer(customer):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    fetch = c.execute(
        """SELECT Invoice_id, Date, Time, Customer_Name FROM Invoices WHERE Order_Status='Item Given' AND Customer_Name ='""" + customer + "'")

    return fetch

    conn.commit()
    conn.close()


def get_Item_Given_of_invoice_no_from_inventory_ledger(invoice_no):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    stock = c.execute("""
        SELECT Inventory.Item_Name, Item_Quantity, Inventory_Ledger.Date, Customer_Contact_No, Inventory_Ledger.Item_Total
        FROM Inventory_Ledger JOIN Inventory ON Inventory_Ledger.Item_Name = Inventory.Inventoryid
        WHERE Invoice_id=""" + str(invoice_no))

    return stock

    conn.commit()
    conn.close()


def get_specific_Item_Given_of_invoice_no_from_inventory_ledger(invoice_no, item):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    stock = c.execute("""
        SELECT Inventory.Item_Name, Item_Quantity, Customer_Name
        FROM Inventory_Ledger JOIN Inventory ON Inventory_Ledger.Item_Name = Inventory.Inventoryid
        WHERE Invoice_id=""" + str(invoice_no) + " AND Inventory_Ledger.Item_Name = '" + str(item) + "'")

    return stock

    conn.commit()
    conn.close()


def get_damaged_item_from_lost_items():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    stock = c.execute("""
        SELECT Lost_Items.Date, Lost_Items.Time, Inventory.Item_name, Item_Quantity, Narration
        FROM Lost_Items JOIN Inventory ON Lost_Items.Item_Name = Inventory.Inventoryid ORDER BY Lost_Items.Date""")

    return stock

    conn.commit()
    conn.close()


def received_back_inventory(invoice_no, customer):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c2 = conn.cursor()
    c3 = conn.cursor()

    stock = c.execute("""
    SELECT Invoice_id, Item_Name, Item_Quantity FROM Inventory_Ledger WHERE Invoice_id=
    """ + str(invoice_no))

    for item in stock:
        date = str(datetime.datetime.now()).split(".")
        date_time = date[0].split(" ")

        c2.execute(
            "INSERT INTO Inventory_Status VALUES (:Date, :Inventory_ID, :Item_Added, :Item_Removed, :Narration, :Time, :Invoice_id)",
            {
                'Date': date_time[0],
                'Inventory_ID': int(item[1]),
                'Item_Added': int((item[2])),
                'Item_Removed': "",
                'Narration': "Returned By Customer " + str(customer),
                'Time': date_time[1],
                'Invoice_id': int(invoice_no)

            })

    c3.execute("""UPDATE Invoices SET
                           Order_Status = :Order_Status

                           WHERE Invoice_id = :Invoice_id""",
               {
                   'Order_Status': "Item Received Back",
                   'Invoice_id': int(invoice_no)
               })

    conn.commit()
    conn.close()


def delete_invoice_from_data(invoice_no):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c2 = conn.cursor()
    c3 = conn.cursor()

    c.execute("""
    DELETE FROM Invoices WHERE Invoice_id=
    """ + str(invoice_no))

    c2.execute("""
    DELETE FROM Inventory_Ledger WHERE Invoice_id=
    """ + str(invoice_no))

    c3.execute("""
    DELETE FROM Inventory_Status WHERE Invoice_id=
    """ + str(invoice_no))

    conn.commit()
    conn.close()


def store_discount_on_invoice(invoice, discount):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    c.execute("""UPDATE Invoices SET                            
                            Discount = :Discount

                            WHERE Invoice_id = :Invoice_id""",
              {
                  'Discount': int(discount),
                  'Invoice_id': int(invoice)
              })

    conn.commit()
    conn.close()


def fetch_discount_on_invoice(invoice):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    discount_amount = 0

    discount = c.execute("""
     SELECT Discount, oid FROM Invoices WHERE Invoice_id=
     """ + str(invoice))

    for value in discount:
        discount_amount = value[0]

    return discount_amount

    conn.commit()
    conn.close()


def get_specific_damaged_item_from_lost_items(invenotry_id):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    stock = c.execute("""
        SELECT Inventory.Item_name, Item_Quantity, Narration
        FROM Lost_Items JOIN Inventory ON Lost_Items.Item_Name = Inventory.Inventoryid WHERE Lost_Items.Item_Name =""" + str(
        invenotry_id))

    return stock

    conn.commit()
    conn.close()


def get_invoices_with_date_range(from_date, to_date):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    stock = c.execute("""
        SELECT Date, Invoice_id, Customer_Name, Order_Status, Discount
        FROM Invoices WHERE Date BETWEEN '""" + str(from_date) + """' AND '""" + str(to_date) + "' ORDER BY Date")

    return stock

    conn.commit()
    conn.close()


def get_items_with_date_range(from_date, to_date, item):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    stock = c.execute("""
        SELECT Item_Quantity, Item_Total
        FROM Inventory_Ledger WHERE Date BETWEEN '""" + str(from_date) + """' AND '""" + str(
        to_date) + "' AND Item_Name= '" + str(item) + "'")

    quantity_total = 0
    item_price_total = 0
    for values in stock:
        quantity_total += int(values[0])
        item_price_total += int(values[1])

    return quantity_total, item_price_total

    conn.commit()
    conn.close()


def get_items_damaged_with_date_range(from_date, to_date, item):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    stock = c.execute("""
        SELECT Item_Quantity, Narration
        FROM Lost_Items WHERE Date BETWEEN '""" + str(from_date) + """' AND '""" + str(
        to_date) + "' AND Item_Name= '" + str(item) + "'")

    damaged_quantity_total = 0
    for values in stock:
        damaged_quantity_total += int(values[0])

    return damaged_quantity_total

    conn.commit()
    conn.close()


def get_total_discounts_with_date_range(from_date, to_date):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    stock = c.execute("""
        SELECT Discount, Customer_Name
        FROM Invoices WHERE Date BETWEEN '""" + str(from_date) + """' AND '""" + str(to_date) + "'")

    disount_total = 0
    for values in stock:
        disount_total += int(values[0])

    return disount_total

    conn.commit()
    conn.close()


def get_invoices_total_item_given(invoice_no):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    stock = c.execute("""
        SELECT Item_Quantity, Item_Total FROM Inventory_Ledger WHERE Invoice_id=""" + str(invoice_no))

    total_quantity = 0
    total_amount = 0

    for value in stock:
        total_quantity += value[0]
        total_amount += value[1]

    return total_quantity, total_amount

    conn.commit()
    conn.close()


def validate_item_type(item):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    stock = c.execute("""
        SELECT Item_Type, Item_Name FROM Inventory WHERE LOWER(Item_Type) LIKE '""" + str(item) + "'")

    item_type = ""
    for i in stock:
        item_type = i[0]

    if str(item_type).lower() == str(item).lower():
        return True
    else:
        return False

    conn.commit()
    conn.close()


def validate_item_name(item):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    stock = c.execute("""
        SELECT Item_Type, Item_Name FROM Inventory WHERE LOWER(Item_Name) LIKE '""" + str(item) + "'")

    item_type = ""
    for i in stock:
        item_type = i[1]

    if str(item_type).lower() == str(item).lower():
        return True
    else:
        return False

    conn.commit()
    conn.close()


def items_to_be_deliverd_today():
    datex = str(datetime.datetime.now()).split(".")
    date_and_time = str(datex[0]).split(" ")
    date = date_and_time[0]
    invoices = []
    today = []

    conn = sqlite3.connect("data.db")

    c = conn.cursor()
    c2 = conn.cursor()

    stock = c.execute("""
            SELECT Inventory_Ledger.Invoice_id, Invoices.Order_Status
            FROM Inventory_Ledger JOIN Invoices ON Invoices.Invoice_id = Inventory_Ledger.Invoice_id WHERE Customer_Delivery_Date='""" + str(
        date) + "' AND Order_Status='Item Given'")

    for i in stock:
        if i[0] not in invoices:
            invoices.append(i[0])

    for invoice in stock:
        if invoice[0] not in invoices:
            invoices.append(invoice[0])

    for i in invoices:
        stock2 = c.execute("""
                SELECT Invoice_id, Customer_Name FROM Invoices WHERE Invoice_id=""" + str(i))
        for j in stock2:
            today.append(j)

    return today

    conn.commit()
    conn.close()


def temporary():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    c.execute("""
    DELETE FROM Invoices;
    """)

    conn.commit()
    conn.close()

