from selenium import webdriver
from selenium.webdriver.common.by import By
import unittest, time
import function_module


"""This module contains a set of common page objects used throughout the Emex application"""

def login(driver, username, password):
    """function logins into the Emex application using given username and password"""
    function_module.wait_for_element_CSS(driver, "button.btn.btn-primary")
    driver.find_element_by_name("UserName").clear()
    driver.find_element_by_name("UserName").send_keys(username)
    driver.find_element_by_name("Password").clear()
    driver.find_element_by_name("Password").send_keys(password)
    driver.find_element_by_css_selector("button.btn.btn-primary").click()    

def logout(driver):
    """fucntion logouts of the Emex application"""
    driver.find_element_by_css_selector("i.fa.fa-power-off").click()
    function_module.wait_for_element_ID(driver, "bot2-Msg1")
    driver.find_element_by_id("bot2-Msg1").click()
    
    
