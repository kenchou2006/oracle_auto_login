import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pyotp
from dotenv import load_dotenv

load_dotenv()

cloud_account_name = os.getenv('CLOUD_ACCOUNT_NAME')
oracle_cloud_login_url = os.getenv('ORACLE_CLOUD_LOGIN_URL')
username = os.getenv('ORACLE_USERNAME')
password = os.getenv('ORACLE_PASSWORD')
otp_secret_key = os.getenv('OTP_SECRET_KEY')

# Chrome Headless
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

#For Github Action
CHROMEDRIVER_PATH = "/usr/bin/chromedriver"
chrome_options.binary_location = "/usr/bin/google-chrome"
webdriver_service = Service(CHROMEDRIVER_PATH)
browser = webdriver.Chrome(service=webdriver_service, options=chrome_options)


#browser = webdriver.Chrome(options=chrome_options)

#browser = webdriver.Chrome()

browser.get('https://www.oracle.com/tw/cloud/sign-in.html')

time.sleep(5)

cloud_account_name_input = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.ID, 'cloudAccountName')))
cloud_account_name_input.send_keys(cloud_account_name)

cloud_account_button = WebDriverWait(browser, 10).until(
    EC.element_to_be_clickable((By.ID, 'cloudAccountButton')))
cloud_account_button.click()

#Cloud Login Url ex:https://idcs-ba989cf3be7845ca8b2b6ctpfoedxghws.identity.oraclecloud.com/ui/v1/signin
WebDriverWait(browser, 10).until(EC.url_to_be(oracle_cloud_login_url))

username_input = WebDriverWait(browser, 30).until(
    EC.presence_of_element_located((By.ID, 'idcs-signin-basic-signin-form-username')))
username_input.send_keys(username)

password_input = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.ID, 'idcs-signin-basic-signin-form-password')))
password_input.send_keys(password)

login_button = WebDriverWait(browser, 10).until(
    EC.element_to_be_clickable((By.ID, 'ui-id-4')))
login_button.click()


otp_input = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.ID, 'idcs-mfa-mfa-auth-passcode-input|input')))

totp = pyotp.TOTP(otp_secret_key)
otp_input.send_keys(totp.now())

verify_button = WebDriverWait(browser, 10).until(
    EC.element_to_be_clickable((By.CLASS_NAME, 'oj-button-text')))
verify_button.click()

time.sleep(20)

browser.quit()
