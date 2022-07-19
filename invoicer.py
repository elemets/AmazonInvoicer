from creatinginvoicesfrominfo import create_invoices
from orderretriever import list_orders
from invoicesubmit import submit_invoice

from sqlalchemy import create_engine, Column, Integer, desc, String, Boolean, Date, DateTime, asc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import IntegrityError
from mws import mws
from DBManage import Invoice
import time

Base = declarative_base()
engine = create_engine('sqlite:///invoices.db', echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)

UK_MARKETPLACE = 'A1F83G8C2ARO7P'
IT_MARKETPLACE = 'APJ6JRA9NG5V4'
SW_MARKETPLACE = 'A2NODRKZP88ZB9'
FR_MARKETPLACE = 'A13V1IB3VIYZZH'
DE_MARKETPLACE = 'A1PA6795UKMFR9'
ES_MARKETPLACE = 'A1RKKUPIHCS9HS'
NL_MARKETPLACE = 'A1805IZSGTT6HS'

access_key = 'AKIAJ4HPAZOAKD66TRTA' #replace with your access key
seller_id = 'A2034TBO3FX4MA' #replace with your seller id
secret_key = '+PqcjI4wwB6lxcczgZki2D1PUW2x94NI38BWG14p' #replace with your secret key



# creating invoices and adding them to database 
# create_invoices(ES_MARKETPLACE)


session = Session()

feeds_api = mws.Feeds(access_key, secret_key, seller_id, 'UK')

feed_submission_list = feeds_api.get_feed_submission_list()

feed_submission_list = feed_submission_list.parsed['FeedSubmissionInfo']

print(feed_submission_list[0])

response = feeds_api.cancel_feed_submissions(feed_submission_list)

print(response.parsed)
# for invoice in session.query(Invoice).order_by(desc('invoice_number')):
#     # invoice.invoice_number = str((int(invoice.invoice_number) + 1))
#     print(invoice.invoice_number)
    
#     # session.add(invoice)
#     # session.commit()
# session.close()
    
# for invoice in session.query(Invoice).filter(Invoice.invoice_submitted ==  False):
#     ## making a queryto the database for all non submitted invoices 
#     feeds_api = mws.Feeds(access_key, secret_key, seller_id, invoice.market_origin)
    
#     feed_submission_list = feeds_api.get_feed_submission_list()
    
#     print(invoice.invoice_submitted)
#     print(invoice.invoice_number)
#     print(invoice.market_origin)
    
#     print(feed_submission_list.parsed)
    
#     print(invoice.date_of_purchase)
#     submission_id = submit_invoice(invoice.market_origin, invoice.order_number, str(invoice.invoice_number))

#     time.sleep(20)


#     feedsubmissionrequest = None
#     while feedsubmissionrequest is None:
#         try:
#             # connect
#             feedsubmissionrequest = feeds_api.get_feed_submission_result(str(submission_id))
#         except:
#             pass
    
    
    
#     print(feedsubmissionrequest.parsed)
    
#     invoice.invoice_submitted = True
#     session.add(invoice)
#     session.commit()
    


session.close()
# submission_id = submit_invoice(IT_MARKETPLACE, 
# order_ids[34]['order_id'],
# str(order_ids[34]['invoicenumber']) + ".pdf")

# print(submission_id)

# submission_id = 65504018651



# feedsubmissionrequest = feeds_api.get_feed_submission_result(str(submission_id))

# # 


# print(feedsubmissionrequest.parsed)