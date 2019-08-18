import praw
import sys
import scrape
import os
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
        self._redditor = self._reddit.user.me()
        self._response = None
        self._comment = None
        self._actions = {"prereqs": self._prereqs, "summary": self._summary}

    def read_comments(self):
        for comment in self._subreddit.stream.comments(skip_existing=True):
            body = comment.body.split(" ")
            tag = None
            action = None

            try:
                tag = body.index(CALL_PHRASE)
                action = body[tag + 1]
                self._comment = comment
                assert action in self._actions
            except AssertionError:
                # reply to calls to the bot with invalid action requests
                self._response = "Sorry, {} is not a valid request.".format(
                    action)
                self._reply()
            except (ValueError, IndexError):
                # body.index() throws ValueError if there's no @course_buddy tag
                # body[tag + 1] throws IndexError if there's nothing after the tag
                pass  # the butter.
            else:
                # call the action method with the rest of the comment body
                self._actions[action](body[tag:])

    def _reply(self):
        self._comment.reply(self._response)

    def _prereqs(self, args):
        try:
            course_dept = args[2]
            course_code = args[3]
            assert course_dept.upper() in subject_codes
            soup = scrape.request_course_page(course_dept, course_code)
            self._response = scrape.get_course_prereqs(soup)
            self._reply()
        except (IndexError, AssertionError):
            pass

    def _summary(self, args):
        # stub for a method that replies with the course summary
        pass


def main():
    buddy = Buddy()
    buddy.read_comments()


if __name__ == "__main__":
    main()
