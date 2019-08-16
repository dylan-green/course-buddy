import urllib.request
import requests
import sys
import re
from bs4 import BeautifulSoup

pre_reqs = None


def request_course_page(course_dept, course_code):
    course_url = "https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-course&dept={}&course={}".format(
        course_dept, course_code
    )
    response = requests.get(course_url)
    return BeautifulSoup(response.text, "html.parser")


def get_course_prereqs(soup):
    pre_reqs = None
    for p in soup.body.find_all("p"):
        try:
            if re.match(re.compile("Pre-reqs:"), p.contents[0]):
                pre_reqs = " ".join(list(filter(None, p.text.split(" "))))
                break
        except:
            pre_reqs = "I could not find pre-reqs for this course"
    return pre_reqs
