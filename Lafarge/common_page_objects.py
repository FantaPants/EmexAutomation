from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, datetime, re, os
import client_variables, function_module, email_module


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

def move_to_module(driver, locator):
    #function_module.wait_for_element_CSS(driver, locator)
    function_module.wait_for_element_XPATH(driver, "//*[@id='dtVFL']/tbody/tr[1]/td[8]/div[2]/div/a[2]/i", 60) #Remove in V8
    driver.find_element_by_css_selector(locator).click()

def click_button(driver, locator):
    function_module.wait_for_element_XPATH(driver, locator, 60)
    driver.find_element_by_xpath(locator).click()

def click_button_css(driver, locator):
    function_module.wait_for_element_CSS(driver, locator, 60)
    driver.find_element_by_css_selector(locator).click()
    
def send_value(driver, locator, value):
    function_module.wait_for_element_XPATH(driver, locator)
    driver.find_element_by_xpath(locator).click()
    driver.find_element_by_xpath(locator).clear()
    driver.find_element_by_xpath(locator).send_keys(value)
    driver.find_element_by_xpath(locator).send_keys(Keys.RETURN)

def send_value_css(driver, locator, value):
    function_module.wait_for_element_CSS(driver, locator)
    driver.find_element_by_css_selector(locator).click()
    driver.find_element_by_css_selector(locator).clear()
    driver.find_element_by_css_selector(locator).send_keys(value)
    driver.find_element_by_css_selector(locator).send_keys(Keys.RETURN)

def select_dropdown_value(driver, locator, value):
    function_module.wait_for_element_XPATH(driver, locator)
    driver.find_element_by_xpath(locator).click()
    Select(driver.find_element_by_xpath(locator)).select_by_visible_text(value)
    driver.find_element_by_xpath(locator).send_keys(Keys.RETURN)

def select_dropdown_value_css(driver, locator, value):
    function_module.wait_for_element_CSS(driver, locator)
    driver.find_element_by_css_selector(locator).click()
    Select(driver.find_element_by_css_selector(locator)).select_by_visible_text(value)
    driver.find_element_by_css_selector(locator).send_keys(Keys.RETURN)
