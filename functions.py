def CreateLinkPushshift(type_of_search, N = 500, search_criteria = {}, fields_to_retrieve = []):
    
    # This is an example to know the fields that can be retrieved
    DICT_OF_FIELDS_COMMENTS = {
        "all_awardings": [],
        "associated_award": None,
        "author": "AutoModerator",
        "author_flair_background_color": None,
        "author_flair_css_class": None,
        "author_flair_richtext": [],
        "author_flair_template_id": None,
        "author_flair_text": None,
        "author_flair_text_color": None,
        "author_flair_type": "text",
        "author_fullname": "t2_6l4z3",
        "author_patreon_flair": False,
        "author_premium": True,
        "awarders": [],
        "body": "questions or concerns",
        "collapsed_because_crowd_control": None,
        "comment_type": None,
        "created_utc": 1600842225,
        "distinguished": "moderator",
        "gildings": {},
        "id": "g6an0is",
        "is_submitter": False,
        "link_id": "t3_iy4wh7",
        "locked": False,
        "no_follow": True,
        "parent_id": "t3_iy4wh7",
        "permalink": "/r/askscience/comments/iy4wh7/how_to_read_a_zippers_influence_to_a_bags_surface/g6an0is/",
        "retrieved_on": 1600842236,
        "score": 1,
        "send_replies": False,
        "stickied": False,
        "subreddit": "askscience",
        "subreddit_id": "t5_2qm4e",
        "top_awarded_type": None,
        "total_awards_received": 0,
        "treatment_tags": []
        }
        
        
    DICT_OF_FIELDS_SUBMISSIONS = {
        "author": "Troy_Llyod",
        "author_flair_css_class": None,
        "author_flair_richtext": [],
        "author_flair_text": None,
        "author_flair_type": "text",
        "can_mod_post": False,
        "contest_mode": False,
        "created_utc": 1530403401,
        "domain": "foxnews.com",
        "full_link": "https://www.reddit.com/r/news/comments/8v62g4/restaurant_manager_fired_after_refusing_to_serve/",
        "gilded": 0,
        "id": "8v62g4",
        "is_crosspostable": True,
        "is_original_content": False,
        "is_reddit_media_domain": False,
        "is_self": False,
        "is_video": False,
        "link_flair_richtext": [],
        "link_flair_text_color": "dark",
        "link_flair_type": "text",
        "locked": False,
        "media_only": False,
        "no_follow": True,
        "num_comments": 0,
        "num_crossposts": 0,
        "over_18": False,
        "parent_whitelist_status": "all_ads",
        "permalink": "/r/news/comments/8v62g4/restaurant_manager_fired_after_refusing_to_serve/",
        "pinned": False,
        "pwls": 6,
        "retrieved_on": 1530403402,
        "rte_mode": "markdown",
        "score": 0,
        "selftext": "",
        "send_replies": True,
        "spoiler": False,
        "stickied": False,
        "subreddit": "news",
        "subreddit_id": "t5_2qh3l",
        "subreddit_subscribers": 16209530,
        "subreddit_type": "public",
        "thumbnail": "default",
        "title": "Restaurant manager fired after refusing to serve customer wearing MAGA hat",
        "url": "http://www.foxnews.com/world/2018/06/30/restaurant-manager-fired-after-refusing-to-serve-customer-wearing-maga-hat.html", 
        "whitelist_status": "all_ads",
        "wls": 6
        }
   
   
    url_0 = 'https://api.pushshift.io/reddit/' + type_of_search +'/search/?'
    
    # Defining the fields to limit the search
    fields = '' # if fields_to_retrieve is empty, the api will download ALL fields
    if(len(fields_to_retrieve)>0):
        fields = '&filter=' + ','.join(fields_to_retrieve)
        
    # Sorting criteria
    sorting = ('&sort_type={0}&sort={1}').format('score', 'desc')

    # Defining the criteria to look for 
    # {'subreddit' : 'politics'}
    search_for = ''
    for x,y in zip(search_criteria.keys(), search_criteria.values()):
        # Defining the filters for the search
        search_for += ('&{0}={1}').format(str(x),str(y))

    search_link = url_0 + '&user_removed=false&mod_removed=false' + '&size=' + str(N) + sorting + fields + search_for

    return(search_link)

def StoreDataPushshift(data, folder, sep = '\t'):

    
    
    return(None)