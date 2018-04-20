#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Andrew Kaplan
# Twitter Bot final project Social Software 4/28/15


# This bot selects a random location where there are trending topics,
# chooses the top ten trending topics from that location,
# then tweets lines from the raven by Edgar Allan Poe, comparing them to the trending topics,
# then follows all of it's followers back because it's lonely

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


    def _decode_list(data):
        """decodes the unicode json object returned by the api.trends_available() method"""
        rv = []
        for item in data:
            if isinstance(item, unicode):
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
        for key, value in data.iteritems():
            if isinstance(key, unicode):
                key = key.encode('utf-8')
            if isinstance(value, unicode):
                value = value.encode('utf-8')
            elif isinstance(value, list):
                value = _decode_list(value)
            elif isinstance(value, dict):
                value = _decode_dict(value)
            rv[key] = value
        return rv


def update_status(trend, place, text):
    """ update twitter status with passed in values """
    trend = trend.replace(" ", "")  # remove all spaces
    trend = trend.replace("#", "")  # remove hashtag if it exists, so I can place my own
    place = place.replace(" ", "")  # remove all spaces from string
    status = text + "...SO much better than " + " #" + trend + " in" + " #" + place
    api.update_status(status=status)
    print("\n", "Status updated!", status)  # I think this printed status is different from actual status posted


filename = open(argFile, 'r')  # open file, with argument r for read
fileLines = filename.readlines()  # line into variable fileLines
random.shuffle(fileLines)  # shuffle lines (so it doesnt start reading from the beginning everytime)
filename.close()  # close file reader


# ----------------------FOLLOW MY FOLLOWERS (a cry for friendship)-------------------------------------
def follow_all():
    followers = api.followers_ids(
        myUID)  # returns id of followers, by default of authenticated account. my info: 2912975613 (the3venthoriz0n)
    following = api.friends_ids(myUID)  # returns list of integers(uid's) of users following specified uid(me)
    print("\n", "MY FOLLOWERS: ", followers)
    # if I wanted to maintain a good following/followers ratio Id have to unfriend people
    if (len(followers) > 0) and (len(following) < len(
            followers)):  # check that followers exist and that I'm not following more people than are following me
        for follower in followers:  # iterate through followers
            api.create_friendship(follower)
            print("I just followed: ", follower)


# --------------------------------------START TRENDS CODE--------------------------------------------------


for line in fileLines:  # loop this code every loopInterval
    trendingPlaces = _decode_list(
        api.trends_available())  # convert unicode reply to normal utf-8 list, assign to variable trend
    trendPlaceDic = {}
    for item in trendingPlaces:  # add name and yahoo world id for each item in trends list to dictionary of key value pairs
        trendPlaceDic[(item['name'])] = item['woeid']
    # print "trendPlaceDic: ", trendPlaceDic

    # topTen is a list containing dictionaries as elements!
    randomPlaceName = random.choice(trendPlaceDic.keys())  # random key from trendPlaceDic
    randomWoeid = trendPlaceDic.get(
        randomPlaceName)  # choose value coresponding to key in trending places dictionary
    topTen = _decode_list(
        api.trends_place(randomWoeid))  # get top tend trends from value(woeid)/place from dictionary(trenPlaceDic)
    try:
        for item in topTen:  # iterate through items in topTen(list)
            for key in item:  # iterate through keys in the dictionary within topTen
                if key == 'trends':
                    topTenList = []
                    topTenList = item.get(key)  # fill list with values from key trends
        # print "topTenList: ", topTenList # list containing dictionaries of top ten trending for specific location
        topTenDic = {}
        for item in topTenList:
            topTenDic[(item['name'])] = item['url']
            # print "topTenDIc: ", topTenDic
    except KeyError:
        print("Uhh oh! Key Error")
    randomTrend = random.choice(topTenDic.keys())
    update_status(randomTrend, randomPlaceName, line)  # update status with line from textfile
    follow_all()  # check/follow followers
    time.sleep((random.randint(240,
                               480)) * 60)  # in seconds, run code/tweet at random interval between 240-480 minutes 4-8 hours
else:
    print("Your credentials are incorrect! Check the config file")
