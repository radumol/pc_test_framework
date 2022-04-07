import time
import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import date_helper

browser = webdriver.Chrome()

'''
1.User goes to the website https://www.plushcare.com/
'''
@pytest.mark.dependency()
def test_main_page_load():
	main_page_url = "https://plushcare.com/"
	browser.get(main_page_url)
	
	current_url = browser.current_url
	assert current_url == main_page_url


'''
2.User click the button book an appointment and lands on optInsurance page:
'''
@pytest.mark.dependency(depends=['test_main_page_load'])
def test_main_page_book_button():
	book_button_xpath = "/html/body/main/section[1]/div[2]/a"
	button_element = browser.find_element(By.XPATH, book_button_xpath)
	button_url = button_element.get_attribute("href")
	browser.get(button_url)
	time.sleep(1)

	#validations:
	optInsurance_page_url = "https://www.plushcare.com/booking/primary-care/method/"
	assert browser.current_url == optInsurance_page_url


'''
3.User clicks ‘I’m paying for myself’ button and lands on Appointment list page:
'''
@pytest.mark.dependency(depends=['test_main_page_book_button'])
def test_optInsurance_page_selfpay_button():
	selfpay_button_xpath = '//*[@id="__next"]/div/div/div/div/div/div/div/button[2]'
	selfpay_button_element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, selfpay_button_xpath)))
	selfpay_button_element.click()
	time.sleep(3)

	#validations:
	appointment_list_page_url = "https://www.plushcare.com/booking/primary-care/appointments/"
	assert browser.current_url == appointment_list_page_url


'''
4.User selects two days after today appointment from date picker:
'''
@pytest.mark.dependency(depends=['test_optInsurance_page_selfpay_button'])
def test_datepicker_next_days_select():
	xpath_datepicker = '//*[@id="date-picker-input"]'
	datepicker_element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, xpath_datepicker)))
	datepicker_element.click()
	
	next_date_aria_label = date_helper.get_next_2days_date()
	next_date_element = browser.find_element(By.CSS_SELECTOR, "[aria-label='" + next_date_aria_label + "']")
	next_date_element.click()
	time.sleep(1)

	#validations:
	info_date_xpath = '//*[@id="appointments-wrapper"]/div[2]/div[1]'
	info_date_element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, info_date_xpath)))


'''
5.Selects a doctor who’s rating is greater than 4.8 by clicking Book button next to the doctor:
'''
@pytest.mark.dependency(depends=['test_datepicker_next_days_select'])
def test_select_high_rated_doctor():
	index = 2

	while True:
		doctor_element_xpath = '//*[@id="appointments-wrapper"]/div[2]/div[' + str(index) + ']'
		doctor_element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, doctor_element_xpath)))

		rating_xpath = '//*[@id="appointments-wrapper"]/div[2]/div[' + str(index) + ']/div/div[2]/div/div[1]/div[1]/span'
		rating_element = doctor_element.find_element(By.XPATH, rating_xpath)
		doctor_rating = float(rating_element.text)

		if doctor_rating > 4.8:
			book_doctor_button_xpath = '//*[@id="appointments-wrapper"]/div[2]/div[' + str(index) + ']/div/div[3]/button'
			doctor_element.find_element(By.XPATH, book_doctor_button_xpath).click()
			time.sleep(2)
			break
		index += 1

'''
6.User lands on Profile creation page:
'''
@pytest.mark.dependency(depends=['test_select_high_rated_doctor'])
def test_profile_creation_page():
	profile_creation_page_url = "https://www.plushcare.com/booking/register/pc/"

	current_url = browser.current_url
	assert current_url == profile_creation_page_url

	time.sleep(3)
	browser.close()





