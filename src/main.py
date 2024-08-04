import argparse
from scripts.browser import Browser


def main(start_page, end_page):
    browser = Browser()
    browser.init_browser()
    # browser.login()
    browser.get_info_all(start_page, end_page)
    browser.browser.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script to run browser automation with page range.')
    parser.add_argument('start_page', type=int, help='The starting page number')
    parser.add_argument('end_page', type=int, help='The ending page number')

    args = parser.parse_args()
    main(args.start_page, args.end_page)
