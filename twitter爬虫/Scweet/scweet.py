from Scweet.scweet import scrape
from Scweet.user import get_user_information, get_users_following, get_users_followers
data = scrape(words=['Olympics'], since="2021-10-01", until="2021-10-02",         interval=1, headless=False, display_type="Top", save_images=False, lang="en",
	resume=False, filter_replies=False, proximity=False, geocode="38.3452,-0.481006,200km")