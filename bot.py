#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Andrew Kaplan
# Twitter Scraper 4/20/18

'''This bot will scrape Twitter for Specified Data'''

import tweepy
import time
import sys
import config as cfg  # import config file with authentication information

argFile = str(sys.argv[1])  # pass text file to command line argument

# ----------------------AUTHENTICATION------------------------------------
auth = tweepy.OAuthHandler(cfg.CONSUMER_KEY, cfg.CONSUMER_SECRET)
auth.set_access_token(cfg.ACCESS_KEY, cfg.ACCESS_SECRET)
api = tweepy.API(auth)
myUID = 2912975613  # my user identification number

if api.verify_credentials():
    print("Your credentials are O.K.")

# --------------------------------Decode JSON funcitons------------------------------------

    def _decode_list(data):
        """decodes the unicode json object returned by the api.trends_available() method"""
        rv = []
        for item in data:
            if isinstance(item, str):
                item = item.encode('utf-8')
            elif isinstance(item, list):
                item = _decode_list(item)
            elif isinstance(item, dict):
                item = _decode_dict(item)
            rv.append(item)
        return rv


    def _decode_dict(data):
        """decodes the unicode json object returned by the api.trends_available() method"""
        rv = {}
        for key, value in data.items():
            if isinstance(key, str):
                key = key.encode('utf-8')
            if isinstance(value, str):
                value = value.encode('utf-8')
            elif isinstance(value, list):
                value = _decode_list(value)
            elif isinstance(value, dict):
                value = _decode_dict(value)
            rv[key] = value
        return rv



# --------------------------------------Count Mentions--------------------------------------------------


# get all retweets from the account

    def getRetweets(page):
        outputFile = open(argFile, 'w')  # open file, with argument w for write
        try:
            for i in range(0, page):
                retweets = api.retweets_of_me(page=i)
                for status in retweets:
                    item = status._json
                    item = str(item) + "\n"
                    outputFile.write(item)  # write to the file
            outputFile.close()  # close file
        except tweepy.TweepError:
            print("Oh no! Something went wrong")
        return


# get all tweets @ the account (mentions)

    def getMentions(count):
        outputFile = open(argFile, 'w')  # open file, with argument w for write
        try:
            mentions = api.retweets_of_me(count=count)
            count = 0
            for status in mentions:
                count += 1
                item = status._json
                item = "Mention: " + str(item) + "\n"
                outputFile.write(item)  # write to the file
            outputFile.close()  # close file
        except tweepy.TweepError:
            print("Oh no! Something went wrong")
        return count



    print(getMentions(200))
    #getRetweets(2)

# run script every 15 minutes
    time.sleep(15 * 60)  # in seconds, run code/tweet at 15 min intervals

else:
    print("Your credentials are incorrect! Check the config file")
