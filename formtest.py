from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.keys import Keys
import time
import csv
import urllib2
import sys

class FormTest:
	def __init__(self, csvfile, output, newsletter, submit):
		self.i = 0
		#prefilled fields for uniformity
		self.fillfirstname = 'BORBDINGNAGIAN'
		self.filllastname = 'NAME'
		self.fillemail = 'nitrotest00+jz' + str(self.i) + '@gmail.com'
		self.fillphone = '510510510'
		self.fillcompany = 'NITROTEST00'
		self.fillusers = 0
		self.fillcomments = 'selenium test pass iteration ' + str(self.i)
		self.fillnewsletter = newsletter

		self.dosubmit = submit
		
		self.browser = webdriver.Firefox() # Get local session of firefox

		try:
			self.reader = csv.reader(csvfile, dialect=csv.excel)
			self.writer = csv.writer(output, dialect=csv.excel)
			self.writer.writerow(['Starting form test'])
			self.currentlog = []
		except csv.Error:
			print "could not read CSV, exitting"
			sys.exit()

	def openurl(self):
		try:
			url = self.reader.next()[0]
		except StopIteration:
			print "end of file"
			self.browser.close()
			sys.exit()
		self.currentlog.append(url)
		try: 
			connection = urllib2.urlopen(url)
			connection.close()
		except urllib2.HTTPError, e:
			print str(e.getcode()) + url
			self.openurl()
			return
		self.browser.get(url) # Load page
	
	def runtest(self):
		self.i += 1
		self.fillemail = 'nitrotest00+jz' + str(self.i) + '@gmail.com'
		self.fillcomments = 'selenium test pass iteration ' + str(self.i)
		self.openurl()
		vlpform = None
		vlptype = None
		formids = ['vlpPageForm', 'businessVlp', 'customers-form', 'vlp', 'vlp_form', 'buy_form', 'openVlpModal']
		for formid in formids:
			try:
				if formid == 'openVlpModal':
					vlpform = self.browser.find_elements_by_class_name(formid)
				else: 			
					vlpform = self.browser.find_element_by_xpath("//form[@id='" + formid + "']")
				vlptype = formid
				break;
			except NoSuchElementException:
				continue;
		if vlpform is None:
			self.currentlog.append(['No matching form found'])
			self.writer.writerow(self.currentlog)
			self.currentlog = []
			runtest()
			return

		if vlptype == 'customers-form':
			self.submitcustomersform(vlpform)
		elif vlptype == 'vlp_form':
			self.submitvlpform(vlpform)
		elif vlptype == 'buy_form':
			self.submitbuyform(vlpform)
		elif vlptype in ['vlpPageForm', 'businessVlp', 'vlp']:
			self.submitmodalform(vlpform)
		else:
			vlpform = self.popmodal(vlpform)
			self.submitmodalform(vlpform)

		self.runtest()



	def submitcustomersform(self, vlpform):
		try:
			firstname = vlpform.find_element_by_xpath(".//input[@name='first_name']")
			lastname = vlpform.find_element_by_xpath(".//input[@name='last_name']")
			email = vlpform.find_element_by_xpath(".//input[@name='email_address']")
			company = vlpform.find_element_by_xpath(".//input[@name='company']")
			comments = vlpform.find_element_by_xpath(".//textarea[@name='comments']")
			submit = vlpform.find_element_by_xpath(".//a[@type='Submit']")

			firstname.send_keys(self.fillfirstname)
			lastname.send_keys(self.filllastname)
			email.send_keys(self.fillemail)
			company.send_keys(self.fillcompany)
			comments.send_keys(self.fillcomments)
			if self.dosubmit:
				submit.click()
			self.currentlog.append('success')
			self.writer.writerow(self.currentlog)
			self.currentlog = []
			time.sleep(2)
		except (NoSuchElementException, ElementNotVisibleException) as e:
			self.currentlog.append(e)
			self.writer.writerow(self.currentlog)
			self.currentlog = []
			return 'error'

	def submitvlpform(self, vlpform):
		try: 
			firstname = vlpform.find_element_by_xpath(".//input[@name='first_name']")
			lastname = vlpform.find_element_by_xpath(".//input[@name='last_name']")
			email = vlpform.find_element_by_xpath(".//input[@name='email_address']")
			phone = vlpform.find_element_by_xpath(".//input[@name='phone']")
			company = vlpform.find_element_by_xpath(".//input[@name='company']")
			users = Select(vlpform.find_element_by_xpath(".//select[@name='vlp_intent']"))
			submit = vlpform.find_element_by_xpath(".//button")

			firstname.send_keys(self.fillfirstname)
			lastname.send_keys(self.filllastname)
			email.send_keys(self.fillemail)
			phone.send_keys(self.fillphone)
			company.send_keys(self.fillcompany)
			users.select_by_index(1)
			if self.dosubmit:
				submit.click()
			self.currentlog.append('success')
			self.writer.writerow(self.currentlog)
			self.currentlog = []
			time.sleep(2)
		except (NoSuchElementException, ElementNotVisibleException) as e:
			self.currentlog.append(e)
			self.writer.writerow(self.currentlog)
			self.currentlog = []
			return 'error'

	def submitbuyform(self, vlpform):
		try:
			buyquantity = Select(vlpform.find_element_by_xpath(".//select[@name='buy_quantity']"))
			buyquantity.select_by_value('11')
			vlpform = self.browser.find_elements_by_class_name('openVlpModal')
			vlpform = self.popmodal(vlpform)
			self.submitmodalform(vlpform)
		except (NoSuchElementException, ElementNotVisibleException) as e:
			self.currentlog.append(e)
			self.writer.writerow(self.currentlog)
			self.currentlog = []
			return 'error'
	def submitmodalform(self, vlpform):
		try:
			firstname = vlpform.find_element_by_xpath(".//input[@name='first_name']")
			lastname = vlpform.find_element_by_xpath(".//input[@name='last_name']")
			email = vlpform.find_element_by_xpath(".//input[@name='email_address']")
			phone = vlpform.find_element_by_xpath(".//input[@name='phone']")
			company = vlpform.find_element_by_xpath(".//input[@name='company']")
			users = Select(vlpform.find_element_by_xpath(".//select[@name='vlp_intent']"))
			newsletter = vlpform.find_element_by_xpath(".//input[@name='newsletter_signup']")
			comments = vlpform.find_element_by_xpath(".//textarea[@name='comments']")
			try:
				submit = vlpform.find_element_by_xpath(".//button[@type='submit']")
			except NoSuchElementException:
				try:
					submit = vlpform.find_element_by_xpath(".//button")
				except NoSuchElementException:
					self.currentlog.append('No submit button found')
					self.writer.writerow(self.currentlog)
					self.currentlog = []
					return 'error'
			
		except NoSuchElementException:
			self.currentlog.append('form field mismatch')
			self.writer.writerow(self.currentlog)
			self.currentlog = []
			return 'error'
		try: 
			firstname.send_keys(self.fillfirstname)
			lastname.send_keys(self.filllastname)
			email.send_keys(self.fillemail)
			phone.send_keys(self.fillphone)
			company.send_keys(self.fillcompany)
			comments.send_keys(self.fillcomments)
			users.select_by_index(1)
			if self.fillnewsletter:
				newsletter.click()
			if self.dosubmit:
				submit.click()
			time.sleep(2)
			self.currentlog.append('success')
			self.writer.writerow(self.currentlog)
			self.currentlog = []
		except (NoSuchElementException, ElementNotVisibleException) as e:
			self.currentlog.append('Could not submit fields')
			self.writer.writerow(self.currentlog)
			self.currentlog = []
			return 'error'

	def popmodal(self, vlpform):
		try:
			for attempt in vlpform:
				try:
					attempt.click()	#pop open vlp modal
					break
				except ElementNotVisibleException:
					print "checking next openVlpModal class"
			return self.browser.find_element_by_xpath("//form[@id='vlpModalForm']")
		except (NoSuchElementException, ElementNotVisibleException) as e:
			self.currentlog.append(e)
			self.writer.writerow(self.currentlog)
			self.currentlog = []
			return 'error'






def main(inputform='forms.csv', outputform='output.csv', newsletter=False, submit=False):
	args = sys.argv
	print args
	try:
		if len(args) == 5:
			inputform = args[1]
			outputform = args[2]
			if args[3] in ['True', 'true']: 
				newsletter = True
			else: newsletter = False
			if args[4] in ['True', 'true']:
				submit = True
			else: submit = False
		elif len(args) == 3:
			if args[1] in ['True', 'true']:
				newsletter = True
			else: newsletter = False
			if args[2] in ['True', 'true']:
				submit = True
			else: submit = False
	except Exception as e: 
		print e
		return

	try:
		with open(inputform, 'rU') as csvfile:
			with open(outputform, 'wb') as output: 
				test1 = FormTest(csvfile, output, newsletter, submit)
				test1.runtest()
	except Exception as e:
		print e
		return

if __name__ == "__main__":
    main()

