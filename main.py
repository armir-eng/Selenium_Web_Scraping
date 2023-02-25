#Pandas is going to be used to structure the raw data extracted into dataframe (pandas table), which on its side will be converted to the desired output file (csv in this case). 
import pandas as pd

#time manipulation modules come in handy, as we have date input values intended to be used with regard to the client's specific request and also record the harvest's timestamp.
#This way, we can do some date format manipulation.
import time, os


#This tool is the most important one, which helps making the harvest process quick and efficient, by making sure searching for multiple products simultaneously.
#The number of workers(products to be harvested at a time) set should match the CPU and memory capacity(the higher, the better support), to ensure a proper performance. 
from concurrent.futures import ThreadPoolExecutor


import data_extraction_function_definitions # The module containing data extraction functions is imported.

# Selenium's necessary functionalities are also needed to be imported
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


#The csv input file is read by pandas and converted to dataframe.
#fillna('') method set empty cell's value to a "null" string. This adjustment is useful for this case, as we will need it for a condition below in the "violation_check" function definition.

df=pd.read_csv(os.path.join(os.getcwd(),'inputs_list.csv')).fillna('')


#With input is meant the list of initial values provided by the client, which are the data we refer to, in order to carry out the process and match the client's requests.
#For example, the value of "ItemNumber" field is always used as search term for each product. Also, 

# We take the rows of input file in form of a list of lists
# This is an elegant pythonic syntax to achieve this.
input_rows_list=[[row.UPC,row.ItemNumber,row.ItemDesc,row.IMAPPrice,row.Promo1Price,row.Promo1Start,row.Promo1End] for row in df.itertuples()] 
print(input_rows_list)


output_file = os.path.join(os.getcwd(),'international_tool_results.csv')



#The below row creates an empty dataframe, with the fields specified, as client requested them.
ouptut_columns_list=['UPC','ItemDesc','SellerName','ProductTitle','ProductURL','ItemNumber','ItemNumber-Website','IMAPPrice','RetailPrice','Promo1Price','Promo1Start','Promo1End','Violation','In-OutofStock','GeoLocation','DateExtractedCST','ErrorMessage']


results_df=pd.DataFrame(columns=ouptut_columns_list)
print(results_df)


#This function will be used to update the above dataframe with every row extracting from scraping process.
def add_results(results_list):
    global results_df,ouptut_columns_list
    page_results_df=pd.DataFrame(results_list,columns=ouptut_columns_list)
    results_df=pd.concat([results_df,page_results_df],ignore_index=True)
    

#This is the main function, that executes the extraction process.

# If the search gets us directly to the product page or in a results list page and there are relevant results, we get the necessary data and check for price VIOLATION.
# Else, we define the information about why there is no data collected for the product as an error message.  


def extract_data(input_row):
    
    global results_df #We need this to access the dataframe we created, in order to update this with the data rows.

    #we declare and assign in a single row the variables, dedicated to field values in inputs list, for simple use in below rows.
    upc,input_item_number,item_desc,imap_price,promo1price,promo1start,promo1end=input_row[0],input_row[1],input_row[2],input_row[3],input_row[4],input_row[5],input_row[6]
   
    driver=webdriver.Chrome()
    driver.get('https://www.internationaltool.com/shop/')    
    driver.find_element(By.CSS_SELECTOR,'li[class="site-search"] input').send_keys(input_item_number)
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR,'li[class="site-search"] input').send_keys(Keys.RETURN)
    time.sleep(2)
    
    # This searches for the presence of a characteristic document element that indicates a pdp page.
    # It creates a list of DOM elements found. We use its length to form a condition when we check for the element. If it is different
    pdp_elements=driver.find_elements(By.CSS_SELECTOR,'div[class="meta"]') 
    
    # This searches for the presence of the element that contain the message that tells the inavailability of the product searched.
    no_results_available_message_elements=driver.find_elements(By.XPATH,'''//div[@class="content__description type--caption"][contains(.,"We're sorry, we couldn't find any results for")]''')

    listed_item_elements=driver.find_elements(By.XPATH,'//li[@class="product-item"]')

    out_of_stock_message_elements=driver.find_elements(By.CSS_SELECTOR,'p[class="non-stock-topDescription"]')
    
    #if we are inside a product page and the result matches the intended searched product, we extract the needed data, else we add an error message for the mismatch encountered.
    if len(pdp_elements)!=0: 
        data_extraction_function_definitions.extract_data_in_pdp(driver,upc,input_item_number,item_desc,imap_price,promo1price,promo1start,promo1end,add_results)
        print(results_df)
    
    
    #if no result is found for search only the error message appeared is extracted.
    elif len(no_results_available_message_elements)!=0:
        data_extraction_function_definitions.no_results_available(driver,upc,input_item_number,item_desc,imap_price,promo1price,promo1start,promo1end,add_results)
        print(results_df)            
    
    #if search shows a list of result, a check for relevant ones is performed and if so, necessary data are got directly in this page.    
    elif len(listed_item_elements)!=0:
        data_extraction_function_definitions.listed_results(driver,upc,input_item_number,item_desc,imap_price,promo1price,promo1start,promo1end,add_results)
        print(results_df)
    

    #if product is not available, the error message appeared is also extracted here.
    elif len(out_of_stock_message_elements)!=0:
        data_extraction_function_definitions.out_of_stock_case(driver,upc,input_item_number,item_desc,imap_price,promo1price,promo1start,promo1end,add_results)
        print(results_df)


# This is the most interesting part, which ensures that the site is opened and harvested multiple times simultaneosly, to make the process faster.
# Set workers number to 10, which is OK for my PC. Raising it, did not change the speed of extraction, as the memory is occupied at max with as many, so the extra others are forced to wait until the previous ones finish scraping.
with ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(extract_data,input_rows_list)


#In the end, we create a csv results file from the final dataframe we obtained.
results_df.to_csv(output_file,index=False)
 


