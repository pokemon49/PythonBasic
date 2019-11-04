from selenium import webdriver

#指定Firefox配置文件
Profile_dir = "C:\\Users\\HASEGAWA\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\o5aal9ci.selenium"
profile = webdriver.FirefoxProfile(Profile_dir)
driver=webdriver.Firefox(profile)
url='http://www.baidu.com'
driver.get(url)
#driver.close()