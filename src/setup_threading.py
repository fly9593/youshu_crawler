import threading

from scripts import logging_config
from scripts.browser import Browser

# 开始页
start_page = 2301
# 结束页
end_page = 2308
# 同时运行的最大线程数
max_threads = 4
# 每个线程执行的页数
page_range_per_thread = 2

ranges = []


# 计算每个线程的 start_page 和 end_page
def calculate_page_ranges(start_page, end_page, page_range_per_thread):
    ranges = []
    while start_page <= end_page:
        thread_end_page = min(start_page + page_range_per_thread - 1, end_page)
        ranges.append((start_page, thread_end_page))
        start_page = thread_end_page + 1
    return ranges


# 执行爬取任务的线程函数
# def thread_function(start_page, end_page):
#     logging_config.setup_logging(start_page, end_page)
#     browser = Browser()
#     browser.display_browser = False
#     browser.init_browser()
#     browser.get_info_all(start_page, end_page)
#     browser.browser.quit()

def thread_function(start_page, end_page, thread_id):
    logging_config.setup_logging_threading(start_page, end_page, thread_id)
    browser = Browser()
    browser.display_browser = False
    browser.init_browser()
    browser.get_info_all(start_page, end_page)
    browser.browser.quit()


# 创建并启动线程
# def start_threads(page_ranges, max_threads):
#     threads = []
#     for (start, end) in page_ranges:
#         if len(threads) >= max_threads:
#             for thread in threads:
#                 thread.join()
#             threads = []
#         thread = threading.Thread(target=thread_function, args=(start, end))
#         thread.start()
#         threads.append(thread)
#     # 等待所有线程完成
#     for thread in threads:
#         thread.join()

def start_threads(page_ranges, max_threads):
    threads = []
    for index, (start, end) in enumerate(page_ranges):
        if len(threads) >= max_threads:
            for thread in threads:
                thread.join()
            threads = []
        thread_id = index + 1  # 设置线程 ID
        thread = threading.Thread(target=thread_function, args=(start, end, thread_id))
        thread.start()
        threads.append(thread)
    # 等待所有线程完成
    for thread in threads:
        thread.join()


page_ranges = calculate_page_ranges(start_page, end_page, page_range_per_thread)
start_threads(page_ranges, max_threads)
