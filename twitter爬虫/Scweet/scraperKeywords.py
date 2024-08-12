from Scweet.scweet import scrape
import json
from Scweet.user import get_user_information, get_users_following, get_users_followers, get_users_posts

# scrape top tweets with the words 'covid','covid19' and without replies. the process is slower as the interval is
# smaller (choose an interval that can divide the period of time betwee, start and max date) scrape english top
# tweets geolocated less than 200 km from Alicante (Spain) Lat=38.3452, Long=-0.481006.


# scrape top tweets of with the hashtag #covid19, in proximity and without replies. the process is slower as the
# interval is smaller (choose an interval that can divide the period of time betwee, start and max date)
#  data = scrape(hashtag="bitcoin", since="2022-3-05", until="2022-4-14", from_account=None, interval=1,
#                headless=True, display_type="Top", save_images=False,
#                resume=False, filter_replies=True, proximity=True)
#
# # Get the main information of a given list of users
# # These users belongs to my following.
#
users = ['nagouzil', '@yassineaitjeddi', 'TahaAlamIdrissi',
         '@Nabila_Gl', 'geceeekusuu', '@pabu232', '@av_ahmet', '@x_born_to_die_x']
#
# this function return a list that contains :
# ["nb of following","nb of followers", "join date", "birthdate", "location", "website", "description"]
#
users_info = get_user_information(users, headless=True)
#
# # Get followers and following of a given list of users Enter your username and password in .env file. I recommande
# # you dont use your main account. Increase wait argument to avoid banning your account and maximise the crawling
# # process if the internet is slow. I used 1 and it's safe.
#
# # set your .env file with SCWEET_EMAIL, SCWEET_USERNAME and SCWEET_PASSWORD variables and provide its path
env_path = ".env"
#
following = get_users_following(users=["@violafutong"], env=env_path, verbose=0, headless=True, wait=2, limit=50, file_path=None)

posts = get_users_posts(user=["@violafutong"], env=env_path,  headless=True, wait=2, limit=50)

followers = get_users_followers(users=users, env=env_path, verbose=0, headless=True, wait=1, limit=50, file_path=None)