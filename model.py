import os
import pandas as pd
import ijson


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





def main():
    # list down all files in folder
    data_list = os.listdir("data")

    # Handle if no file in data folder
    if len(data_list) == 0:
        print 'no file'
        return

    # importing data
    data_df = tweets_to_df(data_list)


main()
