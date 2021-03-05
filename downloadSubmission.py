# https://pushshift.io/api-parameters/
# https://www.reddit.com/r/pushshift/comments/8h31ei/documentation_pushshift_api_v40_partial/


#  all the replies to a specific comment
# https://www.reddit.com/r/pushshift/comments/a7zzhn/using_parent_id_to_search_for_comments/

import pandas as pd
from psaw import PushshiftAPI
import requests
import os
import praw
import sys
import datetime

from functions import CreateLinkPushshift

###############################################################################
my_client_id = '74CBTlXRo31zAg'
my_client_secret = 'qvpDreHLSY2-QicrieFmc_R-NfM'
my_user_agent = 'newVisualization'
reddit = praw.Reddit(client_id = my_client_id,
                     client_secret = my_client_secret,
                     user_agent = my_user_agent)

api = PushshiftAPI(reddit)

 # Defining folder paths
parent_folder = '/home/jpre/Documents/DTU/COVIDpolitics/'
data_folder = parent_folder + 'data/'
posts_folder = data_folder + 'posts/'
element_folder = posts_folder + 'submissions/'

 # Reading relevant lists 
# covid_posts_id = pd.read_csv(posts_folder + 'covid_id_posts.txt', names=['id'], header=None).id.tolist()
# us_states_subreddits = pd.read_csv(parent_folder + 'us_states_subreddits.txt', names=['id'], header=None).id.tolist()
# us_states_subreddits = [x[2:] for x in us_states_subreddits]

BODYTITLE_DICT = {'comment' : 'body', 'submission' : 'title'}

# Defining the date range
# %H:%M:%S %d/%m/%Y
# datetime.datetime.fromtimestamp(1582260266)

first_t = datetime.datetime.strptime(('{0}:{1}:{2} {3}/{4}/{5}').format(0,0,0,1,1,2020), '%H:%M:%S %d/%m/%Y')
last_t = datetime.datetime.strptime(('{0}:{1}:{2} {3}/{4}/{5}').format(0,0,0,1,2,2021), '%H:%M:%S %d/%m/%Y')


delta_t = 60*60*12
range_of_t = range(int(first_t.timestamp()),int(last_t.timestamp()), delta_t)

###############################################################################

 # Defining search
type_of_search = 'submission' # there are three main options: comment, submission, subreddit
# https://pushshift.io/api-parameters/
filters = {}


fields = ['created_utc',
          'author',
          'subreddit',
          'score',
          'id',
          'title',
          'num_comments',
          'num_crossposts',
          'subreddit_subscribers',
          'author_flair_text',
          'author_flair_type']


b_t = 'title'

########################################
########################################
istest = False
########################################
########################################

# Name of the file where to store all data
for foldername in ['coronavirus']:
    
    filters['subreddit'] = foldername
    
    # Creating a folder where to store the data
    file_folder = element_folder + foldername + '/'
    
    if istest:
        file_folder = file_folder + 'test/'
    
    if not os.path.exists(file_folder):
        os.makedirs(file_folder)
    
    # Creating main files
    file_elements = open(file_folder + 'data1' +'.txt', 'w')
    file_metadata_elements = open(file_folder + 'metadata1' +'.txt', 'w')

    for day_i in range_of_t:
        
        # To find comments from a specific post: filters['link_id'] = post_id
        filters['after'] = day_i
        filters['before'] = filters['after'] + delta_t
        
        search_link = CreateLinkPushshift(type_of_search,
                                          search_criteria = filters,
                                          fields_to_retrieve = fields + [b_t],
                                          N = 100)
        
        #download all comments from post
        # "https://api.pushshift.io/reddit/comment/search/?link_id=bc99el"
    
        try:
            # Get the data from Pushshift as JSON.
            retrieved_data = requests.get(search_link)
            returned_elements = retrieved_data.json()['data']
            
            for element in returned_elements:
                
                # element is a dictionary      
                element_info = '\t'.join([str(element[field]) for field in fields]) + '\n'
            
                file_elements.write(element[b_t] + '_/zvzvzvzv/EndOfElement\yxyxyxy\_')
                file_metadata_elements.write(element_info)
        except:
            continue
                    
    file_elements.close()
    file_metadata_elements.close()


    
    
    
    
    
    
    
    