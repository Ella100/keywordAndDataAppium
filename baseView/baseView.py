from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import logging
class BaseView(object):
    def __init__(self,driver):
        self.locationTypeDict = {
            "xpath": By.XPATH,
            "id": By.ID,
            "name": By.NAME,
            "class_name": By.CLASS_NAME,
            "tag_name":By.TAG_NAME,
            "link_text":By.LINK_TEXT,
            "partial_link_text": By.PARTIAL_LINK_TEXT

        }
        self.driver = driver


    def get_element(self, locationType,locatorExpression):
        try:
            ele = WebDriverWait(self.driver,10).until(lambda x:x.find_element(by=self.locationTypeDict[locationType.lower()],value=locatorExpression))

        except Exception as e:
            logging.info(locatorExpression+"--该元素未找到")
        return ele

    def get_elements(self, locationType,locatorExpression):
        try:
            eles = WebDriverWait(self.driver,10).until(lambda x:x.find_elements(by=self.locationTypeDict[locationType.lower()],value=locatorExpression))
        except Exception as e:
            logging.info(locatorExpression+"--这些元素未找到")

        return eles

    # def get_window_size(self):
    #     return self.driver.get_window_size()
    #
    # def swipe(self,start_x,start_y,end_x,end_y,duration=None):
    #     return self.driver.swipe(start_x,start_y,end_x,end_y,duration=None)
