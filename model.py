import os
import pandas as pd
import ijson
from fuzzywuzzy import fuzz
from sklearn.preprocessing import MinMaxScaler


def tweets_to_df(data_list):
    # importing data
    # data intialization
    data = []
    for filename in data_list:
        with open('data/' + filename, 'r') as f:
            print filename
            # ijson will iteratively parse the json file work with large files
            objects = ijson.items(f, 'tweets.item')  # extract all items
            rows = list(objects)
            for row in rows:
                selected_row = []
                selected_row = [
                    row.get(
                        'text', {}), row.get(
                        'created_at', {}), row.get(
                        'author', {}).get('screen_name'), row.get(
                        'author', {}).get('followers_count')]
                data.append(selected_row)

    # using data frame
    df = pd.DataFrame(data)
    df.columns = ['text', 'created_at', 'screen_name', 'followers_count']
    # conveted to date
    df['created_at'] = pd.to_datetime(df['created_at'], unit='s')

    # converted tweet to lower case
    df['text'] = map(lambda x: x.lower(), df['text'])

    return df


def assign_group(df):
    # assigning group number to each tweet
    df['group_no'] = 0
    groups = list()  # groups of names with distance > 90 in fuzzywuzzy

    for index, row in df.iterrows():
        # 
        doc = row['text']
        for g in groups:
            if all(fuzz.partial_ratio(doc, w) > 90 for w in g):
                g.append(doc)
                df.at[index, 'group_no'] = groups.index(g) + 1
                break
        else:  # if all distance < 90 new group is made
            groups.append([doc, ])
            df.at[index, 'group_no'] = groups.index([doc, ]) + 1

    return [df, groups]


def main():
    # list down all files in folder
    data_list = os.listdir("data")

    # Handle if no file in data folder
    if len(data_list) == 0:
        print 'no file'
        return

    # importing data
    data_df = tweets_to_df(data_list)

    # assigning group to tweets
    [tweet_df, groups] = assign_group(data_df)

    # group tweets and finding stats
    # aggregation function
    aggregation_functions = {
        'followers_count': {
            'no_of_followers': 'sum',
            'no_of_tweets': 'count'},
        'created_at': {
            'max_date': 'max',
            'min_date': 'min',
            'engagement_time_in_seconds': lambda x: (
                max(x) -
                min(x)).total_seconds()}}
    date_accu = tweet_df.groupby(['group_no']).aggregate(aggregation_functions)
    date_accu.columns = date_accu.columns.get_level_values(1)
    date_accu.reset_index(inplace=True)

    # scaling values between 0 and 1
    scaler = MinMaxScaler()
    date_accu['no_of_tweets_scaled'] = scaler.fit_transform(
        date_accu['no_of_tweets'].values.reshape(-1, 1))
    date_accu['no_of_followers_scaled'] = scaler.fit_transform(
        date_accu['no_of_followers'].values.reshape(-1, 1))
    date_accu['engagement_time_in_seconds_scaled'] = scaler.fit_transform(
        date_accu['engagement_time_in_seconds'].values.reshape(-1, 1))
    date_accu['rank_score'] = date_accu.apply(
        lambda x: x['no_of_tweets_scaled'] +
        x['no_of_followers_scaled'] +
        x['engagement_time_in_seconds_scaled'],
        axis=1)
    date_accu = date_accu.sort_values(by='rank_score', ascending=False)
    date_accu['tweets'] = date_accu.apply(
        lambda x: groups[x['group_no'] - 1], axis=1)
    print date_accu

    # export to csv
    if os.path.isdir('result') is False:
        os.makedirs('result')
    date_accu.to_csv(
        'result/groups.csv',
        sep='\t',
        encoding='utf-8',
        index=False)


main()
