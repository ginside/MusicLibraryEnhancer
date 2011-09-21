# -*- coding: utf-8 -*- #
'''
Created on 29 mars 2011

@author: dfrancois
'''
import os,duplicate_finder,re,Tkinter
from duplicate_finder import filename
from mutagen import easyid3
from mutagen import flac
from mutagen.flac import FLAC

AUDIO_EXTENSIONS = ["mp3","wav","flac","wma","aac","aif"]
PLAYLIST_EXTENSIONS = ["m3u","pls"]

def directory_lister(directory):
    """ directory_lister(path)-> list of tuples
        Returns a list of tuples containing data about 
        the audio files: ( file directory, filename,file extension)
    
    
    """
    os.chdir(directory)
    current_dir = os.getcwd()
    library = []
    
    for actual_dir, dirs_in_actual_dir, files in os.walk(current_dir):
        for file in files:
            extension = file.split(".")
            extension = extension[len(extension)-1]
            if extension in AUDIO_EXTENSIONS:
                library.append([ actual_dir, file, extension])
    return library

def tag_reader(file):
    """
        Read tags in audio files 
        
    
    
    """
    file_path = os.path.join(file[0],file[1])
    if file[2] == "mp3":
        try:
            tag = easyid3.EasyID3(file_path)
            return tag
        except:
            return "None"
            # print "tag reading error/ no tag/empty tag for file "+file_path
    elif file[2] == "flac":
        try:
            flac_file = FLAC.load(file_path)
            flac_file.tags # ??
        
            # ?????
            return "None"
        except:
            return "None"
    else:
        print file[2]+" filetype has no tag format processed."
        
    return "None"
    
def scanDirectory(self,directory,progressMeter):
    
    library = []
    directory_contents = self.directory_lister(directory)
    many_files = len(directory_contents)
    i = 1.0
#    retrieve informations about audio files paths and filenames
    for audio_file in directory_contents:
        progressMeter.set(value= i/many_files ,text="Scanning folder for audio files...")
        library.append({"sys_info" : audio_file,"tags_info" : self.tag_reader(audio_file)})
        i = i + 1
        
#    duplicates_indexes_tags = filename.compare_tags(library)
    

    print str(len(library))+" fichiers audio dans le répertoire "+ directory
    
    return library

def deleteFiles(library,indexes):
        i = 0
        for index in indexes:
               os.remove(library[index]["sys_info"][0]+'\\'+library[index]["sys_info"][1])
               i = i + 1
        return i
    
