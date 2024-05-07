from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Enter your email and password to log in to hrm/cal state la portal
email = 'EMAIL'
password = 'PASSWORD'

'''
Set the path to the directory containing ChromeDriver
chromedriver_path = '/usr/local/Caskroom/chromedriver/124.0.6367.91/chromedriver-mac-x64/chromedriver'

options = Options() options.binary_location = ('/Users/abrahamlimon/chrome-mac-x64/Google Chrome for 
Testing.app/Contents/MacOS/Google Chrome for Testing') options.add_argument("--headless")

# service = Service(executable_path=chromedriver_path)
'''

driver = webdriver.Chrome()

# ***LOG IN TO HRM AND NAVIGATE TO TIMESHEET PAGE AND COPY AND PASTE LINK HERE IF THIS ONE DOESN'T WORK***
driver.get("https://cmshr.calstatela.edu/psp/HLAPRD/EMPLOYEE/HRMS/c/ROLE_EMPLOYEE.TL_MSS_EE_SRCH_PRD.GBL"
           "?PORTALPARAM_PTCNAV=HC_TL_SS_JOB_SRCH_EE_GBL&EOPP.SCNode=HRMS&EOPP.SCPortal=EMPLOYEE&EOPP.SCName"
           "=CO_EMPLOYEE_SELF_SERVICE&EOPP.SCLabel=Report%20Time&EOPP.SCFName=HC_RECORD_TIME&EOPP.SCSecondary=true"
           "&EOPP.SCPTfname=HC_RECORD_TIME&FolderPath=PORTAL_ROOT_OBJECT.CO_EMPLOYEE_SELF_SERVICE.HC_TIME_REPORTING"
           ".HC_RECORD_TIME.HC_TL_SS_JOB_SRCH_EE_GBL&IsFolder=false")

# Wait for page to load before looking for element, adding wait to ensure page fully loads
WebDriverWait(driver, 20).until(EC.title_contains("Sign in to your account"))

# Looking for input field and entering username
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="i0116"]')))
email_input = driver.find_element(By.XPATH, '//*[@id="i0116"]')
email_input.send_keys(email)

# Finding and Pressing email next button
next_email_button = driver.find_element(By.XPATH, '//*[@id="idSIButton9"]')
time.sleep(1)
next_email_button.click()

# Finding password element and inputting password
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="i0118"]')))
password_input = driver.find_element(By.XPATH, '//*[@id="i0118"]')
time.sleep(1)
password_input.send_keys(password)

# Find password submit button and click it
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="idSIButton9"]')))
next_password_button = driver.find_element(By.XPATH, '//*[@id="idSIButton9"]')
next_password_button.click()

# Stay signed in, press next
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="idSIButton9"]')))
next_stay_signed_in_button = driver.find_element(By.XPATH, '//*[@id="idSIButton9"]')
next_stay_signed_in_button.click()

# Two-step verification switch to IFrame and then  press 'Call ME'
WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//*[@id="duo_iframe"]')))
time.sleep(3)
WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="auth_methods"]/fieldset/div[1]/button')))
verification_button = driver.find_element(By.XPATH, '//*[@id="auth_methods"]/fieldset/div[1]/button')
verification_button.click()
driver.switch_to.default_content()

'''
* NOT NECESSARY* ONLY NEEDED TO IMPLEMENT THE NAVIGATION TO HRM ONCE ON MYCALSTATELA PORTAL 
  TO NAVIGATE TO ACTUAL TIMESHEET DIRECTLY JUST INCLUDE LINK STRAIGHT TO TIMESHEET PAGE 
# Find HRM AND OPEN IT
time.sleep(1)
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="vpc_WebPart.QuickLaunchWebPart'
                                                                      '.external.f7875ed1-f182-4136-8289-138feac92d36'
                                                                      '"]/div/div/div[3]/div[2]/div[6]/a')))
hrm_button = driver.find_element(By.XPATH, '//*[@id="vpc_WebPart.QuickLaunchWebPart.external.f7875ed1-f182-4136-8289'
                                           '-138feac92d36"]/div/div/div[3]/div[2]/div[6]/a')
time.sleep(1)
hrm_button.click()
'''

# Start To Fill Timesheet

# Index 0 = start, Index 1 = end, Index 2 = start, Index 3 = end
# *ADJUST CODE IF NEEDED FOR MORE SHIFTS*
monday = []
tuesday = ['7:45:00AM', '10:00:00AM', '11:00:00AM', '1:15:00PM']
wednesday = ['7:45:00AM', '12:00:00PM']
thursday = ['12:00:00PM', '1:15:00PM']
friday = ['7:45:00AM', '8:05:00AM', '11:45:00AM', '12:15:00PM']

# Find out which week the page is on
time.sleep(3)
WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//*[@id="ptifrmtgtframe"]')))

'''
date_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*['
                                                                                           '@id'
                                                                                           '="win0divTR_'
                                                                                           'PUNCH_GRIDGP$0"]')))

date_text = date_element.text

entire_date = date_text[5:15]
month = entire_date[:2]
day = entire_date[3:5]
year = entire_date[6:]

year = int(year)
day = int(day)
month = int(month)

start_date = datetime(year, month, day)
'''

# OPEN THE DROPDOWN MENU AND OPEN TIMESHEET FOR ENTIRE TIME PERIOD
dropdown = driver.find_element(By.XPATH, '//*[@id="DERIVED_TL_WEEK_VIEW_BY_LIST"]')
select = Select(dropdown)
select.select_by_value('T')


def get_rows():
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="TR_PUNCH_GRID$scrolli$0"]')))
    table = driver.find_element(By.XPATH, '//*[@id="TR_PUNCH_GRID$scrolli$0"]')
    return_rows = table.find_elements(By.TAG_NAME, 'tr')
    return return_rows


def get_day_of_week(day_of_week_row):  # Return String of what day it is
    rows_fn = get_rows()
    if day_of_week_row.text == '':
        row_fn = rows_fn[rows_index - 1]
        return row_fn.text[0:3]
    else:
        return day_of_week_row.text[0:3]


def get_inputs(in_row):
    input_boxes_fn = in_row.find_elements(By.TAG_NAME, 'input')
    start_time_input_fn = input_boxes_fn[0]
    end_time_input_fn = input_boxes_fn[3]
    start_end_list = [start_time_input_fn, end_time_input_fn]
    return start_end_list


# Num Rows - 5 for the 5 headers
time.sleep(3)
num_rows = (len(get_rows()) - 5)
num_dates_inserted = 0
# Start at index 5 because 0-4 are headers
rows_index = 5

while num_rows > rows_index:

    if rows_index == 5:
        time.sleep(2)

    rows = get_rows()
    row = rows[rows_index]

    # Remove this to fill out entire timesheet. This is used to stop at a certain date
    time.sleep(2)
    row_info = row.find_elements(By.TAG_NAME, 'span')
    date = row_info[1]
    date = date.text
    # END OF REMOVE ^

    day_of_week = get_day_of_week(row)

    # Find the input boxes for each row:
    input_boxes = get_inputs(row)
    start_time_input = input_boxes[0]
    end_time_input = input_boxes[1]
    add_row_button = row.find_elements(By.TAG_NAME, 'a')

    match day_of_week:
        case 'Mon':
            if 0 < len(monday) <= 2:
                start_time_input.send_keys(monday[0])
                end_time_input.send_keys(monday[1])
            elif 0 < len(monday) > 2:
                # Add another row to input time
                add_row_button[5].click()
                time.sleep(3)
                # Gets the new rows
                rows = get_rows()
                # Gets first Row for day and input boxes
                row = rows[rows_index]
                input_boxes = get_inputs(row)
                start_time_input = input_boxes[0]
                end_time_input = input_boxes[1]
                # Insert time into input boxes
                start_time_input.send_keys(monday[0])
                end_time_input.send_keys(monday[1])

                # Goes to newly added row
                time.sleep(2)
                new_rows = get_rows()
                rows_index += 1
                num_rows += 1
                row = rows[rows_index]
                # Gets input boxes for new row
                input_boxes = get_inputs(row)
                start_in = input_boxes[0]
                end_in = input_boxes[1]
                # Input time into new boxes
                start_in.send_keys(monday[2])
                end_in.send_keys(monday[3])
        case 'Tue':
            if 0 < len(tuesday) <= 2:
                start_time_input.send_keys(tuesday[0])
                end_time_input.send_keys(tuesday[1])
            elif 0 < len(tuesday) > 2:
                # Add another row to input time
                add_row_button[5].click()
                time.sleep(3)
                # Gets the new rows
                rows = get_rows()
                # Gets first Row for day and input boxes
                row = rows[rows_index]
                input_boxes = get_inputs(row)
                start_time_input = input_boxes[0]
                end_time_input = input_boxes[1]
                # Insert time into input boxes
                start_time_input.send_keys(tuesday[0])
                end_time_input.send_keys(tuesday[1])

                # Goes to newly added row
                time.sleep(2)
                new_rows = get_rows()
                rows_index += 1
                num_rows += 1
                row = rows[rows_index]
                # Gets input boxes for new row
                input_boxes = get_inputs(row)
                start_in = input_boxes[0]
                end_in = input_boxes[1]
                # Input time into new boxes
                start_in.send_keys(tuesday[2])
                end_in.send_keys(tuesday[3])
        case 'Wed':
            if 0 < len(wednesday) <= 2:
                start_time_input.send_keys(wednesday[0])
                end_time_input.send_keys(wednesday[1])
            elif 0 < len(wednesday) > 2:
                # Add another row to input time
                add_row_button[5].click()
                time.sleep(3)
                # Gets the new rows
                rows = get_rows()
                # Gets first Row for day and input boxes
                row = rows[rows_index]
                input_boxes = get_inputs(row)
                start_time_input = input_boxes[0]
                end_time_input = input_boxes[1]
                # Insert time into input boxes
                start_time_input.send_keys(wednesday[0])
                end_time_input.send_keys(wednesday[1])

                # Goes to newly added row
                time.sleep(2)
                new_rows = get_rows()
                rows_index += 1
                num_rows += 1
                row = rows[rows_index]
                # Gets input boxes for new row
                input_boxes = get_inputs(row)
                start_in = input_boxes[0]
                end_in = input_boxes[1]
                # Input time into new boxes
                start_in.send_keys(wednesday[2])
                end_in.send_keys(wednesday[3])
        case 'Thu':
            if 0 < len(thursday) <= 2:
                start_time_input.send_keys(thursday[0])
                end_time_input.send_keys(thursday[1])
            elif 0 < len(thursday) > 2:
                # Add another row to input time
                add_row_button[5].click()
                time.sleep(3)
                # Gets the new rows
                rows = get_rows()
                # Gets first Row for day and input boxes
                row = rows[rows_index]
                input_boxes = get_inputs(row)
                start_time_input = input_boxes[0]
                end_time_input = input_boxes[1]
                # Insert time into input boxes
                start_time_input.send_keys(thursday[0])
                end_time_input.send_keys(thursday[1])

                # Goes to newly added row
                time.sleep(2)
                new_rows = get_rows()
                rows_index += 1
                num_rows += 1
                row = rows[rows_index]
                # Gets input boxes for new row
                input_boxes = get_inputs(row)
                start_in = input_boxes[0]
                end_in = input_boxes[1]
                # Input time into new boxes
                start_in.send_keys(thursday[2])
                end_in.send_keys(thursday[3])
        case 'Fri':
            if 0 < len(friday) <= 2:
                start_time_input.send_keys(friday[0])
                end_time_input.send_keys(friday[1])
            elif 0 < len(friday) > 2:
                # Add another row to input time
                add_row_button[5].click()
                time.sleep(3)
                # Gets the new rows
                rows = get_rows()
                # Gets first Row for day and input boxes
                row = rows[rows_index]
                input_boxes = get_inputs(row)
                start_time_input = input_boxes[0]
                end_time_input = input_boxes[1]
                # Insert time into input boxes
                start_time_input.send_keys(friday[0])
                end_time_input.send_keys(friday[1])

                # Goes to newly added row
                time.sleep(2)
                new_rows = get_rows()
                rows_index += 1
                num_rows += 1
                row = rows[rows_index]
                # Gets input boxes for new row
                input_boxes = get_inputs(row)
                start_in = input_boxes[0]
                end_in = input_boxes[1]
                # Input time into new boxes
                start_in.send_keys(friday[2])
                end_in.send_keys(friday[3])
        case _:
            print("Weekend Nothing to Input")

    rows_index += 1

    # Remove this to fill out entire timesheet. This is used to stop at a certain date
    if date == '5/10':
        num_rows -= 100
    else:  # Remove if else and keep this to fill entire timesheet
        num_rows = len(rows)


# DONE INPUTTING, NOW SUBMIT TIMESHEET
submit_button = driver.find_element(By.XPATH, '//*[@id="TL_LINK_WRK_SUBMIT_PB$418$"]')
submit_button.click()
time.sleep(10)

'''
for entry in driver.get_log('browser'):
    print(entry)
'''

driver.quit()
