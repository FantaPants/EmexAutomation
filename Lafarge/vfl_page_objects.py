from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time
import client_variables, function_module, email_module


"""This module contains a set of page objects specific to the VFL Module"""
    
"""SHOW HIDE COLUMNS PAGE OBJECT"""

def click_show_hide_checkbox_xpath(driver, locator):
    """function opens the Show Hide Columns object and selects a checkbox using an XPATH locator"""
    function_module.wait_for_element_XPATH(driver, "//div[@id='dtVFL_wrapper']/div/div/button")
    driver.find_element_by_xpath("//div[@id='dtVFL_wrapper']/div/div/button").click()
    function_module.wait_for_element_XPATH(driver, locator)
    driver.find_element_by_xpath(locator).click()
    main = driver.find_element_by_xpath("//*[@id='main']")
    main.click()
    time.sleep(2)

def click_show_hide_checkbox_css(driver, locator):
    """function opens the Show Hide Columns object and selects a checkbox using a CSS locator"""
    function_module.wait_for_element_XPATH(driver, "//div[@id='dtVFL_wrapper']/div/div/button")
    driver.find_element_by_xpath("//div[@id='dtVFL_wrapper']/div/div/button").click()
    function_module.wait_for_element_CSS(driver, locator)
    driver.find_element_by_css_selector(locator).click()
    main = driver.find_element_by_xpath("//*[@id='main']")
    main.click()
    time.sleep(2)

def column_hidden(driver, column_object, column_name):
    """function asserts whether the given column is hidden"""
    try:
        assert column_object.is_displayed()
    except StaleElementReferenceException:
        function_module.log_to_file('Test_VFL_Module:test024_vfl_show_hide_columns:' +column_name+ ' column successfully hidden', 'PASSED')
        print column_name+' column successfully hidden'
    else:
        function_module.log_to_file('Test_VFL_Module:test024_vfl_show_hide_columns:Failed to hide' +column_name+ ' column', 'FAILED') 
        print 'ERROR WARNING - Failed to hide' +column_name+ ' column'
        email_module.error_mail('VFL Test024', 'Test could not successfully hide the' +column_name+ ' column on the VFL List View page', 'StaleElementReferenceException')
        return False
