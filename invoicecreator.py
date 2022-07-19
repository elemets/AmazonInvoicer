from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import time


def create_invoice(data):
  invoice_counter = 10

  file_name = "FBAInvoice" + str(invoice_counter) + ".pdf"

  doc = SimpleDocTemplate(
    file_name,
    pagesize=letter,
    rightMargin=72,
    leftMargin=72,
    topMargin=72,
    bottomMargin=18
  )

  Story=[]

  formatted_time = time.ctime()
  company_name = "Invoice, SmallStoreUK FBA"
  full_name = "Arthur Funnell"
  address_parts = ["3 Rockfield Terrace", "Talyllyn", "Brecon", "Powys"]

  styles=getSampleStyleSheet()
  styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

  styles.add(ParagraphStyle(
      name= 'right',
      parent=styles['Normal'],
      leftIndent= 350
  ))

  styles.add(ParagraphStyle(
      name='centre',
      parent=styles['Normal'],
      alignment = TA_JUSTIFY
  ))

  invoice_counter_as_str = str(invoice_counter)
  invoice_string = "Invoice no. " + str(invoice_counter)

  ptext = '<font size="12">%s</font>' % company_name
  Story.append(Paragraph(ptext, styles["Normal"]))
  ptext = '<font size="12">%s</font>' % formatted_time
  Story.append(Paragraph(ptext, styles["Normal"]))
  Story.append(Spacer(1,12))
  ptext = '<font size="10">%s</font>' % invoice_string
  Story.append(Paragraph(ptext, styles["right"]))
  ptext = '<font size="10">%s</font>' % "Date of purchase:"
  Story.append(Paragraph(ptext, styles["right"]))
  ptext = '<font size="10">%s</font>' % "the date of purchase"
  Story.append(Paragraph(ptext, styles["right"]))
  Story.append(Spacer(1, 4))
  # creating the business address
  ptext = '<i><font size="12">%s</font></i>' % "Business address"
  Story.append(Paragraph(ptext, styles["right"]))
  Story.append(Spacer(1, 4))
  ptext = '<font size="10">%s</font>' % "SmallStoreUK"
  Story.append(Paragraph(ptext, styles["right"]))
  ptext = '<font size="10">%s</font>' % "3 Rockfield Terrace"
  Story.append(Paragraph(ptext, styles["right"]))
  ptext = '<font size="10">%s</font>' % "Talyllyn"
  Story.append(Paragraph(ptext, styles["right"]))
  ptext = '<font size="10">%s</font>' % "Brecon"
  Story.append(Paragraph(ptext, styles["right"]))
  ptext = '<font size="10">%s</font>' % "Powys"
  Story.append(Paragraph(ptext, styles["right"]))
  ptext = '<font size="10">%s</font>' % "LD3 7TB"
  Story.append(Paragraph(ptext, styles["right"]))
  Story.append(Spacer(1, 12))

  ## This is customers address 
  ptext = '<i><font size="12">%s</font></i>' % "Shipped to"
  Story.append(Paragraph(ptext, styles["Normal"]))
  Story.append(Spacer(1, 4))
  ptext = '<font size="10">%s</font>' % "Name of Person"
  Story.append(Paragraph(ptext, styles["Normal"]))
  ptext = '<font size="10">%s</font>' % "Address line 1"
  Story.append(Paragraph(ptext, styles["Normal"]))
  ptext = '<font size="10">%s</font>' % "Address line 2"
  Story.append(Paragraph(ptext, styles["Normal"]))
  ptext = '<font size="10">%s</font>' % "State or Region"
  Story.append(Paragraph(ptext, styles["Normal"]))
  ptext = '<font size="10">%s</font>' % "Post code"
  Story.append(Paragraph(ptext, styles["Normal"]))
  ptext = '<font size="10">%s</font>' % "Country"
  Story.append(Paragraph(ptext, styles["Normal"]))
  Story.append(Spacer(1, 36))

  # defining elements in the table
  quantity_of_units = 1
  product_title = "USB c to HDMI KEBIDU HDMI CHARGER CONVERTOR OR JUST GENERAL CABLE..."
  unit_price = 8.99
  total = unit_price * quantity_of_units

  quantity_of_units2, product_title2, unit_price2 = '', '', ''

  total2 = 0.00

  quantity_of_units3, product_title3, unit_price3 = '', '', ''

  total3 = 0.00

  data = [['Quantity', 'Product Title', 'Unit Price', 'Total'],
  [quantity_of_units, product_title, unit_price, '£' + str(total) ],
  [quantity_of_units2, product_title2, unit_price2, '£' + str(total2)],
  [quantity_of_units3, product_title3, unit_price3, '£' + str(total3)],
  ['', '', 'SUBTOTAL', "£" + str(total + total3 + total2)],
  ['', '', 'TAXES', '£0.00'],
  ['', '', 'DUE', "£" + str(total + total3 + total2) ]]

  table = Table(data)

  table.setStyle(TableStyle([
  ('TEXTCOLOR',(1,1), (1,1),colors.blue),
  ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
  ('BOX', (0,0), (-1,-1), 0.25, colors.black)
  ]))

  Story.append(table)
  Story.append(Spacer(1, 50))
  ptext = '<font size="8">%s</font>' % "If you have any questions or feel like you were sent this as a mistake please do not hesitate to contact us at:"
  Story.append(Paragraph(ptext, styles["centre"]))
  Story.append(Spacer(1, 4))

  ptext = '<font size="8">%s</font>' % "Phone number: 07583202801"
  Story.append(Paragraph(ptext, styles["centre"]))
  Story.append(Spacer(1, 4))
  ptext = '<font size="8">%s</font>' % "Email Address: alafunnell@gmail.com"
  Story.append(Paragraph(ptext, styles["centre"]))

  doc.build(Story)