uname='Enter your yourname here'
pword='Enter your password here'


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from datetime import datetime
import os
from collections import OrderedDict
import urllib.request
from pathlib import Path
from requests import get
import time

# levelOfNesting = 2
tags = ['<', '>', '/', '|', '\\','*']

minimumWindow = False
# Set random defaults
listOfLevel1 = ['Computer Networks',
                'Computer Organization and Architecture',
                'Combinatorics and Propositional logic',
                'Databases',
                'Theory of Computation',
                'Linear Algebra',
                'Aptitude',
                'Graph Theory',
                'Compiler Design',
                'Calculus',
                'Probability',
                'Set Theory & Algebra',
                'Algorithms',
                'Digital Logic',
                'Operating System',
                "Programming and Data Structures"]


def internet_on():
    i = 0
    while True:
        try:
            urllib.request.urlopen('http://www.google.com', timeout=20)
            return True
        except:
            print("Internet not found for last %s minutes" % i)
            i = i + 1
            time.sleep(60)
            pass

try:
    with open('last.txt', 'r') as f:
        lines = f.readlines()
        currentSubject = str(lines[0]).strip()
        startFromTopic = int(lines[1])
        startFromVideo = int(lines[2])
except:
    currentSubject = 'Computer Networks'
    startFromTopic = 0
    startFromVideo = 0
    with open('done.txt','w') as f:
        pass


# Seconds to wait for the page to load
delay = 1

# Set the webdriver, we are using chrome
browser = webdriver.Chrome()
browser.maximize_window()
if minimumWindow:
    pyautogui.moveTo(600, 3, 1)
    pyautogui.dragTo(0, 200, 1, button='left')

# Go to the ravindrababu website
browser.get('http://eclassesbyravindra.com/login/index.php')
username = browser.find_element_by_id('username')
password = browser.find_element_by_id('password')

# Enter Credentials
username.send_keys(uname)
password.send_keys(pword)


def download(url, file_name):
    # get request
    response = get(url)
    # open in binary mode
    with open(file_name, "wb") as file:
        # write to file
        file.write(response.content)


def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Y', suffix)


try:
    try:
        myElm = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#loginbtn')))
    except TimeoutException:
        browser.refresh()
        myElm = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#loginbtn')))
        print("too much time")
    myElm.click()

    for level1 in listOfLevel1:
        if level1 in open('done.txt', 'r').read():
            continue
        browser.get('http://eclassesbyravindra.com')
        try:
            myElm = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.LINK_TEXT, level1)))
        except TimeoutException:
            browser.refresh()
            myElm = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.LINK_TEXT, level1)))
            print("too much time")
        myElm.click()

        # if levelOfNesting == 2:
        listOfSubjects = []
        listOfSubUrl = []
        listOfSubLinks = []
        linksOnPage = browser.find_elements_by_partial_link_text('')
        # Remove redundant links if present
        d = OrderedDict()
        for x in listOfSubLinks:
            d[x] = True
        listOfSubUrl = []
        for x in d:
            listOfSubUrl.append(x)
        # print(listOfSubUrl)
        totalSubs = len(listOfSubUrl)
        subjectNumber = 0
        for SubjectLink in listOfSubUrl:
            subjectNumber = subjectNumber + 1
            if subjectNumber < startFromTopic and level1 == currentSubject:
                continue

            browser.get(SubjectLink)
            SubTitle = browser.title
            for tag in tags:
                SubTitle = SubTitle.replace(tag, '_')
            print("Downloading " + str(subjectNumber) + SubTitle)
            if "eclassesbyravindra.com" in SubTitle:
                raise Exception
            SubTitle = str(subjectNumber) + SubTitle.split(':')[-1]
            print(SubTitle)
            SubTitle = "E:\Coding\\test\\" + level1 + "\\" + SubTitle
            try:
                makedirs(SubTitle)
            except:
                pass
            links = browser.find_elements_by_partial_link_text('')
            listOfLinks = []
            listOfURL = []
            listOfTitle = []

            # Find useful links on the page
            for i in links:

                link = str(i.get_attribute('href'))
                if link[30:38] == 'mod/page':
                    listOfLinks.append(link)

            # Save current tab
            mainWindow = browser.current_window_handle

            # Remove redundant links if present
            d = OrderedDict()
            for x in listOfLinks:
                d[x] = True
            listOfLinks = []
            for x in d:
                listOfLinks.append(x)
            # print(listOfLinks)
            totalLinks = len(listOfLinks)
            download(durl, fnameWithDir)

            i = 0

            # For each link, get the video link
            for link in listOfLinks:
                i = i + 1
                if i < startFromVideo and level1 == currentSubject and subjectNumber <= startFromTopic:
                    continue
                if level1=='Digital Logic' and subjectNumber==5:
                    continue
                browser.get(link)
                if 'Your session has timed out. Please log in again.' in browser.page_source:
                    raise Exception
                if 'youtube' in browser.page_source:
                    print("It is a youtube video")
                    print("================================================================================")
                    continue
                print('Topics in this Subject ', subjectNumber, '/', totalSubs, sep='')

                print('Videos in this topic ', i, '/', totalLinks, sep='')
                title = browser.title
                result = None
                counterForLink = 0
                browser.close()
                browser.switch_to.window(mainWindow)
                listOfURL.append(mainlink)
                filename = mainlink.split('/')[-1]
                listOfTitle.append((filename, title))
                # f.write(mainlink + '\n')
                durl = mainlink
                # print(durl)
                fname = title + '_720p.mp4'
                for tag in tags:
                    fname = fname.replace(tag, " ")
                fnameWithDir = SubTitle + "\\" + fname
                # print("SUb title is ", SubTitle, "\n and filename is ", fname)


                size = urllib.request.urlopen(durl).info()['Content-Length']
                size = int(size)
                print(sizeof_fmt(size))
                internet_on()

                try:
                    if Path(SubTitle + '\\' + fname).is_file():
                        if str(urllib.request.urlopen(durl).info()['Content-Length']).strip() != str(
                                os.stat(fnameWithDir).st_size).strip():
                            os.remove(SubTitle + '\\' + fname)
                            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                  "\nDownloading " + fnameWithDir.replace(' ', '_'))
                            # print(str(urllib.request.urlopen(durl).info()['Content-Length']).strip())
                            try:
                                # urllib.request.urlretrieve(durl, fnameWithDir)
                                download(durl, fnameWithDir)
                                # browser.close()

                            except:
                                with open("error.txt", "a") as f:
                                    f.write(durl + "    " + fnameWithDir + " \n")
                                raise Exception
                        else:
                            print("Already Downloaded as " + fnameWithDir.replace(" ", '_'))
                    else:
                        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '\n',
                              "Downloading " + fnameWithDir.replace(" ", '_'))
                        try:
                            download(durl, fnameWithDir)
                            # browser.close()
                        except:
                            with open("error.txt", "a") as f:
                                f.write(durl + "    " + fnameWithDir + " \n")
                            raise Exception
                    if subjectNumber == totalSubs and i == totalLinks:
                        with open('done.txt', 'a') as f:
                            f.write(level1 + '\n')
                except:
                    raise Exception
                with open('last.txt', 'w') as f:
                    f.write(level1 + '\n' + str(subjectNumber) + '\n' + str(i))
                for qw in range(100):
                    print("=", end='')
                print("\n")

except Exception as errorIs:
    with open('Out.txt', 'w') as f:
        f.write("Error Bro")
    with open('AllOuts.txt', 'a') as f:
        f.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        f.write(str(errorIs))
        f.write('\n\n\n')
    print('\x1b[6;31m' + str(errorIs) + '\x1b[0m')
