#!/usr/bin/python3

from datetime import datetime, date, timedelta

import json

import sys

import twint
c = twint.Config()


def collect_tweets(name, articleDate, delta=30):
    name = name.lower()

    articleDate = datetime.strptime(articleDate, '%m/%d/%y')
    beginDate = (articleDate - timedelta(days=delta)).strftime("%Y-%m-%d")
    endDate = (articleDate + timedelta(days=delta)).strftime("%Y-%m-%d")

    # Collect tweets with mentions in the form of "FirstNameLastName"
    no_space_name = name.replace(' ', '')

    c.Search = name
    c.Store_csv = True
    c.Since = beginDate
    c.Until = endDate
    # CSV Fieldnames
    c.Custom = ["id", "user_id", "username", "tweet", "date", "time"]

    c.Output = name + "0.json"

    twint.run.Search(c)

    c.Search = no_space_name
    c.Output = name + "1.json"

    twint.run.Search(c)


if __name__ == '__main__':
    name = input("Name (FirstName LastName): ")
    articleDate = input("Article date (mm/dd/yy): ")
    days = input("Number of days before/after to look at: ")

    print('Collecting tweets for ' + name)
    print('Article release ~ ' + articleDate + '\n')
    if not days:
        print("Looking at tweets 30 days before and after article release")
        collect_tweets(name, articleDate)
    else:
        print("Looking at tweets " + str(days) + " days before and after article release")
        collect_tweets(name, articleDate, int(days))
