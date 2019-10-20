from baseView.baseView import BaseView
from selenium.common.exceptions import NoSuchElementException
import logging
from selenium.webdriver.common.by import By
import time
import os
from common.capability_yaml import desired_caps
import csv

class Common(BaseView):
    skipBtn = (By.ID, "com.tal.kaoyan:id/tv_skip")
    myselfBtn = (By.ID, "com.tal.kaoyan:id/mainactivity_button_mysefl")
    usernameBtn = (By.ID, "com.tal.kaoyan:id/activity_usercenter_username")
    wrapperBtn = (By.ID, "com.tal.kaoyan:id/myapptitle_RightButtonWraper")
    loginOutBtn = (By.ID, "com.tal.kaoyan:id/setting_logout_text")
    loginOutSureBtn = (By.ID, "com.tal.kaoyan:id/tip_commit")

    def check_skipBtn(self):
        logging.info("==========check_skipBtn============")
        try:
            skipBtn = self.find_element(*self.skipBtn)
        except NoSuchElementException:
            print("no skipBtn")
        else:
            skipBtn.click()

        #  跳转登入页面,因为登入和注册都要使用该模块
    def check_loginPage(self):
        logging.info("=======check_loginPage=======")
        self.driver.implicitly_wait(2)
        self.check_skipBtn()
        try:
            self.find_element(*self.myselfBtn).click()
        except NoSuchElementException:
            # 说明已经在登录页面
            self.getScreenShot('myselfbuttton Fail')
            logging.info("no mainactivity_button_mysefl")
        else:
            try:
                self.driver.implicitly_wait(5)
                username = self.find_element(*self.usernameBtn)
            except NoSuchElementException:
                print("no logined username")
            else:
                usernameText = username.get_attribute("text")
                if (usernameText == "未登录"):
                    username.click()
                else:
                    # 由于退出登入重新返回首页，所以重新进行登入
                    self.find_element(*self.wrapperBtn).click()
                    self.find_element(*self.loginOutBtn).click()
                    self.find_element(*self.loginOutSureBtn).click()
                    self.find_element(*self.myselfBtn).click()
                    self.find_element(*self.usernameBtn).click()

    def get_size(self):
        x = self.driver.get_window_size()['width']
        y = self.driver.get_window_size()['height']
        return x,y

    def swipeLeft(self):
        l = self.get_size()
        x1 = int(l[0]*0.9)
        y1 = int(l[1]*0.5)
        x2 = int(l[0]*0.1)
        self.swipe(x1,y1,x2,y1,1000)

    def getTime(self):
        self.now = time.strftime("%Y-%m-%d %H_%M_%S")
        return self.now

    def getScreenShot(self,module):
        time = self.getTime()
        image_file = os.path.dirname(os.path.dirname(__file__))+'/screenshots/%s_%s.png' % (module,time)
        logging.info("image_file:%s" % image_file)

        logging.info('get %s screenshot' % module)
        self.driver.get_screenshot_as_file(image_file)

    def get_csv_data(self,csv_file,line):
        logging.info("========get_csv data========")
        with open(csv_file,'r',encoding='utf-8-sig') as file:
            reader= csv.reader(file)
            for index,row in enumerate(reader,0):
                if index == line:
                    return row

if  __name__ == '__main__':
    driver = desired_caps()
    com = Common(driver)
    com.check_loginPage()
    # com.getScreenShot('startApp')

    # list = ["这","是","一个","测试","数据1"]
    # for i in range(len(list)):
    #     # print(i,list[i])
    #     pass
    #
    # list1 = ["这","是","一个","测试","数据2"]
    # for index,value in enumerate(list1,start=0):
    #     # print(index, value)
    #     pass
    #
    #
    #
    #
    # csv_file = '../data/account.csv'
    # data = get_csv_data(csv_file,0)
    # print(data)



