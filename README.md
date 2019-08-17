# course-buddy
Bot for the r/ubc subreddit to provide useful course information.

This bot uses PRAW (Python Reddit API Wrapper), and is deployed on Heroku.

Right now the bot provides pre-requisite course information for courses at the University of British Columbia.
It only replies when called, and a valid call to the bot is `@course_buddy <service> <course department> <course code>`.

Services right now are limited to `prereqs`, though new services will be coming soon.

## Contributing
I'd love help adding new features, so if you'd like to contribute start by cloning the repo. 

See [this page](https://docs.python.org/3/tutorial/venv.html) and follow the steps to set up a virtual python environment.
Then run `pip install -r requirements.txt`.

You'll also need to create a `.env` file with the necessary environment variables to create a PRAW Reddit instance.

To run the bot locally just run `python3 buddy.py`.
