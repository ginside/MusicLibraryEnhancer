# -*- coding: utf-8 -*- #
'''
Created on 29 mars 2011

@author: dfrancois
'''
import re
import __builtin__

def normalize(filename):
    ""
    try:
        filename =  str(filename)
    except TypeError:
        print "filename is not a string !!"
    
    #normalize space characters
    filename = re.compile("((\s|_|%20)+)|(_+)").sub("_",filename)
    #capitalize everything
    filename = filename.lower()
    
    return filename

def hash_words(filename):
    """Hashes words and numbers contained in filenames
    
    """
    try:
        filename =  str(filename[0])
    except TypeError:
        print "filename is not a string !!"
    numbers_in_filename = re.findall("(\d+)",filename)
    words_in_filename = re.findall("[a-zA-Z]+",filename)
    numbers_in_filename.sort()
    words_in_filename.sort()
    hashed = hash("".join(numbers_in_filename).join(words_in_filename))
    
    #if "foules" in filename:
    #    print "HASH "+filename+" LETS GO !!"
    #    print numbers_in_filename
    #    print words_in_filename
    #    print 
    #    print str(hashed)
    return hashed
    
def compare_tags(filenames,progressMeter):
    """ Compares the tags of the files and returns the indexes of the tags considered as 
        identical. 
        The series of duplicates of the same element are separated by a "$" element.
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
    hashed_tags = []
    for tag in tags_infos:
        progressMeter.set(value = i/many_tags,
                           text="Scanning tags information...")
        i = i + 1
        str_tag = ""
        tag_keys = ['artist','title','track','album','...']
        
        for key in tag_keys:
            if tag[0].has_key(key):
                str_tag += " " + str(tag[0][key])
        hashed_tags.append([hash(str_tag),tag[1]])
        
    hashed_tags.sort()

    for i in range(many_tags-1):
        progressMeter.set(value = i/many_tags,
                           text="Detecting duplicate tags information...")
        
        if hashed_tags[i][0] == hashed_tags[i+1][0]:
            if hashed_tags[i][1] not in duplicate_tags:
                duplicate_tags.append("$")
                duplicate_tags.append(hashed_tags[i][1])
            if hashed_tags[i+1][1] not in duplicate_tags:
                duplicate_tags.append(hashed_tags[i+1][1])
    
    return duplicate_tags
    
def compare(filenames,progressMeter):
    """ Compares the list of filenames and returns the indexes of the duplicated 
        elements, the series of duplicates of the same element are separated by 
        a "$" element.
        Also compares the hashed lists of words and numbers contained in
        the filename to find duplicates.
    """
    duplicate_filenames_indexes,normalized,hashes = [],[],[]
    j = 1.0
    
    # normalize the filenames and keep the index in the original list of the element.
    # also hashes words contained in the filename
    for file in filenames:
        progressMeter.set(value=0,text="Normalizing filenames...")
        
        normalized.append([normalize(file["sys_info"][1]),filenames.index(file)])
        hashes.append([hash_words(normalized[-1]),filenames.index(file)])
    #sorts the list to put similar filenames one after another
    normalized.sort()
    hashes.sort()
    many_files = len(hashes)-1
    #check if two following elements in the sorted list have the same normalized filename.
    for i in range(many_files):
        if i%10 == 0:
            progressMeter.set(value= j/many_files,text=
                          "Scanning library for duplicates filenames...")
        j = j + 1
        if normalized[i][0] == normalized[i+1][0]:
            #the first of the two elements tested isnt already in the returned list
            #insert a separator element in the returned list.
            if not (normalized[i][1] in duplicate_filenames_indexes):
                duplicate_filenames_indexes.append("$")
                duplicate_filenames_indexes.append(normalized[i][1])
            if not (normalized[i+1][1] in duplicate_filenames_indexes):
                duplicate_filenames_indexes.append(normalized[i+1][1])
        
        elif hashes[i][0] == hashes[i+1][0]:
            #the first of the two elements tested isnt already in the returned list
            #insert a separator element in the returned list.
            if not (hashes[i][1] in duplicate_filenames_indexes):
                duplicate_filenames_indexes.append("$")
                duplicate_filenames_indexes.append(hashes[i][1])
            if not (hashes[i+1][1] in duplicate_filenames_indexes): 
                duplicate_filenames_indexes.append(hashes[i+1][1])
            
    return duplicate_filenames_indexes