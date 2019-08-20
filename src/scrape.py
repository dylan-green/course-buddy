import urllib.request
import requests
import re
from bs4 import BeautifulSoup


def request_course_page(subject="", course_code=""):
    course_url = "https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-course&dept={}&course={}".format(
        subject, course_code
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
            pre_reqs = "Sorry, I couldn't find anything for this course."
    return pre_reqs


def get_course_summary(soup):
    try:
        # title is the only <h4> </h4>
        title = soup.find("h4").text
        # summary is always the first <p> </p>
        return title + "\n\n" + soup.find("p").text
    except AttributeError:
        return "Sorry, I couldn't find a summary for this course."
