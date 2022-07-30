from fpdf import FPDF
from sql_working import *
import datetime
import os

def completed_report(from_date, to_date):
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
            self.cell(65, 20, 'Completed Orders', border=True, ln=0, align='C')
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

            self.set_fill_color(r=150, g=230, b=150)
            self.cell(10, 10, "S.No", border=True, ln=0)
            self.cell(20, 10, "Date", border=True, ln=0)
            self.cell(20, 10, "Invoice No", border=True, ln=0)
            self.cell(43, 10, "Customer Name", border=True, ln=0)
            self.cell(22, 10, "Items Given", border=True, ln=0)
            self.cell(16, 10, "Amount", border=True, ln=0)
            self.cell(19, 10, "Discounts", border=True, ln=0)
            self.cell(14, 10, "Paid", border=True, ln=0)
            self.cell(25, 10, "Status", border=True, ln=1)

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
    pdf.set_auto_page_break(auto = True, margin = 50)

    #Add Page
    pdf.add_page()

    # specify font
    pdf.set_font('helvetica', '', 10)

    serial = 0
    for value in get_invoices_with_date_range(str(from_date), str(to_date)):
        if value[3] == "Item Given":
            pass
        else:
            pdf.cell(1)
            serial += 1
            pdf.cell(10, 10, str(serial), border=True, ln=0)
            pdf.cell(20, 10, str(value[0]), border=True, ln=0)
            pdf.cell(20, 10, str(value[1]), border=True, ln=0)
            pdf.cell(43, 10, str(value[2]), border=True, ln=0)
            item_given = get_invoices_total_item_given(value[1])
            pdf.cell(22, 10, str(item_given[0]), border=True, ln=0)
            total_amount = get_invoices_total_item_given(value[1])
            pdf.cell(16, 10, str("{:,}".format(total_amount[1])), border=True, ln=0)
            pdf.cell(19, 10, str(value[4]), border=True, ln=0)
            paid_amount = int(get_invoices_total_item_given(value[1])[1]) - int(value[4])
            pdf.cell(14, 10, str("{:,}".format(paid_amount)), border=True, ln=0)
            status_split = str(value[3]).split(" ")
            status = status_split[0] + " " + status_split[1]
            pdf.cell(25, 10, str(status), border=True, ln=1)




    pdf.output('pdf.pdf')
    os.startfile('pdf.pdf')








