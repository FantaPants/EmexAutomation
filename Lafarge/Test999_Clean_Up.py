# -*- coding: utf-8 -*-
from selenium import webdriver
import unittest, email_module, function_module, client_variables, common_page_objects, vfl_page_objects, time

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
        common_page_objects.login(driver, client_variables.username1, client_variables.pword1)
        print "Logged in successfully"
        #Select the VFL Module
        vfl_page_objects.open_vfl_module(driver)
        print "Moved to VFL Module"
        time.sleep(5)
        #Delete all VFL records
        vfl_page_objects.delete_remaining_vfl_records(driver)
        print "Total number of Test VFL Records now = 0"
        #Log out of the application
        common_page_objects.logout(driver)
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
        email_module.summary_mail()

    def test_009_clear_out_test_run_data(self):
        """remove all files created during test run"""
        function_module.remove_outputs_zip()
        function_module.clear_client_outputs()     
    
    def tearDown(self):
        """Test Tear Down method"""
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
