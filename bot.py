#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Andrew Kaplan
# Twitter Scraper 4/20/18

'''This bot will scrape Twitter for Specified Data'''

import tweepy
import time
import sys
import random
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
        for i in range(0, page):
            retweets = api.retweets_of_me(page=i)
            for status in retweets:
                item = status._json
                item = str(item) + "\n"
                outputFile.write(item)  # write to the file
        outputFile.close()  # close file
        return



    #getRetweets(2)


# get all tweets @ the account (mentions)

    def getMentions(count):
        outputFile = open(argFile, 'a')  # open file, with argument w for write
        mentions = api.retweets_of_me(count=count)
        for status in mentions:
            item = status._json
            item = "Mention: " + str(item) + "\n"
            outputFile.write(item)  # write to the file
        outputFile.close()  # close file
        return



    getMentions(5)


# count all mentions of account



# save output to file, overwrite

    #text = "THIS IS A TEST \nTHIS IS NEW LINE"
    # outputFile = open(argFile, 'w')  # open file, with argument w for write
    # outputFile.write(text)  # write to the file
    # outputFile.close()  # close file



# run script every 15 minutes
    # time.sleep((random.randint(240, 480)) * 60)  # in seconds, run code/tweet at random interval between 240-480 minutes 4-8 hours

else:
    print("Your credentials are incorrect! Check the config file")
