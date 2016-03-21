
# coding: utf-8

# # Reading a subset of the provided dataset from last.fm

# Tag-cleanining: only keep tags with weight 100 and clean them.

import re
tags = {}
for line in open('dataShort.csv', 'r'):
    line = line.strip().split(',')
    mbid, track_tags = line[0], line[1:]
    if track_tags == []: continue # ignore tracks with no tags
    tags[mbid] = []
    for i in range(len(track_tags)/2):
        if track_tags[i*2+1]>'0':
            tag = track_tags[i*2]
            tag = tag.lower()
            tag = re.sub(r'[^a-zA-Z0-9]','', tag) # remove non-alphanumeric symbols
            if tag != '':
                tags[mbid].append(tag)
print "Number of dataset elements: ",len(tags),"\n"

# let's see what we've got: 10 first values
for mbid in tags.keys()[:10]: 
    print "MusicBrainz ID ", mbid," Tags ", tags[mbid]


# Tag histogram in order to see which are the most frequent tags.

all_tags = []
for mbid, track_tags in tags.iteritems():
    all_tags += track_tags
print "Total different tags:", len(set(all_tags))

# create a tag histogram
tags_hist = {}
for t in all_tags:
    tags_hist.setdefault(t, 0)
    tags_hist[t] += 1

# VERY slow: 
tags_hist = dict((t, all_tags.count(t)) for t in all_tags)

# sort tags by occurrence frequency
import operator
sorted_tags_hist = sorted(tags_hist.items(), key=operator.itemgetter(1), reverse=True)

print "Top 100 tags:"
print sorted_tags_hist[:100]


# # Dataset creation based on decade tags

# Searching for tags related to decade: dictionary creation.

new_dict = {}
for i in range(len(tags.keys())):
    tags_per_row = tags[tags.keys()[i]]
    for j in tags_per_row:
        if j =='mellow':
            new_dict[tags.keys()[i]] = 'mellow'     # Crear diccionario

        if j =='love':
            new_dict[tags.keys()[i]] = 'love'
            
        if j =='sad':
            new_dict[tags.keys()[i]] = 'sad'
            
        if j =='psychedelic':
            if tags.keys()[i] == "c24451ea-b70d-46b9-99fb-93e43ffdf4fa":
                continue
            else:
                new_dict[tags.keys()[i]] = 'psychedelic'
                
print len(new_dict)


# Dictionary to CSV file. This CSV will be evaluated on AcousticBrainz.

import csv
writer = csv.writer(open('dictMood.csv','w'))
for key, value in new_dict.items():
    key = key.replace('"', '')
    writer.writerow([key,value])
    print key, value



