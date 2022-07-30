from fpdf import FPDF
from sql_working import *
import datetime
import os

def temporary_invioce_print(invoice_no):
    class PDF(FPDF):
        def header(self):
            date_complete = str(datetime.datetime.now()).split(".")
            date_and_time = date_complete[0].split(" ")
            date = date_and_time[0]

            global customer_name
            customer_details = fetch_customer_details_from_inventory_ledger(invoice_no)
            customer_name = customer_details[0]
            customer_contact_no = customer_details[1]
            customer_nic_no = customer_details[5]
            customer_delivery_date = customer_details[2]
            customer_address = customer_details[3]
            invoice_date = customer_details[4]


            # Logo
            self.image('logo.png', 10, 8, 55)
            self.ln(5)
            # font
            self.set_font('helvetica', 'B', 20)
            # Padding
            self.cell(70)
            # Title
            self.cell(60, 10, 'BILL RECEIPT', border=True, ln=0, align='C')
            self.set_font('helvetica', '', 12)
            self.cell(80, 10, '', border=False, ln=1, align='R')
            # Line break
            self.ln(15)
            # font
            self.set_font('helvetica', 'B', 12)
            self.cell(40, 6, 'Customer Name: ' + customer_name, border=False, ln=0, align='L')
            self.cell(150, 6, 'Delivery Date: ' + customer_delivery_date, border=False, ln=1, align='R')
            self.cell(40, 6, 'Customer No: ' + customer_contact_no, border=False, ln=0, align='L')
            self.cell(150, 6, 'Invoice Date : ' + invoice_date, border=False, ln=1, align='R')
            self.cell(40, 6, 'Customer NIC: ' + customer_nic_no, border=False, ln=0, align='L')
            self.cell(150, 6, 'Invoice Number:      ' + str(invoice_no), border=False, ln=1, align='R')
            self.cell(40, 6, 'Customer Address: ' + customer_address, border=False, ln=1, align='L')

            self.set_line_width(0.5)
            self.set_draw_color(r=0, g=0, b=0)
            self.line(x1=10, y1=65, x2=200, y2=65)
            # Line break
            self.ln(5)

            self.set_font('times', 'B', 12)
            self.cell(1)

            self.set_fill_color(r=150, g=230, b=150)
            self.cell(15, 10, "S.No", border=True, ln=0)
            self.cell(40, 10, "Item Type", border=True, ln=0)
            self.cell(45, 10, "Item Name", border=True, ln=0)
            self.cell(22, 10, "Item Rate", border=True, ln=0)
            self.cell(30, 10, "Item Quantity", border=True, ln=0)
            self.cell(20, 10, "For Days", border=True, ln=0)
            self.cell(18, 10, "Total", border=True, ln=1)

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
    pdf.set_font('helvetica', 'BIU', 16)



    inventory = current_invoice(invoice_no)

    serial = 0
    grand_total = 0



    pdf.set_font('times', '', 12)

    for item in inventory:
        serial += 1
        grand_total += int(item[4])
        pdf.cell(1)
        pdf.cell(15, 10, str(serial), border=True, ln=0)
        pdf.cell(40, 10, str(item[0]), border=True, ln=0)
        pdf.cell(45, 10, str(item[1]), border=True, ln=0)
        pdf.cell(22, 10, str(item[2]), border=True, ln=0)
        pdf.cell(30, 10, str(item[3]), border=True, ln=0)
        pdf.cell(20, 10, str(item[6]), border=True, ln=0)
        pdf.cell(18, 10, str("{:,}".format(item[4])), border=True, ln=1)
    pdf.cell(1)
    pdf.set_font('helvetica', 'B', 16)
    pdf.cell(190, 10, "Grand Total:    " + str("{:,}".format(grand_total)) + " ", border=True, ln=1, align='R')


    discount = fetch_discount_on_invoice(invoice_no)
    if discount != 0:
        pdf.cell(141)
        pdf.set_font('helvetica', 'B', 16)
        pdf.cell(30, 10, "Discount:     -" + "{:,}".format(discount), border=0, ln=1)

        pdf.ln(5)

        payable = int(grand_total) - int(discount)

        pdf.cell(142)
        pdf.set_font('helvetica', 'B', 16)
        pdf.cell(50, 10, "Payable:      " + "{:,}".format(payable), border=1, ln=1)

    pdf.output("pdf.pdf")
    os.startfile("pdf.pdf")


