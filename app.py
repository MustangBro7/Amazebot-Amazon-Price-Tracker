from flask import Flask, request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
import re
import json
import requests
from PIL import Image
from io import BytesIO
import requests
import pytesseract
from flask_cors import CORS
from database import insert_data , update_data , get_data , delete_data

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
app = Flask(__name__)
CORS(app)
@app.route('/' , methods = ['GET' , "POST" ])

def bot():
    if request.method == 'POST':
        data = request.get_json()
        print(data['url'])
    # elif request.method == 'DELETE':
    #     data = request.get_json()
    #     print(data)
    #     delete_data(data['url'])
    # url = "https://www.amazon.in/Nike-Vision-Black-White-Sneaker-DN3577-101/dp/B09NMH8JY4/ref=sr_1_5?crid=1O7EIEUA1OKT7&keywords=nike%2Bshoes&qid=1706368305&sprefix=nike%2Bshoe%2Caps%2C375&sr=8-5&th=1&psc=1"
    url = data['url']
    # url2 = "https://www.amazon.in/Nike-Zoom-Court-3-WHITE-MNNAVY-DV3258-102-4UK/dp/B09NMHT118/ref=sr_1_20?crid=1TOSKMKZDWZZ0&dib=eyJ2IjoiMSJ9.E1W9kL0ibMVlEbBqU_T8D5l6vRQXv0fyoDC8fpWqBmD--NzyAcpjAbu4gPZwf66B0RRKoKIb6ET3-IdZEQ2GT-7tc4crcSIlJbH9QoylLTrxAa1Uh4PLWyudCEUjZzEnK_DuV7K4TTPpu8DVQffQZ8X6amPOFBLm1ZcUGftEstjrvcn7VZFVCkgEGy6hJBmlEOZ-t0tPDvGJ97l1qViddD7uN5oqOWizR-8KNY5P8oVQ32Gneu3LN3QnOYDRXZQgl6kVZLp92XQY6BI6lMD9BOUoMRGlZWHzfdv74bj5p3E.mBPeeF_N_h06bN_NNBnWtaaJBhAcuHNhyRF7lXtSLrI&dib_tag=se&keywords=nike%2Bshoes%2Bfor%2Bmen&qid=1705725987&sprefix=nike%2B%2Caps%2C190&sr=8-20&th=1"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    # captcha = driver.find_element(By.CSS_SELECTOR, 'iframe[role=presentation]')
    # driver.switch_to.frame(captcha)

    try:    
        captcha =  driver.find_element(By.XPATH, f"//h4[contains(text(), 'Enter the characters you see below')]") 
        try:
            image = driver.find_element(By.TAG_NAME , "img")
            image_url = image.get_attribute('src')
            print(image_url)
            response = requests.get(image_url)
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                text = pytesseract.image_to_string(img)
            print(text)
            print(captcha.text)
            print('\nPlease solve the captcha now')
            wait = WebDriverWait(driver, 30)
            try:
                wait.until(ec.presence_of_element_located(('css selector', 'span[aria-checked="true"]')))
            except TimeoutException:
                print('\nFailed to solve captcha in the expected time')
            else:
                print('\nCaptcha solved successfully, proceeding to click!')
        except NoSuchElementException:
            print("Couldn't Find Image")
    except NoSuchElementException:
        # If the element doesn't exist, print a message
        print("No Captcha!!!")



    # print(source)
    with open("D:\python projects\page.html" , "w" , encoding = 'utf-8') as file:
        file.write(driver.page_source)
    source = driver.page_source
    soup = bs(source , 'html.parser')
    # print(soup)
    price = soup.findAll(string=re.compile("₹|Rs\.?"))
    # price1 = soup.findAll(string = re.compile("displayPrice"))
    # price1 = driver.find_element(By.CLASS_NAME , "a-price-whole")
    price1 = soup.find('span' , class_="a-price-whole")
    symbol = soup.find('span' , class_="a-price-symbol")
    print(price1)
    # image_container = soup.find('div' , class_='a-image-container a-dynamic-image-container greyBackground')
    # product_image = image_container.find('img')
    # link = product_image.get('src')
    image_container = driver.find_element(By.CLASS_NAME , "imgTagWrapper")
    image_link = image_container.find_element(By.TAG_NAME , 'img')
    img_src = image_link.get_attribute('src')
    print(img_src)
    name = soup.find('span' , id = "productTitle")
    product_name = name.text.strip()    
    if price1 :
        # print(price1[0])
        # data = json.loads(price1[0])
        # # Extract the value associated with the key "displayPrice"
        # display_price = data['desktop_buybox_group_1'][0]['displayPrice']
        display_price = symbol.text + price1.text
        print(display_price)
    else:
        print("Out of Stock")
        display_price = "Out of stock"
    driver.close()
    updated_data = update_data(display_price , product_name , url , img_src)
    # print(json.dumps(updated_data[2]))
    # full_data = get_data()
    return {"Price": display_price , "Name": product_name , "link":url , "img_link":img_src}

    

@app.route('/getdata' , methods = ['GET' , "POST"])
def getdata():
    full_data = get_data()
    real_data = []
    for i in full_data:
        real_data.append({"Price": i[1] , "Name": i[2] , "link":i[3] , "img_link":i[4]})
    return(real_data)

@app.route('/delete' , methods = ['DELETE'])
def deletedata():
    data = request.get_json()
    print(data)
    delete_data(data['url'])
    return data
if __name__ == '__main__':
    app.run(debug=True)
    