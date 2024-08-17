import argparse

def main(start_page, end_page, max_threads, page_range):
    threads = []
    pages_per_thread = page_range

    # 计算每个线程处理的页数范围
    current_page = start_page
    while current_page <= end_page:
        next_page = min(current_page + pages_per_thread - 1, end_page)
        thread = ScrapeThread(current_page, next_page)
        thread.start()
        threads.append(thread)
        current_page = next_page + 1

        # 控制线程数量
        if len(threads) >= max_threads:
            for thread in threads:
                thread.join()
            threads = []

    # 等待所有线程完成
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script to run browser automation with page range.')
    parser.add_argument('start_page', type=int, help='The starting page number')
    parser.add_argument('end_page', type=int, help='The ending page number')
    parser.add_argument('max_threads', type=int, help='The maximum number of threads to run simultaneously')
    parser.add_argument('page_range', type=int, help='The number of pages each thread will handle')

    args = parser.parse_args()
    main(args.start_page, args.end_page, args.max_threads, args.page_range)
