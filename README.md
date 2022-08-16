# Inventory-and-Sales Application
 Inventory Add, Sales, Invoices
 
 _An application that stores and track the record of your inventory. Suitable for rent out inventory business_
 

## Options in the program:


1- Add Inventory with Price

2- Add Quantity

3- View Invnetory

4- Remove Inventory

5- Change Price

6- Add Damaged Inventory Quantity with Narration

7- Quick Estimate Calculator with print Option

8- Generate Invoice with print option.
_All Invoices Will Be Stored by the company names folder in OS standard documents folder_

9- View Old Invoices (shows list with print button)

10- View Only Those Invoces whom items are not delivered yet (shows list with print button)

11- Delete Invoices (Only Those Invoices can be deleted from recored whose items are not received back yet). 
_Invoices Will Also Be deleted from the company names folder in OS standard documents folder_

12- Receive Back Inventory



## Reports Designed:


1- Bill Receipt

2- Over All Inventory Report

3- Available Inventory Report

5- Damaged Inventory Report

6- Over All Orders (Date Ranged Must Be Given First)

7- Orders Whose items are not received back yet Report

8- Completed Orders report (Date Ranged Must Be Given First)

9- Sales Report (Date Ranged Must Be Given First)

## Customization

You can set Compamny name in enter_company_name.ini

You can set Compamny name in enter_footer_here.ini max 2 lines

## Note:

This software will create a folder by company_name + invoices in Documents folder and store invoices there. So if you change the compnay name later onwards another folder will be created in documents folder and all new invoices will be stroed there and you wont be able to delete old invoices after changing the name. So it is recommended that set the company name first

It is also recommended that set chrome as default PDF Viewer if not then close any opened PDF report first then open another one

______________________________________________________________________________________________________________
### Development:
In python _with native programming skills_

For front end tkinter is used

For reports FPDF library is used

For database store and management SQLITE3 library is used

### Compatiblility:
Windows 7 sp1 or above

______________________________________________________________________________________________________________
### Oracle Apex:
Redesigning the same project in Oracle Apex. (Learning Purpose)

You are free to see and test the app

Link: https://apex.oracle.com/pls/apex/r/rubick_erp/caterers-inventory-manager/login?session=3393113222158

ID: user

Pass: 123456789

