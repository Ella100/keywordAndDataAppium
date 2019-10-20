from common.capability_yaml import desired_caps
from appium import webdriver
from common.ObjectMap import get_element
from selenium.webdriver.support.ui import WebDriverWait
from time import strftime, localtime
import time
import logging
import os

# 定义全局driver变量
driver = None

def open_app():
    global driver
    driver = desired_caps()

def quit_app():
    global driver
    driver.quit()

def visit_url(url,*arg):
    global driver
    driver.get(url)

def sleep(sleepSeconds, *arg):
    try:
        time.sleep(int(sleepSeconds))
    except Exception as e:
        raise e

def clear(locationType,locatorExpression,*args):
    global driver
    try:
        get_element(driver,locationType,locatorExpression).clear()
    except Exception as e:
        raise e

def input_string(locationType,locatorExpression,inputContent):
    global driver
    try:
        get_element(driver,locationType,locatorExpression).send_keys(inputContent)
    except Exception as e:
        raise e

def click(locationType,locatorExpression,*arg):
    global driver
    try:
        get_element(driver,locationType,locatorExpression).click()
    except Exception as e:
        raise e

def assert_string_in_pagesource(assertString,*arg):
    global driver
    try:
        assert assertString in driver.page_source," %s not found in page_source" % assertString
    except AssertionError as e:
        raise AssertionError(e)
    except Exception as e:
        raise e

#获取当前上下文情况
def get_context():
    global driver
    try:
        contexts = driver.contexts
        print(contexts)
    except Exception as e:
        raise e

def switch_to_context(contextName):
    global driver
    try:
        driver.switch_to.context(contextName)
    except Exception as e:
        raise e

def get_size(*arg):
    global driver
    x = driver.get_window_size()['width']
    y = driver.get_window_size()['height']
    return x,y

def swipeLeft(*arg):
    global driver
    l = get_size()
    x1 = int(l[0]*0.9)
    y1 = int(l[1]*0.5)
    x2 = int(l[0]*0.1)
    driver.swipe(x1,y1,x2,y1,1000)

def swipeUp(*arg):
    global driver
    l = get_size()
    x1=int(l[0]*0.5)
    y1=int(l[1]*0.2)
    y2=int(l[1]*0.9)
    driver.swipe(x1,y1,x1,y2,1000)

def getScreenShot(sheetname,*arg):
    global driver
    time = strftime('%Y%m%d%H_%M_%S',localtime())
    image_file = os.path.dirname(os.path.dirname(__file__))+'\screenshots\%s_%s.png' % (sheetname,time)
    logging.info("image_file:%s" % image_file)
    driver.get_screenshot_as_file(image_file)
    return image_file


