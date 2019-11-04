from selenium import webdriver
driver=webdriver.Chrome()  #调用chrome浏览器
driver.get('https://www.baidu.com')
driver.quit()