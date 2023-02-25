#This one is the most important for the client. It serves the need to check if the price captured is lower than promo price (if we are in the promo period) or the everyday price (if there is no promotion period)
#If so, this is considered a price VIOLATION to them. This is the essence of the project.
from datetime import datetime

def violation_check(retailer_price,imap_price,promo1price,promo1start,promo1end):
    
    if promo1start!='' and promo1end!='': #if there is a promotion period for the product
        format="%m/%d/%Y"
        current_date=datetime.strptime(datetime.now().strftime(format),format)
        start_date=datetime.strptime(promo1start,format)
        end_date=datetime.strptime(promo1end,format)
        if current_date>start_date and current_date<end_date: #if we are within the promotion period, e compare the extracted price with the promotion one, else we do with the everyday price.
            if float(retailer_price)<float(promo1price):  
                return "YES"
            return "NO"            
        else:
            if float(retailer_price)<float(imap_price):
                return "YES"
            return "NO"

    else:
        if float(retailer_price)<float(imap_price):
            return "YES"
        return "NO"


