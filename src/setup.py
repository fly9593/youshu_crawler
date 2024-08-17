from scripts import logging_config
from scripts.browser import Browser

# logging_config.setup_logging()
# import logging
#
# logger = logging.getLogger(__name__)
# logger.info("Logging is configured.")

start_page = 2321
end_page = 2322

logging_config.setup_logging(start_page, end_page)

browser = Browser()
browser.display_browser = False
browser.init_browser()
# browser.login()
# browser.get_info_all(start_page, end_page)
browser.get_info_all_retry(start_page, end_page)
browser.browser.quit()
