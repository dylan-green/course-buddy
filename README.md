# course-buddy
Bot for the r/ubc subreddit to provide useful course information.

This bot uses PRAW (Python Reddit API Wrapper), and is deployed on Heroku.

Right now the bot provides pre-requisite course information for courses at the University of British Columbia.
It only replies when called, and a valid call to the bot is `@course_buddy <service> <course department> <course code>`.

#### Services 
`prereqs`: lists all required and recommend prerequisite courses

`summary`: provides a brief summary of the course

## Contributing
I'd love help adding new features, so if you'd like to contribute start by cloning the repo. 

See [this page](https://docs.python.org/3/tutorial/venv.html) and follow the steps to set up a virtual python environment.
Then run `pip install -r requirements.txt`.

You'll need to set the necessary environment variables to create a PRAW Reddit instance:

```
REDDIT_USER=<username>
REDDIT_PASS=<password>
CLIENT_ID=<client id>
CLIENT_SECRET=<secret>
SUBREDDIT=coursebuddy
```

`coursebuddy` is the subreddit for development and testing; the deployement environment points to `r/ubc`.

To run the bot locally just run `python3 src/buddy.py`.
