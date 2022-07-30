from fpdf import FPDF
from sql_working import *
import datetime
import os

def quick_estimate_report(item_cart):
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
            self.cell(70)
            # Title
            self.cell(60, 10, 'Raw Estimate', border=True, ln=0, align='C')
            self.set_font('helvetica', '', 12)
            # Line break
            self.ln(15)
            self.cell(80, 10, '', border=False, ln=1, align='R')
            self.cell(40, 6, 'Date: ' + str(date), border=False, ln=0, align='L')
            self.cell(150, 6, 'Time: ' + str(time), border=False, ln=1, align='R')
            # font
            self.set_line_width(0.5)
            self.set_draw_color(r=0, g=0, b=0)
            self.line(x1=10, y1=50, x2=200, y2=50)
            # Line break

            self.ln(10)
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

    for i in item_cart:
        print(i)

    serial = 0
    grand_total = 0

    pdf.set_font('times', '', 12)

    for items in item_cart:
        item = items.split("*")
        serial += 1
        pdf.cell(1)
        pdf.cell(15, 10, str(serial), border=True, ln=0)
        pdf.cell(40, 10, str(item[0]), border=True, ln=0)
        pdf.cell(45, 10, str(item[1]), border=True, ln=0)
        pdf.cell(22, 10, str(item[3]), border=True, ln=0)
        pdf.cell(30, 10, str(item[2]), border=True, ln=0)
        pdf.cell(20, 10, str(item[4]), border=True, ln=0)
        sub_total = int(item[2]) * int(item[3]) * int(item[4])
        grand_total += sub_total
        pdf.cell(18, 10, str("{:,}".format(sub_total)), border=True, ln=1)
    pdf.cell(1)
    pdf.set_font('helvetica', 'B', 16)
    pdf.cell(190, 10, "Grand Total:    " + str("{:,}".format(grand_total)) + " ", border=True, ln=1, align='R')




    pdf.output('pdf.pdf')
    os.startfile('pdf.pdf')


