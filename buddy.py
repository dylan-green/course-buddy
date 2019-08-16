import praw
import sys
import scrape

USER_AGENT = "github.com/dylan-green/ubc-course-bot:v0.1.0 (by /u/mr_nefario)"
PRAW_CLIENT = "course_buddy"
CALL_PHRASE = "@course\\_buddy"
SUBREDDIT = "ubc"


class Buddy:
    def __init__(self):
        self._reddit = praw.Reddit(PRAW_CLIENT, user_agent=USER_AGENT)
        self._subreddit = self._reddit.subreddit(SUBREDDIT)
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
            except (ValueError, IndexError):
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
        prereqs = scrape.get_course_prereqs(soup)
        self._response = prereqs
        self._reply()


def main():
    buddy = Buddy()
    buddy.read_comments()


if __name__ == "__main__":
    main()
