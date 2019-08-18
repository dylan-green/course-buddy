import praw
import sys
import scrape
import os

USER_AGENT = "github.com/dylan-green/course-buddy:v0.1.0 (by /u/mr_nefario)"
CALL_PHRASE = "@course\\_buddy"

reddit_username = os.environ["reddit_username"]
reddit_password = os.environ["reddit_password"]
client_id = os.environ["client_id"]
client_secret = os.environ["client_secret"]
subreddit = os.environ["subreddit"]


class Buddy:
    def __init__(self):
        self._reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            username=reddit_username,
            password=reddit_password,
            user_agent=USER_AGENT)
        self._subreddit = self._reddit.subreddit(subreddit)
        self._redditor = self._reddit.user.me()
        self._response = None
        self._comment = None
        self._actions = {"prereqs": self._prereqs}

    def read_comments(self):
        for comment in self._subreddit.stream.comments(skip_existing=True):
            body = comment.body.split(" ")
            try:
                tag = body.index(CALL_PHRASE)
                command = body[tag + 1]
                self._comment = comment
                self._actions[command](body[tag:])
            except (ValueError, IndexError, KeyError):
                pass  # the butter

    def _reply(self):
        # print(self._response)
        try:
            self._comment.reply(self._response)
        except Exception:
            print(Exception)

    def _prereqs(self, args):
        course_dept = args[2]
        course_code = args[3]

        soup = scrape.request_course_page(course_dept, course_code)
        self._response = scrape.get_course_prereqs(soup)
        self._reply()


def main():
    buddy = Buddy()
    buddy.read_comments()


if __name__ == "__main__":
    main()
