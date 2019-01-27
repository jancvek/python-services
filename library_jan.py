from selenium import webdriver
import time
import datetime
import smtplib
from email.message import EmailMessage

#---------USER INPUT------
card_num = "0104232"
passw = "knjiga"
loan_link = "siktrz/104232"
jan_email = "jan.cvek@gmail.com"
#-------------------------

# -----ADDED TO RUN BROWSER HEADLESS-----
#LOOK AT: https://blog.testproject.io/2018/02/20/chrome-headless-selenium-python-linux-servers/
from pyvirtualdisplay import Display 

display = Display(visible=0, size=(1024, 768)) 
display.start() 
#--------------END----------------------

#----------------SET EMAIL AGENT-----------
import smtplib
from email.message import EmailMessage

msg = EmailMessage()
msg['Subject'] = "KNJIŽNICA - VRNI!"
msg['From'] = 'jan.cvek@gmail.com'
msg['To'] = [ 'jan.cvek@domain.com' ]
#-----------------END-----------------------

for x in range(3):

    driver = webdriver.Firefox(timeout=60)

    driver.get('https://plus.si.cobiss.net/opac7/user/login/aai/cobiss')

    #wait to script bild whole web page
    time.sleep(2)

    driver.find_element_by_xpath("//div[@class='tableField']/div[1]/div[1]").click()

    #wait to dropdown bild (1000 inputs)
    time.sleep(3)

    driver.find_element_by_xpath("//div[@class='tableField']/div[1]/div[2]/div[1]/div[@data-value='siktrz']").click()

    libMemberID = driver.find_element_by_id("libMemberID")
    password = driver.find_element_by_id("password1")

    libMemberID.send_keys(card_num)
    password.send_keys(passw)

    time.sleep(1)

    driver.find_element_by_id("wp-submit1").click()

    #wait to load new page 
    time.sleep(3)

    logInFlag = False
    for x in range(6):
        if driver.current_url == "https://plus.si.cobiss.net/opac7/memberships":
            logInFlag = True
            break

        time.sleep(3)

    if not logInFlag:
        print("Error: can not log in!")
        driver.close()
    else:
        break

if not logInFlag:
    print("Sent error email")

    msg.set_content("Error: dostop do COBISS ni uspel!")
    server = smtplib.SMTP_SSL('smtp.gmail.com')
    server.ehlo()
    server.login("jan.cvek@gmail.com", "5266jana")

    server.send_message(msg)
    server.quit()

    exit()

driver.get('https://plus.si.cobiss.net/opac7/mylib/'+loan_link+'/loan')

time.sleep(5)

booksAtHome = driver.find_elements_by_xpath("//tbody [@id='extLoanStuleBody']/tr")

minDays = 100

for book in booksAtHome:
    #check_box = book.find_element_by_xpath(".//td[1]/div/span/input")
    return_date = book.find_element_by_xpath(".//td[2]")
    #title = book.find_element_by_xpath("/td[3]")
    #take_date = book.find_element_by_xpath("/td[6]")

    #print(return_date.text)

    return_date_date = datetime.datetime.strptime(return_date.text, '%d.%m.%Y') + datetime.timedelta(days=1)

    today = datetime.datetime.now()

    delta = return_date_date - today

    print(delta.days)

    if delta.days < minDays:
        minDays = delta.days

    if delta.days < 3:
        print("Sent email")

        msg.set_content("Vrni knjige v knjižnico: kartica Jan! Še "+ str(minDays) +" do poteka ("+ return_date+")!")
        server = smtplib.SMTP_SSL('smtp.gmail.com')
        server.ehlo()
        server.login("jan.cvek@gmail.com", "5266jana")

        server.send_message(msg)
        server.quit()

        break

driver.close()