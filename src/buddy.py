import os
import praw
import scrape
from collections import namedtuple
from subject_codes import subject_codes

USER_AGENT = "github.com/dylan-green/course-buddy:v0.1.0 (by /u/mr_nefario)"
CALL_PHRASE = "@course\\_buddy"

reddit_user = os.environ["REDDIT_USER"]
reddit_pass = os.environ["REDDIT_PASS"]
client_id = os.environ["CLIENT_ID"]
client_secret = os.environ["CLIENT_SECRET"]
subreddit = os.environ["SUBREDDIT"]

UserRequest = namedtuple(
    'UserRequest', ['action', 'subject', 'course_code'])


class Buddy:
    def __init__(self):
        self._reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            username=reddit_user,
            password=reddit_pass,
            user_agent=USER_AGENT)
        self._subreddit = self._reddit.subreddit(subreddit)
        self._redditor = self._reddit.user.me()
        self._response = None
        self._comment = None
        self._actions = {"prereqs": self._prereqs, "summary": self._summary}

    def read_comments(self):
        for comment in self._subreddit.stream.comments(skip_existing=True):
            body = comment.body.split(" ")
            user_request = parse_comment_body(body)

            if user_request is not None:
                self._comment = comment
                action = user_request.action
                subject = user_request.subject.upper()
                course_code = user_request.course_code
                try:
                    assert action in self._actions, "Sorry, I don't understand {}.".format(
                        action)
                    assert subject in subject_codes, "Sorry, {} isn't a subject code.".format(
                        subject)
                except AssertionError as error:
                    self._response = error
                    self._reply()
                else:
                    self._actions[action](subject, course_code)

    def _reply(self):
        self._comment.reply(self._response)

    def _prereqs(self, subject, course_code):
        soup = scrape.request_course_page(subject, course_code)
        self._response = scrape.get_course_prereqs(soup)
        self._reply()

    def _summary(self, subject, course_code):
        soup = scrape.request_course_page(subject, course_code)
        self._response = scrape.get_course_summary(soup)
        self._reply()


def parse_comment_body(body):
    try:
        base = body.index(CALL_PHRASE)
        action = body[base + 1]
        subject = body[base + 2]
        course_code = body[base + 3]
        return UserRequest(action, subject, course_code)
    except (ValueError, IndexError):
        return None


def main():
    buddy = Buddy()
    buddy.read_comments()


if __name__ == "__main__":
    main()
