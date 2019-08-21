from __future__ import unicode_literals

from selenium import webdriver
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import os,sys,argparse
from random import randint


def main(un,pw,inpurl):
    # open a new chrome browser, redirect to linkedin main page, and log in.
    driver = webdriver.Chrome(executable_path = "/Users/jiajiefan/Desktop/Project1/chromedriver")
    driver.get('https://www.linkedin.com')
    sleep(3)
    login(un,pw,driver)

    # redirect to the input second degree connection's linkedin page. 
    driver.get(inpurl)

    # scrape provided link for person's info
    personalInfo = get_persons_info(driver)
    personalInfo.append(inpurl)
    dataheaders = ['name','title','location','url']
    output2 = dict(zip(dataheaders, personalInfo))

    # wait and ensure that the "mutual connection" element has been loaded
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight*1/4);")
    delay = 3
    try:
        myElem = WebDriverWait( driver, delay).until(EC.presence_of_element_located((By.XPATH, './/*[@class = "pv-entity__summary-title Sans-17px-black-85%-semibold"]')))
        print("Page is ready!")
    except TimeoutException:
        print("Still Loading")

    # Once the element above has loaded, click on it to go the "mutual connections" page
#    if len(driver.find_elements_by_xpath('.//*[@class = "pv-entity__summary-title Sans-17px-black-85%-semibold"]')) > 0:
#        link_click = driver.find_element_by_xpath('.//*[@class = "pv-entity__summary-title Sans-17px-black-85%-semibold"]')
#        driver.execute_script("window.scrollTo(" + str( link_click.location['x']) + "," + str( link_click.location['y']-150) + ");")
#        link_click.click()

    if len(driver.find_elements_by_xpath('.//*[@class = "highlight-entity pv-profile-section__card-item shared-connections ember-view"]')) > 0:
        link = driver.find_element_by_xpath('.//*[@class = "highlight-entity pv-profile-section__card-item shared-connections ember-view"]/a')
        driver.execute_script("window.scrollTo(" + str( link.location['x']) + "," + str( link.location['y']-150) + ");")
        url =  link.get_attribute('href').encode('ascii', 'ignore')
        print url
        driver.get(url)
    else:
        print "you guys don't have common connection"

    # scrape the mutual connections data for connections information
    sleep(2)
    connection_info = get_connection_detail(driver)
    driver.close()
    output1 = [dict(zip(dataheaders, ci)) for ci in connection_info]
    return output1, output2

# login information or you can manually input the username and password
def login(username, password, driver):
   # insert username
   username_form =  driver.find_element_by_id("login-email")
   username_form.send_keys(username)
   # insert password
   password_form =  driver.find_element_by_id("login-password")
   password_form.send_keys(password)
   # submit form
   login_attempt = driver.find_element_by_xpath('//*[@type="submit"]')
   login_attempt.submit()


def get_persons_info(driver):
    name = driver.find_element_by_xpath(".//*[@class='pv-top-card-section__information mt3']/h1").text
    headline = driver.find_element_by_xpath(".//*[@class='pv-top-card-section__information mt3']/h2").text
    numShared = driver.find_element_by_xpath(".//*[@class='highlight-entity pv-profile-section__card-item shared-connections ember-view']/a/div/h3").text.split()[0]
    location = driver.find_element_by_xpath(".//*[@class='pv-top-card-section__information mt3']/h3").text
    return [name,headline,location,numShared]

def scrolling_down_page(driver):
    # scroll down the page to the approriate height
    scheight = .1
    while scheight < 9.9:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/%s);" % scheight)
        scheight += .05
    print('you are scrolling the page to get essential element')

def get_connection_detail(driver):
    # extract all the details of each mutual connection
    connection_details = list()
    while True:
        scrolling_down_page(driver)
        delay = 5
        try:
            myElem = WebDriverWait( driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[class ="next"]')))
            # print "Page is ready!"
            print("Page is ready!")
        except TimeoutException:
            # print "Still Loading"
            print("Still Loading")

        link = [i.get_attribute('href').encode('ascii', 'ignore') for i in driver.find_elements_by_xpath(".//*[@class='search-result__info pt3 pb4 ph0']/a")]
        kw = ['1st', 'Premium member']
        rawinfolist = [i.text.encode('ascii', 'ignore') for i in driver.find_elements_by_xpath(".//*[@class='search-result__info pt3 pb4 ph0']")]
        for count,item in enumerate(rawinfolist):
            # s[count] = [i for i in rawinfolist[count].splitlines()]
            info = [i for i in rawinfolist[count].splitlines() if kw[0] not in i if kw[1] not in i]
            info[-1] = int(((info[-1]).split())[0]) # convert numshared from str to int (e.g. '23 shared connections' to 23)
            info.append(link[count])
            connection_details.append(info)
        sleep(2)

        # click next page if needed
        if len(driver.find_elements_by_css_selector('button[class ="next"]')) > 0:
            nextp = driver.find_element_by_css_selector('button[class ="next"]')
            driver.execute_script("window.scrollTo(" + str( nextp.location['x']) + "," + str( nextp.location['y']-150) + ");")
            try:
                nextp.click()
                # print "you click"
                print("next page clicked")
            except:
                # print "please try again"
                print("please try again")
        else:
            break
    print("\nAll done!")
    return connection_details

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--u',required=True) # get linkedin username
    parser.add_argument('--p',required=True) # get linkedin password
    parser.add_argument('--url',required=True)
    args = parser.parse_args()
    un = args.u
    pw = args.p
    inpurl = args.url
    main(un,pw,inpurl)



