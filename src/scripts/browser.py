import logging
import os
import time
from datetime import datetime
from typing import List

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from scripts import logging_config
from scripts.config import Config
from scripts.sqlAlchemyConn import SQLAlchemyConn
from vo.book import Book

# 设置日志配置
logging_config.setup_logging()
# 使用日志记录器
logger = logging.getLogger(__name__)


class Browser(webdriver.ChromeOptions):
    # 初始化
    def __init__(self):
        super().__init__()
        self.conf = Config()
        self.logger = logging.getLogger(__name__)
        self.sqlConn = SQLAlchemyConn()
        self.display_browser = self.conf.config.getboolean("config", "display_browser")

        # 获取config文件中的所有key和value，对其进行初步的优化

        # 驱动路径
        self.driver_path = os.path.join(self.conf.project_dir,
                                        self.conf.config["config"]["chromedriver_path"].strip('"'))
        self.browser: webdriver.Chrome = None

    def init_options(self):
        # 配置Chrome选项
        options = webdriver.ChromeOptions()
        # 无头模式，不显示浏览器界面
        if self.display_browser:
            options.add_argument("--headless")
        # 排除自动化工具
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # 禁用自动化扩展
        options.add_experimental_option("useAutomationExtension", False)
        # 禁用GPU加速
        options.add_argument("--disable-gpu")
        # 不加载图片
        options.add_argument("blink-settings=imagesEnabled=false")
        # 解决DevToolsActivePort文件不存在的报错
        options.add_argument("--no-sandbox")
        # 隐藏滚动条, 应对一些特殊页面
        options.add_argument("--hide-scrollbars")
        # 设置中文
        # options.add_argument("--lang=zh-CN")
        # options.add_argument('lang=zh_CN.UTF-8')

        # 添加header
        options.add_argument('accept=%s' % self.conf.config["header"]["accept"].strip('"'))

        options.add_argument('accept-encoding=%s' % self.conf.config["header"]["accept_encoding"].strip('"'))

        options.add_argument("accept-language=%s" % self.conf.config["header"]["accept_language"].strip('"'))

        options.add_argument('connection=%s' % self.conf.config["header"]["connection"].strip('"'))

        options.add_argument('user-agent=%s' % self.conf.config["header"]["user_agent"].strip('"'))

        return options

    def init_service(self):
        service = webdriver.ChromeService(str(self.driver_path))
        # service = webdriver.ChromeService(config['config']['chromedriver_path'])
        return service

    def init_browser(self):
        service = self.init_service()
        options = self.init_options()
        # 创建WebDriver对象
        # browser = webdriver.Chrome(options=options)
        browser = webdriver.Chrome(options=options, service=service)

        # 设置分辨率
        browser.set_window_size(1920, 1080)
        # 关闭浏览器上部提示语：Chrome正在受到自动软件的控制
        browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
        　　    Object.defineProperty(navigator, 'webdriver', {
        　　      get: () => undefined
        　　    })
            """
        })
        self.browser = browser
        # return browser

    # # 登录并设置cookie
    # def login(self):
    #     if self.browser is None:
    #         raise Exception("Browser is not initialized. Please call init_browser() first.")
    #
    #     # 从dat文件中读取cookie
    #
    #     self.browser.get(self.conf.config["config"]["base_url"])
    #     for cookie in self.cookie_list:
    #         self.browser.add_cookie(cookie)
    #     self.browser.get(self.conf.config["config"]["base_url"])

    def to_library(self):
        if self.browser is None:
            raise Exception("Browser is not initialized. Please call init_browser() first.")
        # 访问首页
        self.browser.get(self.conf.config["config"]["base_url"])
        # 点击"书库"
        time.sleep(int(self.conf.config["config"]["wait_time"]))
        self.browser.find_element(By.XPATH, './/div[@class="navbar-main"]/a[@href="/bookstore/?channel"]').click()
        time.sleep(int(self.conf.config["config"]["wait_time"]))

    def get_info_one_page(self, book_list: List[WebElement]):
        for book in book_list:

            # 书名
            book_name = book.find_element(By.XPATH, './/a[@class="book-name"]').text.strip()

            # 作者
            book_author = book.find_element(By.XPATH, './/a[contains(@class, "author-name")]').text.strip()
            if not book_author:
                book_author = "暂缺"
            # 考虑作者名为空的情况
            # 暂时直接输到数据库中

            # 字数
            book_word_count = book.find_element(By.XPATH, './/div[@class="book-info"]/p[1]/span[1]').text.strip()
            # book_word_count = book_word_count.replace("万字", "").replace("字", "")

            # 更新状态
            book_status = book.find_element(By.XPATH, './/div[@class="book-info"]/p[1]/span[3]').text.strip()

            # 更新时间
            book_update_time = book.find_element(By.XPATH,
                                                 './/div[@class="book-info"]/p[@class="hidden-sm-and-down book-info-update"]/span').text.strip()

            # 评分
            book_score = book.find_element(By.XPATH, './/div[@class="book-score"]/p[1]').text.strip()
            # 评分可能为“-”,即无人评分或评分人数不够,如果为“-”，设为-1
            if isinstance(book_score, (int, float)):
                pass
            elif isinstance(book_score, str):
                try:
                    book_score = float(book_score) if '.' in book_score else int(book_score)
                except ValueError:
                    book_score = -1
            else:
                book_score = -1

            # 评分人数
            book_score_count = book.find_element(By.XPATH, './/div[@class="book-score"]/p[2]').text.strip()
            if book_score_count == "无人评分":
                book_score_count = -1
            else:
                book_score_count = book_score_count.strip("人评分").strip()
            try:
                book_score_count = int(book_score_count)
            except ValueError:
                book_score_count = -1

            # 标签
            # 可能有0个或多个标签,使用find_elements先获取集合
            tag_list = book.find_elements(By.XPATH, './/p[@class="bookinfo-tags"]/*')
            tag_texts = []
            for tag in tag_list:
                tag_texts.append(tag.text)
            book_tag = ','.join(tag_texts)
            # url
            book_url = book.find_element(By.XPATH, './/a[@class="book-name"]').get_attribute('href')

            print("书名：", book_name)
            print("作者：", book_author)
            print("字数：", book_word_count)
            print("更新状态：", book_status)
            print("更新时间：", book_update_time)
            print("评分：", book_score)
            print("评分人数：", book_score_count)
            print("标签：", book_tag)
            print("url：", book_url)
            print("-----------------------------------")
            # 插入数据库
            book = Book(book_name=book_name, book_author=book_author,
                        book_url=book_url, book_word_count=book_word_count,
                        book_status=book_status, book_update_time=book_update_time,
                        book_score=book_score, book_score_count=book_score_count,
                        book_tag=book_tag, update_time=datetime.now())
            book.info_check()
            self.sqlConn.insert_or_update_book(book)

    def get_info_all(self, start_page=1, end_page=0):
        # 第一页

        # 点击按钮
        # //div[@class="el-pagination is-background"]/button[@class="btn-next"]

        # 算了，还是直接输url吧
        # page = 1
        # page_end = 3
        if start_page < 0 or end_page < 0:
            raise ValueError("参数异常，start_page：", start_page, "end_page：", end_page)
        if end_page == 0:
            end_page = 15713
        # page_url = self.conf.config["config"]["page_url"]

        # 跳转到书库页面
        self.to_library()

        try:
            while start_page <= end_page:
                # url = "{}={}".format(page_url, start_page)
                print("第", start_page, "页......")
                # print("url：", url)
                # self.browser.get(url)

                # 选择input输入框
                input_box = self.browser.find_element(By.XPATH,
                                                      './/div[@class="el-input el-pagination__editor is-in-pagination"]/input[@class="el-input__inner"]')
                # input_box.clear()
                # input_box.clear()
                # 全选
                input_box.send_keys(Keys.CONTROL, "a")
                # 输入页数
                input_box.send_keys(start_page)
                input_box.send_keys(Keys.RETURN)
                # time.sleep(5)

                # # 点击下一页按钮
                # self.browser.find_element(By.XPATH, './/button[@class="btn-next"]').click()

                time.sleep(int(self.conf.config["config"]["wait_time"]))

                book_list = self.browser.find_elements(By.XPATH, '//div[@class="result-item-layout-body"]')
                self.get_info_one_page(book_list)
                start_page = start_page + 1
        except Exception as e:
            print("出现异常，当前页数为：", start_page, "异常信息：", e)

# browser = Browser()
# print(browser.current_dir)
# print(browser.project_dir)
# print(browser.config_path)
# print(browser.driver_path)
# current_path = os.path.dirname(os.path.abspath(__file__))
# root_path = os.path.dirname(current_path)
# print(root_path)

# print(os.path.exists("../../resources/config.ini"))
# print(os.path.exists("./resources/config.ini"))
# print(os.path.exists("/resources/config.ini"))
# print(os.path.exists("resources/config.ini"))
# print(os.path.exists("config.ini"))
# print(os.path.exists("/config.ini"))

# project_dir=os.path.dirname(sys.argv[0])
# print(project_dir)
# print(os.path.dirname(os.path.abspath(__file__)))
# print(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../"))

# print(f"Current directory: {pathlib.Path.cwd()}")
# print(f"Home directory: {pathlib.Path.home()}")
