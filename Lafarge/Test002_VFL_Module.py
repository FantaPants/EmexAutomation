# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, datetime, re, os
import client_variables, function_module, email_module, common_page_objects, vfl_page_objects

    
class Test_001_VFL_Forms(unittest.TestCase):
    """Set of tests responsible for testing the functionality of
    VFL Details and Acts forms. Used with Creating and Editing
    VFL Records"""                
    def setUp(self):
        """Standard test setup method"""
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = client_variables.base_url
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_001_add_new_vfl_test_details(self):
        """Testing the VFL details form when adding a new VFL Record.
        Test includes asserts to ensure each particular field adheres
        to expected behaviour"""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        common_page_objects.login(driver, client_variables.username1, client_variables.pword1)
        function_module.log_to_file('VFL_Module:test001_add_new_VFL_record_test_details:Successfully logged in and started test')
        print "Logged in successfully"
        #Select the VFL Module
        """Replace with VFL Page Object 'open_vfl_module' once V8 is active"""
        function_module.wait_for_element_CSS(driver, "i.fa.fa-lg.fa-fw.fa-comments")
        driver.find_element_by_css_selector("i.fa.fa-lg.fa-fw.fa-comments").click()
        print "Moved to VFL Module"
        #Choose to add a new VFL Record
        vfl_page_objects.add_new_vfl_record(driver)
        print "Found new VFL button successfully"
        #Verify Due Date is Mandatory
        function_module.field_is_mandatory_css(driver, "#VflDate")
        #Verify WorkGroup is Mandatory
        function_module.field_is_mandatory_css(driver, "#WorkGroup")
        #Verify Product Line is Read Only
        function_module.field_is_read_only_css(driver, "#ProductLine")
        #Verify Product Line is Mandatory
        function_module.field_is_mandatory_css(driver, "#ProductLine")
        #Verify TimeIn is Mandatory
        function_module.field_is_mandatory_css(driver, "#TimeIn")
        #Verify TimeOut is Mandatory
        function_module.field_is_mandatory_css(driver, "#TimeIn")
        #Verify Minutes is Read Only
        function_module.field_is_read_only_css(driver, "#minutes")
        function_module.log_to_file('VFL_Module:test001_add_new_VFL_record_test_details:Successfully verified all mandatory and/or read only fields', 'PASSED')
        print "All mandatory and read only fields verfied"
        #Select the 1st day of the month. Selecting the 1st day will help ensure test doesn't fail for wrong reasons
        vfl_page_objects.vfl_date(driver, function_module.first_day_of_month())
        print "Selected first day of the month for VFL Date field"
        #Select Site with NO Default Product Line & Allow Data = NO
        vfl_page_objects.vfl_workgroup_selector(driver, client_variables.root_wg)
        #Assert WorkGroup cannot be found
        function_module.verify_value(driver, "//*[@id='select2-drop']/ul/li", 'No matches found', 'VFL', 'test001_add_new_VFL_record_test_details',
        'Workgroup with Allow Data = NO cannot be selected', 'Workgroup with Allow Data = NO was selected')
        time.sleep(1)
        #Select a new Site with a Default Business Unit & Allow Data = YES
        vfl_page_objects.vfl_workgroup_selector(driver, client_variables.wg_default_true)
        #Assert that Business Unit field has been automatically populated
        function_module.verify_dropdown_value(driver, "//*[@id='ProductLine']", client_variables.bu1, 'VFL', 'test001_add_new_VFL_record_test_details',
        'Default Business Unit was selected automatically', 'Business Unit field was not automaticallly populated by WGs default Product Line')
        time.sleep(1)
        #Clear Site field and select Site with NO Default Business Unit & Allow Data = YES
        vfl_page_objects.clear_selected_vfl_workgroup(driver)
        vfl_page_objects.vfl_workgroup_selector(driver, client_variables.wg_default_false)
        print "Selected a WorkGroup with no Default Business Unit, but Allow Data = Yes"
        #Select Business Unit
        vfl_page_objects.vfl_business_unit(driver, client_variables.bu2)
        print "Selected Business Unit successfully"
        #Select Location
        vfl_page_objects.vfl_location(driver, client_variables.location1)
        print "Selected Location successfully"
        #Assert Participants field is automatically populated with current user
        function_module.verify_value(driver, "//*[@id='s2id_Participants']/ul/li[1]/div", client_variables.fullname1, 'VFL', 'test001_add_new_VFL_record_test_details',
        'Participants field was automatically populated with current user', 'Participants field not automatically populated with current user')
        time.sleep(1)
        #Add second user to Participants field
        vfl_page_objects.vfl_participants(driver, client_variables.fullname2)
        print "Added second user to Participants field"
        #Assert Second Participant added successfully
        function_module.verify_value(driver, "//*[@id='s2id_Participants']/ul/li[2]/div", client_variables.fullname2, 'VFL', 'test001_add_new_VFL_record_test_details',
        'Second Participant was added successfully', 'Second Participant was NOT added successfully')
        time.sleep(1)
        #Add value to Employees Spoken to field
        vfl_page_objects.vfl_employees(driver, "Richie Test")
        print "Entered value into Employees Spoken Too field"
        #Enter a string into the Comments field
        vfl_page_objects.vfl_comment(driver, "testing automated VFL creation")
        print "Entered value into Comments field"
        #Set time to 60 minutes
        vfl_page_objects.vfl_time(driver, "0:00", "1:00")
        print "Set the Time In and Time Out fields"
        #Move successfully to the next tab
        vfl_page_objects.vfl_next_button(driver)
        print "Moved to Acts Tab"
        #Select the finish button to return to the Main List View
        vfl_page_objects.vfl_finish_button(driver)
        function_module.log_to_file('VFL_Module:test001_add_new_VFL_record_test_details:Successfully saved new VFL record')
        print "Successfully saved VFL Record and returned to list view"
        #Log out of the application
        common_page_objects.logout(driver)
        function_module.log_to_file('VFL_Module:test001_add_new_VFL_record_test_details:TEST COMPLETED', 'PASSED')
        print "VFL_Module:test001_add_new_VFL_record_test_details:TEST COMPLETED"

    def test_002_edit_existing_vfl_record(self):
        """Test to ensure that existing VFL records can be edited successfully"""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        common_page_objects.login(driver, client_variables.username1, client_variables.pword1)
        function_module.log_to_file('VFL_Module:test002_edit_existing_vfl_record:Successfully logged in and started test')
        print "Logged in successfully"
        #Select the VFL Module
        vfl_page_objects.open_vfl_module(driver)
        print "Moved to VFL Module"
        #Edit the latest VFL Record
        vfl_page_objects.edit_latest_vfl_record(driver)
        print "Found Edit VFL button for latest VFL Record"
        #Change value of Comments field
        vfl_page_objects.vfl_comment(driver, "testing automated VFL creation - EDITED")
        print "Successfullt edited Comments field"
        #Move successfully to the next tab
        vfl_page_objects.vfl_next_button(driver)
        print "Moved to Acts Tab"
        #Select the finish button to return to the Main List View
        vfl_page_objects.vfl_finish_button(driver)
        print "Successfully saved VFL Record and returned to list view"
        #Assert that the changes to the VFL record have been saved
        function_module.verify_value(driver, "//*[@id='dtVFL']/tbody/tr[1]/td[7]", "testing automated VFL creation - EDITED", 'VFL', 'test002_edit_existing_vfl_record',
        'Changes made to VFL record were saved successfully', 'Changes made to VFL record were not saved successfully')
        time.sleep(1)
        #Log out of the application
        common_page_objects.logout(driver)
        function_module.log_to_file('VFL_Module:test002_edit_existing_vfl_record:TEST COMPLETED', 'PASSED')
        print "VFL_Module:test002_edit_existing_vfl_record:TEST COMPLETED"

    def test_003_add_edit_delete_safe_acts(self):
        """Test to add a new Safe Act on the Acts tab. The newly created
        Act is then edited and also deleted. The Act is deleted so as to
        to simplify following tests."""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        common_page_objects.login(driver, client_variables.username1, client_variables.pword1)
        function_module.log_to_file('VFL_Module:test003_add_edit_delete_safe_acts:Successfully logged in and started test')
        print "Logged in successfully"
        #Select the VFL Module
        vfl_page_objects.open_vfl_module(driver)
        print "Moved to VFL Module"
        #Choose to edit existing VFL Record
        vfl_page_objects.edit_latest_vfl_record(driver)
        print "Found Edit VFL button for latest VFL Record"
        #Move successfully to the next tab
        vfl_page_objects.vfl_next_button(driver)
        print "Moved to Acts Tab"
        #Add a Safe Act of type 1
        vfl_page_objects.add_vfl_act(driver, 1, client_variables.act_type1)
        time.sleep(2)
        print "Added Safe Act - First option in dropdown"
        #Assert that Safe Act of type 1 cannot be selected again, hence asserting that it has been successfully added
        function_module.verify_radio_dropdown_element_is_disabled(driver, "//*[@id='formActs']/div/section[1]/div/label[1]/i", "//*[@id='Acts']/option[2]", 'VFL', 'test003_add_edit_delete_safe_acts',
        'Successfully asserted Safe Act type 1 cannot be added twice (1)', 'User can select the same Safe Act Twice (1)')
        time.sleep(1)
        #Edit a Safe Act of type 1 and change to type 2
        vfl_page_objects.edit_top_act(driver, client_variables.act_type2)
        time.sleep(2)
        print "Edited Safe Act - Second option in dropdown"
        #Assert that Safe Act of type 2 cannot be selected again, hence asserting the act has been successfully edited
        function_module.verify_radio_dropdown_element_is_disabled(driver, "//*[@id='formActs']/div/section[1]/div/label[1]/i", "//*[@id='Acts']/option[3]", 'VFL', 'test003_add_edit_delete_safe_acts',
        'Successfully asserted Safe Act type 2 cannot be added twice (2)', 'User can select the same Safe Act Twice (2)')
        time.sleep(1)
        #Delete Safe Act
        vfl_page_objects.delete_top_act(driver)
        time.sleep(5)
        #Verify Act was deleted by confirming that the edit Act button is not present
        self.driver.implicitly_wait(0)
        function_module.verify_element_not_present_CSS(driver, "i.glyphicon.glyphicon-pencil", 'VFL', 'test003_add_edit_delete_safe_acts',
        'Successfully deleted Safe Act', 'Test failed to verify that the Safe Act was successfully deleted')
        self.driver.implicitly_wait(30)
        #Select the finish button to return to the Main List View
        vfl_page_objects.vfl_finish_button(driver)
        print "Successfully saved VFL Record and returned to list view"
        #Log out of the application
        common_page_objects.logout(driver)
        function_module.log_to_file('VFL_Module:test003_add_edit_delete_safe_acts:TEST COMPLETED', 'PASSED')
        print "VFL_Module:test003_add_edit_delete_safe_acts:TEST COMPLETED"

    def test_004_add_edit_unsafe_acts(self):
        """Test to add a new Unsafe Act on the Acts tab. The newly created
        Act is then edited but not deleted. At least one Act needs to remain
        in order to successfully complete tests for comments and actions"""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        common_page_objects.login(driver, client_variables.username1, client_variables.pword1)
        function_module.log_to_file('VFL_Module:test004_add_edit_unsafe_acts:Successfully logged in and started test')
        print "Logged in successfully"
        #Select the VFL Module
        vfl_page_objects.open_vfl_module(driver)
        print "Moved to VFL Module"
        #Choose to edit existing VFL Record
        vfl_page_objects.edit_latest_vfl_record(driver)
        print "Found Edit VFL button for latest VFL Record"
        #Move successfully to the next tab
        vfl_page_objects.vfl_next_button(driver)
        print "Moved to Acts Tab"
        #Add an Unsafe Act of type 1
        vfl_page_objects.add_vfl_act(driver, 2, client_variables.act_type1)
        time.sleep(2)
        print "Added Unsafe Act - First option in dropdown"
        #Assert that Unsafe Act of type 1 cannot be selected again, hence asserting that it has been successfully added
        function_module.verify_radio_dropdown_element_is_disabled(driver, "//*[@id='formActs']/div/section[1]/div/label[2]/i", "//*[@id='Acts']/option[2]", 'VFL', 'test004_add_edit_unsafe_acts',
        'Successfully asserted Unsafe Act type 1 cannot be added twice (1)', 'User can select the same Unsafe Act Twice (1)')
        time.sleep(1)
        #Edit an Unsafe Act of type 1 and change to type 2
        vfl_page_objects.edit_top_act(driver, client_variables.act_type2)
        time.sleep(2)
        print "Edited Unsafe Act - Second option in dropdown"
        #Assert that Safe Act of type 2 cannot be selected again, hence asserting the act has been successfully edited
        function_module.verify_radio_dropdown_element_is_disabled(driver, "//*[@id='formActs']/div/section[1]/div/label[2]/i", "//*[@id='Acts']/option[3]", 'VFL', 'test004_add_edit_unsafe_acts',
        'Successfully asserted Unsafe Act type 2 cannot be added twice (2)', 'User can select the same Unsafe Act Twice (2)')
        time.sleep(1)
        #Select the finish button to return to the Main List View
        vfl_page_objects.vfl_finish_button(driver)
        print "Successfully saved VFL Record and returned to list view"
        #Log out of the application
        common_page_objects.logout(driver)
        function_module.log_to_file('VFL_Module:test004_add_edit_unsafe_acts:TEST COMPLETED', 'PASSED')
        print "VFL_Module:test004_add_edit_unsafe_acts:TEST COMPLETED"

    def test_005_add_conversations(self):
        """Test to add conversation to an existing Act"""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        common_page_objects.login(driver, client_variables.username1, client_variables.pword1)
        function_module.log_to_file('VFL_Module:test005_add_conversations:Successfully logged in and started test')
        print "Logged in successfully"
        #Select the VFL Module
        vfl_page_objects.open_vfl_module(driver)
        print "Moved to VFL Module"
        #Choose to edit existing VFL Record
        vfl_page_objects.edit_latest_vfl_record(driver)
        print "Found Edit VFL button for latest VFL Record"
        #Move successfully to the next tab
        vfl_page_objects.vfl_next_button(driver)
        print "Moved to Acts Tab"
        #Add a Conversation & assert that Comment field is mandatory
        vfl_page_objects.add_conversation(driver, "Testing adding conversations")      
        #Assert that Conversation has been added correctly
        function_module.verify_value(driver, "//*[@class='col col-8']/label[1]", "Testing adding conversations", 'VFL', 'test005_add_conversations',
        'Successfully asserted conversation was added', 'Test could not successfully verify that the Conversation was added as expected')
        time.sleep(1)
        #Select the finish button to return to the Main List View
        vfl_page_objects.vfl_finish_button(driver)
        print "Successfully saved VFL Record and returned to list view"
        #Log out of the application
        common_page_objects.logout(driver)
        function_module.log_to_file('VFL_Module:test005_add_conversations:TEST COMPLETED', 'PASSED')
        print "VFL_Module:test005_add_conversations:TEST COMPLETED"

    def test_006_edit_conversations(self):
        """Test to ensure that exisitng conversations can be edited successfully and
        that image files can be successfully attached to a conversation"""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        common_page_objects.login(driver, client_variables.username1, client_variables.pword1)
        function_module.log_to_file('VFL_Module:test006_edit_conversations:Successfully logged in and started test')
        print "Logged in successfully"
        #Select the VFL Module
        vfl_page_objects.open_vfl_module(driver)
        print "Moved to VFL Module"
        #Choose to edit existing VFL Record
        vfl_page_objects.edit_latest_vfl_record(driver)
        print "Found Edit VFL button for latest VFL Record"
        #Move successfully to the next tab
        vfl_page_objects.vfl_next_button(driver)
        print "Moved to Acts Tab"
        #Edit the Conversation
        vfl_page_objects.edit_conversation(driver, "Testing adding conversations - EDITED")
        driver.refresh()
        #Verify that Conversation has been edited correctly
        vfl_page_objects.expand_latest_act(driver)
        function_module.verify_value(driver, "//*[@class='col col-8']/label[1]", "Testing adding conversations - EDITED", 'VFL', 'test006_edit_conversations',
        'Successfully edited an existing conversation', 'Test could not successfully verify that the Conversation was edited as expected')
        driver.refresh()
        #Edit the conversation and add an image
        vfl_page_objects.add_image(driver, "V:\QA\Automation\Automation_Resources\Attachments\Conversation Image\PM5544_with_non-PAL_signals.png")
        driver.refresh()
        print "Attached image file to conversation correctly"
        #Verify the image has been successfully attached
        function_module.verify_element_is_present_CSS(driver, ".fa.fa-picture-o", 'VFL', 'test006_edit_conversations',
        'Successfully attached an Image to a conversation', 'Test could not successfully verify that an image was attached to the conversation')
        #Select the finish button to return to the Main List View
        vfl_page_objects.vfl_finish_button(driver)
        print "Successfully saved VFL Record and returned to list view"
        #Log out of the application
        common_page_objects.logout(driver)
        function_module.log_to_file('VFL_Module:test006_edit_conversations:TEST COMPLETED', 'PASSED')
        print "VFL_Module:test006_edit_conversations:TEST COMPLETED"

    def test_007_delete_conversations(self):
        """Test to ensure that existing conversations can be successfully deleted"""
        driver = self.driver
        self.driver.implicitly_wait(30)
        driver.get(self.base_url + "/")
        #Login to the application
        common_page_objects.login(driver, client_variables.username1, client_variables.pword1)
        function_module.log_to_file('VFL_Module:test007_delete_conversations:Successfully logged in and started test')
        print "Logged in successfully"
        #Select the VFL Module
        vfl_page_objects.open_vfl_module(driver)
        print "Moved to VFL Module"
        #Choose to edit existing VFL Record
        vfl_page_objects.edit_latest_vfl_record(driver)
        print "Found Edit VFL button for latest VFL Record"
        #Move successfully to the next tab
        vfl_page_objects.vfl_next_button(driver)
        print "Moved to Acts Tab"
        #Delete the Conversation
        vfl_page_objects.delete_conversation(driver)
        driver.refresh()
        #Verify Conversation was deleted by confirming that the edit conversation button is not present
        vfl_page_objects.expand_latest_act(driver)
        self.driver.implicitly_wait(0)
        function_module.verify_element_not_present_CSS(driver, "i.fa.fa-pencil", 'VFL', 'test007_delete_conversations',
        'Asserted Conversation has been successfully deleted', 'Test could not successfully verify that the Conversation was deleted as expected')
        self.driver.implicitly_wait(30)
        #Select the finish button to return to the Main List View
        vfl_page_objects.vfl_finish_button(driver)
        print "Successfully saved VFL Record and returned to list view"
        #Log out of the application
        common_page_objects.logout(driver)
        function_module.log_to_file('VFL_Module:test007_delete_conversations:TEST COMPLETED', 'PASSED')
        print "VFL_Module:test007_delete_conversations:TEST COMPLETED"

    def test_008_add_action(self):
        """Test to ensure that VFL Corrective Actions can be added to existin Acts
        All fields with mandatory requirements on the action from are tested with assertions
        NOTE: Test is unfinished as would like to add SQL based assertion to ensure Action was
        synced with main application correctly"""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        common_page_objects.login(driver, client_variables.username1, client_variables.pword1)
        function_module.log_to_file('VFL_Module:test008_add_action:Successfully logged in and started test')
        print "Logged in successfully"
        #Select the VFL Module
        vfl_page_objects.open_vfl_module(driver)
        print "Moved to VFL Module"
        #Choose to edit existing VFL Record
        vfl_page_objects.edit_latest_vfl_record(driver)
        print "Found Edit VFL button for latest VFL Record"
        #Move successfully to the next tab
        vfl_page_objects.vfl_next_button(driver)
        print "Moved to Acts Tab"
        #Add an Action
        vfl_page_objects.add_action(driver, function_module.today(), "Low", "testing automated VFL Corrective Actions", client_variables.username2)
        #Assert that Action has been added correctly
        function_module.verify_value(driver, "//*[@class='col col-6']/label[1]", "testing automated VFL Corrective Actions", 'VFL', 'test008_add_action',
        'Successfully asserted action was added', 'Failed to add a action to an existing act')
        time.sleep(1)
        """
        ADDTIONAL WORK REQUIRED;

        WHEN ACTIONS MODULE READY - After adding a VFL Action, this test should then confirm that the Action has synced with the Action module correctly

        POSSIBLY CHECK DATABASE - Research & Add SQL Based Assertions to check that Action has been added correctly. 
        """
        #Select the finish button to return to the Main List View
        vfl_page_objects.vfl_finish_button(driver)
        print "Successfully saved VFL Record and returned to list view"
        #Log out of the application
        common_page_objects.logout(driver)
        function_module.log_to_file('VFL_Module:test008_add_action:TEST COMPLETED', 'PASSED')
        print "VFL_Module:test008_add_action:TEST COMPLETED"

    def test_009_edit_action(self):
        """Test to ensure that existing actions can be edited successfully"""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        common_page_objects.login(driver, client_variables.username1, client_variables.pword1)
        function_module.log_to_file('VFL_Module:test009_edit_action:Successfully logged in and started test')
        print "Logged in successfully"
        #Select the VFL Module
        vfl_page_objects.open_vfl_module(driver)
        print "Moved to VFL Module"
        #Choose to edit existing VFL Record
        vfl_page_objects.edit_latest_vfl_record(driver)
        print "Found Edit VFL button for latest VFL Record"
        #Move successfully to the next tab
        vfl_page_objects.vfl_next_button(driver)
        print "Moved to Acts Tab"
        #Edit an Action
        vfl_page_objects.edit_action(driver, function_module.today(), "High", "testing automated VFL Corrective Actions - EDITED", client_variables.username2)
        driver.refresh()       
        #Assert that Action has been edited correctly
        vfl_page_objects.expand_latest_act(driver)
        function_module.verify_value(driver, "//*[@class='col col-6']/label[1]", "testing automated VFL Corrective Actions - EDITED", 'VFL', 'test009_edit_action',
        'Successfully saved changes to Action', 'Test failed to verify that the VFL Action was edited as expected')
        time.sleep(1)
        #Select the finish button to return to the Main List View
        vfl_page_objects.vfl_finish_button(driver)
        print "Successfully saved VFL Record and returned to list view"
        #Log out of the application
        common_page_objects.logout(driver)
        function_module.log_to_file('VFL_Module:test009_edit_action:TEST COMPLETED', 'PASSED')
        print "VFL_Module:test009_edit_action:TEST COMPLETED"

    def test_010_delete_action(self):
        """Test to ensure that existing VFL Corrective Actions can be deleted successfully"""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        common_page_objects.login(driver, client_variables.username1, client_variables.pword1)
        function_module.log_to_file('VFL_Module:test010_delete_action:Successfully logged in and started test')
        print "Logged in successfully"
        #Select the VFL Module
        vfl_page_objects.open_vfl_module(driver)
        print "Moved to VFL Module"
        #Choose to edit existing VFL Record
        vfl_page_objects.edit_latest_vfl_record(driver)
        print "Found Edit VFL button for latest VFL Record"
        #Move successfully to the next tab
        vfl_page_objects.vfl_next_button(driver)
        print "Moved to Acts Tab"
        #Delete an Action
        vfl_page_objects.delete_action(driver)
        driver.refresh()
        #Verify Action was deleted by confirming that the edit Action button is not present
        vfl_page_objects.expand_latest_act(driver)
        self.driver.implicitly_wait(0)
        function_module.verify_element_not_present_XPATH(driver, "//*[@id='dtVFL']/tbody/tr[1]/td[8]/div[2]/div/a[2]/i", 'VFL', 'test010_delete_action',
        'Verified Action has been successfully deleted', 'Test failed to verify that the VFL Action was deleted as expected')
        self.driver.implicitly_wait(30)
        #Select the finish button to return to the Main List View
        vfl_page_objects.vfl_finish_button(driver)
        print "Successfully saved VFL Record and returned to list view"
        #Log out of the application
        common_page_objects.logout(driver)
        function_module.log_to_file('VFL_Module:test010_delete_action:TEST COMPLETED', 'PASSED')
        print "VFL_Module:test010_delete_action:TEST COMPLETED"

    def test_011_view_existing_vfl_record(self):
        """Test to ensure that VFL records behave as expected when in view mode.
        All fields on the first tab have assertions to verify that they are disabled
        and various checks are performed on the Acts tab to ensure that controls for
        adding/editing acts are not present"""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        common_page_objects.login(driver, client_variables.username1, client_variables.pword1)
        function_module.log_to_file('VFL_Module:test011_view_existing_vfl_record:Successfully logged in and started test')
        print "Logged in successfully"
        #Select the VFL Module
        vfl_page_objects.open_vfl_module(driver)
        print "Moved to VFL Module"
        #View the latest VFL Record (READ-ONLY)
        vfl_page_objects.view_latest_vfl_record(driver)
        print "Found View VFL button for latest VFL Record"
        #Verify that all fields on the details tab are disabled
        function_module.field_is_read_only_css(driver, "#VflDate")
        function_module.field_is_read_only_css(driver, "#WorkGroup")
        function_module.field_is_read_only_css(driver, "#ProductLine")
        function_module.field_is_read_only_css(driver, "#Location")
        function_module.field_is_read_only_css(driver, "#TimeIn")
        function_module.field_is_read_only_css(driver, "#TimeOut")
        function_module.field_is_read_only_css(driver, "#minutes")
        function_module.field_is_read_only_css(driver, "#Participants")
        function_module.field_is_read_only_css(driver, "#PersonsSpokenTo")
        function_module.field_is_read_only_css(driver, "#Comments")
        print "Verified that all fields on the VFL Details tab are set to read only when in View Mode"
        #Move successfully to the next tab
        vfl_page_objects.vfl_next_button(driver)
        print "Moved to Acts Tab"
        #Verify that Safe Acts radio button is not present on page
        function_module.wait_for_element_XPATH(driver, "//*[@id='bootstrap-wizard-1']/div[2]/div[3]/div/div/ul/li[2]/a", 20)
        self.driver.implicitly_wait(0)
        function_module.verify_element_not_present_XPATH(driver, "//*[@id='formActs']/div/section[1]/div/label[1]/i", "VFL", "test011_view_existing_vfl_record",
        "Verified that Safe Acts cannot be selected in View Mode", "Could not verify that Safe Acts cannot be selected in View Mode")
        #Verify that UnSafe Acts radio button is not present on page
        function_module.verify_element_not_present_XPATH(driver, "//*[@id='formActs']/div/section[1]/div/label[2]/i", "VFL", "test011_view_existing_vfl_record",
        "Verified that Unsafe Acts cannot be selected in View Mode", "Could not verify that Unsafe Acts cannot be selected in View Mode")
        #Verify that Add Acts button is not present on page
        function_module.verify_element_not_present_XPATH(driver, "//*[@id='btnSubmitFormActs']", "VFL", "test011_view_existing_vfl_record",
        "Verified that Acts cannot be added in View Mode", "Could not verify that Acts cannot be added in View Mode")
        #Verify that Add Comments button is not present on page
        function_module.verify_element_not_present_CSS(driver, "i.fa.fa-comment-o.glyphicon-size", "VFL", "test011_view_existing_vfl_record",
        "Verified that Comments cannot be added in View Mode", "Could not verify that Comments cannot be added in View Mode")
        #Verify that Add Actions button is not present on page
        function_module.verify_element_not_present_CSS(driver, "i.fa.fa-text-o.glyphicon-size", "VFL", "test011_view_existing_vfl_record",
        "Verified that Actions cannot be added in View Mode", "Could not verify that Actions cannot be added in View Mode")
        #Verify that Edit Act button is not present on page
        function_module.verify_element_not_present_CSS(driver, "i.glyphicon.glyphicon-pencil", "VFL", "test011_view_existing_vfl_record",
        "Verified that Acts cannot be edited in View Mode", "Could not verify that Acts cannot be edited in View Mode")
        #Verify that Delete Act button is not present on page
        function_module.verify_element_not_present_CSS(driver, "i.glyphicon.glyphicon-trash", "VFL", "test011_view_existing_vfl_record",
        "Verified that Acts cannot be deleted in View Mode", "Could not verify that Acts cannot be deleted in View Mode")
        self.driver.implicitly_wait(30)
        #Select the finish button to return to the Main List View
        vfl_page_objects.vfl_finish_button(driver)
        print "Successfully saved VFL Record and returned to list view"
        #Log out of the application
        common_page_objects.logout(driver)
        function_module.log_to_file('Test_VFL_Module:test011_view_existing_vfl_record:TEST COMPLETED', 'PASSED')
        print "Test_VFL_Module:test011_view_existing_vfl_record:TEST COMPLETED"

    def test_012_delete_existing_vfl_record(self):
        """Simple test to ensure that individual VFL record under test can be deleted successfully"""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        common_page_objects.login(driver, client_variables.username1, client_variables.pword1)
        function_module.log_to_file('Test_VFL_Module:test012_delete_existing_vfl_record:Successfully logged in and started test')
        print "Logged in successfully"
        #Select the VFL Module
        vfl_page_objects.open_vfl_module(driver)
        print "Moved to VFL Module"
        #Delete the latest VFL Record
        vfl_page_objects.delete_latest_vfl_record(driver)
        time.sleep(3)
        print "Successfully found the Delete VFL Record button"
        #Assert that the VFL Record has been deleted correctly
        function_module.verify_value(driver, "//*[@id='dtVFL_info']", '0 to 0 of 0 entries', 'VFL', "test012_delete_existing_vfl_record",
        "Successfully deleted VFL Record", "Failed to delete VFL Record")
        #Log out of the application
        common_page_objects.logout(driver)
        function_module.log_to_file('Test_VFL_Module:test012_delete_existing_vfl_record:TEST COMPLETED', 'PASSED')
        print "Test_VFL_Module:test012_delete_existing_vfl_record:TEST COMPLETED"
    
    def tearDown(self):
        """basic test tear down method"""
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


class Test_002_VFL_Main(unittest.TestCase):
    """Set of tests responsible for testing the functionality of
    the main VFL view/landing page"""
    def setUp(self):
        """Standard test setup method"""
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = client_variables.base_url
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_013_verify_default_filters(self):
        """Test to ensure that on initial page load the default filters of Creator = Current User
        and Participant = Current User are selected and applied as expected"""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        common_page_objects.login(driver, client_variables.username1, client_variables.pword1)
        function_module.log_to_file('Test_VFL_Module:test013_verify_default_filters:Successfully logged in and started test')
        print "Logged in successfully"
        #Select the VFL Module
        """Replace with VFL Page Object 'open_vfl_module' once V8 is active"""
        function_module.wait_for_element_CSS(driver, "i.fa.fa-lg.fa-fw.fa-comments")
        driver.find_element_by_css_selector("i.fa.fa-lg.fa-fw.fa-comments").click()
        print "Moved to VFL Module"
        #Verify Filter Panel is hidden, then expand
        vfl_page_objects.expand_filters(driver)
        #Assert creator field is automatically populated with current user
        function_module.verify_value(driver, "//*[@id='s2id_CreatedBy']/ul/li[1]/div", client_variables.fullname1, 'VFL', "test013_verify_default_filters",
        "Creator field was automatically populated with current user", "Creator field is not automatically populated with current user")
        time.sleep(1)
        #Assert Participants field is automatically populated with current user
        function_module.verify_value(driver, "//*[@id='s2id_Participants']/ul/li[1]/div", client_variables.fullname1, 'VFL', "test013_verify_default_filters",
        "Participants field was automatically populated with current user", "Participants field is not automatically populated with current user")
        time.sleep(1)
        #Log out of the application
        common_page_objects.logout(driver)
        function_module.log_to_file('Test_VFL_Module:test013_verify_default_filters:TEST COMPLETED', 'PASSED')
        print "Test_VFL_Module:test013_verify_default_filters:TEST COMPLETED"

    def test_014_delete_multiple_VFL_records(self):
        """Test creates three new VFL records. After records are successfully created we verify that
        the delete multiple VFL records button is disabled by default. We then select all three
        records and delete them simultaneously. A safety check is included to delete all other
        records, if any."""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        common_page_objects.login(driver, client_variables.username1, client_variables.pword1)
        function_module.log_to_file('Test_VFL_Module:test014_delete_multiple_VFL_records:Successfully logged in and started test')
        print "Logged in successfully"
        #Select the VFL Module
        """Replace with VFL Page Object 'open_vfl_module' once V8 is active"""
        function_module.wait_for_element_CSS(driver, "i.fa.fa-lg.fa-fw.fa-comments")
        driver.find_element_by_css_selector("i.fa.fa-lg.fa-fw.fa-comments").click()
        print "Moved to VFL Module"
        #Add multiple VFL records for test
        vfl_page_objects.add_basic_vfl_records(driver, 3, "Test 14", client_variables.wg_default_false, client_variables.bu2, client_variables.location2, '')
        print "Total number of Test VFL Records now = 3"
        #Delete All existing VFL Records
        vfl_page_objects.delete_multiple_vfl_records(driver)
        function_module.log_to_file('Test_VFL_Module:test014_delete_multiple_VFL_records:All existing VFL Records have been deleted', 'PASSED')
        #If any records still exist, delete these also
        vfl_page_objects.delete_remaining_vfl_records(driver)
        print "Total number of Test VFL Records now = 0"
        #Log out of the application
        common_page_objects.logout(driver)
        function_module.log_to_file('Test_VFL_Module:test014_delete_multiple_VFL_records:TEST COMPLETED', 'PASSED')
        print "Test_VFL_Module:test014_delete_multiple_VFL_records:TEST COMPLETED"

    def test_015_filter_by_date_range(self):
        """Test adds three new VFL records. After adding the records successfully, the default
        filters are cleared and a date range added instead. On applying the filters we verify that
        our three VFL records are returned as they exist within the specified date range. Calendar
        interactions are control by functions taken from the function_module.py file. The WorkGroup used in
        this test will be the parent of the WorkGroup used in test_016"""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        common_page_objects.login(driver, client_variables.username1, client_variables.pword1)
        function_module.log_to_file('Test_VFL_Module:test015_filter_by_date_range:Successfully logged in and started test')
        print "Logged in successfully"
        #Select the VFL Module
        """Replace with VFL Page Object 'open_vfl_module' once V8 is active"""
        function_module.wait_for_element_CSS(driver, "i.fa.fa-lg.fa-fw.fa-comments")
        driver.find_element_by_css_selector("i.fa.fa-lg.fa-fw.fa-comments").click()
        print "Moved to VFL Module"
        #Add multiple VFL records for test
        vfl_page_objects.add_basic_vfl_records(driver, 3, "Test 15", client_variables.wg_parent, client_variables.bu1, client_variables.location2, '')
        print "Total number of Test VFL Records now = 3"
        #Expand Filter Panel
        vfl_page_objects.expand_filters(driver)
        print "Expanded filter panel successfully"
        #Set From Date
        vfl_page_objects.set_vfl_from_date(driver, function_module.first_day_of_month())
        print "Set From Date equals the first day of the current month"
        #Set To Date
        vfl_page_objects.set_vfl_to_date(driver, function_module.today())
        print "Set To Date equals todays date"
        #Apply Filters
        vfl_page_objects.apply_filters(driver)
        time.sleep(5)
        print "Have selected the Apply Filters button"
        #Verify expected amount of rows returned
        function_module.verify_value(driver, "//*[@id='dtVFL_info']", 'Showing 1 to 3 of 3 entries', 'VFL', "test015_filter_by_date_range",
        "Asserted that filtering by Date Range works as expected", "Failed to successfully filter by Date Range")
        time.sleep(1)
        #Log out of the application
        common_page_objects.logout(driver)
        function_module.log_to_file('Test_VFL_Module:test015_filter_by_date_range:TEST COMPLETED', 'PASSED')
        print "Test_VFL_Module:test015_filter_by_date_range:TEST COMPLETED"

    def test_016_filter_by_workgroup_no_subgroups(self):
        """Another three VFL records are added. They are added to a workgroup that is a child of the
        workgroup used in test_015. We also specifically select a Location for these three WorkGroups
        for use in test_018. We now have 6 VFL records to work. After successfully creating the new
        VFL records we clear the default filters and select the parent workgroup used in test_015.
        My unticking the SubWorkGroups checkbox and applying the filters we get three VFL recrods
        returned in the list view"""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        common_page_objects.login(driver, client_variables.username1, client_variables.pword1)
        function_module.log_to_file('Test_VFL_Module:test016_filter_by_workgroup_no_subgroups:Successfully logged in and started test')
        print "Logged in successfully"
        #Select the VFL Module
        vfl_page_objects.open_vfl_module(driver)
        print "Moved to VFL Module"
        #Add multiple VFL records for test
        vfl_page_objects.add_basic_vfl_records(driver, 3, "Test 16", client_variables.wg_child, client_variables.bu2, client_variables.location1, '')
        print "Total number of Test VFL Records now = 6"
        #Expand Filter Panel
        vfl_page_objects.expand_filters(driver)
        print "Expanded filter panel successfully"
        #Select a WorkGroup
        vfl_page_objects.set_vfl_workgroup(driver, client_variables.wg_child)
        print "Parent WorkGroup selected"
        #Disable SubGroups
        vfl_page_objects.select_vfl_workgroup_subgroups(driver)
        print "Disabled SubGroups checkbox"
        #Apply Filters
        vfl_page_objects.apply_filters(driver)
        time.sleep(5)
        #function_module.wait_for_element_XPATH(driver, "//*[@id='dtFilterHeaderContainerVfl']/div/a[2]")
        print "Have selected the Apply Filters button"
        #Assert expected amount of rows returned
        function_module.verify_value(driver, "//*[@id='dtVFL_info']", 'Showing 1 to 3 of 3 entries', 'VFL', "test016_filter_by_workgroup_no_subgroups",
        "Asserted that filtering by WorkGroup (No SubGroup) works as expected", "Failed to successfully filter by WorkGroup (No SubGroup)")
        time.sleep(1)
        #Log out of the application
        common_page_objects.logout(driver)
        function_module.log_to_file('Test_VFL_Module:test016_filter_by_workgroup_no_subgroups:TEST COMPLETED', 'PASSED')
        print "Test_VFL_Module:test016_filter_by_workgroup_no_subgroups:TEST COMPLETED"

    def test_017_filter_by_workgroup_with_subgroups(self):
        """We remove the default filters and select WorkGroup equals the same parent WorkGroup selected
        in test_016. However this time we leave the SubWorkGroups checkbox selected and hence will get
        6 VFL records returned in the list view when the filters are applied"""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        common_page_objects.login(driver, client_variables.username1, client_variables.pword1)
        function_module.log_to_file('Test_VFL_Module:test017_filter_by_workgroup_with_subgroups:Successfully logged in and started test')
        print "Logged in successfully"
        #Select the VFL Module
        vfl_page_objects.open_vfl_module(driver)
        print "Moved to VFL Module"
        #Expand Filter Panel
        vfl_page_objects.expand_filters(driver)
        print "Expanded filter panel successfully"
        #Select a WorkGroup
        vfl_page_objects.set_vfl_workgroup(driver, client_variables.wg_parent)
        print "Parent WorkGroup selected with SubGroups checkbox left checked"
        #Apply Filters
        vfl_page_objects.apply_filters(driver)
        time.sleep(5)
        print "Have selected the Apply Filters button"
        #Assert expected amount of rows returned
        function_module.verify_value(driver, "//*[@id='dtVFL_info']", 'Showing 1 to 6 of 6 entries', 'VFL', "test017_filter_by_workgroup_with_subgroups",
        "Asserted that filtering by WorkGroup (With SubGroup) works as expected", "Failed to successfully filter by WorkGroup (With SubGroup)")
        time.sleep(1)
        #Log out of the application
        common_page_objects.logout(driver)
        function_module.log_to_file('Test_VFL_Module:test017_filter_by_workgroup_with_subgroups:TEST COMPLETED', 'PASSED')
        print "Test_VFL_Module:test017_filter_by_workgroup_with_subgroups:TEST COMPLETED"

    def test_018_filter_by_location(self):
        """We clear the default filters and then select the same Location used when
        creating VFL records in test_016. After applying the Location filter we will
        have three VFL records returned"""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        common_page_objects.login(driver, client_variables.username1, client_variables.pword1)
        function_module.log_to_file('Test_VFL_Module:test018_filter_by_location:Successfully logged in and started test')
        print "Logged in successfully"
        #Select the VFL Module
        vfl_page_objects.open_vfl_module(driver)
        print "Moved to VFL Module"
        #Expand Filter Panel
        vfl_page_objects.expand_filters(driver)
        print "Expanded filter panel successfully"
        #Select Location
        vfl_page_objects.set_vfl_location(driver, client_variables.location1)
        print "Selected a value for Location filter"
        #Apply Filters
        vfl_page_objects.apply_filters(driver)
        time.sleep(5)
        print "Have selected the Apply Filters button"
        #Assert expected amount of rows returned
        function_module.verify_value(driver, "//*[@id='dtVFL_info']", 'Showing 1 to 3 of 3 entries', 'VFL', "test018_filter_by_location",
        "Asserted that filtering by Location works as expected", "Failed to successfully filter by Location")
        time.sleep(1)
        #Log out of the application
        common_page_objects.logout(driver)
        function_module.log_to_file('Test_VFL_Module:test018_filter_by_location:TEST COMPLETED', 'PASSED')
        print "Test_VFL_Module:test018_filter_by_location:TEST COMPLETED"

    def test_019_filter_by_business_unit(self):
        """We clear the default filters and then select the same business unit used when
        creating VFL records in test_016. After applying the business unit filter we will
        have three VFL records returned"""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        common_page_objects.login(driver, client_variables.username1, client_variables.pword1)
        function_module.log_to_file('Test_VFL_Module:test019_filter_by_business_unit:Successfully logged in and started test')
        print "Logged in successfully"
        #Select the VFL Module
        vfl_page_objects.open_vfl_module(driver)
        print "Moved to VFL Module"
        #Expand Filter Panel
        vfl_page_objects.expand_filters(driver)
        print "Expanded filter panel successfully"
        #Select business unit
        vfl_page_objects.set_vfl_business_unit(driver, client_variables.bu2)
        print "Select a value from the Business Unit filter"
        #Apply Filters
        vfl_page_objects.apply_filters(driver)
        time.sleep(5)
        print "Have selected the Apply Filters button"
        #Assert expected amount of rows returned
        function_module.verify_value(driver, "//*[@id='dtVFL_info']", 'Showing 1 to 3 of 3 entries', 'VFL', "test019_filter_by_business_unit",
        "Asserted that filtering by Business Unit works as expected", "Failed to successfully filter by Business Unit")
        time.sleep(1)
        #Log out of the application
        common_page_objects.logout(driver)
        function_module.log_to_file('Test_VFL_Module:test019_filter_by_business_unit:TEST COMPLETED', 'PASSED')
        print "Test_VFL_Module:test019_filter_by_business_unit:TEST COMPLETED"

    def test_020_filter_by_creator_or_participant(self):
        """We login to the application using the user2 credentials and delete any records that currently
        exist that are associated to this user. We then add a single VFL record with this user, assigning
        user1 as a participant. Then we clear the default filters and test various combinations of the
        Creator & Participant fields. When all tests are finished we delete the record created using
        user2"""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        common_page_objects.login(driver, client_variables.username2, client_variables.pword2)
        function_module.log_to_file('Test_VFL_Module:test020_filter_by_creator_or_participant:Successfully logged in (as User2) and started test')
        print "Logged in successfully"
        #Select the VFL Module
        """Replace with VFL Page Object 'open_vfl_module' once V8 is active"""
        function_module.wait_for_element_CSS(driver, "i.fa.fa-lg.fa-fw.fa-comments")
        driver.find_element_by_css_selector("i.fa.fa-lg.fa-fw.fa-comments").click()
        print "Moved to VFL Module"
        #Delete all, if any, existing user2 records
        vfl_page_objects.delete_remaining_vfl_records(driver)
        print "Amount of VFL Records created by user2 = 0"
        #Add a single VFL record with Admin as a participant
        vfl_page_objects.add_basic_vfl_records(driver, 1, "Test 17", client_variables.wg_default_false, client_variables.bu2, client_variables.location1, client_variables.fullname1)       
        print "Amount of VFL Records created by user2 = 1"
        print "Total number of Test VFL Records now = 7"
        #FILTER BY CREATOR = USER1 ONLY
        #Expand Filter Panel
        vfl_page_objects.expand_filters(driver)
        print "Expanded filter panel successfully (1)"
        #Remove Default Filters
        vfl_page_objects.clear_selected_creator(driver)
        vfl_page_objects.clear_selected_first_participant(driver)
        print "All default filters have been cleared (1)"
        #Filter by just Creator = user1
        vfl_page_objects.set_vfl_creator(driver, client_variables.fullname1)
        print "User1 selected for just Creator filter"
        #Apply Filters
        vfl_page_objects.apply_filters(driver)
        time.sleep(5)
        print "Have selected the Apply Filters button (1)"
        #Assert expected amount of rows returned
        function_module.verify_value(driver, "//*[@id='dtVFL_info']", 'Showing 1 to 6 of 6 entries', 'VFL', "test020_filter_by_creator_or_participant",
        "Asserted that filtering by just Creator works as expected", "Failed to successfully filter by just Creator")
        time.sleep(1)
        #FILTER BY PARTICIPANT = USER1 ONLY
        #Clear filters
        vfl_page_objects.clear_filters_main(driver)
        print "Existing filters have been cleared (1)"
        #Expand Filter Panel
        vfl_page_objects.expand_filters(driver)
        print "Expanded filter panel successfully (2)"
        #Remove Default Filters
        vfl_page_objects.clear_selected_creator(driver)
        vfl_page_objects.clear_selected_first_participant(driver)
        print "All default filters have been cleared (2)"
        #Filter by just Participant = user1
        vfl_page_objects.set_vfl_participant(driver, client_variables.fullname1)
        print "User1 selected for Participant filter"
        #Apply Filters
        vfl_page_objects.apply_filters(driver)
        time.sleep(5)
        print "Have selected the Apply Filters button (2)"
        #Assert expected amount of rows returned
        function_module.verify_value(driver, "//*[@id='dtVFL_info']", 'Showing 1 to 7 of 7 entries', 'VFL', "test020_filter_by_creator_or_participant",
        "Asserted that filtering by just Participant works as expected (1)", "Failed to successfully filter by just Participant (1)")
        time.sleep(1)
        #FILTER BY PARTICIPANT = USER2 ONLY
        #Clear filters
        vfl_page_objects.clear_filters_main(driver)
        print "Existing filters have been cleared (2)"
        #Expand Filter Panel
        vfl_page_objects.expand_filters(driver)
        print "Expanded filter panel successfully (3)"
        #Remove Default Filters
        vfl_page_objects.clear_selected_creator(driver)
        vfl_page_objects.clear_selected_first_participant(driver)
        print "All default filters have been cleared (3)"
        #Filter by just Participant = user2
        vfl_page_objects.set_vfl_participant(driver, client_variables.fullname2)
        print "User2 selected for Participant filter"
        #Apply Filters
        vfl_page_objects.apply_filters(driver)
        time.sleep(5)
        print "Have selected the Apply Filters button (3)"
        #Assert expected amount of rows returned
        function_module.verify_value(driver, "//*[@id='dtVFL_info']", 'Showing 1 to 1 of 1 entries', 'VFL', "test020_filter_by_creator_or_participant",
        "Asserted that filtering by just Participant works as expected (2)", "Failed to successfully filter by just Participant (2)")
        time.sleep(1)
        #FILTER BY CREATOR = USER2 & PARTICIPANT = USER1
        #Expand Filter Panel & Clear filters using alternative button
        vfl_page_objects.clear_filters_alt(driver)
        print "Existing filters have been cleared (3)(ALTERNATIVE METHOD)"
        #Expand Filter Panel again
        vfl_page_objects.expand_filters(driver)
        print "Expanded filter panel successfully again (4)"
        #Remove Default Filters
        vfl_page_objects.clear_selected_creator(driver)
        vfl_page_objects.clear_selected_first_participant(driver)
        print "All default filters have been cleared (4)"
        #Filter by Creator = user2 and participant = user1
        vfl_page_objects.set_vfl_creator(driver, client_variables.fullname2)
        vfl_page_objects.set_vfl_participant(driver, client_variables.fullname1)
        print "User2 selected for Creator filter AND User1 selected for Participant filter"
        #Apply Filters
        vfl_page_objects.apply_filters(driver)
        time.sleep(5)
        print "Have selected the Apply Filters button (4)"
        #Assert expected amount of rows returned
        function_module.verify_value(driver, "//*[@id='dtVFL_info']", 'Showing 1 to 7 of 7 entries', 'VFL', "test020_filter_by_creator_or_participant",
        "Asserted that filtering by Creator AND Participant works as expected", "Failed to successfully filter by Creator AND Participant")
        time.sleep(1)
        #DELETE RECORD ADDED BY USER2
        #Clear filters
        vfl_page_objects.clear_filters_main(driver)
        print "Existing filters have been cleared (4)"
        #Delete record
        vfl_page_objects.delete_remaining_vfl_records(driver)
        time.sleep(3)
        print "Amount of VFL Records created by user2 = 0"
        print "Total number of Test VFL Records now = 6"
        #Log out of the application
        common_page_objects.logout(driver)
        function_module.log_to_file('Test_VFL_Module:test020_filter_by_creator_or_participant:TEST COMPLETED', 'PASSED')
        print "Test_VFL_Module:test020_filter_by_creator_or_participant:TEST COMPLETED"

    def test_021_pagination(self):
        """This test takes a long time as we first have to loop through the creation of 49 VFL Records.
        After all records have been added we should have a total of 55 VFL records. Using the pagination
        controls and assertions based on the string at the bottom left of the view, we verify that we
        are moving to the expected pages"""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        common_page_objects.login(driver, client_variables.username1, client_variables.pword1)
        function_module.log_to_file('Test_VFL_Module:test021_pagination:Successfully logged in and started test')
        print "Logged in successfully"
        #Select the VFL Module
        vfl_page_objects.open_vfl_module(driver)
        print "Moved to VFL Module"
        #Add multiple VFL records for test
        vfl_page_objects.add_basic_vfl_records(driver, 50, "Test 21", client_variables.wg_default_false, client_variables.bu2, client_variables.location1, '')
        print "Total number of Test VFL Records now = 56"
        print "Is it really though???"
        vfl_page_objects.check_amount_of_vfl_records(driver, 'Showing 1 to 10 of 56 entries')
        time.sleep(1)
        #Move to next page
        vfl_page_objects.pagination_next(driver, 'Showing 11 to 20 of 56 entries')
        function_module.verify_value(driver, "//*[@id='dtVFL_info']", 'Showing 11 to 20 of 56 entries', 'VFL', "test021_pagination",
        "Asserted that we can successfully navigate to the next page", "Test failed to move to NEXT page - Showing 11 to 20 of 56 entries")
        time.sleep(1)
        #Move to previous page
        vfl_page_objects.pagination_prev(driver, 'Showing 1 to 10 of 56 entries')
        function_module.verify_value(driver, "//*[@id='dtVFL_info']", 'Showing 1 to 10 of 56 entries', 'VFL', "test021_pagination",
        "Asserted that we can successfully navigate to the previous page", "Test failed to move to PREVIOUS page - Showing 1 to 10 of 56 entries")
        time.sleep(1)
        #Move to last page
        vfl_page_objects.pagination_last(driver, 'Showing 51 to 56 of 56 entries')
        function_module.verify_value(driver, "//*[@id='dtVFL_info']", 'Showing 51 to 56 of 56 entries', 'VFL', "test021_pagination",
        "Asserted that we can successfully navigate to the last page", "Test failed to move to LAST page - Showing 51 to 56 of 56 entries")
        time.sleep(1)
        #Move to first page
        vfl_page_objects.pagination_first(driver, 'Showing 1 to 10 of 56 entries')
        function_module.verify_value(driver, "//*[@id='dtVFL_info']", 'Showing 1 to 10 of 56 entries', 'VFL', "test021_pagination",
        "Asserted that we can successfully navigate to the first page", "Test failed to move to FIRST page - Showing 1 to 10 of 56 entries")
        time.sleep(1)
        #Change to display 5 records
        vfl_page_objects.pagination_number_of_records(driver, '5', 'Showing 1 to 5 of 56 entries')
        function_module.verify_value(driver, "//*[@id='dtVFL_info']", 'Showing 1 to 5 of 56 entries', 'VFL', "test021_pagination",
        "Asserted that we can successfully display 5 records", "Test failed to move to display FIVE records - Showing 1 to 5 of 56 entries")
        time.sleep(1)
        #Change to display 10 records
        vfl_page_objects.pagination_number_of_records(driver, '10', 'Showing 1 to 10 of 56 entries')
        function_module.verify_value(driver, "//*[@id='dtVFL_info']", 'Showing 1 to 10 of 56 entries', 'VFL', "test021_pagination",
        "Asserted that we can successfully display 10 records", "Test failed to move to display TEN records - Showing 1 to 10 of 56 entries")
        time.sleep(1)
        #Change to display 25 records
        vfl_page_objects.pagination_number_of_records(driver, '25', 'Showing 1 to 25 of 56 entries')
        function_module.verify_value(driver, "//*[@id='dtVFL_info']", 'Showing 1 to 25 of 56 entries', 'VFL', "test021_pagination",
        "Asserted that we can successfully display 25 records", "Test failed to move to display TWENTY FIVE records - Showing 1 to 25 of 56 entries")
        time.sleep(1)
        #Change to display 50 records
        vfl_page_objects.pagination_number_of_records(driver, '50', 'Showing 1 to 50 of 56 entries')
        function_module.verify_value(driver, "//*[@id='dtVFL_info']", 'Showing 1 to 50 of 56 entries', 'VFL', "test021_pagination",
        "Asserted that we can successfully display 50 records", "Test failed to move to display FIFTY records - Showing 1 to 50 of 56 entries")  
        time.sleep(1)
        #Change to display 100 records
        vfl_page_objects.pagination_number_of_records(driver, '100', 'Showing 1 to 56 of 56 entries')
        function_module.verify_value(driver, "//*[@id='dtVFL_info']", 'Showing 1 to 56 of 56 entries', 'VFL', "test021_pagination",
        "Asserted that we can successfully display 100 records", "Test failed to move to display ONE HUNDRED records - Showing 1 to 56 of 56 entries")
        time.sleep(1)
        #Log out of the application
        common_page_objects.logout(driver)
        function_module.log_to_file('Test_VFL_Module:test021_delete_existing_vfl_record:TEST COMPLETED', 'PASSED')
        print "Test_VFL_Module:test021_delete_existing_vfl_record:TEST COMPLETED"

    def test_022_tool_tips(self):
        """Test includes a set of basic assertions to ensure that various elements on the main
        page have the expected tool-tip text that will be displayed on Mouse Over"""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        common_page_objects.login(driver, client_variables.username1, client_variables.pword1)
        function_module.log_to_file('Test_VFL_Module:test022_tool_tips:Successfully logged in and started test')
        print "Logged in successfully"
        #Select the VFL Module
        vfl_page_objects.open_vfl_module(driver)
        print "Moved to VFL Module"
        #Assert Information text is correct
        elem = driver.find_element_by_xpath("//*[@id='dtVFL']/tbody/tr[1]/td[8]/div[1]/label/i")
        information_text = elem.get_attribute("data-content")
        assert information_text == '<div>Total Minutes <br /><b>60</b></div><div>Site <br /><b>France</b></div><div>No. Conversations <br /><b>0</b></div><div>Safe Act(s) <br /><b>None</b></div><div>Unsafe Act(s) <br /><b>None</b></div>'
        print "Information Tool Tip for first VFL Record displays correct data"
        #Assert View ToolTip
        elem = driver.find_element_by_xpath("//*[@id='dtVFL']/tbody/tr[1]/td[8]/div[2]/div/a[1]")
        view_tool_tip = elem.get_attribute("data-original-title")
        assert view_tool_tip == 'View VFL'
        print "Tool Tip for View button is correct"
        #Assert Edit ToolTip
        elem = driver.find_element_by_xpath("//*[@id='dtVFL']/tbody/tr[1]/td[8]/div[2]/div/a[2]")
        view_tool_tip = elem.get_attribute("data-original-title")
        assert view_tool_tip == 'Edit VFL'
        print "Tool Tip for Edit  button is correct"
        #Assert Delete ToolTip
        elem = driver.find_element_by_xpath("//*[@id='dtVFL']/tbody/tr[1]/td[8]/div[2]/div/a[3]")
        view_tool_tip = elem.get_attribute("data-original-title")
        assert view_tool_tip == 'Delete VFL'
        print "Tool Tip for Delete button is correct"
        #Assert Add ToolTip
        elem = driver.find_element_by_xpath("//*[@id='widDtVFLs']/div/div[2]/div[1]/div/div[2]/div/div/a[1]")
        add_tool_tip = elem.get_attribute("data-original-title")
        assert add_tool_tip == 'Add New VFL'
        print "Tool Tip for Add button is correct"
        #Assert Delete All ToolTip
        elem = driver.find_element_by_xpath("//*[@id='widDtVFLs']/div/div[2]/div[1]/div/div[2]/div/div/a[2]")
        delete_all_tool_tip = elem.get_attribute("data-original-title")
        assert delete_all_tool_tip == 'Delete Selected VFL'
        print "Tool Tip for Delete Selected button is correct"
        #Assert Print ToolTip
        elem = driver.find_element_by_xpath("//*[@id='widDtVFLs']/div/div[2]/div[1]/div/div[2]/div/div/a[3]")
        print_tool_tip = elem.get_attribute("data-original-title")
        assert print_tool_tip == 'VFL Print Reports'
        print "Tool Tip for Print Reports button is correct"
        #Assert Export ToolTip
        elem = driver.find_element_by_xpath("//*[@id='widDtVFLs']/div/div[2]/div[1]/div/div[2]/div/div/a[4]")
        export_tool_tip = elem.get_attribute("data-original-title")
        assert export_tool_tip == 'Export Selected VFL'
        print "Tool Tip for Export button is correct"
        function_module.log_to_file('Test_VFL_Module:test022_tool_tips:All Tool Tips are correct', 'PASSED')
        #Log out of the application
        common_page_objects.logout(driver)
        function_module.log_to_file('Test_VFL_Module:test022_tool_tips:TEST COMPLETED', 'PASSED')
        print "Test_VFL_Module:test022_tool_tips:TEST COMPLETED"

    def test_023_creator_participant_rights(self):
        """All previous tests have proven that a Creator can view, edit and delete their own records.
        By adding User2 as a participant to the first record in the view and then logging in as User2,
        we can proceed to verify that as participants User2 can edit and view a record, but not delete it.
        We tend filter the view to only display issues where User1 is the exclusive participant. User2
        will therefore be limited to only viewing these records."""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        common_page_objects.login(driver, client_variables.username1, client_variables.pword1)
        function_module.log_to_file('Test_VFL_Module:test023_creator_participant_rights:Successfully logged in (as User1) and started test')
        print "Logged in as User1 successfully"
        #Select the VFL Module
        vfl_page_objects.open_vfl_module(driver)
        print "Moved to VFL Module"
        #Edit first Record and add User2 as Participant
        vfl_page_objects.edit_latest_vfl_record(driver)
        vfl_page_objects.vfl_participants(driver, client_variables.fullname2)
        time.sleep(1)
        print "User 2 added as Participant to first VFL Record"
        #Move successfully to the next tab, close and log out
        vfl_page_objects.vfl_next_button(driver)
        print "Moved to Acts Tab"
        vfl_page_objects.vfl_finish_button(driver)
        print "Successfully saved VFL Record and returned to list view"
        common_page_objects.logout(driver)
        time.sleep(1)
        print "Logged out of application as User 1"
        #Login as User2
        common_page_objects.login(driver, client_variables.username2, client_variables.pword2)
        function_module.log_to_file('Test_VFL_Module:test023_creator_participant_rights:Successfully logged in (as User2) and started test')
        print "Logged in as User2 successfully"
        #Select the VFL Module
        vfl_page_objects.open_vfl_module(driver)
        print "Moved to VFL Module"
        #Verify Delete button is disabled for Participant
        function_module.field_is_read_only_xpath(driver, "//*[@id='dtVFL']/tbody/tr/td[8]/div[2]/div/a[3]")
        print "User2 does not have permission to delete VFL Records where they are not the creator"
        #FILTER BY CREATOR & PARTICIPANT = USER1 ONLY
        #Expand Filter Panel
        vfl_page_objects.expand_filters(driver)
        print "Expanded filter panel successfully"
        #Remove Default Filters
        vfl_page_objects.clear_selected_creator(driver)
        vfl_page_objects.clear_selected_first_participant(driver)
        print "All default filters have been cleared"
        #Select Creator = user1
        vfl_page_objects.set_vfl_creator(driver, client_variables.fullname1)
        print "Selected User1 as Creator"
        #Select Participant = user1
        vfl_page_objects.set_vfl_participant(driver, client_variables.fullname1)
        print "Selected User1 as Participant"
        #Apply Filters
        vfl_page_objects.apply_filters(driver)
        time.sleep(5)
        print "Have selected the Apply Filters button"
        #Verify Delete button is disabled for any user
        function_module.field_is_read_only_xpath(driver, "//*[@id='dtVFL']/tbody/tr/td[8]/div[2]/div/a[3]")
        print "User2 does not have permission to delete VFL Records where they are neither the creator or the participant"
        time.sleep(1)
        #Verify Edit button is disabled for any user
        function_module.field_is_read_only_xpath(driver, "//*[@id='dtVFL']/tbody/tr/td[8]/div[2]/div/a[2]")
        print "User2 does not have permission to edit VFL Records where they are neither the creator or the participant"
        function_module.log_to_file('Test_VFL_Module:test023_creator_participant_rights:Successfully verified limited permissions for non creators AND/OR participants', 'PASSED')
        #Log out of the application
        common_page_objects.logout(driver)
        function_module.log_to_file('Test_VFL_Module:test023_creator_participant_rights:TEST COMPLETED', 'PASSED')
        print "Test_VFL_Module:test023_creator_participant_rights:TEST COMPLETED"

    def test_024_vfl_show_hide_columns(self):
        """Testing the VFL List View can have its columns both hidden and displayed"""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        common_page_objects.login(driver, client_variables.username1, client_variables.pword1)
        function_module.log_to_file('Test_VFL_Module:test024_vfl_show_hide_columns:Successfully logged in and started test')
        print "Logged in successfully"
        #Select the VFL Module
        vfl_page_objects.open_vfl_module(driver)
        vfl_page_objects.wait_for_vfl_records(driver)
        print "Moved to VFL Module" 
        #define objects to locate column headers
        function_module.wait_for_element_CSS(driver, ".dt-datetime.sorting_desc")
        created_on_header = driver.find_element_by_css_selector(".dt-datetime.sorting_desc")
        header_list = driver.find_elements_by_css_selector(".sorting_disabled")                          
        conversations_header = header_list[1]
        site_header = header_list[2]
        participants_header = header_list[3]
        creator_header = header_list[4]
        comments_header = header_list[5]
        #Select the Show Hide Columns dropdown and HIDE the Created On column
        vfl_page_objects.click_show_hide_checkbox_css(driver)
        #Assert the Created On column has been successfully hidden
        self.driver.implicitly_wait(0)
        vfl_page_objects.column_hidden(driver, created_on_header, "Created On")
        self.driver.implicitly_wait(30)
        #Select the Show Hide Columns dropdown and UNHIDE the Created On column
        vfl_page_objects.click_show_hide_checkbox_css(driver)
        #Select the Show Hide Columns dropdown and HIDE the Conversations column
        vfl_page_objects.click_show_hide_checkbox_xpath(driver, "(//input[@type='checkbox'])[14]")
        #Assert the conversations column has been successfully hidden
        self.driver.implicitly_wait(0)
        vfl_page_objects.column_hidden(driver, conversations_header, "Conversations")
        self.driver.implicitly_wait(30)
        #Select the Show Hide Columns dropdown and UNHIDE the Conversations column
        vfl_page_objects.click_show_hide_checkbox_xpath(driver, "(//input[@type='checkbox'])[14]")
        #Select the Show Hide Columns dropdown and HIDE the site column
        vfl_page_objects.click_show_hide_checkbox_xpath(driver, "(//input[@type='checkbox'])[15]")
        #Assert the site column has been successfully hidden
        self.driver.implicitly_wait(0)
        vfl_page_objects.column_hidden(driver, site_header, "Site")
        self.driver.implicitly_wait(30)
        #Select the Show Hide Columns dropdown and UNHIDE the Site column
        vfl_page_objects.click_show_hide_checkbox_xpath(driver, "(//input[@type='checkbox'])[15]")
        #Select the Show Hide Columns dropdown and HIDE the Participants column
        vfl_page_objects.click_show_hide_checkbox_xpath(driver, "(//input[@type='checkbox'])[16]")
        #Assert the Participants column has been successfully hidden
        self.driver.implicitly_wait(0)
        vfl_page_objects.column_hidden(driver, participants_header, "Participants")
        self.driver.implicitly_wait(30)
        #Select the Show Hide Columns dropdown and UNHIDE the Participants column
        vfl_page_objects.click_show_hide_checkbox_xpath(driver, "(//input[@type='checkbox'])[16]")
        #Select the Show Hide Columns dropdown and HIDE the Creator column
        vfl_page_objects.click_show_hide_checkbox_xpath(driver, "(//input[@type='checkbox'])[17]")
        #Assert the Creator column has been successfully hidden
        self.driver.implicitly_wait(0)
        vfl_page_objects.column_hidden(driver, creator_header, "Creator")
        self.driver.implicitly_wait(30)
        #Select the Show Hide Columns dropdown and UNHIDE the Creator column
        vfl_page_objects.click_show_hide_checkbox_xpath(driver, "(//input[@type='checkbox'])[17]")
        #Select the Show Hide Columns dropdown and HIDE the Comments column
        vfl_page_objects.click_show_hide_checkbox_xpath(driver, "(//input[@type='checkbox'])[18]")
        #Assert the Comments column has been successfully hidden
        self.driver.implicitly_wait(0)
        vfl_page_objects.column_hidden(driver, comments_header, "Comments")
        self.driver.implicitly_wait(30)
        #Select the Show Hide Columns dropdown and UNHIDE the Comments column
        vfl_page_objects.click_show_hide_checkbox_xpath(driver, "(//input[@type='checkbox'])[18]")
        #Capture a screenshot to ensure list view has not been corrupted due to hiding & displaying columns
        driver.get_screenshot_as_file('V:/QA/Automation/Automation_Resources/Output/show_hide_columns.png')
        function_module.log_to_file('Test_VFL_Module:test024_vfl_show_hide_columns:Successfully took a screenshot of list view')
        time.sleep(3)
        print "took screenshot and saved to output folder"
        #Move screenshot into client specific folder
        function_module.move_file(client_variables.output_folder, client_variables.client_folder)
        function_module.log_to_file('Test_VFL_Module:test024_vfl_show_hide_columns:Successfully moved screenshot of list view into client specific folder')
        time.sleep(2)
        #Log out of the application
        common_page_objects.logout(driver)
        function_module.log_to_file('Test_VFL_Module:test024_vfl_show_hide_columns:TEST COMPLETED', 'PASSED')
        print "Test_VFL_Module:test024_vfl_show_hide_columns:TEST COMPLETED"
        
    def tearDown(self):
        """Standard test tear down method"""
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)



class Test_003_VFL_Settings(unittest.TestCase):
    """Set of tests responsible for testing the functionality of
    VFL Settings dialog box"""
    def setUp(self):
        """Standard test setup method"""
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = client_variables.base_url
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_025_add_year(self):
        """Test opens the VFL Setting dialog and a row with Year = Current Year and
        # of Visits = 3. Various assertions are used to ensure the increase and decrease
        buttons function correctly for both fields"""
        driver = self.driver
        driver.get(self.base_url + "/")
        current_year = datetime.datetime.now().year
        #Login to the application
        common_page_objects.login(driver, client_variables.username1, client_variables.pword1)
        function_module.log_to_file('Test_VFL_Module:test025_add_year:Successfully logged in and started test')
        print "Logged in successfully"
        #Select the VFL Module
        vfl_page_objects.open_vfl_module(driver)
        vfl_page_objects.wait_for_vfl_records(driver)
        print "Moved to VFL Module"
        #Open the VFL Settings Window
        vfl_page_objects.open_vfl_settings(driver)
        print "Successfully opened VFL Settings dialog"
        #Assert that Year field is automatically populated with current year
        vfl_page_objects.vfl_year_default_current(driver)
        #Increase Year by 1 and assert change
        vfl_page_objects.vfl_year_increment(driver, 1)
        #Decrease Year by 1 and assert change
        vfl_page_objects.vfl_year_decrement(driver, 1)
        #Assert that No. Visits field is automatically populated value = 0
        vfl_page_objects.vfl_visits_default_current(driver)
        #Ensure that No. Visits can not have negative value entered
        vfl_page_objects.vfl_visits_negative(driver, 3)
        #Increase No. Visits by 5 and assert change
        vfl_page_objects.vfl_visits_increment(driver, 5)
        #Decrease No. Visits by 2 and assert change
        vfl_page_objects.vfl_visits_decrement(driver, 2)
        #Add a row with Current Year and No. Visits = 3
        vfl_page_objects.submit_vfl_settings(driver)
        print "Have submitted the current year with 3 visits"
        #Assert first row has year = current year
        vfl_page_objects.verify_vfl_settings_first_row(driver, current_year, 3)
        #Close the VFL Settings window
        vfl_page_objects.close_vfl_settings(driver)
        print "Closed VFL Settings dialog box"
        #Log out of the application
        common_page_objects.logout(driver)
        function_module.log_to_file('Test_VFL_Module:test025_add_year:TEST COMPLETED', 'PASSED')
        print "Test_VFL_Module:test025_add_year:TEST COMPLETED"

    def test_026_update_year(self):
        """Test verifies the various methods a user can update an existing row.
        A row can be updated by either attempting to add a value for a year that
        already exists OR by selecting the edit button for an existing row"""
        driver = self.driver
        driver.get(self.base_url + "/")
        current_year = datetime.datetime.now().year
        #Login to the application
        common_page_objects.login(driver, client_variables.username1, client_variables.pword1)
        function_module.log_to_file('Test_VFL_Module:test026_update_year:Successfully logged in and started test')
        print "Logged in successfully"
        #Select the VFL Module
        vfl_page_objects.open_vfl_module(driver)
        vfl_page_objects.wait_for_vfl_records(driver)
        print "Moved to VFL Module"
        #Open the VFL Settings Window
        vfl_page_objects.open_vfl_settings(driver)
        print "Successfully opened VFL Settings dialog"
        #Assert that Year field is automatically populated with current year
        vfl_page_objects.vfl_year_default_current(driver)
        #Assert first row No. Visits = 3
        vfl_page_objects.verify_vfl_settings_first_row(driver, current_year, 3)
        #Change Current Years No. Visits = 5 without using Edit button
        vfl_page_objects.vfl_visits_increment(driver, 5)
        vfl_page_objects.submit_vfl_settings(driver)
        vfl_page_objects.refresh_vfl_settings(driver)
        print "Changed current years number of Visits from 3 to 5 without using the Edit button"
        #Assert first row No. Visits = 5
        vfl_page_objects.verify_vfl_settings_first_row(driver, current_year, 5)
        #Edit first row, cancel change and verify row remains unchanged
        vfl_page_objects.edit_vfl_settings(driver)
        vfl_page_objects.cancel_edit_vfl_settings(driver)
        vfl_page_objects.refresh_vfl_settings(driver)
        vfl_page_objects.verify_vfl_settings_first_row(driver, current_year, 5)
        #Change the Current Years No. Visits = 2 by using the Edit button
        vfl_page_objects.edit_first_row(driver, current_year, 2)
        vfl_page_objects.refresh_vfl_settings(driver)
        vfl_page_objects.verify_vfl_settings_first_row(driver, current_year, 3)
        print "Changed current years number of Visits from 5 to 2 by using the Edit button"
        #Close the VFL Settings window
        vfl_page_objects.close_vfl_settings(driver)
        print "Closed VFL Settings dialog box"
        #Log out of the application
        common_page_objects.logout(driver)
        function_module.log_to_file('Test_VFL_Module:test026_update_year:TEST COMPLETED', 'PASSED')
        print "Test_VFL_Module:test026_update_year:TEST COMPLETED"

    def test_027_delete_year(self):
        """Test is used to delete the row to the VFL Settings table
        that was just added and edited."""
        driver = self.driver
        #self.driver.implicitly_wait(5)
        driver.get(self.base_url + "/")
        #Login to the application
        common_page_objects.login(driver, client_variables.username1, client_variables.pword1)
        function_module.log_to_file('Test_VFL_Module:test027_delete_year:Successfully logged in and started test')
        print "Logged in successfully"
        #Select the VFL Module
        vfl_page_objects.open_vfl_module(driver)
        vfl_page_objects.wait_for_vfl_records(driver)
        print "Moved to VFL Module"
        #Open the VFL Settings Window
        vfl_page_objects.open_vfl_settings(driver)
        print "Successfully opened VFL Settings dialog"
        #Delete first row for current year
        vfl_page_objects.delete_vfl_settings(driver)
        print "Deleting the first row"
        time.sleep(5)
        #Verify that first row has been deleted
        self.driver.implicitly_wait(0)
        function_module.verify_element_not_present_XPATH(driver, "//*[@id='dtSettingsContainer']/tr/td[1]", 'VFL', 'test027_delete_year',
        'Verified that the first row has been deleted', 'Test could not successfully verify that the first row from the Settings page was deleted as expected')
        self.driver.implicitly_wait(30)
        #Close the VFL Settings window
        vfl_page_objects.close_vfl_settings(driver)
        print "Closed VFL Settings dialog box"
        #Log out of the application
        common_page_objects.logout(driver)
        function_module.log_to_file('Test_VFL_Module:test027_delete_year:TEST COMPLETED', 'PASSED')
        print 'Test_VFL_Module:test027_delete_year:TEST COMPLETED'

    def tearDown(self):
        """Standard test tear down method"""
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


class Test_004_VFL_Export(unittest.TestCase):
    """Set of tests responsible for testing the export function for the VFL List View."""
    def setUp(self):
        """Setup edited so that its uses a specific firefox profile called 'auto_test_profile'.
        When using this firefox profile the user will not be prompted when downloading specific
        file types, such as .xlsx and .csv. Lines were left in but commented out that control
        the setup and tear down of a temp directory to be used for downloads. This approach might
        be revisited at a later stage."""
        auto_test_profile = webdriver.FirefoxProfile("C:/Users/rhoward.EMEX/AppData/Roaming/Mozilla/Firefox/Profiles/kz6phe2o.auto_test_profile")
        self.driver = webdriver.Firefox(firefox_profile=auto_test_profile)
        self.driver.implicitly_wait(30)
        self.base_url = client_variables.base_url
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_028_export_all_excel(self):
        """Test creates .xlsx file which includes all current 55 VFL records. After the file is
        downloaded, the move_file() function is used to place the file into its client specific
        folder."""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        common_page_objects.login(driver, client_variables.username1, client_variables.pword1)
        function_module.log_to_file('Test_VFL_Module:test028_export_all_excel:Successfully logged in and started test')
        time.sleep(5)
        print "Logged in successfully"
        #Select the VFL Module
        vfl_page_objects.open_vfl_module(driver)
        vfl_page_objects.wait_for_vfl_records(driver)
        print "Moved to VFL Module"
        #export all current records
        vfl_page_objects.vfl_export(driver, "Excel", "1")
        #Copy export to client specific folder
        function_module.move_file(client_variables.output_folder, client_variables.client_folder)
        function_module.log_to_file('Test_VFL_Module:test028_export_all_excel:Successfully moved excel file into client specific folder')
        time.sleep(2)
        print "Moved file into client specific folder"
        #Log out of the application
        common_page_objects.logout(driver)
        function_module.log_to_file('Test_VFL_Module:test028_export_all_excel:TEST COMPLETED', 'PASSED')
        print "Test_VFL_Module:test028_export_all_excel:TEST COMPLETED"

    def test_029_export_current_page_excel(self):
        """Test creates .xlsx file which includes all current page of VFL records (10 in total). After the file is
        downloaded, the move_file() function is used to place the file into its client specific
        folder."""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        common_page_objects.login(driver, client_variables.username1, client_variables.pword1)
        function_module.log_to_file('Test_VFL_Module:test029_export_current_page_excel:Successfully logged in and started test')
        time.sleep(5)
        print "Logged in successfully"
        #Select the VFL Module
        vfl_page_objects.open_vfl_module(driver)
        vfl_page_objects.wait_for_vfl_records(driver)
        print "Moved to VFL Module"
        #export current page of VFL records
        vfl_page_objects.vfl_export(driver, "Excel", "2")
        #Copy export to client specific folder
        function_module.move_file(client_variables.output_folder, client_variables.client_folder)
        function_module.log_to_file('Test_VFL_Module:test029_export_current_page_excel:Successfully moved excel file into client specific folder')
        time.sleep(2)
        print "Moved file into client specific folder"
        #Log out of the application
        common_page_objects.logout(driver)
        function_module.log_to_file('Test_VFL_Module:test029_export_current_page_excel:TEST COMPLETED', 'PASSED')
        print "Test_VFL_Module:test029_export_current_page_excel:TEST COMPLETED"

    def test_030_export_selected_rows_excel(self):
        """Test creates .xlsx file which includes only selected VFL records (5 in total). After the file is
        downloaded, the move_file() function is used to place the file into its client specific
        folder."""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        common_page_objects.login(driver, client_variables.username1, client_variables.pword1)
        function_module.log_to_file('Test_VFL_Module:test030_export_selected_rows_excel:Successfully logged in and started test')
        time.sleep(5)
        print "Logged in successfully"
        #Select the VFL Module
        vfl_page_objects.open_vfl_module(driver)
        vfl_page_objects.wait_for_vfl_records(driver)
        print "Moved to VFL Module"
        #Manually select top five records
        vfl_page_objects.select_multiple_vfl_records(driver, 6)
        #export selected records only
        vfl_page_objects.vfl_export(driver, "Excel", "3")
        #Copy export to client specific folder
        function_module.move_file(client_variables.output_folder, client_variables.client_folder)
        function_module.log_to_file('Test_VFL_Module:test030_export_selected_rows_excel:Successfully moved excel file into client specific folder')
        time.sleep(2)
        print "Moved file into client specific folder"
        #Log out of the application
        common_page_objects.logout(driver)
        function_module.log_to_file('Test_VFL_Module:test030_export_selected_rows_excel:TEST COMPLETED', 'PASSED')
        print "Test_VFL_Module:test030_export_selected_rows_excel:TEST COMPLETED"

    def test_031_export_all_csv(self):
        """Test creates .csv file which includes all current 55 VFL records. After the file is
        downloaded, the move_file() function is used to place the file into its client specific
        folder."""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        common_page_objects.login(driver, client_variables.username1, client_variables.pword1)
        function_module.log_to_file('Test_VFL_Module:test031_export_all_csv:Successfully logged in and started test')
        time.sleep(5)
        print "Logged in successfully"
        #Select the VFL Module
        vfl_page_objects.open_vfl_module(driver)
        vfl_page_objects.wait_for_vfl_records(driver)
        print "Moved to VFL Module"
        #export all current records
        vfl_page_objects.vfl_export(driver, "CSV", "1")
        #Copy export to client specific folder
        function_module.move_file(client_variables.output_folder, client_variables.client_folder)
        function_module.log_to_file('Test_VFL_Module:test031_export_all_csv:Successfully moved csv file into client specific folder')
        time.sleep(2)
        print "Moved file into client specific folder"
        #Log out of the application
        common_page_objects.logout(driver)
        function_module.log_to_file('Test_VFL_Module:test031_export_all_csv:TEST COMPLETED', 'PASSED')
        print "Test_VFL_Module:test031_export_all_csv:TEST COMPLETED" 

    def test_032_export_current_page_csv(self):
        """Test creates .csv file which includes all current page of VFL records (10 in total). After the file is
        downloaded, the move_file() function is used to place the file into its client specific
        folder."""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        common_page_objects.login(driver, client_variables.username1, client_variables.pword1)
        function_module.log_to_file('Test_VFL_Module:test032_export_current_page_csv:Successfully logged in and started test')
        time.sleep(5)
        print "Logged in successfully"
        #Select the VFL Module
        vfl_page_objects.open_vfl_module(driver)
        vfl_page_objects.wait_for_vfl_records(driver)
        print "Moved to VFL Module"
        #export current page of VFL records
        vfl_page_objects.vfl_export(driver, "CSV", "2")
        #Copy export to client specific folder
        function_module.move_file(client_variables.output_folder, client_variables.client_folder)
        function_module.log_to_file('Test_VFL_Module:test032_export_current_page_csv:Successfully moved csv file into client specific folder')
        time.sleep(2)
        print "Moved file into client specific folder"
        #Log out of the application
        common_page_objects.logout(driver)
        function_module.log_to_file('Test_VFL_Module:test032_export_current_page_csv:TEST COMPLETED', 'PASSED')
        print "Test_VFL_Module:test032_export_current_page_csv:TEST COMPLETED"

    def test_033_export_selected_rows_csv(self):
        """Test creates .csv file which includes only selected VFL records (5 in total). After the file is
        downloaded, the move_file() function is used to place the file into its client specific
        folder."""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        common_page_objects.login(driver, client_variables.username1, client_variables.pword1)
        function_module.log_to_file('Test_VFL_Module:test033_export_selected_rows_csv:Successfully logged in and started test')
        time.sleep(5)
        print "Logged in successfully"
        #Select the VFL Module
        vfl_page_objects.open_vfl_module(driver)
        vfl_page_objects.wait_for_vfl_records(driver)
        print "Moved to VFL Module"
        #Manually select top five records
        vfl_page_objects.select_multiple_vfl_records(driver, 6)
        #export selected records only
        vfl_page_objects.vfl_export(driver, "CSV", "3")
        #Copy export to client specific folder
        function_module.move_file(client_variables.output_folder, client_variables.client_folder)
        function_module.log_to_file('Test_VFL_Module:test033_export_selected_rows_csv:Successfully moved excel file into client specific folder')
        time.sleep(2)
        print "Moved file into client specific folder"
        #Log out of the application
        common_page_objects.logout(driver)
        function_module.log_to_file('Test_VFL_Module:test033_export_selected_rows_csv:TEST COMPLETED', 'PASSED')
        print "Test_VFL_Module:test033_export_selected_rows_csv:TEST COMPLETED"
    
    def tearDown(self):
        """Test Tear Down method"""
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)
        

class Test_005_VFL_Reports(unittest.TestCase):
    """Set of tests responsible for testing the various VFL reports available to the user."""
    def setUp(self):
        """Setup edited so that its uses a specific firefox profile called 'auto_test_profile'.
        When using this firefox profile the user will not be prompted when downloading specific
        file types, such as .xlsx and .csv. Lines were left in but commented out that control
        the setup and tear down of a temp directory to be used for downloads. This approach might
        be revisited at a later stage."""
        auto_test_profile = webdriver.FirefoxProfile("C:/Users/rhoward.EMEX/AppData/Roaming/Mozilla/Firefox/Profiles/kz6phe2o.auto_test_profile")
        self.driver = webdriver.Firefox(firefox_profile=auto_test_profile)
        self.driver.implicitly_wait(30)
        self.base_url = client_variables.base_url
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_034_vfl_activity_summary_report_no_subgroups(self):
        """Test generates a VFL Activity Summary Report. The report is in .pdf format but gets openeding
        inside the browser. The test will change tab to the new tab and download the .pdf report for review
        later. NO Subgroups will be contained in this report"""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        common_page_objects.login(driver, client_variables.username1, client_variables.pword1)
        function_module.log_to_file('Test_VFL_Module:test034_vfl_activity_summary_report_no_subgroups:Successfully logged in and started test')
        time.sleep(5)
        print "Logged in successfully"
        #Select the VFL Module
        vfl_page_objects.open_vfl_module(driver)
        vfl_page_objects.wait_for_vfl_records(driver)
        print "Moved to VFL Module"
        #Move to the Reports section
        vfl_page_objects.vfl_reports_button(driver)
        #Open the VFL Activity Summary Report parameters & Verify that WorkGroup field is mandatory
        #Enter a high tiered WorkGroup that has lots of VFL records created during test.
        #Don't select the Include SubGroups checkbox.
        vfl_page_objects.generate_basic_vfl_activity_summary_report(driver, client_variables.wg_default_false)
        print "Opened VFL Activity Summary Report parameters, generated and download VFL summary report - WorkGroup with NO SubGroups"        
        #Rename and move report to client specific folder
        function_module.rename_file(client_variables.output_folder, 'GetTotalByYearReport', 'Summary Report No Subgroups.pdf')
        function_module.move_file(client_variables.output_folder, client_variables.client_folder)
        function_module.log_to_file('Test_VFL_Module:test034_vfl_activity_summary_report_no_subgroups:Successfully moved report file into client specific folder')
        time.sleep(2)
        print "Moved file into client specific folder"
        #Log out of the application
        common_page_objects.logout(driver)
        function_module.log_to_file('Test_VFL_Module:test034_vfl_activity_summary_report_no_subgroups:TEST COMPLETED', 'PASSED')
        print "Test_VFL_Module:test034_vfl_activity_summary_report_no_subgroups:TEST COMPLETED"

    def test_035_vfl_activity_summary_report_with_subgroups(self):
        """Test generates a VFL Activity Summary Report. The report is in .pdf format but gets openeding
        inside the browser. The test will change tab to the new tab and download the .pdf report for review
        later. Subgroups will be contained in this report"""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        common_page_objects.login(driver, client_variables.username1, client_variables.pword1)
        function_module.log_to_file('Test_VFL_Module:test035_vfl_activity_summary_report_with_subgroups:Successfully logged in and started test')
        time.sleep(5)
        print "Logged in successfully"
        #Select the VFL Module
        vfl_page_objects.open_vfl_module(driver)
        vfl_page_objects.wait_for_vfl_records(driver)
        print "Moved to VFL Module"
        #Move to the Reports section
        vfl_page_objects.vfl_reports_button(driver)
        #Open the VFL Activity Summary Report parameters
        #Enter a root WorkGroup that has lots of VFL records created during test.
        #Select Include SubGroups checkbox.
        vfl_page_objects.generate_basic_vfl_activity_summary_report_with_subgroups(driver, client_variables.root_wg)
        print "Opened VFL Activity Summary Report parameters, generated and download VFL summary report - WorkGroup with SubGroups"        
        #Rename and Copy report to client specific folder
        function_module.rename_file(client_variables.output_folder, 'GetTotalByYearReport', 'Summary Report With Subgroups.pdf')
        function_module.move_file(client_variables.output_folder, client_variables.client_folder)
        function_module.log_to_file('Test_VFL_Module:test035_vfl_activity_summary_report_with_subgroups:Successfully moved report file into client specific folder')
        time.sleep(2)
        print "Moved file into client specific folder"
        #Log out of the application
        common_page_objects.logout(driver)
        function_module.log_to_file('Test_VFL_Module:test035_vfl_activity_summary_report_with_subgroups:TEST COMPLETED', 'PASSED')
        print "Test_VFL_Module:test035_vfl_activity_summary_report_with_subgroups:TEST COMPLETED"

    def test_036_vfl_summary_report(self):
        """Test generates a VFL Summary Report. No output file is generated by this report, so only capturing
        a screengrab can be used to ensure the report was correctly generated during testing."""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        common_page_objects.login(driver, client_variables.username1, client_variables.pword1)
        function_module.log_to_file('Test_VFL_Module:test036_vfl_summary_report:Successfully logged in and started test')
        time.sleep(5)
        print "Logged in successfully"
        #Select the VFL Module
        vfl_page_objects.open_vfl_module(driver)
        vfl_page_objects.wait_for_vfl_records(driver)
        print "Moved to VFL Module"
        #Edit first VFL record in list, adding acts with comments, attachments and actions
        vfl_page_objects.edit_latest_vfl_record(driver)
        print "Edited first VFL record on list view page"
        #Move successfully to the next tab
        vfl_page_objects.vfl_next_button(driver)
        print "Moved to Acts Tab"
        #Add a Safe Act of type 1
        vfl_page_objects.add_vfl_act(driver, 1, client_variables.act_type1)
        print "Added a Safe Act of type1"
        #Add a Conversation & attach an image
        vfl_page_objects.add_conversation(driver, "Testing adding conversations")
        driver.refresh()
        vfl_page_objects.add_image(driver, "V:\QA\Automation\Automation_Resources\Attachments\Conversation Image\PM5544_with_non-PAL_signals.png")
        driver.refresh()
        print "Added a conversation with image file attached"
        #Add an Action
        vfl_page_objects.add_action(driver, function_module.today(), "Low", "testing automated VFL Corrective Actions", client_variables.username2)
        print "Added an Action"
        #Select the finish button to return to the Main List View
        vfl_page_objects.vfl_finish_button(driver)
        print "Successfully saved VFL Record and returned to list view"
        #Assert the Print Report button is disabled by default
        #Select the first VFL record and choose the Print Report button
        #Take a screengrab of the generated report
        vfl_page_objects.generate_summary_report_for_vfl_record(driver)
        function_module.log_to_file('Test_VFL_Module:test036_vfl_summary_report:Successfully took a screenshot of report')
        print "took screenshot and saved to output folder"
        time.sleep(6)
        #Rename and Copy screengrab to client specific folder
        function_module.rename_file(client_variables.output_folder, 'GetTotalByYearReport', 'Print Report Screengrab.png')
        function_module.move_file(client_variables.output_folder, client_variables.client_folder)
        print "Moved file into client specific folder"
        #Log out of the application
        driver.switch_to_window(driver.window_handles[0])
        time.sleep(2)
        common_page_objects.logout(driver)
        function_module.log_to_file('Test_VFL_Module:test036_vfl_summary_report:TEST COMPLETED', 'PASSED')
        print "Test_VFL_Module:test036_vfl_summary_report:TEST COMPLETED"
    
    def tearDown(self):
        """Test Tear Down method"""
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    unittest.main()
