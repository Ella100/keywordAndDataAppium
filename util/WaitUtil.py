from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class WaitUtil(object):
    def __init__(self, driver):
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
        self.wait = WebDriverWait(self.driver, 30)
    #
    # def presenceOfElementLocated(self, locatorMethod, locatorExpression, *args):
    #     '''
    #     显式等待页面算是出现在DOM中，但并不一定可见
    #     存在则返回该页面元素对象
    #     '''
    #     try:
    #         if self.locationTypeDict.has_key(locatorMethod.lower()):
    #             self.wait.until(
    #                 EC.presence_of_element_located((
    #                     (self.locationTypeDict[locatorMethod.lower()],locatorExpression)
    #                 ))
    #             )
    #         else:
    #             raise TypeError("未找到定位方式，请确认定位方法是否写正确")
    #     except Exception as e:
    #         raise e


    def visibility_element_located(self, locationType, locatorExpression, *args):
        '''
        显式等待元素页面的出现
        '''
        try:
            element = self.wait.until(EC.visibility_of_element_located
                                      ((self.locationTypeDict[locationType.lower()], locatorExpression)))
            return element
        except Exception as e:
            raise e


# if __name__ == "__main__":
#     from selenium import webdriver
#     driver = webdriver.Chrome()
#     driver.get("http://mail")
#     waitUtil = WaitUtil(driver)
