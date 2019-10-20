from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import logging

locationTypeDict = {
    "xpath": By.XPATH,
    "id": By.ID,
    "name": By.NAME,
    "class_name": By.CLASS_NAME,
    "tag_name":By.TAG_NAME,
    "link_text":By.LINK_TEXT,
    "partial_link_text": By.PARTIAL_LINK_TEXT

}

def get_element(driver, locationType,locatorExpression):
    try:
        ele = WebDriverWait(driver,10).until(lambda x:x.find_element(by=locationTypeDict[locationType.lower()],value=locatorExpression))

    except Exception as e:
        logging.info(locatorExpression+"--该元素未找到")
    return ele

def get_elements(driver, locationType,locatorExpression):
    try:
        eles = WebDriverWait(driver,10).until(lambda x:x.find_elements(by=locationTypeDict[locationType.lower()],value=locatorExpression))
    except Exception as e:
        logging.info(locatorExpression+"--这些元素未找到")

    return eles

