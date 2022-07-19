
import mws
import hashlib
import xml.dom.minidom
import time

def submit_invoice(region, order_id, invoice): 
    access_key = 'AKIAJ4HPAZOAKD66TRTA' #replace with your access key
    seller_id = 'A2034TBO3FX4MA' #replace with your seller id
    secret_key = '+PqcjI4wwB6lxcczgZki2D1PUW2x94NI38BWG14p' #replace with your secret key
    
    
    if region == 'UK':
        marketplace = 'A1F83G8C2ARO7P'
    elif region == 'IT':
        marketplace = 'APJ6JRA9NG5V4'
    elif region == 'SW':
        marketplace = 'A2NODRKZP88ZB9'
    elif region == 'FR':
        marketplace = 'A13V1IB3VIYZZH'
    elif region == 'ES':
        marketplace = 'A1RKKUPIHCS9HS'

    feeds_api = mws.Feeds(access_key, secret_key, seller_id, region=region)

    

    ## importing invoice
    invoiceFile = open("./Invoices/" + region +"/"+ invoice + "_" + region +".pdf", "r")
    ## converting invoice to bytes
    invoiceFileInBytes = invoiceFile.read()
    ## setting up MD5 Hash
    MD5 = hashlib.md5()
    MD5.update(invoiceFileInBytes.encode())
    # generating MD5
    contentMD5 = MD5.digest()

    amazon_order_id = order_id
    invoice_number = invoice

    feed_options = {'orderid': amazon_order_id, 'invoicenumber': invoice_number}

    response = feeds_api.submit_feed(
        feed=invoiceFileInBytes.encode(),
        feed_type='_UPLOAD_VAT_INVOICE_',
        feed_options=feed_options,
        marketplaceids=marketplace,
    )


    response_parsed = response.parsed
    
    submission_id = response_parsed['FeedSubmissionInfo'].FeedSubmissionId
    
    time.sleep(3)
        
    #print(response.parsed)
    # feedsubmissionrequest = feeds_api.get_feed_submission_result(submission_id)
    
    # time.sleep(5)
    
    # print(feedsubmissionrequest.parsed)
    
    # feedsubmissionrequest = feeds_api.get_feed_submission_result(str(submission_id))
    
    # print(feedsubmissionrequest)
    
    
    return submission_id
    #feedlist = feed.get_feed_submission_list()
