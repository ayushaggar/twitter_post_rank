## Objective
> Grouping and Ranking Twitter posts

**** 
> Grouping same Twitter post appearing many times due to retweets and comments

> Ranking these groups of Twitter posts by popularity
**** 

**Constraints** :
1) Parameters in input data - tweet, created_at, author's followers_count, author's screen_name
2) No other data from twitter.com can be used

**Output**
1) Popularity Rank score with each group
2) Output file - groups are saved rank wise
3) Output file parameter - group_no, no_of_followers, no_of_tweets, engagement_time_in_seconds, max_date, min_date,       no_of_tweets_scaled, no_of_followers_scaled, engagement_time_in_seconds_scaled, rank_score, tweets
4) rank_score = no_of_tweets_scaled + no_of_followers_scaled + engagement_time_in_seconds_scaled

**Note**: Output is shown as print and saved as csv file

**** 

## Tools use 
> Python 2.7

> Main Libraries Used -
1) pandas
2) fuzzywuzzy
3) ijson
4) scikit-learn

**** 

## Installing

```sh
$ git clone https://github.com/ayushaggar/twitter_post_rank.git
$ cd twitter_post_rank
$ pip install -r requirements.txt
``` 
For Output - Task 1 and Tak 2
```sh
$ python model.py
```

****
## Various Steps in approach are -

1) Text processing techniques used -
    1) Lower Case - convert all tweets to lower case

2) Sentence Similarity
   Sentence similarity is find by considering small typos using fuzzywuzzy. It uses Levenshtein distance which is a  is a string metric for measuring the difference between two sequences. Informally, the Levenshtein distance between two words is the minimum number of single-character edits (insertions, deletions or substitutions) required to change one word into the other.

3) Cases considered -
    If 2 or 1 retweet post is there but not original tweet in data provided then also it groups and take care of if anything is added before post like RT @ or MT @ or both. capitalization, punctuation, or white-spacing is taken care of by using partial_ratio in fuzzywuzzy

    In my sentence matching, position of words should be fixed. 
    
    These are different group
    RT @ this is a task number 1
    RT @ this is a number 1 task

    These are same group
    RT @ this is a task number 1
    RT @ this is a task number 1!

4) Scaling -
    To get rank score scaling is used to bring all features at same scale

5) Popularity -
    So what will be popular group? One which has highest number of followers, group which have hughest number of retweet in data provided or the tweet which is retweet after two days too? Popularity m,ainly depend on user profile. So a combination of all is chosen? The problem gets complicated pretty quickly.