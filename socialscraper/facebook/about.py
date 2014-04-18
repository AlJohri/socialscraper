import requests, lxml.html, lxml.etree

ABOUT_URL = "https://www.facebook.com/%s/info"

import pdb

def search(browser, graph_name):

	response = browser.get(ABOUT_URL % graph_name)
	doc = lxml.html.fromstring(response.text)
	for element in doc.cssselect(".hidden_elem"): 
		comment = element.xpath("comment()")
		if not comment: continue
		element_from_comment = lxml.html.tostring(comment[0])[5:-4]
		doc = lxml.html.fromstring(element_from_comment)
		fbTimelineSection = doc.cssselect('.fbTimelineSection')
		if not fbTimelineSection: continue
		for thing in fbTimelineSection:
			title = thing.cssselect('.uiHeaderTitle')
			if not title: continue
			title = title[0].text_content()
			print ""
			print title
			print "=================================================="			
			if title == "Work and Education":
				data = thing.cssselect('.profileInfoTable')
				if not data: continue
				for table in data[0].cssselect('tbody'): 
					for row in table.cssselect('tr'): 
						for header in row.cssselect('th'):
							print ""
							print header.text_content()

						for cell in row.cssselect('td'):
							for experience in cell.cssselect(".experienceContent"):
								experienceTitle = experience.cssselect(".experienceTitle")[0].text_content()
								experienceBody = experience.cssselect(".experienceBody")[0].text_content()
								print experienceTitle, experienceBody
			elif title == "Relationship":
				data = thing.cssselect('.profileInfoTable')
				if not data: continue
				for table in data[0].cssselect('tbody'): 
					for row in table.cssselect('tr'): 
						for cell in row.cssselect('td'):
							name = cell.cssselect('div div div div div div div')[0].text_content()
							status = cell.cssselect('div div div div div div div')[1].text_content()
							print name, status
			elif "Places Lived" in title:
				data = thing.cssselect('.profileInfoTable')
				if not data: continue
				# print data[0].text_content()
				for table in data[0].cssselect('tbody'): 
					for row in table.cssselect('tr'): 
						for cell in row.cssselect('td'):
							if len(cell.getchildren()) == 1 and (cell.getchildren()[0].tag == 'hr' or cell.getchildren()[0].tag == 'a'): continue
							name = cell.cssselect('div div div')[0].getchildren()[1].getchildren()[0].text_content()
							status = cell.cssselect('div div div')[0].getchildren()[1].getchildren()[1].text_content()
							print name, status
			elif "Family" in title: # empty
				data = thing.cssselect('.profileInfoTable')
				if not data: continue
				print data[0].text_content()
			elif "Contact Information" in title:
				data = thing.cssselect('.profileInfoTable')
				if not data: continue
				print data[0].text_content()
			elif "Basic Information" in title:
				data = thing.cssselect('.profileInfoTable')
				if not data: continue
				for table in data[0].cssselect('tbody'): 					
					for row in table.cssselect('tr'): 
						header = row.cssselect('th')[0]
						content = row.cssselect('td')[0]
						print header.text_content(), content.text_content()
			elif "Life Events" in title:
				data = thing.getchildren()[1].text_content()
				print data
			elif "About" in title: # About Carson
				data = thing.getchildren()[1].text_content()
				print data
			elif "Favorite Quotations" in title:
				data = thing.getchildren()[1].text_content()
				print data
			else:
				data = thing.getchildren()[1].text_content()
				print data
			
			# pdb.set_trace()
			
	# pdb.set_trace()

	# data = thing.cssselect('.profileInfoTable')
