# -*- coding: utf-8 -*- #
'''
Created on 29 mars 2011

@author: dfrancois
'''
import re

def normalize(filename):
    ""
    try:
        filename =  str(filename)
    except TypeError:
        print "filename is not a string !!"
    
    #normalize space characters
    filename = re.compile("(\s|_|%20)+").sub("_",filename)
    filename = filename.capitalize()
    return filename

def compare_tags(filenames,progressMeter):
    """ Compares the tags of the files and returns the indexes of the tags considered as 
        identical. the series of duplicates of the same element are separated by a "$" element.
    """
    
    tags_infos = []
    duplicate_tags = []
    i = 1.0
    
    progressMeter.set(value=0,text="Scanning library for tags...")
    for file in filenames:
        if not isinstance(file["tags_info"],str):
            if ("artist" and "title") in file["tags_info"].keys():
                tags_infos.append([file["tags_info"],filenames.index(file)])
                
    many_tags = len(tags_infos)
    for tag in tags_infos:
        progressMeter.set(value = i/many_tags, text="Detecting duplicate tags information...")
        for tag2 in tags_infos:
            if tag[1] != tag2[1]:
                if (tag[0]["artist"] == tag2[0]["artist"] 
                    and tag[0]["title"] == tag2[0]["title"]):
                        if tag[1] not in duplicate_tags:
                            duplicate_tags.append("$")
                            duplicate_tags.append(tag[1])
                        if tag2[1] not in duplicate_tags:
                            duplicate_tags.append(tag2[1])
        i = i + 1
                            
    return duplicate_tags
    
def compare(filenames,progressMeter):
    """ Compares the list of filenames and returns the indexes of the duplicated elements,
        the series of duplicates of the same element are separated by a "$" element.
    """
    normalized = []
    duplicate_filenames_indexes = []
    j = 1.0
    
    # normalize the filenames and keep the index in the original list of the element.
    for file in filenames:
        progressMeter.set(value=0,text="Normalizing filenames...")
        normalized.append([normalize(file["sys_info"][1]),filenames.index(file)])
        
    #sorts the list to put similar filenames one after another
    normalized.sort()
    many_files = len(normalized)-1
    #check if two following elements in the sorted liste have the same normalized filename.
    for i in range(many_files):
        progressMeter.set(value= j/many_files,text="Scanning library for duplicates filenames...")
        if normalized[i][0] == normalized[i+1][0]:
            #the first of the two elements tested isnt already in the returned list
            #insert a separator element in the returned list.
            if not (normalized[i][1] in duplicate_filenames_indexes):
                duplicate_filenames_indexes.append("$")
                duplicate_filenames_indexes.append(normalized[i][1])   
            duplicate_filenames_indexes.append(normalized[i+1][1])
        j = j + 1
    print j
    return duplicate_filenames_indexes