# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import unittest, email_module, function_module, client_variables, time

class Test_002_VFL_Clean_Up(unittest.TestCase):
    """Run VFL Module clean up at end of test run"""
    def setUp(self):
        """Standard test setup method"""
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = client_variables.base_url
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_001_delete_all_VFL_records(self):
        """Test accesses VFL Module and deletes all VLF records created
        during the test run"""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        driver.find_element_by_name("UserName").clear()
        driver.find_element_by_name("UserName").send_keys(client_variables.username1)
        driver.find_element_by_name("Password").clear()
        driver.find_element_by_name("Password").send_keys(client_variables.pword1)
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        print "Logged in successfully"
        #Select the VFL Module
        driver.find_element_by_css_selector("i.fa.fa-lg.fa-fw.fa-comments").click()
        time.sleep(5)
        print "Moved to VFL Module"
        time.sleep(5)
        #Delete all VFL records
        amount_of_records = driver.find_element_by_xpath("//*[@id='dtVFL_info']").text
        time.sleep(1)
        while amount_of_records != '0 to 0 of 0 entries':
            driver.find_element_by_xpath("//*[@id='dtVFL']/thead/tr/th[1]/input").click()
            time.sleep(1)
            driver.find_element_by_xpath("//*[@id='removeVfl']/i").click()
            time.sleep(1)
            driver.find_element_by_xpath("//*[@id='bot2-Msg1']").click()
            time.sleep(3)
            amount_of_records = driver.find_element_by_xpath("//*[@id='dtVFL_info']").text
            print amount_of_records
        print "Total number of Test VFL Records now = 0"
        #Log out of the application
        driver.find_element_by_css_selector("i.fa.fa-power-off").click()
        driver.find_element_by_id("bot2-Msg1").click()
        print "All VFL Records deleted"

    def tearDown(self):
        """Standard test tear down method"""
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

class Test_999_System_Clean_Up(unittest.TestCase):
    """Run system clean up functions at end of test run"""
    def setUp(self):
        """Standard test setup method"""
        self.verificationErrors = []
        self.accept_next_alert = True
        
    def test_008_generate_summary_email(self):
        """generate and send summary email"""
        email_module.SummaryMail()

    def test_009_clear_out_test_run_data(self):
        """remove all files created during test run"""
        function_module.remove_outputs_zip()
        function_module.clear_client_outputs()     
    
    def tearDown(self):
        """Test Tear Down method"""
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
