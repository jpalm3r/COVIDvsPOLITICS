def CovidRelated(title_string):
    title_string = title_string.lower()
    covid_tags = ['coronavirus', 'covid', 'quarantine','c19','c-19', 'wuhan', 'fauci', 'mask',
                  'pandemic', 'virus', 'epidemic', 'lockdown','sars', 'CoV-2','corona','infection']
    covid_in_title = [x in title_string for x in covid_tags]
    return int(sum(covid_in_title) > 0)


def ReadSubreddit(sr, agg_step = 'week', year = 2020):

    import pandas as pd

    parent_folder = '/home/jpre/Documents/DTU/COVIDpolitics2021/COVIDvsPOLITICS/'
    data0_folder = parent_folder + 'data/'
    comment_folder = data0_folder + 'posts/comments/'
    data_folder = comment_folder + sr + '/'
    
    if year != 2020:
        data_folder = data_folder = comment_folder + sr + '/' + str(year) + '/'

    metadf1_column_titles = ['created_utc',
                             'retrieved_on',
                             'author',
                             'subreddit',
                             'score',
                             'id',
                             'parent_id',
                             'link_id',
                             'author_flair_text',
                             'author_flair_type',
                             'total_awards_received']

    #time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(praw_submission.created_utc))
    awkward_sep = '_/zvzvzvzv/EndOfElement\yxyxyxy\_'

    # creating empty elements
    metadat0 = pd.DataFrame(columns = metadf1_column_titles)

    titles_file_path = data_folder + 'data1.txt'
    meta_file_path = data_folder + 'metadata1.txt'

    #df1_column_titles = ['title']
    with open(titles_file_path, 'r') as file:
        all_comments = file.read().replace('\n', '')

    comment_list = all_comments.split(awkward_sep)[:-1] # removing the last one because it is empty

    metadat0 = pd.read_csv(meta_file_path, sep='\t', header = None, names = metadf1_column_titles)
    metadat0['TimeStamp'] = pd.to_datetime(metadat0['created_utc'], unit = 's')
    metadat0['TimeStamp_retrieved'] = pd.to_datetime(metadat0['retrieved_on'], unit = 's')
    metadat0['deltaT'] = (metadat0['TimeStamp_retrieved'].astype('int') - metadat0['TimeStamp'].astype('int'))/1e9

    metadat0[['pre_pID', 'pID']] = metadat0['parent_id'].str.split('_',expand=True)

    metadat0['date'] = metadat0['TimeStamp'].dt.date
    metadat0['1dayafter'] = metadat0['TimeStamp'] + pd.DateOffset(1)

    #metadat0['period'] = metadat0['TimeStamp'].astype('int')//(1e9*60*60*24*7)
    metadat0['week'] = metadat0['TimeStamp'].dt.week
    metadat0['day'] = metadat0['TimeStamp'].dt.dayofyear
    metadat0['month'] = metadat0['TimeStamp'].dt.month
    
    metadat0['period'] = metadat0[agg_step]

    metadat0['comments'] = comment_list

    dat1 = metadat0[metadat0['TimeStamp'].dt.year.isin([year])]
    dat1['hour'] = dat1['TimeStamp'].dt.hour
    dat1['hour_retrieved'] = dat1['TimeStamp_retrieved'].dt.hour
    
    return(dat1)
