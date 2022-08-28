



def get_cokie_and_user_agent(id):
    from selenium import webdriver
    driver = webdriver.Chrome()
    driver.get('https://old.bankrot.fedresurs.ru/MessageWindow.aspx?ID=BB0097A2C31157D8B2440115D38BB101')
    cookies = driver.get_cookie("bankrotcookie")["value"]
    user_agent = driver.execute_script("return navigator.userAgent")
    driver.close()
    return [cookies,user_agent,id]


