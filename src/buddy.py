import os
import sys
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


class Buddy:
    def __init__(self):
        self._reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            username=reddit_user,
            password=reddit_pass,
            user_agent=USER_AGENT)
        self._subreddit = self._reddit.subreddit(subreddit)
        self._response = None
        self._comment = None
        self._actions = {"prereqs": self._prereqs, "summary": self._summary}

    def read_comments(self):
        # stream.comments retrieves new comments as they become available
        for comment in self._subreddit.stream.comments(skip_existing=True):
            # only read comments posted by other users
            # reddit_user is the username of self
            if comment.author != reddit_user:
                body = comment.body.split(" ")
                user_request = parse_comment_body(body)

                if user_request:  # @course_buddy was called in the comment
                    # user_request = (action, subject, course_code)
                    self._comment = comment
                    action = user_request.action
                    subject = user_request.subject.upper()
                    course_code = user_request.course_code

                    if action not in self._actions:
                        # @course_buddy called with an invalid action
                        self._response = "Sorry, I don't understand {}.".format(
                            action)
                        self._reply()
                    elif subject not in subject_codes:
                        # @course_buddy called with an incorrect subject code
                        self._response = "Sorry, {} isn't a subject code.".format(
                            subject)
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


UserRequest = namedtuple(
    'UserRequest', ['action', 'subject', 'course_code'])


# return None if the "@course_buddy" tag is not found or
# the comment is too short to be a valid bot call.
# Otherwise return a UserRequest tuple
def parse_comment_body(body):
    if CALL_PHRASE not in body:
        return None
    base = body.index(CALL_PHRASE)
    if len(body[base:]) < 4:
        return None
    else:
        action = body[base + 1]
        subject = body[base + 2]
        course_code = body[base + 3]
        return UserRequest(action, subject, course_code)


def main():
    buddy = Buddy()
    buddy.read_comments()


if __name__ == "__main__":
    main()
