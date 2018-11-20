import requests
import re
from bs4 import BeautifulSoup
import pyttsx3
import os
import numpy as np
import pandas as pd

# get the data
data = requests.get('https://www.dailywire.com/')

# load the data into bs4
soup = BeautifulSoup(data.text, 'html.parser')

#print(soup)

data = []
titles = []

for article in soup.find_all('article'):
    for h2 in article.find_all('h2'):
        #print(a)
        values = h2
        data.append(values)
    for a in article.find_all('a'):
        title = a.text
        titles.append(title)


print(data)

#print(titles)

#print(titles[1:len(titles):2])

justTitles = titles[1:len(titles):2]

i = 0
titlesString = ""
for t in range(0,len(justTitles)):
    i += 1
    titlesString = titlesString + "Article Number " + str(i) + ": " + justTitles[t] + ".\n"

print()
print(titlesString)

whichArticle = int(input("Which article would you like to listen to? (Please enter just the integer) "))
whichArticle = whichArticle - 1

#####################################################
# work in progress

print(data[whichArticle])

news = re.findall(r'href=".*"', str(data[whichArticle]))

print(news)

news = re.findall(r'/.*"', str(news))

news = str(news)
#news = news[whichArticle][0:(len(news[whichArticle])-1)]
news = news[2:(len(news)-3)]
print(news)


#############################################################
data = requests.get('https://www.dailywire.com' + news)

soup = BeautifulSoup(data.text, 'html.parser')

articletext = ""
for body in soup.find_all('div', { 'class': 'field-body' }):
    for p in body.find_all('p'):
        articletext = articletext + " " + p.text

data = []
div = soup.find('div', { 'class': 'field-body' })
for p in div.find_all('p'):
    values = p.text
    data.append(values)

#print(data)

#----------------------------------------------
# Estimated Time to Read article
wordCount = len(articletext.split())
#wordsPerMinute = 80
#estimatedMinutes = wordCount / wordsPerMinute

print("This article is " + str(wordCount) + " words.")


from gtts import gTTS

filename = str(input("What would you like to name the file (not including .mp3 extension) "))

#filename = str(re.findall(r'/.*(?!/)', news))
#print(filename)
#filename = filename[3:len(filename)-3]

print(filename + '.mp3')

tts = gTTS(articletext)
tts.save(filename + '.mp3')

#engine = pyttsx3.init('espeak')
#import pyttsx3
#engine = pyttsx3.init()
#engine.say(articletext)
#engine.setProperty('rate',wordsPerMinute)  #120 words per minute
#engine.setProperty('volume',0.9)
#engine.runAndWait()

#################################################

cwd = os.getcwd()

df = pd.DataFrame(data)
df.to_csv(cwd + '/' + filename + "Text.csv")

articleTextCSV = cwd + '/' + filename + "Text.csv"


################################################################################
# Text Analysis In R

import rpy2.robjects as ro

ro.r('setwd("~/Projects/NewsApp")')

ro.r('library(tidytext)')
ro.r('library(dplyr)')
ro.r('library(tidyr)')

ro.r('text_df <- read.csv("' + articleTextCSV + '", stringsAsFactors = FALSE)')
#text_df <- read.csv("articletext.csv", stringsAsFactors = FALSE)

ro.r('colnames(text_df) <- c("paragraph", "text")')
#colnames(text_df) <- c('paragraph', 'text')

ro.r('text_df <- text_df %>% unnest_tokens(word, text)')
#text_df <- text_df %>% unnest_tokens(word, text)
ro.r('data(stop_words)')
#data(stop_words)
ro.r('text_df <- text_df %>% anti_join(stop_words)')
#text_df <- text_df %>% anti_join(stop_words)
ro.r('library(wordcloud)')
#library(wordcloud)

ro.r('text_df %>% count(word) %>% with(wordcloud(word, n))')
ro.r('png(filename="~/Projects/NewsApp/' + filename + 'Wordcloud.png")')
#png(filename="~/Projects/NewsApp/articlewordcloud.png")
ro.r('text_df %>% count(word) %>% with(wordcloud(word, n))')
#text_df %>% count(word) %>% with(wordcloud(word, n))
ro.r('dev.off()')
#dev.off()
