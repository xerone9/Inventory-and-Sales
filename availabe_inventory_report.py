from fpdf import FPDF
from sql_working import *
import datetime
import os

def available_inventory_report():
    class PDF(FPDF):
        def header(self):
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
            self.cell(90, 20, 'AVAILABLE INVENTORY', border=True, ln=0, align='C')
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

            self.set_fill_color(r=150, g=230, b=150)
            self.cell(15, 10, "S.No", border=True, ln=0)
            self.cell(60, 10, "Item Type", border=True, ln=0)
            self.cell(60, 10, "Item Name", border=True, ln=0)
            self.cell(25, 10, "Rate", border=True, ln=0)
            self.cell(28, 10, "Quantity", border=True, ln=1)

        # Page footer
        def footer(self):
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
    pdf.set_auto_page_break(auto = True, margin = 50)

    #Add Page
    pdf.add_page()

    # specify font
    pdf.set_font('times', '', 16)

    count = 0
    list = []
    for value in inventory_Register():
        if value[0] + "-" + value[1] not in list:
            list.append(value[0] + "-" + value[1])

    list.sort()

    items = []
    for value in list:
        breaking_items = str(value).split("-")
        items.append(breaking_items[1])

    for value in items:
        pdf.set_font('times', '', 16)
        count += 1
        inventory_type = get_inventory_type(str(get_inventory_id(str(value))))
        inventory_name = value
        inventory_rate = get_inventory_rate(str(get_inventory_id(str(value))))
        inventory_available_quantity = get_current_quantity(get_inventory_id(str(value)))

        pdf.cell(1)
        pdf.cell(15, 10, str(count), border=True, ln=0)
        pdf.set_font('times', 'B', 14)
        pdf.cell(60, 10, str(inventory_type), border=True, ln=0)
        pdf.set_font('times', 'I', 16)
        pdf.cell(60, 10, str(inventory_name), border=True, ln=0)
        pdf.set_font('times', '', 16)
        pdf.cell(25, 10, str(inventory_rate) + " Rs.", border=True, ln=0)
        pdf.set_font('times', 'B', 16)
        pdf.cell(28, 10, str("{:,}".format(inventory_available_quantity)), border=True, ln=1)






    #
    #
    # discount = fetch_discount_on_invoice(invoice_no)
    #
    # pdf.cell(141)
    # pdf.set_font('helvetica', 'B', 16)
    # pdf.cell(30, 10, "Discount:     -" + "{:,}".format(discount), border=0, ln=1)
    #
    # pdf.ln(5)
    #
    # payable = int(grand_total) - int(discount)
    #
    # pdf.cell(142)
    # pdf.set_font('helvetica', 'B', 16)
    # pdf.cell(50, 10, "Payable:      " + "{:,}".format(payable), border=1, ln=1)

    pdf.output('pdf.pdf')
    os.startfile('pdf.pdf')



