from fpdf import FPDF
from sql_working import *
import datetime
import os

def sales_report(from_date, to_date):
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
            self.cell(70)
            # Title
            self.cell(60, 20, 'SALES REPORT', border=True, ln=0, align='C')
            self.set_font('helvetica', '', 12)
            self.cell(80, 10, '', border=False, ln=1, align='R')
            # Line break
            self.ln(25)
            # font
            self.set_font('helvetica', 'B', 12)
            self.cell(40, 6, 'From Date: ' + str(from_date), border=False, ln=0, align='L')
            self.cell(150, 6, 'To Date: ' + str(to_date), border=False, ln=1, align='R')

            # self.ln(25)

            self.set_line_width(0.5)
            self.set_draw_color(r=0, g=0, b=0)
            self.line(x1=10, y1=57, x2=200, y2=57)
            # Line break
            self.ln(7)

            self.set_font('helvetica', 'B', 10)
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
    pdf.set_font('helvetica', '', 10)

    item_types = []
    for types in fetch_inventory_types():
        if types != "Other":
            item_types.append(types)

    pdf.cell(1)
    pdf.set_text_color(0, 0, 0)

    sales_total = 0

    for type in item_types:
        pdf.set_text_color(0, 0, 0)
        pdf.cell(57)
        pdf.set_font('helvetica', 'B', 25)
        pdf.cell(28, 10, "*** " + str(type).upper() + " ***", border=False, ln=1)
        pdf.ln(10)
        for item in fetch_item_names(str(type)):
            pdf.set_text_color(0, 0, 0)
            pdf.set_font('times', 'IU', 19)
            pdf.cell(28, 10, str(item), border=False, ln=1)
            inventory_id = get_inventory_id(item)
            pdf.cell(5)
            pdf.set_font('times', '', 19)
            item_total_quantity_and_total_price = get_items_with_date_range(from_date, to_date, inventory_id)
            pdf.cell(28, 10, "Total Quantity Given: " + str("{:,}".format(item_total_quantity_and_total_price[0])), border=False, ln=1)
            pdf.cell(5)
            pdf.cell(28, 10, "At Price (Excluding Discounts): ", border=False, ln=0, align="L")
            pdf.cell(120)
            pdf.cell(28, 10, str("{:,}".format(item_total_quantity_and_total_price[1])), border=False, ln=1, align="R")
            sales_total += int(item_total_quantity_and_total_price[1])
            pdf.cell(5)
            item_damaged_quantity = get_items_damaged_with_date_range(from_date, to_date, inventory_id)
            if item_damaged_quantity != 0:
                pdf.set_font('times', 'I', 14)
                pdf.set_text_color(255, 0, 0)
                pdf.cell(28, 10, "Quantity Lost/Damaged During The Period: " + str(item_damaged_quantity), border=False, ln=1)
            pdf.ln(7)
        pdf.ln(20)

    pdf.cell(75)
    pdf.cell(55, 10, "Sales:           " + str("{:,}".format(sales_total)), border=True, ln=1)
    pdf.cell(75)
    pdf.cell(40, 10, "Discount:     " + str("{:,}".format(get_total_discounts_with_date_range(from_date, to_date))), border=False, ln=1)
    pdf.ln(10)
    pdf.cell(55)
    pdf.set_font('helvetica', '', 32)
    pdf.cell(40, 10, "Revenue: " + str("{:,}".format(int(sales_total) - int(get_total_discounts_with_date_range(from_date, to_date)))),
             border=False, ln=1)

    pdf.output('pdf.pdf')
    os.startfile('pdf.pdf')











