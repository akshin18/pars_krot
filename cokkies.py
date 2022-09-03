



def get_cokie_and_user_agent(id):
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
    driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)
    driver.get('https://old.bankrot.fedresurs.ru/MessageWindow.aspx?ID=BB0097A2C31157D8B2440115D38BB101')
    cookies = driver.get_cookie("bankrotcookie")["value"]
    user_agent = driver.execute_script("return navigator.userAgent")
    driver.close()
    return [cookies,user_agent,id]


def get_pages(page,txt,date_s,date_e):
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
    # driver = webdriver.Chrome(chrome_options=chrome_options)
    driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)
    driver.get(f"https://tbankrot.ru/reestr?page={page}&type=mess&text={txt}&debtor=&dt_1={date_s}&dt_2={date_e}&t%5B%5D=2&t%5B%5D=7")
    return driver.page_source.encode("utf-8")

