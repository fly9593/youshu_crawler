from scripts.browser import Browser

start_page = 1
end_page = 15715

browser = Browser()
# browser.display_browser = False
browser.init_browser()
# browser.login()
browser.get_info_all(10, 1180)
browser.browser.quit()
