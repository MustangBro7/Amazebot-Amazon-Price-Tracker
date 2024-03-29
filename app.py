from flask import Flask, request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
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
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
scheduler = APScheduler()

@app.after_request
def add_csp_header(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline';"
    return response

def scheduled_update():
    current_data = get_data()
    for i in current_data:
        url1 = i[3]
        print(url1)
        data = {"url":url1}
        requests.post("http://localhost:5000" , json = data)
        # requests.post("https://amazebot.onrender.com" , json = data)

@app.route('/' , methods = [ "POST" ])

def bot():
    print("Welcome to amazebot")
    if request.method == 'POST':
        data = request.get_json()
        print(data['url'])
        url = data['url']
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage' )

        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
            # Add more user agents as needed
        ]

        # driver_path = ChromeDriverManager().install()
        # print(driver_path)
        # driver_service = Service(driver_path)
        # # driver_service = Service(driver_path)
        # d = services(driver_path)
        # driver = webdriver.Chrome(options=chrome_options)
        
        user_agent = random.choice(user_agents)
        chrome_options.add_argument(f"user-agent={user_agent}")
        driver = webdriver.Chrome(options=chrome_options)

        driver.get(url)
        time.sleep(random.uniform(3, 5))
        cookies = driver.get_cookies()
        for cookie in cookies:
            driver.add_cookie(cookie)
        print(cookies)
        driver.get(url)

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



        
        source = driver.page_source
        # print(source)
        soup = bs(source , 'html.parser')
        # print(soup)
        price = soup.findAll(string=re.compile("₹|Rs\.?"))
        price1 = soup.find('span' , class_="a-price-whole")
        # price1 = soup.find('span' , class_="a-offscreen")
        symbol = soup.find('span' , class_="a-price-symbol")
        # print(price1)
        # image_container = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "imgTagWrapper")))
        # image_link = image_container.find_element(By.TAG_NAME , 'img')
        # img_src = image_link.get_attribute('src')
        try:
            stock = soup.find('span' , class_='a-size-medium a-color-success')
        except:
            stock.text = "Available"
        print(stock)
        image_container = soup.find(class_='imgTagWrapper')
        image_link = image_container.find('img')
        img_src = image_link.get('src')
        # print(img_src)
        name = soup.find('span' , id = "productTitle")
        product_name = name.text.strip()    
        if stock:
            if stock.text == " Currently unavailable. ":
                print("Out of Stock")
                display_price = "Out of stock"
            else :
                display_price = symbol.text + price1.text
                print(display_price)
        else :
            display_price = symbol.text + price1.text
            print(display_price)
            
        driver.close()
        updated_data = update_data(display_price , product_name , url , img_src)

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