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




def tokenizer(text):
       
    #Import visualization tools for LDA models
    from nltk.stem.snowball import SnowballStemmer
    import string
    
    '''
    -covert everything to lowercase
    -remove punctuations
    -remove stopwords
    -stemmer
    '''
    
    # Using alternative stopwords    
    stopwords_alt = []
    with open('/home/jpre/Documents/DTU/COVIDpolitics2021/COVIDvsPOLITICS/stopword_list.txt', 'r') as file:
        stopwords_alt = file.read().split('\n')
        
    stopwords_alt = stopwords_alt + ['time', 'state', '10','–',
                                     '1','2','3','2020','amid','de','en','day',
                                     'people','case','cases','florida','live','update','updating',
                                     'covid19', 'coronavirus','covid','virus']
       
    
    #All characters in this string will be converted to lowercase
    text = text.lower()
    
    #Removing sentence punctuations
    for punctuation_mark in string.punctuation:
        text = text.replace(punctuation_mark,'')
    
    #Creating our list of tokens
    list_of_tokens = text.split(' ')
    #Creating our cleaned tokens list 
    cleaned_tokens = []
    #Let us use a stemmer
    stemmer = SnowballStemmer(language = 'english')
    
    #Removing Stop Words in our list of tokens and any tokens that happens to be empty strings
    for token in list_of_tokens:
        if (not token in stopwords_alt) and (token != ''):
            #Stem tokens
            token_stemmed = stemmer.stem(token)
            #appending our finalized cleaned token
            cleaned_tokens.append(token_stemmed)
    
    return cleaned_tokens


def NumWords(string):
    global tokenizer
    
    return(len(tokenizer(string)))


def empty_canvas(p):
    p.xaxis.axis_label = ""
    p.yaxis.axis_label = ""
    p.xaxis.visible = False
    p.yaxis.visible = False
    p.grid.visible = False
    p.background_fill_color = 'seashell'
    p.background_fill_alpha = 1

    p.outline_line_color = None
    p.background_fill_color = None
    p.border_fill_color = None
    
    return(p)




def AddText(p_j, xy, word, fs, ci):
    

    from bokeh.models import ColumnDataSource
    from bokeh.models import Text
    
    # Adding text in the middle
    glyph_text = Text(x='x', y='y', text="text", text_baseline = 'middle', text_align = 'center',
              angle=0., text_font_size = fs, text_color=ci, text_alpha = 0.6,
              text_font_style = 'bold')
    p_j.add_glyph(ColumnDataSource(dict(x=[xy[0]], y=[xy[1]], text=[word])),glyph_text) 
    
    return(p_j)


def CreateDfRelevant(word_i, Nr, dc19, datest, impact_metric = 'num_comments'):
       
    def declare_global_word(w):
        global word_j
        word_j = w
    
    def HasCOVIDword(tokens):
        global word_j
        return(word_j in tokens)
    
    declare_global_word(word_i)

    word_j = word_i    
    titles_withword = dc19[['period',impact_metric,'title']].loc[dc19.tokens.apply(HasCOVIDword) == True]
    idx_rel = titles_withword.groupby(['period'])[impact_metric].transform(max) == titles_withword[impact_metric]
    titles_withword = titles_withword[['period','title',impact_metric]][idx_rel]
    titles_withword = titles_withword.set_index('period')
    
    titles_withword = titles_withword.dropna()
    
    i_relevant = titles_withword.num_comments.nlargest(Nr).index
    df_relevant = datest.join(titles_withword, how='outer').reset_index().iloc[i_relevant]
    
    return(df_relevant)

def CreateCalendarPlot(word_i, relevant_days, relevant_titles, width = 320, ms = 6):
    
    import numpy as np
    import datetime
    import pandas as pd
    
    from bokeh.models import ColumnDataSource, HoverTool
    from bokeh.plotting import figure
    
    TOOLTIPS_title = """
        <div>
            <div>
                <span style="font-size: 15px; font-weight: bold;">@date</span>
            </div>
            <div style="width:200px; height: 30%;">
                <span style="font-size: 13px; color: #966;">@title</span>
            </div>
        </div>
    """


    # Create a calendar matrix
    calendar_rows = 10
    calendar_cols = 37

    # Creating coordinate points
    x_calendar = [list(range(calendar_cols)) for i in range(calendar_rows)]
    y_calendar = [[i for _ in range(calendar_cols)] for i in range(calendar_rows)][::-1]

    x_calendar_flat = [item for sublist in x_calendar for item in sublist]
    y_calendar_flat = [item for sublist in y_calendar for item in sublist]

    x_calendar_flat = x_calendar_flat[:365]
    y_calendar_flat = y_calendar_flat[:365]

    # Plot attributes
    plot_height = int(np.floor(width*(calendar_rows/calendar_cols)))

    color_points = ['blue' for _ in x_calendar_flat]
    color_points[50] = 'red'

    # Selecting the relevant days
    x_calendar_flat = list(np.array(x_calendar_flat)[relevant_days])
    y_calendar_flat = list(np.array(y_calendar_flat)[relevant_days])
    color_points = list(np.array(color_points)[relevant_days])
    
    relevant_dates = []
    for rd in relevant_days:
        x = datetime.datetime.strptime(' '.join(['2020', str(rd)]), '%Y %j')
        relevant_dates.append(x.strftime('%d/%m/%Y'))
    
    df_calendar = pd.DataFrame({'x':x_calendar_flat,
                                'y':y_calendar_flat,
                                'color':color_points,
                                'date':relevant_dates,
                                'title':relevant_titles})
    source = ColumnDataSource(df_calendar.dropna())

    # Initializing figure
    p_cal = figure(plot_width=width, plot_height=plot_height, title = None, tools = '', tooltips = None,
                   x_range=(-0.5,calendar_cols-0.5), y_range = (-0.5,calendar_rows-0.5))
    # Adding relevant posts
    r_post = p_cal.square(x='x', y = 'y', source = source,
                          line_color = None, fill_color = 'color',
                          size = ms)
    # Adding hover tool
    hover1 = HoverTool(tooltips=TOOLTIPS_title,renderers = [r_post], mode = 'mouse')
    p_cal.tools.append(hover1)   

    # Adding ini and end of year
    p_cal.triangle(0, calendar_rows-1, line_color = None, fill_color = 'black', size = ms, angle = -np.pi/2)
    leftover_days = (calendar_rows*calendar_cols - 365)
    Dec31_x = calendar_cols - leftover_days
    p_cal.triangle(Dec31_x, 0, line_color = None, fill_color = 'black', size = ms, angle = np.pi/2)
    # Adding x's to mark end of array
    for d in range(leftover_days):
        p_cal.x(Dec31_x + d + 1, 0, line_color = 'grey', size = ms)

    # Other plot attributes
    p_cal.grid.visible = True
    p_cal.axis.visible = False

    p_cal.xgrid.ticker = list([x-0.5 for x in range(calendar_cols)])
    p_cal.ygrid.ticker = list([y-0.5 for y in range(calendar_cols)])
    
    p_cal.background_fill_color = "seashell"
    
    p_cal.outline_line_color = None
    p_cal.border_fill_color = None

    return(p_cal)



def flatten(l):
    return([item for sublist in l for item in sublist])

def CreateRankingPlot(dat5, controversy_topics):
    
    from scipy import interpolate
    import pandas as pd
    import numpy as np
    from bokeh.models import ColumnDataSource, TapTool, MultiLine, Text
    from bokeh.plotting import figure
    
    def add_widths(x, y, width=0.1):
        """ Adds flat parts to widths """
        new_x = []
        new_y = []
        for i,j in zip(x,y):
            new_x += [i-width, i, i+width]
            new_y += [j, j, j]
        return new_x, new_y
    

    TOOLTIPS_word = """
        <div>
            <div>
                <span style="font-size: 18px; font-weight: bold; color: #FF4500;">@word</span>
            </div>
        </div>
    """

    # Getting the series of the most used coronaword per biweek

    #dat5 = list4['rep']
    #dat5 = datest
    dat5['x'] = [x for x in range(dat5.shape[0])]

    dat5['period'] = dat5.x//14
    dat5 = dat5[['period'] + controversy_topics]
    dat5 = dat5.groupby(['period']).agg(sum).reset_index()
    dat5_melt = pd.melt(dat5, id_vars=['period'])

    idx_list = dat5_melt.groupby(['period'])['value'].apply(lambda x: x.sort_values(ascending=False)).index
    idx = [x[1] for x in idx_list]
    dat5_max = dat5_melt.loc[idx]

    rankings = []
    for p_i in dat5_max.period.unique():
        idx = dat5_max.period == p_i
        nwords = dat5_max[idx].shape[0]
        rankings.append(list(range(1,nwords+1))[::-1]) # IMPORTANT: the positions are inverted so the best are on the top (19)

    dat5_max['position'] = flatten(rankings)


    n_periods = len(dat5_max.period.unique())
    dict_multi = {'x' : [], 'y' : [], 'word' : []}

    for pos0, wordi in enumerate(controversy_topics):

        dfi = dat5_max[dat5_max.variable == wordi].sort_values('period')
        xi = dfi['period'].to_numpy()
        yi = dfi['position'].to_numpy()
        xi, yi = add_widths(xi, yi)
        xi_smooth = np.linspace(0, n_periods, num=n_periods*40, endpoint=True)
        yi_smooth = interpolate.PchipInterpolator(xi, yi)(xi_smooth)

        # I add the selection glyph because I want to fix a particular line for comparing

        dict_multi['x'].append(xi_smooth)
        dict_multi['y'].append(yi_smooth)
        dict_multi['word'].append(wordi)



    words_0 = dat5_max[dat5_max.period == 0].variable.tolist()[::-1]

    source = ColumnDataSource(dict_multi)

    p6 = figure(plot_width = 950, plot_height = 360, tools = '', y_range = (0,19.5), x_range = (-3, 26),
                tooltips=TOOLTIPS_word)
    ml = p6.multi_line(xs='x', ys='y',line_width=1, line_color='skyblue',line_alpha=0.3,
                 hover_line_color='orangered', hover_line_alpha=1.0,
                 source=source)
    
    ml.hover_glyph.line_width=2.5
#    ml.tap_glyph.line_color='red'

# Adding selection tool
    selected_line = MultiLine(line_width=2.5, line_color='#f4aa42')
    ml.selection_glyph = selected_line
    tap_line = TapTool(renderers=[ml])
    p6.add_tools(tap_line)

    p6 = empty_canvas(p6)

    text1 = Text(x='x', y='y', text="text", text_font_size = '14pt', y_offset = 0, x_offset = 0, 
                  text_color = 'blue', text_baseline = 'middle', text_align = 'right')

    p6.add_glyph(ColumnDataSource(dict(x=[-0.2 for _ in words_0],
                                       y=[h + 1 for h in range(len(words_0))],
                                       text=words_0)), text1)

    return(p6,dict_multi)





# def GenerateTimelinePLot(i, indx, titles_withword, sizeplot = (320,80), TOOLS = 'box_zoom,reset'):
    
#     global datest, dc19, word_i
    
#     impact_metric = 'num_comments'
    
#     smooth_i = '_'.join([i,'ks'])
    
#     max_freq = 1.5*max(datest[i])
#     min_freq = -0.5*max_freq
#     med_freq = (max_freq + min_freq)/2
    
#     min_x = -5
#     max_x = 370
    
#     p = figure(plot_width= sizeplot[0], plot_height=sizeplot[1], title = None,
#                x_range=(min_x,max_x), y_range = (min_freq,max_freq), tools = TOOLS)
    
   
#     # Selecting the Nr relevant posts
#     Nr = 19
#     bsl = med_freq
#     i_relevant = titles_withword.num_comments.nlargest(Nr).index
#     df_relevant = datest.join(titles_withword, how='outer').reset_index().iloc[i_relevant]
#     df_relevant['baseline'] = bsl
#     source_posts = ColumnDataSource(data= df_relevant)
    
#     glyph_text = Text(x='x', y='y', text="text", text_baseline = 'middle', text_align = 'center',
#                       angle=0., text_font_size = '42pt', text_color=c3, text_alpha = 0.6,
#                       text_font_style = 'bold')
    
    
#     # Vertical line
#     event_lines = []
#     # 7 / 7-Jan / Chinese authorities report coronavirus
#     # 20 / 20-Jan / First reported COVID case in the US
#     # 24 / 24-Jan / First reported COVID case in the Europe
#     # 73 / 13-Mar / Major lockdown in Europe
#     # 106 / 15-Apr / Europe surpasses 1mil death
#     # 285 / 11-Oct / Trump test positive    
#     # 308 / 13-Nov / US elections
#     # 343 / 8-Dec / First person gets vaccinated
#     Events = [7,20,24,73,106,285,308,343]
#     for event in Events:
#         event_lines.append(Span(location=event, dimension='height', line_color='green',
#                                 line_width=0.5, line_dash = 'dotted', level = 'underlay'))
#         p.renderers.extend(event_lines)

  
#     # Timeline
#     p.line(x=[1,365],y=[bsl,bsl], line_color = c3, line_width = 2)
#     p.scatter(x=[1,365],y=[bsl,bsl], color = c3, line_color = c3, line_width = 2, angle =0)
     
#     # Relevant posts
#     r = p.scatter(y='baseline', x='index', color=c1, source=source_posts,
#                   alpha = 1, size=16, marker = 'diamond', line_color = c3, line_width = 2)
    
#     # curtain rectangle
#     r_rect = p.rect(x=-100, y = -100, height = 1000, width = 1000, fill_color = 'white', fill_alpha = 1)
        
#     r_text = p.add_glyph(ColumnDataSource(dict(x=[30*6], y=[med_freq], text=[i])), glyph_text) 
    
    
#     hover1 = HoverTool(tooltips=TOOLTIPS_title,renderers = [r], mode = 'vline')
#     hover2 = HoverTool(tooltips = None, renderers = [r_text], mode = 'mouse')
#     hover3 = HoverTool(tooltips = None,renderers = [r_rect], mode = 'mouse')
    
#     p.tools.append(hover1)
#     p.tools.append(hover2)
#     p.tools.append(hover3)

#     selected_rect = Rect(fill_alpha=0., fill_color = 'white')
#     selected_text = Text(text_alpha=0.3, text_font_size = '42pt', text_color = c3,
#                          text_font_style = 'bold', text_baseline = 'middle', text_align = 'center')

#     # I add the selection glyph because I want to fix a particular line for comparing
#     r_text.hover_glyph = selected_text
#     r_rect.hover_glyph = selected_rect
    
#     # Adjusting plot parameters
#     #p.x_range.range_padding = 0.05
#     p.xaxis.axis_label = ""
#     p.yaxis.axis_label = ""
#     p.xaxis.visible = False
#     p.yaxis.visible = False
#     p.yaxis.axis_line_width = 1
#     p.yaxis.ticker = [0,max_freq]
#     p.grid.visible = False
#     p.background_fill_alpha = 1
    
#     p.outline_line_color = None
#     p.border_fill_color = None
    
#     p.background_fill_color = "seashell"
        
#     return p