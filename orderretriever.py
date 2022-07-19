from mws import mws
import time


def list_orders(marketplace):
    access_key = 'AKIAJ4HPAZOAKD66TRTA' #replace with your access key
    seller_id = 'A2034TBO3FX4MA' #replace with your seller id
    secret_key = '+PqcjI4wwB6lxcczgZki2D1PUW2x94NI38BWG14p' #replace with your secret key
    marketplace = marketplace

    # this imports the orders into an object which contains all the orders created after the date specified
    orders_api = mws.Orders(access_key, secret_key, seller_id, region='UK')
    orders = orders_api.list_orders(marketplaceids=[marketplace], created_after='2017-07-07')

    # this parses the order as a dictionary so we can find the values needed
    orders_as_dict = orders.parsed

    # This gives us the orders as a list where the first element is the oldest order in the list 
    orders_as_list = orders_as_dict.Orders.Order

    list_of_all_details = []

    ## this is going to fetch me everything I need to build an invoice 
    for orders in orders_as_list:
        if (orders.OrderStatus != "Canceled"):
            singular_details = []

            # print(orders_api.list_order_items(amazon_order_id=orders.AmazonOrderId).parsed.OrderItems.OrderItem.keys())
            ## getting the shipping address of the orders
            address_of_orders = orders.ShippingAddress
            ## adding shipping address to the list
            singular_details.append(address_of_orders)
            ## getting the price of the orders
            price_of_orders = "£" + str(orders.OrderTotal.Amount)
            singular_details.append(price_of_orders)
            ## getting the name of the item
            finding_item = orders_api.list_order_items(amazon_order_id=orders.AmazonOrderId).parsed.OrderItems.OrderItem.Title
            # print(orders.AmazonOrderId)
            singular_details.append(finding_item)
            ## Date of Purchase
            date_of_purchase = orders.PurchaseDate
            singular_details.append(date_of_purchase)
            ## Number of units purchased
            number_of_units = orders.NumberOfItemsShipped
            singular_details.append(number_of_units)
            singular_details.append(orders.AmazonOrderId)
            ## stop for a couple seconds so we don't overwhelm the system
            time.sleep(2)
            ## adding all these details to a list of lists
            list_of_all_details.append(singular_details)
    
    return list_of_all_details

## this is the list of all the details each entry in this list is one invoices

## and then each entry in the list in the sub section below it is either the address date of purchase etc etc... 


## now that we have the required information we just need to build the invoices.


