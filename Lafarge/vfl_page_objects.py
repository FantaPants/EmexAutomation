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
import client_variables, function_module, email_module, common_page_objects


"""This module contains a set of page objects specific to the VFL Module"""

"""VFL Specific Buttons"""
def open_vfl_module(driver):
    common_page_objects.move_to_module(driver, "i.fa.fa-lg.fa-fw.fa-comments")

def add_new_vfl_record(driver):
    function_module.wait_for_element_CSS(driver, "i.glyphicon.glyphicon-plus", 60)
    driver.find_element_by_css_selector("i.glyphicon.glyphicon-plus").click()

def edit_latest_vfl_record(driver):
    function_module.wait_for_element_XPATH(driver, "//*[@id='dtVFL']/tbody/tr[1]/td[8]/div[2]/div/a[2]/i", 60)
    driver.find_element_by_xpath("//*[@id='dtVFL']/tbody/tr[1]/td[8]/div[2]/div/a[2]/i").click()

def vfl_next_button(driver):
    common_page_objects.click_button(driver, "//*[@id='btnNextSubmit']")
    
def vfl_finish_button(driver):
    common_page_objects.click_button(driver, "//*[@id='bootstrap-wizard-1']/div[2]/div[3]/div/div/ul/li[2]/a")

"""VFL specific fields"""

def vfl_date(driver, date):
    common_page_objects.send_value(driver, "//*[@id='VflDate']", date)

def vfl_workgroup_selector(driver, workgroup):
    common_page_objects.send_value(driver, "//*[@id='s2id_autogen1']", workgroup)

def vfl_business_unit(driver, bu):
    common_page_objects.select_dropdown_value(driver, "//*[@id='ProductLine']", bu)

def vfl_location(driver, location):
    common_page_objects.select_dropdown_value(driver, "//*[@id='Location']", location)

def vfl_participants(driver, participant):
    common_page_objects.send_value(driver, "//*[@id='s2id_autogen2']", participant)

def vfl_employees(driver, employee):
    common_page_objects.send_value(driver, "//*[@id='formDetails']/div/section[2]/section[2]/div/div/input", employee)

def vfl_comment(driver, comment):
    common_page_objects.send_value(driver, "//*[@id='Comments']", comment)

def vfl_time(driver, time_in, time_out):
    common_page_objects.send_value(driver, "//*[@id='TimeIn']", time_in)
    common_page_objects.send_value(driver, "//*[@id='TimeOut']", time_out)

"""VFL ACTS"""

def add_vfl_act(driver, radio, act_type):
    radio_string = str(radio)
    function_module.wait_for_element_XPATH(driver, "//*[@id='formActs']/div/section[1]/div/label["+radio_string+"]/i")
    driver.find_element_by_xpath("//*[@id='formActs']/div/section[1]/div/label["+radio_string+"]/i").click()
    Select(driver.find_element_by_xpath("//*[@id='Acts']")).select_by_visible_text(act_type)
    common_page_objects.click_button(driver, "//*[@id='btnSubmitFormActs']")
    
def edit_top_act(driver, act_type):
    function_module.wait_for_element_CSS(driver, "i.glyphicon.glyphicon-pencil")
    driver.find_element_by_css_selector("i.glyphicon.glyphicon-pencil").click()
    Select(driver.find_element_by_xpath("//*[@class='col col-6']/div/div/label/select")).select_by_visible_text(act_type)
    driver.find_element_by_css_selector(".fa.fa-save.glyphicon-size").click()

def delete_top_act(driver):
    function_module.wait_for_element_CSS(driver, "i.glyphicon.glyphicon-trash")
    driver.find_element_by_css_selector("i.glyphicon.glyphicon-trash").click()
    function_module.wait_for_element_XPATH(driver, "//*[@id='bot2-Msg1']")
    driver.find_element_by_xpath("//*[@id='bot2-Msg1']").click()
    

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
