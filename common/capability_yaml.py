from appium import webdriver
import yaml
import logging
import logging.config
import os

CON_LOG = '../config/log.conf'
log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), CON_LOG )
logging.config.fileConfig(log_file_path)
logging = logging.getLogger()


def desired_caps():

    desired_caps_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..\config\desired_caps.yaml')
    with open(desired_caps_path,'r', encoding='utf-8') as file:
        data = yaml.load(file, Loader=yaml.Loader)
     # 文件可能被占用状态，导致后面不能读取,with 可以避免此问题

    desired_caps = {}

    desired_caps['platformName']=data['platformName']
    desired_caps['platformVersion']=data['platformVersion']
    # desired_caps['udid']=data['udid']
    desired_caps['deviceName']=data['deviceName']
    desired_caps['appPackage']=data['appPackage']
    desired_caps['appActivity']=data['appActivity']
    desired_caps['noReset']=data['noReset']
    desired_caps['unicodeKeyboard']=data['unicodeKeyboard']
    desired_caps['resetKeyboard']=data['resetKeyboard']
    desired_caps['chromedriverExecutable'] = data['chromedriverExecutable']

    logging.info("start app...")
    driver =webdriver.Remote('http://'+str(data['ip'])+':'+str(data['port'])+'/wd/hub',desired_caps)
    return driver


if __name__ == "__main__":
    desired_caps()
    base_dir = os.path.dirname(os.path.dirname(__file__))
    print(os.path.dirname(__file__))
    print(base_dir)
    desired_caps_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..\config\desired_caps.yaml')
    print(desired_caps_path)
