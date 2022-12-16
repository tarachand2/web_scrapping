from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import json

# Creating driver object for scraping website
serv = Service(r"D:/web_scrapping/chromedriver.exe")
driver = webdriver.Chrome(service=serv)
driver.get("https://collegedunia.com/usa/college/1090-harvard-university-cambridge")
driver.implicitly_wait(8)
driver.maximize_window()
try:
    # closing pre Registration form
    close = driver.find_element(By.CLASS_NAME, 'pointer')
    close.click()
except:
    print("Registration form is not visible")

# -------> Scraping institute details <------- #
data = {"Name": driver.find_element(By.CSS_SELECTOR, 'a[title="HARVARD UNIVERSITY"]').text,
        "Description": driver.find_element(By.CSS_SELECTOR, 'div[class="cdcms_section1"]:nth-child(1)').text}


# -------> Scraping fees & Deadline table <------- #
fees_table = driver.find_element(By.CLASS_NAME, 'table-common')
rows = [row for row in fees_table.find_elements(By.TAG_NAME, 'tr')]

fees_deadline = []
for row in rows:
    fees = {
        "Program": row.find_element(By.CSS_SELECTOR, 'td a').text,
        "Application Deadline": [deadline.text for deadline in row.find_elements(By.CSS_SELECTOR, 'td div')],
        "Fees": str(row.find_element(By.CSS_SELECTOR, 'td:nth-child(3)').text)
    }
    fees_deadline.append(fees)

data["Fees & Deadline"] = fees_deadline


# -------> scraping courses <------- #
courses = []
for course in driver.find_elements(By.CSS_SELECTOR, 'div.cards-container div.avatar-container'):
    courses.append({"Name": course.find_element(By.CLASS_NAME, 'program-heading').text,
                    "Duration": course.find_element(By.CSS_SELECTOR, 'span.pb-2').text,
                    "Fee": course.find_element(By.CSS_SELECTOR, 'span.fees').text,
                    "Available Courses": course.find_element(
                        By.CSS_SELECTOR, 'div.content-container div:nth-child(1) div.card-info').text,
                    "Exam Score": course.find_element(
                        By.CSS_SELECTOR, 'div.content-container div:nth-child(2) div:nth-child(2)').text,
                    "Application Deadline": course.find_element(
                        By.CSS_SELECTOR, 'div.content-container div:nth-child(3) div:nth-child(2)').text})
data["Courses"] = courses


# -------> scraping ranking <------- #
# wur --> world university ranking
wur = driver.find_element(By.CSS_SELECTOR, '#ranking_scroll div:nth-child(2) div:nth-child(1)')
world_university_rank = {"Overall": wur.find_element(By.CSS_SELECTOR, 'span:nth-child(2)').text,
                         "Business": wur.find_element(By.CSS_SELECTOR, 'div.text-lg span.text-primary').text}
# unr --> us_news_ranking
unr = driver.find_element(By.CSS_SELECTOR, '#ranking_scroll div:nth-child(3) .pl-4')
us_news_rank = {}
for field in unr.find_elements(By.CSS_SELECTOR, 'div.mt-4.text-lg'):
    name = field.find_element(By.CSS_SELECTOR, 'span:nth-child(1)').text
    rank = field.find_element(By.CSS_SELECTOR, 'span:nth-child(2)').text
    us_news_rank[name] = rank

data["Ranking"] = {"World University Rank": world_university_rank,
                   "US News Rank": us_news_rank}

# -------> scraping rating <------- #
ratings = {}
for rating in driver.find_elements(By.CSS_SELECTOR, '.overall-rating-review-container .rating-box'):
    rate_type = rating.find_element(By.CSS_SELECTOR, 'div > span.name').text
    rate = rating.find_element(By.CSS_SELECTOR, 'div > span.value').text
    ratings[rate_type] = rate
data["Rating"] = ratings


# -------> scraping admission <------- #
admission = driver.find_element(By.CSS_SELECTOR, 'div[data-csm-title="Harvard University Admissions"]')
admission.click()
portal_link = admission.find_element(By.CSS_SELECTOR, 'div:nth-child(2) > div.portal p a').text
# ead --> early admission deadline
ead = admission.find_element(By.XPATH, '//*[@id="__next"]/div[2]/section/div/div[1]/div[3]/div[1]/div/div[10]/div/div'
                                       '/div[2]/div[2]/div/div/div/div/p[1]').text
# rdd --> regular decision deadline
rdd = admission.find_element(By.XPATH, '//*[@id="__next"]/div[2]/section/div/div[1]/div[3]/div[1]/div/div[10]/div/div/'
                                       'div[2]/div[3]/div/div/div/div/p[1]').text
# fad --> financial aid deadline
fad = admission.find_element(By.XPATH, '//*[@id="__next"]/div[2]/section/div/div[1]/div[3]/div[1]/div/div[10]/div/div/'
                                       'div[2]/div[4]/div/div/div/div/p[1]').text
data["Admission"] = {
    "Portal Link": portal_link,
    "Early Admission Deadline": ead,
    "Regular Decision Deadline": rdd,
    "Financial Aid Application Deadline": fad
}


# -------> scraping acceptance rate <------- #
acceptance = driver.find_element(By.CSS_SELECTOR, 'div[data-csm-title="Harvard University Acceptance Rate"]')
acceptance.click()
undergraduate = acceptance.find_element(By.CSS_SELECTOR, 'div:nth-child(4) > div > div:nth-child(2)')
graduate = acceptance.find_element(By.CSS_SELECTOR, 'div:nth-child(4) > div > div:nth-child(4)')
data["Acceptance Rate"]= {
    "Undergraduate": {
        "Rate": undergraduate.find_element(By.CSS_SELECTOR, 'div > div:nth-child(2)').text,
        "Total Applicants": undergraduate.find_element(By.CSS_SELECTOR, 'div:nth-child(2) > div:nth-child(2) > '
                                                                        'div:nth-child(2)').text,
        "Total Enrolled": undergraduate.find_element(By.CSS_SELECTOR, 'div:nth-child(3) > div:nth-child(2)').text
    },
    "Graduate": {
        "Rate": graduate.find_element(By.CSS_SELECTOR, 'div > div:nth-child(2)').text,
        "Total Applicants": graduate.find_element(By.CSS_SELECTOR, 'div:nth-child(2) > div:nth-child(2)').text,
        "Total Enrolled": graduate.find_element(By.CSS_SELECTOR, 'div:nth-child(3) > div:nth-child(2)').text
    }
}


# -------> scraping enrollment <------- #
enrollment = driver.find_element(By.CSS_SELECTOR, 'div[data-csm-title="Harvard University enrollment"]')
enrollment.click()
enrolled = enrollment.find_element(By.CSS_SELECTOR, 'div:nth-child(2) > div > div:nth-child(2)')
data["Enrollment"] = {
    "Enrollment": {
        "Harvard University Enrollment": enrolled.find_element(By.CSS_SELECTOR, 'div > div:nth-child(2)').text,
        "Undergraduate Enrollment": enrolled.find_element(By.CSS_SELECTOR, 'div:nth-child(2) > div:nth-child(2) > '
                                                                           'div:nth-child(2)').text,
        "Graduate Enrollment": enrolled.find_element(By.CSS_SELECTOR, 'div:nth-child(3) > div:nth-child(2)').text
    },
    "Graduation Rate": enrollment.find_element(By.CSS_SELECTOR, 'div:nth-child(4) > div > div:nth-child(2)').text
}


# -------> scraping attendance cost <------- #
attendance_cost = driver.find_element(By.CSS_SELECTOR, 'div[data-csm-title="Attendance Cost"]')
attendance_cost.click()
tuition = attendance_cost.find_element(By.CSS_SELECTOR, 'div:nth-child(3) > div > div:nth-child(2)')
on_campus = attendance_cost.find_element(By.CSS_SELECTOR, 'div:nth-child(3) > div > div:nth-child(4)')
data["Attendance Cost"] = {
    "Tuition Fees": {
        "Undergraduate Programs": str(tuition.find_element(By.CSS_SELECTOR, 'div:nth-child(2) > div:nth-child(2)').text),
        "Post Graduate Programs": str(tuition.find_element(By.CSS_SELECTOR, 'div > div:nth-child(2)').text)
    },
    "On Campus": {
        "Rooms": str(on_campus.find_element(By.CSS_SELECTOR, 'div > div:nth-child(2)').text),
        "Meals": str(on_campus.find_element(By.CSS_SELECTOR, 'div:nth-child(2) > div:nth-child(2)').text),
        "Other Expenses": str(on_campus.find_element(By.CSS_SELECTOR, 'div:nth-child(3) > div:nth-child(2)').text),
        "Books and Supplies": str(on_campus.find_element(By.CSS_SELECTOR, 'div:nth-child(4) > div:nth-child(2)').text)
    }
}


# -------> scraping campus location <------- #
location = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/section/div/div[1]/div[3]/div[1]/div/div[16]/div[1]'
                                         '/div/div/div[2]')
data["Campus Location"] = {
    "Website": location.find_element(By.CSS_SELECTOR, 'div a').text,
    "Telephone": location.find_element(By.CSS_SELECTOR, 'div:nth-child(2) > span:nth-child(2)').text,
    "Email": location.find_element(By.CSS_SELECTOR, 'div:nth-child(3) > a').text,
    "Address": location.find_element(By.CSS_SELECTOR, 'div:nth-child(4) > div').text
}

# Saving data in data.json file
with open("data.json", "w") as file:
    json.dump(data, file, indent=4)

driver.quit()
