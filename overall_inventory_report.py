from fpdf import FPDF
from sql_working import *
import datetime
import os

def overall_inventory_report():
    class PDF(FPDF):
        def header(self):
            pdf.set_text_color(0, 0, 0)
            date_complete = str(datetime.datetime.now()).split(".")
            date_and_time = date_complete[0].split(" ")
            date = date_and_time[0]
            time = date_and_time[1]

            # Logo
            self.image('logo.png', 10, 8, 55)
            self.ln(5)
            # font
            self.set_font('helvetica', 'B', 20)
            # Padding
            self.cell(60)
            # Title
            self.cell(90, 20, 'Overall Inventory', border=True, ln=0, align='C')
            self.set_font('helvetica', '', 12)
            self.cell(80, 10, '', border=False, ln=1, align='R')
            # Line break
            self.ln(25)
            # font
            self.set_font('helvetica', 'B', 12)
            self.cell(40, 6, 'Date: ' + str(date), border=False, ln=0, align='L')
            self.cell(150, 6, 'Time: ' + str(time), border=False, ln=1, align='R')

            # self.ln(25)

            self.set_line_width(0.5)
            self.set_draw_color(r=0, g=0, b=0)
            self.line(x1=10, y1=57, x2=200, y2=57)
            # Line break
            self.ln(7)

            self.set_font('helvetica', 'B', 16)
            self.cell(1)


        # Page footer
        def footer(self):
            pdf.set_text_color(0, 0, 0)
            # Set position of the footer
            self.set_y(-20)
            # set font

            self.cell(80)
            self.set_font('helvetica', 'B', 10)
            line1 = 'SET FOOTERS IN "enter_footer_here.ini" FILE'
            line2 = 'SET FOOTERS IN "enter_footer_here.ini" FILE'
            try:
                f = open("enter_footer_here.ini", "r")
                for x in f:
                    name = str(x)
                    if "line1" in name:
                        line1 = name.split(" = ")[1]
                    if "line2" in name:
                        line2 = name.split(" = ")[1]
                f.close()
            except FileNotFoundError:
                line1 = '"enter_footer_here.ini" file missing'
                line2 = "CONTACT SUPPORT"
            self.cell(40, 6, line1, border=False, ln=1, align='C')
            self.cell(80)
            self.cell(40, 6, line2, border=False, ln=1, align='C')


            self.cell(0, 2, f'Page {self.page_no()}/{{nb}}', align='R')
            self.set_line_width(0.5)
            self.set_draw_color(r=0, g=0, b=0)
            self.line(x1=10, y1=270, x2=200, y2=270)

    # Create a PDF object
    pdf = PDF('P', 'mm', 'A4')

    # get total page numbers
    pdf.alias_nb_pages()

    # Set auto page break
    pdf.set_auto_page_break(auto = True, margin = 30)

    #Add Page
    pdf.add_page()

    # specify font
    pdf.set_font('times', '', 16)

    item_types = []
    for types in fetch_inventory_types():
        if types != "Other":
            item_types.append(types)

    pdf.cell(1)

    for type in item_types:
        pdf.cell(85)
        pdf.set_font('helvetica', 'B', 25)
        pdf.cell(28, 10,"*** " + str(type).upper() + " ***", border=False, ln=1, align='C')
        for item in fetch_item_names(str(type)):
            pdf.set_font('times', 'IU', 19)
            pdf.cell(28, 10, str(item), border=False, ln=1)
            inventory_id = get_inventory_id(item)
            damaged_inventory = get_specific_damaged_item_from_lost_items(inventory_id)
            total_damage = 0
            for damage in damaged_inventory:
                total_damage += int(damage[1])
            total_quantity = int(get_total_quantity(inventory_id)) + total_damage
            available_quantity = get_current_quantity(inventory_id)
            pdf.cell(10)
            pdf.set_font('times', 'B', 14)
            pdf.cell(28, 10, "Total Quantity:", border=False, ln=0, align='L')
            pdf.cell(140, 10, '"Purchased"', border=False, ln=0, align='C')
            pdf.cell(1, 10, str(total_quantity), border=False, ln=1, align='R')
            pdf.set_font('times', '', 14)
            for values in get_Item_Given_Invoices():
                for items in get_Item_Given_of_invoice_no_from_inventory_ledger(values[0]):
                    if items[0] == item:
                        item_names = get_inventory_id(item)
                        for products in get_specific_Item_Given_of_invoice_no_from_inventory_ledger(values[0], item_names):
                            pdf.cell(10)
                            pdf.cell(28, 10, "Item Given:", border=False, ln=0, align="L")
                            pdf.cell(140, 10, "To Customer " + str(products[2]), border=False, ln=0, align="C")
                            pdf.cell(1, 10, "(" + str(products[1]) + ")", border=False, ln=1, align="R")
            damaged_inventory = get_specific_damaged_item_from_lost_items(inventory_id)

            for damage in damaged_inventory:
                pdf.cell(10)
                damaged_quantity = damage[1]
                damaged_narration = damage[2]
                pdf.cell(28, 10, "Damaged quantity:", border=False, ln=0, align="L")
                pdf.cell(140, 10, str(damaged_narration), border=False, ln=0, align="C")
                pdf.cell(1, 10, "(" + str(damaged_quantity) + ")", border=False, ln=1, align="R")
            pdf.cell(10)
            pdf.set_font('times', 'B', 14)
            pdf.cell(28, 10, "Available Quantity:", border=False, ln=0, align="L")
            pdf.cell(140, 10, '"In Stock"', border=False, ln=0, align="C")
            pdf.cell(1, 10, str(available_quantity), border=False, ln=1, align="R")
            pdf.set_font('times', '', 14)
            pdf.ln(5)

        pdf.ln(5)







    pdf.output('pdf.pdf')
    os.startfile('pdf.pdf')







