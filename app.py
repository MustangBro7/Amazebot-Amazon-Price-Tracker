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
from selenium_stealth import stealth
import schedule
from flask_apscheduler import APScheduler

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
app = Flask(__name__)
CORS(app)
scheduler = APScheduler()
# scheduler.init_app(app)

# @scheduler.task('cron', hour=23, minute=10 , timezone='Asia/Kolkata')
def scheduled_update():
    current_data = get_data()
    for i in current_data:
        url1 = i[3]
        print(url1)
        data = {"url":url1}
        requests.post("http://localhost:5000" , json = data)

@app.route('/' , methods = ['GET' , "POST" ])

def bot():
    if request.method == 'POST':
        data = request.get_json()
        print(data['url'])
    url = data['url']
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    # chrome_options.add_argument("user-data-dir=selenium")
    driver = webdriver.Chrome(options=chrome_options)
    # stealth(driver,
    #    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.105 Safari/537.36',
    #    languages=["en-US", "en"],
    #    vendor="Google Inc.",
    #    platform="Win32",
    #    webgl_vendor="Intel Inc.",
    #    renderer="Intel Iris OpenGL Engine",
    #    fix_hairline=True,
    #    )
    driver.get(url)
    cookies = driver.get_cookies()
    for cookie in cookies:
        driver.add_cookie(cookie)
    print(cookies)
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
    

    # schedule.every().day.at("22:03").do(scheduled_update)
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
    scheduler.add_job(id = "job1" , func= scheduled_update , trigger = "cron", day_of_week = 'mon-sun' , hour= 9 , minute=00 )
    scheduler.add_job(id = "job2" , func= scheduled_update , trigger = "cron", day_of_week = 'mon-sun' , hour= 21 , minute=00 )
    scheduler.start()  
    app.run(debug=True)
    


# def run_scheduled_update_in_thread():
#     while True:
#         schedule.run_pending()
#         time.sleep(1)
# schedule.run_pending()