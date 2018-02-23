# -*- coding: utf-8 -*-
"""
Created on Fri Feb 02 18:07:56 2018

@author: Trapeezey
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from timezonefinder import TimezoneFinder
from os import path
from PIL import Image
from statsmodels.graphics.mosaicplot import mosaic
tf = TimezoneFinder()
from wordcloud import WordCloud, STOPWORDS

with open('scrubbed.csv') as datafile:
    ufo = pd.read_csv(datafile, low_memory=False)

ufo = ufo.head(10) #small portion to test


#valid latitudes between 90 and -90
#valid longitudes between 180, -180
ufo['latitude'] = pd.to_numeric(ufo['latitude'], errors = 'coerce')
ufo['longitude '] = pd.to_numeric(ufo['longitude '], errors = 'coerce')

ufo = ufo[(abs(ufo['latitude']) <= 90.0)]
ufo = ufo[(abs(ufo['longitude ']) <= 180.0)]
#print(np.dtype(ufo['longitude ']))

#Add timezones
my_func = TimezoneFinder().closest_timezone_at
ufo['timezone'] = ufo.apply(lambda x: my_func(lng=x['longitude '], lat=x['latitude']), axis=1)

#Determine each time in gmt
#for x in ufo:
#   ufo['utc_dt'] = tf.astimezone(utc)

#Separate comments column to text file for wordcloud
ufo['comments'] = ufo['comments'] + ' ' 
comment_txt = ufo['comments'].astype(str).sum()
comment_txt = re.sub('[!@#$&)(/\.;]','', comment_txt)
comment_txt = re.sub('[0-9]','', comment_txt)
comment_txt = comment_txt.lower()
#print(comment_txt[0:2000])

stopwords = set(STOPWORDS)
#wc = WordCloud(max_words=1000, stopwords=stopwords, margin=10,
#               random_state=1).generate(comment_txt)

d = path.dirname("C:\Users\Leahtan\Documents\Python Scripts\ugo.png")
print(d)
mask = np.array(Image.open(path.join(d, "ugo.png")))
print(mask)
# Generate a word cloud image
wordcloud = WordCloud(stopwords = stopwords, mask = mask).generate(comment_txt)

# Display the generated image:
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()


ufo['duration (seconds)'] = ufo['duration (seconds)'].astype(str).map(lambda x: re.sub(r'\W+', '', x))
ufo['duration (seconds)'] = ufo['duration (seconds)'].astype(float)

plt.boxplot(ufo['duration (seconds)'], showfliers = False) #Set showfliers to false or else you will be engulfed by the maddness
plt.show()

plt.hist(ufo['duration (seconds)'], range = [0,3000], bins = 100)
plt.show()

#worth categorizing into short, medium, long, and extra-long encounters
#looks like the majority are short encounters

ufo['length'] = 'None'

#where duration < 15 is glimpse, duration 15 < x < 60 is short, 60 < x < 300 is med, 300 < x < 1500 is long, > 1500 is xlong

ufo.loc[ufo['duration (seconds)'] <= 15, ['length']] = 'glimpse'
ufo.loc[(ufo['duration (seconds)'] > 15) & (ufo['duration (seconds)'] <= 60), ['length']] = 'short'
ufo.loc[(ufo['duration (seconds)'] > 60) & (ufo['duration (seconds)'] <= 600), ['length']] = 'medium'
ufo.loc[(ufo['duration (seconds)'] > 600), ['length']] = 'long'

print(ufo)

ufo['length'].value_counts().plot(kind='bar')
plt.show()

print(len(ufo['shape'].unique()))
print(ufo['shape'].unique())

mosaic(ufo, ['length', 'shape'])
plt.show()

ufo['timezone'].value_counts().plot(kind = 'bar')
plt.show()

mosaic(ufo, ['timezone', 'length'])
plt.show()

mosaic(ufo, ['timezone', 'shape'])
plt.show()


ufo['year']=pd.to_numeric(ufo['datetime'].str[::-1].str[6:10].str[::-1])
ufo['date']=pd.to_datetime(ufo['datetime'].str[::-1].str[6:].str[::-1])
ufo['time'] = pd.to_datetime(ufo['datetime'].str[-5:],format= '%H:%M' ).dt.time
ufo['weekday']=ufo['date'].dt.weekday


ufo['duration (seconds)'] = ufo['duration (seconds)'].astype(str).map(lambda x: re.sub(r'\W+', '', x))
ufo['duration (seconds)'] = ufo['duration (seconds)'].astype(float)
weekdays = ufo[ufo['weekday']<5]
weekends = ufo[ufo['weekday']>=5]
weekdays.hist('year', range = [1962,2012], bins = 50)
plt.show()

ufo['workday']='No'
ufo.loc[ufo['weekday']<5, ['workday']]='Yes'

ufo.hist('weekday', bins=7)
plt.show()

print(ufo.head(10))

