

from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import time
from DBManage import Invoice
import datetime



from sqlalchemy import create_engine, Column, Integer, desc, String, Boolean, Date, DateTime, asc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import IntegrityError
from mws import mws
import time

import os
import os.path as path



def create_invoices(marketplace):
    access_key = # #replace with your access key
    seller_id = 'A2034TBO3FX4MA' #replace with your seller id
    secret_key = # #replace with your secret key
    marketplace_uk = marketplace
    
    marketplacefolder = ''
    region = ''
    
    if marketplace == 'A1F83G8C2ARO7P':
        marketplacefolder = 'UK'
        region = 'UK'
    elif marketplace == 'APJ6JRA9NG5V4':
        marketplacefolder = 'IT'
        region = 'IT'
    elif marketplace == 'A2NODRKZP88ZB9':
        marketplacefolder = 'SW'
        region = 'SW'
    elif marketplace == 'A13V1IB3VIYZZH':
        marketplacefolder = 'FR'
        region = 'FR'
    elif marketplace == 'A1RKKUPIHCS9HS':
        marketplacefolder = 'ES'
        region = 'ES'
    elif marketplace == 'A1PA6795UKMFR9':
        marketplacefolder = 'DE'
        region = 'DE'

    date_to_go_from = '2020-05-05'
    
    Base = declarative_base()
    engine = create_engine('sqlite:///invoices.db', echo=True)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)

    # checking if any invoices exist within the directory
    session = Session()
    latest_invoice = session.query(Invoice).order_by(desc('invoice_number')).first()
    session.close()
    if latest_invoice is not None:
        next_invoice_number = int(latest_invoice.invoice_number) + 1 
        
        # date_to_go_from = latest_invoice.date_of_purchase
        # date_to_go_from = str(date_to_go_from)[:10]
    else:
        next_invoice_number = 200
    

    # this imports the orders into an object which contains all the orders created after the date specified
    orders_api = mws.Orders(access_key, secret_key, seller_id, region=region)
    orders = orders_api.list_orders(marketplaceids=[marketplace], created_after=date_to_go_from)

    # this parses the order as a dictionary so we can find the values needed
    orders_as_dict = orders.parsed

    # This gives us the orders as a list where the first element is the oldest order in the list 
    
    print(orders_as_dict)
    orders_as_list = orders_as_dict.Orders.Order

    if marketplace_uk != "A1F83G8C2ARO7P":
        currency = "€"
    else:
        currency = "£"

    list_of_all_details = []
    
    order_id_list = []

    # this is going to fetch me everything I need to build an invoice 
    # then put the relevant information into a database
    
    for orders in orders_as_list:
        if (orders.OrderStatus != "Canceled"):
            

            singular_details = []
            ## getting the shipping address of the orders
            address_of_orders = orders.ShippingAddress
            ## adding shipping address to the list
            singular_details.append(address_of_orders)
            ## getting the price of the orders
            price_of_orders = currency + str(orders.OrderTotal.Amount)
            singular_details.append(price_of_orders)
            ## getting the name of the item and waiting if the request gets blocked for being too much
            try:
                finding_item = orders_api.list_order_items(amazon_order_id=orders.AmazonOrderId).parsed.OrderItems.OrderItem.Title
            except: 
                time.sleep(40)
                finding_item = orders_api.list_order_items(amazon_order_id=orders.AmazonOrderId).parsed.OrderItems.OrderItem.Title
                print("Cool down on requests..")

            singular_details.append(finding_item)
            ## Date of Purchase
            date_of_purchase = orders.PurchaseDate
            singular_details.append(date_of_purchase)
            ## Number of units purchased
            number_of_units = orders.NumberOfItemsShipped
            singular_details.append(number_of_units)
            singular_details.append(orders.AmazonOrderId)
            order_id_list.append({ "order_id": orders.AmazonOrderId,
                                  'invoicenumber': next_invoice_number
            })
            
                       

            ## Adding orders to database with information about them
            
                
            date_of_purchase = datetime.datetime.strptime(date_of_purchase, '%Y-%m-%dT%H:%M:%S.%fZ')

            
            session = Session()

            invoice = Invoice()
            invoice.order_number = (orders.AmazonOrderId)
            invoice.invoice_number = int(next_invoice_number)
            invoice.date_of_purchase = date_of_purchase
            invoice.market_origin = region
            invoice.title = finding_item
            
            session.add(invoice)
            
            try: 
                session.commit()
                next_invoice_number += 1 
            except IntegrityError:
                session.rollback()
                session.close()
                continue


            
            
            file_name = "./Invoices/" + str(region) +"/"+ str(next_invoice_number) + "_" + str(region) + ".pdf"
        
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

            invoice_string = "Invoice no. " + str(next_invoice_number)

            ptext = '<font size="12">%s</font>' % company_name
            Story.append(Paragraph(ptext, styles["Normal"]))
            ptext = '<font size="12">%s</font>' % formatted_time
            Story.append(Paragraph(ptext, styles["Normal"]))
            Story.append(Spacer(1,12))
            ptext = '<font size="10">%s</font>' % invoice_string
            Story.append(Paragraph(ptext, styles["right"]))
            ptext = '<font size="10">%s</font>' % "Date of purchase:"
            Story.append(Paragraph(ptext, styles["right"]))
            ptext = '<font size="10">%s</font>' % str(date_of_purchase)[:-10]
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
            ptext = '<font size="10">%s</font>' % address_of_orders.Name
            Story.append(Paragraph(ptext, styles["Normal"]))
            ## checking if addressline 1 exists in the invoices dictionary then find it and print it if not don't 
            if 'AddressLine1' in address_of_orders:
                ptext = '<font size="10">%s</font>' % address_of_orders.AddressLine1
            else:
                ptext = ""
            Story.append(Paragraph(ptext, styles["Normal"]))
            ## checking if addressline 2 exists in the invoices dictionary then find it and print it if not don't 
            if 'AddressLine2' in address_of_orders:
                ptext = '<font size="10">%s</font>' % address_of_orders.AddressLine2
            else:
                ptext = ""
            try:
                Story.append(Paragraph(ptext, styles["Normal"]))
                ptext = '<font size="10">%s</font>' % address_of_orders.StateOrRegion
                Story.append(Paragraph(ptext, styles["Normal"]))
            except:
                print("Error: State or region")
                print()
            try:
                ptext = '<font size="10">%s</font>' % address_of_orders.PostalCode
                Story.append(Paragraph(ptext, styles["Normal"]))
            except:
                print("Error: Postal code")
                print()
            try:
                ptext = '<font size="10">%s</font>' % address_of_orders.CountryCode
                Story.append(Paragraph(ptext, styles["Normal"]))
            except:
                print("Error: Country code")
                print()
            # defining elements in the table
            quantity_of_units = number_of_units
            product_title = finding_item
            product_title = product_title[:65] + "..."
            unit_price = price_of_orders
            total = unit_price

            quantity_of_units2, product_title2, unit_price2 = '', '', ''

            total2 = 0.00

            quantity_of_units3, product_title3, unit_price3 = '', '', ''

            total3 = 0.00

            total = total[1:]

            

            data = [['Quantity', 'Product Title', 'Unit Price', 'Total'],
            [quantity_of_units, product_title, unit_price,  currency + str(total) ],
            [quantity_of_units2, product_title2, unit_price2, currency + str(total2)],
            [quantity_of_units3, product_title3, unit_price3, currency + str(total3)],
            ['', '', 'SUBTOTAL', currency + str(float(total) + float(total3) + float(total2))],
            ['', '', 'TAXES', '0.00'],
            ['', '', 'DUE', currency + str(float(total) + float(total3) + float(total2)) ]]

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
            
        
            


            
            ## stop for a couple seconds so we don't overwhelm the system
            time.sleep(1)
            ## adding all these details to a list of lists
            
            # print(list_of_all_details)
            
    ## this is the list of all the details each entry in this list is one invoice
    ## and then each entry in the list in the sub section below it is either the address date of purchase etc etc... 
    
    ## grab all invoices from database where pdf has not yet been created 
