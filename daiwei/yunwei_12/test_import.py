from daiwei.common.baseView import BaseView
from daiwei.common.myunit import StartEnd
from daiwei.common.loginView import LoginView
from daiwei.common.quitView import QuitView
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import unittest
import time
import logging
import openpyxl
import re
import os

# 运维管理 - 管道段信息管理 - 导入

class GddTest(StartEnd, BaseView):

    ywglBtn = (By.XPATH, '//*[@id="css3menu"]//*[text()="运维管理"]')  # 运维管理
    gxzygl = (By.XPATH, '//*[@id="tt1"]//*[text()="管线资源管理"]')  # 管线资源管理
    gddgl = (By.XPATH, '//*[@id="tt1"]//*[text()="管道段信息管理"]')  # 管道段信息管理
    excel_start_name = '滴滴滴'
    excel_end_name = '哒哒哒'
    excel_province = '北京市'
    excel_city = '北京市'
    excel_county = '东城区'
    string = (By.XPATH, '//*[@id="tt"]/div[1]/div/div[2]/div[1]')  # 右下角该模块数据条数
    importBtn = (By.XPATH, '/html/body/div[1]/div[2]/div/a[2]')  # 导入
    download = (By.XPATH, '//*[@id="win"]/div[2]/a/span/span')  # 下载模板
    slavepath = r'C:\Users\Ymd\Downloads\管道段信息导入模板.xlsx'  # 文件全路径
    file_select = (By.XPATH, '//*[@id="FormUpdate"]/div/span/a/label')  # 点击选择文件
    submitBtn = (By.XPATH, '//*[@id="win"]/div[3]/a[1]/span/span')  # 提交
    close_alert = (By.XPATH, '/html/body/div[7]/div[1]/div[2]/a')  # 关闭提示信息
    resetBtn = (By.XPATH, '//*[@id="searchBox"]/ul/li[6]/a[2]')  # 重置
    deleteBtn = (By.XPATH, '//*[@id="datagrid-row-r1-2-0"]/td[21]/div/a[2]')  # 删除
    certain = (By.XPATH, '//*[text()="确定"]')  # 确定

    def test_login_zhaobingcheng(self):
        logging.info('=========test_login_zhaobingcheng============')
        l = LoginView(self.driver)
        data = l.get_csv_data(self.csv_file, 1)
        l.login_action(data[0], data[1])
        time.sleep(2)

        self.driver.find_element(*self.ywglBtn).click()
        time.sleep(2)
        self.driver.find_element(*self.gxzygl).click()
        time.sleep(2)
        self.driver.find_element(*self.gddgl).click()
        l.join_iframe()
        time.sleep(3)

    # 获取该模块数据条数
        be_string_num = self.driver.find_element(*self.string).text
        be_nums = re.findall('\d+\.?', be_string_num)
        be_num = be_nums[2]
        be_NUM = int(be_num)
        logging.info('导入前当前页共有数据%s条' % be_NUM)

    # 导出模板并写入内容
        self.driver.find_element(*self.importBtn).click()
        WebDriverWait(self.driver, 5).until(lambda x: x.find_element(*self.download))
        self.driver.find_element(*self.download).click()
        time.sleep(2)
        workbook = openpyxl.load_workbook(self.slavepath)  # 读取excel
        sheet = workbook['Sheet1']

    # 写入实际内容（第二行）
        logging.info("系统即将执行Excel写入...")
        sheet['D2'] = self.excel_start_name
        sheet['F2'] = self.excel_end_name
        sheet['Q2'] = self.excel_province
        sheet['R2'] = self.excel_city
        sheet['S2'] = self.excel_county

        workbook.save(self.slavepath)  # 保存
        logging.info("写入完成，即将上传")
        self.driver.find_element(*self.file_select).click()
        time.sleep(2)
        l.win32_pick_slave(self.slavepath)
        time.sleep(2)
        WebDriverWait(self.driver, 5).until(lambda x: x.find_element(*self.submitBtn))
        self.driver.find_element(*self.submitBtn).click()
        time.sleep(2)
        self.driver.find_element(*self.close_alert).click()
        self.driver.find_element(*self.resetBtn).click()
        time.sleep(2)

    # 获取导入一条数据后该模块数据条数
        af_string_num = self.driver.find_element(*self.string).text
        af_nums = re.findall('\d+\.?', af_string_num)
        af_num = af_nums[2]
        af_NUM = int(af_num)
        logging.info('导入后当前页共有数据%s条' % af_NUM)
        time.sleep(1)
        try:
            assert af_NUM == be_NUM + 1
            logging.info('管道段信息管理导入成功')
        except:
            logging.info('管道段信息管理导入失败')
            l.getScreenShot('管道段信息管理导入失败')
        time.sleep(1)

    # 删除该导入数据
        self.driver.find_element(*self.deleteBtn).click()
        self.driver.find_element(*self.certain).click()
        time.sleep(2)
        self.driver.find_element(*self.resetBtn).click()
        time.sleep(1)
        string_num = self.driver.find_element(*self.string).text
        nums = re.findall('\d+\.?', string_num)
        num = nums[2]
        NUM = int(num)
        logging.info('删除后当前页共有数据%s条' % NUM)
        time.sleep(1)
        try:
            assert NUM == be_NUM
            logging.info('导入的数据删除成功')
        except:
            logging.info('导入的数据删除失败')
            l.getScreenShot('导入的数据删除失败')
        time.sleep(1)

        os.remove(self.slavepath)

        time.sleep(1)
        l.quit_iframe()
        k = QuitView(self.driver)
        k.quit_action()


if __name__ == '__main__':
    unittest.main()
