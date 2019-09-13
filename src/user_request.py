from collections import namedtuple

CALL_PHRASE = "@course\\_buddy"

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
