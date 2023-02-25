# This module contains is mainly used to define the functions that do the data extraction, based on search results cases.
# So, there are separate functions dedicated to get the data when product search results in: 
# 1- product page (When search directly shows the page of product we are looking for)
# 2- results list (When search shows a list of results and we look for the specific product we are interested in. There are also cases when all results are irrelevant.)
# 3- no results available (A message is shown to indicate that the product is not available)
# 4- out of stock case (A message is shown to indicate that the product is out of stock) 

#Selenium library is going to be used to automate the data extraction process.
from selenium.webdriver.common.by import By 
from violation_check import violation_check

#time manipulation modules come in handy, as we have date input values intended to be used with regard to the client's specific request and also record the harvest's timestamp.
#This way, we can do some date format manipulation.
from datetime import datetime
import pytz
    
#We need to record the timestamp to fill the field "DateofScrape", which is required to belong to the US/Central timezone
def timestamp():
    return datetime.now().astimezone(pytz.timezone('US/Central')).strftime('%m/%d/%Y, %H:%M:%S %p')




def extract_data_in_pdp(driver,upc,input_item_number,item_desc,imap_price,promo1price,promo1start,promo1end,add_results):

    # This searches for the presence of a characteristic document element that indicates a pdp page.
    # It creates a list of DOM elements found. We use its length to form a condition when we check for the element. If it is different than 0, it means that it is present.
    
    product_title=driver.find_element(By.CSS_SELECTOR,'div[class="name"]').text
    product_url=driver.current_url
    seller_name='International Tool'
         
    item_number_element_text=driver.find_element(By.CSS_SELECTOR,'span[class="vendor-number"] strong').text
        
    if(item_number_element_text==input_item_number):
            
        item_number_website=driver.find_element(By.CSS_SELECTOR,'span[class="vendor-number"] strong').text
        print(input_item_number)
            
        retailer_price=driver.find_element(By.CSS_SELECTOR,'div[class="price text-align-right"] p').text.strip().replace("$","").replace(",","")
            
        violation=violation_check(retailer_price,imap_price,promo1price,promo1start,promo1end)            
            
        if len(driver.find_elements(By.CSS_SELECTOR,'button[id="addToCartButton"]'))!=0:
            stock='In Stock'
            
        else:
            stock='Out of Stock'
                
            
        print(stock) 
        global results_list
        results_list=[upc,item_desc,seller_name,product_title,product_url,input_item_number,item_number_website,imap_price,retailer_price,promo1price,promo1start,promo1end,violation,stock,'',timestamp(),'']
        add_results([results_list])
    
        
                
    else:
        error_message='The "ItemNumber" input does not match the one in the pdp.'    
        results_list=[upc,item_desc,seller_name,product_title,product_url,input_item_number,'',imap_price,'',promo1price,promo1start,promo1end,"NO",'','',timestamp(),error_message]
        add_results([results_list])
    


def no_results_available(driver,upc,input_item_number,item_desc,imap_price,promo1price,promo1start,promo1end,add_results):
    error_message=driver.find_elements(By.XPATH,'''//div[@class="content__description type--caption"][contains(.,"We're sorry, we couldn't find any results for")]''')[0].text
    results_list=[upc,item_desc,'','','',input_item_number,'',imap_price,'',promo1price,promo1start,promo1end,'NO','','',timestamp(),error_message]
    add_results([results_list])



def listed_results(driver,upc,input_item_number,item_desc,imap_price,promo1price,promo1start,promo1end,add_results):
    
    exact_product_xpath='//li[@class="product-item"][.//span[@class="vendor-number"]//strong[text()="{}"]][1]'.format(input_item_number) #this xpath expression locates the product card of the one with the item-number used to search it 
    relevant_results=driver.find_elements(By.XPATH,exact_product_xpath)
        
    #if there are relevant results (ones of a product with the item number searched with), the needed data are extracted for all of them.
    if len(relevant_results)!=0:
        
        for result in relevant_results:
            
            product_title=result.find_element(By.XPATH,'.//a[@class="name"]').text.strip()
            
            if "https://www.internationaltool.com" in result.find_element(By.XPATH,'.//a[@class="name"]').get_attribute('href'):
                product_url=result.find_element(By.XPATH,'.//a[@class="name"]').get_attribute('href')    
            
            else:
                product_url="https://www.internationaltool.com"+result.find_element(By.XPATH,'.//a[@class="name"]').get_attribute('href')
            
            
            retailer_price=result.find_element(By.XPATH,'.//span[@class="list-item-price"]').text.strip().replace("$","").replace("EACH","").replace(",","")
            violation=violation_check(retailer_price,imap_price,promo1price,promo1start,promo1end)
            print(violation)
            seller_name='International Tool'
            

            if len(result.find_elements(By.XPATH,'.//button[contains(.,"Add to Cart")]'))!=0:
                stock='In Stock'
            else:
                stock=''
            
            if result.find_element(By.XPATH,'.//span[@class="vendor-number"]//strong').text.strip().lower()==input_item_number.strip().lower():
                item_number_website=result.find_element(By.XPATH,'.//span[@class="vendor-number"]//strong').text.strip()
                results_list=[upc,item_desc,seller_name,product_title,product_url,input_item_number,item_number_website,imap_price,retailer_price,promo1price,promo1start,promo1end,violation,stock,'',timestamp(),'']            
                add_results([results_list])           
                        
            
            else:
                retailer_price=''
                error_message='The "ItemNumber" input does not match the one in the pdp.'
                results_list=[upc,item_desc,seller_name,product_title,product_url,input_item_number,item_number_website,imap_price,retailer_price,promo1price,promo1start,promo1end,'NO',stock,'',timestamp(),error_message]        
                add_results([results_list])
                
    #if there is no relevant result, the below error message is used to indicate that the product we searched for is not present.
    else:
        error_message='There is no relevant item in the results list.'
        results_list=[upc,item_desc,'','','',input_item_number,'',imap_price,'',promo1price,promo1start,promo1end,'NO','','',timestamp(),error_message]
        add_results([results_list])
        

def out_of_stock_case(driver,upc,input_item_number,item_desc,imap_price,promo1price,promo1start,promo1end,add_results):
    error_message=driver.find_element(By.CSS_SELECTOR,'p[class="non-stock-topDescription"]').text.strip()
    results_list=[upc,item_desc,'','','',input_item_number,'',imap_price,'',promo1price,promo1start,promo1end,'NO','','',timestamp(),error_message]
    add_results([results_list])
    
