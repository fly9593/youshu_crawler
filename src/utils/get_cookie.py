import time

from scripts.browser import Browser
from scripts.config import Config

# 用于获取cookie，请将cookie复制到resources/cookie.dat文件中

browser = Browser()
browser.display_browser = False
browser.init_browser()
conf = Config()
# 此时会弹出一个浏览器页面，请点击登录
browser.browser.get(conf.config["config"]["base_url"])
# 等待登录...
time.sleep(60)
cookies = browser.browser.get_cookies()
# 输出cookie
print(cookies)
