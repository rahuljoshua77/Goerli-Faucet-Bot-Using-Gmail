from seleniumwire import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import os, time
import random
from selenium.webdriver.chrome.options import Options
from multiprocessing import Pool
 
from faker import Faker
cwd = os.getcwd()
# mobile_emulation = {
#     "deviceMetrics": { "width": 360, "height": 650, "pixelRatio": 3.4 },
#     }



firefox_options = webdriver.ChromeOptions()
firefox_options.add_argument('--no-sandbox')
firefox_options.headless = True
firefox_options.add_argument('--disable-setuid-sandbox')
firefox_options.add_argument('disable-infobars')
firefox_options.add_argument('--ignore-certifcate-errors')
firefox_options.add_argument('--ignore-certifcate-errors-spki-list')
#firefox_options.add_argument('--disable-accelerated-2d-canvas')
firefox_options.add_argument('--no-zygote')
firefox_options.add_argument('--no-first-run')
firefox_options.add_argument('--disable-dev-shm-usage')
firefox_options.add_argument("--disable-infobars")
firefox_options.add_argument("--disable-extensions")
firefox_options.add_argument("--disable-popup-blocking")
firefox_options.add_argument('--log-level=3') 
firefox_options.add_argument('--disable-blink-features=AutomationControlled')
firefox_options.add_experimental_option("useAutomationExtension", False)
firefox_options.add_experimental_option("excludeSwitches",["enable-automation"])
 
firefox_options.add_argument('--disable-notifications')
from python_anticaptcha import AnticaptchaClient, NoCaptchaTaskProxylessTask
firefox_options.add_argument("--mute-audio")
 
from selenium.webdriver.common.action_chains import ActionChains
 
from faker import Faker
fake = Faker('en_US')
from selenium.webdriver.common.action_chains import ActionChains
# firefox_options.add_experimental_option("mobileEmulation", mobile_emulation)
random_angka = random.randint(100,999)
random_angka_dua = random.randint(10,99)
def xpath_ex(el):
    element_all = wait(browser,15).until(EC.presence_of_element_located((By.XPATH, el)))
    #browser.execute_script("arguments[0].scrollIntoView();", element_all)
    return browser.execute_script("arguments[0].click();", element_all)

def xpath_long(el):
    element_all = wait(browser,30).until(EC.presence_of_element_located((By.XPATH, el)))
    #browser.execute_script("arguments[0].scrollIntoView();", element_all)
    return browser.execute_script("arguments[0].click();", element_all) 

def xpath_type(el,word):
    return wait(browser,30).until(EC.presence_of_element_located((By.XPATH, el))).send_keys(word)
def xpath_id(el,word):
    return wait(browser,30).until(EC.presence_of_element_located((By.XPATH, f'//input[@{el}]'))).send_keys(word)

def job(address,email):
    #6LcoGwYfAAAAACjwEkpB-PeW6X-GkCgETtEm32s1  
    xpath_id('type="address"',address)
     
    site_key = '6LcKyLYbAAAAANM74ESqR5Q7Z_W2yolLdyK3fzFP'  # grab from site
    url = 'https://faucets.chain.link'
    api_key = open(f"{cwd}\\api_key.txt","r")
    api_key = api_key.read()

    client = AnticaptchaClient(api_key)
    task = NoCaptchaTaskProxylessTask(url, site_key)
    job = client.createTask(task)
    job.join()
    token_captcha = job.get_solution_response()
    browser.execute_script("document.getElementsByClassName('g-recaptcha-response')[0].innerHTML = "
                                    f"'{token_captcha}';")
    sleep(2)
    try:
        xpath_ex('//button[@class="alchemy-faucet-button btn btn-dark btn-lg"]')
        
        notif = wait(browser,30).until(EC.presence_of_element_located((By.XPATH, f'//div[@class="alchemy-faucet-table-data d-md-block d-sm-none d-none col"]/time'))).text
        print(f"[*] [{email}] {notif}")
        with open(f'success.txt','a') as f:
            f.write(f"{email}\n")
    except:
        print(f"[*] [{email}] Failed to get goerli!")    
        with open(f'failed.txt','a') as f:
            f.write(f"{email}\n")
def action(data):
    data = data.split("|")
    email = data[0]
    password = data[1]
    address = data[2]
    # password  = data[1] http://lum-customer-hl_5ac7e0cc-zone-data_center-route_err-pass_dyn:os3j66cvtik2@zproxy.lum-superproxy.io:22225
 
    proxy_options = {
        'proxy': {
            'http': 'http://lum-customer-hl_5ac7e0cc-zone-data_center-route_err-pass_dyn:os3j66cvtik2@zproxy.lum-superproxy.io:22225',
            'https': 'http://lum-customer-hl_5ac7e0cc-zone-data_center-route_err-pass_dyn:os3j66cvtik2@zproxy.lum-superproxy.io:22225'
        
           },
        "backend": "default",
        'mitm_http2': False 
    }
    get_url = r"https://auth.alchemyapi.io/signup?redirectUrl=https%3A%2F%2Fgoerlifaucet.com"
    firefox_options.add_argument(f"user-agent=Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Mobile Safari/537.36")
                 
    global browser
    browser = webdriver.Chrome(options=firefox_options,seleniumwire_options=proxy_options,executable_path=f"{cwd}\\chromedriver.exe")
  
    try:
        browser.get(get_url)
        browser.refresh()
        xpath_ex('//button[text()=" with Google"]')
        sleep(random.randint(1,3))
        browser.switch_to.window(browser.window_handles[1])
        xpath_id('type="email"',email)
        sleep(random.randint(1,3))
        xpath_id('type="email"',Keys.ENTER)
 
        sleep(random.randint(1,3))
        xpath_id('type="password"',password)
        sleep(random.randint(1,3))
        xpath_id('type="password"',Keys.ENTER)
        notif = wait(browser,30).until(EC.presence_of_element_located((By.XPATH, f'//p[@class="alchemy-faucet-login-description"]'))).text
        print(f"[*] [{email}] {notif}")
        job(address,email)
                
    except Exception as e:
        print(f"[*] [{email}] Failed Login")
        with open(f'failed.txt','a') as f:
            f.write(f"{email}|{password}\n")
            
    
if __name__ == '__main__':
    print("[*] Registration Account")
    
    jumlah = input("[*] Multiprocessing: ")
    file_list_akun = "acc.txt"
    myfile_akun = open(f"{cwd}/{file_list_akun}","r")
    akun = myfile_akun.read()
    list_accountsplit = akun.split()
    k = list_accountsplit
    start = time.time()
    with Pool(int(jumlah)) as p:  
        p.map(action, k)
    