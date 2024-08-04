import configparser
import os


class Config:
    def __init__(self):
        self.config = configparser.ConfigParser()
        # 当前文件路径
        self.current_dir = os.path.abspath(__file__)
        # 项目根路径
        self.project_dir = os.path.dirname(os.path.dirname(os.path.dirname(self.current_dir)))
        self.resources_dir = os.path.join(self.project_dir, "resources")
        # 配置文件路径
        self.config_path = os.path.join(self.project_dir, "resources/config.ini")
        self.config.read(self.config_path, encoding="utf-8")
        self.driver_path = os.path.join(self.project_dir, self.config["config"]["chromedriver_path"].strip('"'))


# c = Config()
# var = c.config["config"]["chromedriver_path"]
# print(var.strip('"'))
