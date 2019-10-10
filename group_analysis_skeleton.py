# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

##!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scene-cat problem set for PSY 1210 - Fall 2018

@author: Michael Mack
"""

#%% import block 

import numpy as np
import scipy as sp
import scipy.stats
import os
import shutil


#%%
# copy files from testing room folders to raw data, rename files to include
# testing room letter in the filename
#
testingrooms = ['A','B','C']
for room in testingrooms:
   file = "/Users/yachen/Documents/GitHub/ps2-Yachen-Li/" + "testingroom" + room + "/experiment_data.csv" 
   new_file = "/Users/yachen/Documents/GitHub/ps2-Yachen-Li/" + "rawdata/" + "experiment_data_" + room + ".csv"
   shutil.copyfile(file, new_file)


#%%
# read in all the data files in rawdata directory using a for loop
# columns: subject, stimulus, pairing, accuracy, median RT
#
data = np.empty((0,5))
for room in testingrooms:
   new_file = "/Users/yachen/Documents/GitHub/ps2-Yachen-Li/" + "rawdata/" + "experiment_data_" + room + ".csv"
   tmp = sp.loadtxt(new_file, delimiter = ',')
   data = np.vstack([data, tmp])
data
#%%
# calculate overall average accuracy and average median RT
#
median_RT = data[:,4]
accuracy = data[:,3]
acc_avg = np.mean(accuracy*100) # 91.48%
mrt_avg = np.mean(median_RT)   # 477.3ms


#%%
# calculate averages (accuracy & RT) split by stimulus using a for loop and an 
# if statement. (i.e., loop through the data to make a sum for each condition, 
# then divide by the number of data points going into the sum)
#
stimulus = data[:,1]
subject = data[:,0]
sumRT_word = 0
sumAcc_word = 0
sumRT_faces = 0
sumAcc_faces = 0
word_count = 0
face_count = 0
for x in range(len(subject)):
    if stimulus[x] == 1:
        word_count += 1
        sumRT_word = sumRT_word + median_RT[x]
        sumAcc_word = sumAcc_word + accuracy[x]
        
    elif stimulus[x] == 2:
        face_count += 1
        sumRT_faces = sumRT_faces + median_RT[x]
        sumAcc_faces = sumAcc_faces + accuracy[x]
        
ave_RTword = sumRT_word/word_count
ave_Accword = (sumAcc_word/word_count)*100 
ave_RTface = sumRT_faces/face_count
ave_Accface = (sumAcc_faces/face_count)*100
    

# words: 88.6%, 489.4ms   faces: 94.4%, 465.3ms


#%%
# calculate averages (accuracy & RT) split by congruency using indexing, 
# slicing, and numpy's mean function 
# wp - white/pleasant, bp - black/pleasant
# (hint: only one line of code is needed per average)
#
acc_wp = np.mean((data[data[:,2]==1])[:,3])*100 # 94.0%
acc_bp = np.mean((data[data[:,2]==2])[:,3])*100  # 88.9%
mrt_wp = np.mean((data[data[:,2]==1])[:,4]) # 469.6ms
mrt_bp = np.mean((data[data[:,2]==2])[:,4])  # 485.1ms


#%% 
# calculate average median RT for each of the four conditions
# use for loops, indexing/slicing, or both!
# (hint: might be easier to slice data into separate words and faces datasets)
## columns: subject, stimulus, pairing, accuracy, median RT
word_data = data[data[:,1]==1]
face_data = data[data[:,1]==2]

wp_wordRT = word_data[word_data[:,2] == 1][:,4]
bp_wordRT = word_data[word_data[:,2] == 2][:,4]
wp_faceRT = face_data[face_data[:,2] == 1][:,4]
bp_faceRT = face_data[face_data[:,2] == 2][:,4]


rt_wp_words = np.mean(wp_wordRT)
rt_bp_words = np.mean(bp_wordRT)
rt_wp_faces = np.mean(wp_faceRT)
rt_bp_faces = np.mean(bp_faceRT)


# words - white/pleasant: 478.4ms
# words - black/pleasant: 500.3ms
# faces - white/pleasant: 460.8ms
# faces - black/pleasant: 469.9ms


#%%        
# compare pairing conditions' effect on RT within stimulus using scipy's 
# paired-sample t-test: scipy.stats.ttest_rel()
#
import scipy.stats

t_test_word = scipy.stats.ttest_rel(wp_wordRT,bp_wordRT)
t_test_face = scipy.stats.ttest_rel(wp_faceRT,bp_faceRT)
# words: t=-5.36, p=2.19e-5
# faces: t=-2.84, p=0.0096


#%%
# print out averages and t-test results
# (hint: use the ''.format() method to create formatted strings)

#
print('\nOVERALL: {:.2f}%, {:.1f} ms'.format(100*acc_avg,mrt_avg))

#Print averages for each pairing conditions:
print('\nWords:\nMedian_RT_White: {:.1f}ms \nMedian_RT_Black: {:.1f}ms \n\nFaces:\nMedian_RT_White: {:.1f}ms \nMedian_RT_Black: {:.1f}ms'.format(rt_wp_words,rt_bp_words,rt_wp_faces,rt_bp_faces))

#Print t_test results:
print('\nWords_RT: White vs Black t-test\n {}\n\nFaces_RT: White vs Black t-test\n {}'.format(t_test_word, t_test_face))
