# -*- coding: utf-8 -*- #
'''
Created on 13 avr. 2011

@author: dfrancois
'''

from Tkinter import *
import tkFileDialog
import tkMessageBox
import Utils
from G_utils import Meter
from duplicate_finder import filename


class Mle_Gui(object):
    """
    GUI class for mle application
    """
    
    def __init__(self):
        """
        GUI elements initialisation..
        """
        #APPS VARS
        self.library = []
        
        #WINDOW INIT
        self.window = Tk()
        self.window.title("Music Library Enhancer")
        self.window.rowconfigure(0, weight=1)
        self.window.columnconfigure(0, weight=1)      
        #BUTTONS INIT
        self.scanButton = Button(self.window,text = "Scan Library", command = self.start_scan)
        
        #LABELS INIT
        self.errorLabel = Label(self.window)
        
        #LISTS INIT
        self.resultListScrollBar = Scrollbar(self.window)
        self.resultList = Listbox(self.window, yscrollcommand=self.resultListScrollBar.set,width=50,height=5)
        self.resultListScrollBar.config(command=self.resultList.yview)
        
        #MENU INIT
        self.main_menu = Menu(self.window)
        
        self.filemenu = Menu(self.main_menu,tearoff = 0)
        self.filemenu.add_command(label="Quit!", command= quit)
        self.library_menu = Menu(self.main_menu,tearoff = 0)
        self.library_menu.add_command(label="Select library directory",command = self.req_directory)
        
        
        self.main_menu.add_cascade(label ="File",menu = self.filemenu)
        self.main_menu.add_cascade(label ="Library",menu = self.library_menu)
        self.window.configure(menu = self.main_menu,width = 100,height= 50)
        
        self.progressMeter = Meter(self.window)

    def req_directory(self):
        """
        Retrieve folder path argument
        """
        self.libDir = tkFileDialog.askdirectory()
        if self.libDir != "":
            self.start_scan()
    

    def start_scan(self):
        """
        Scan folder for music files and tags associated
        """
        #Re-init GUI
        self.errorLabel.config(text = "")
        self.resultList.delete(0,END)
        self.progressMeter.grid(row=1,column=0)
        if self.libDir != "":
            # try:
            self.library =  Utils.scanDirectory(Utils,self.libDir,self.progressMeter)
            if len(self.library) == 0:
                self.resultList.insert(END,"No supported audio files in this directory.")
                self.resultList.config(width=50,height=5)
                self.progressMeter.grid_remove()
            else:
                for item in self.library:
                    self.resultListScrollBar.grid(row=0,column=1,sticky=N+S+W)
                    self.resultList.config(height=40,width=80,selectmode="multiple")
                    self.resultList.insert(END,str(self.library.index(item))+"."+item["sys_info"][0]+"\\"+ item["sys_info"][1])
            #  except:
            #     self.errorLabel.config(text = "Library scanning error !")
            #     self.errorLabel.grid(row=100,column=1)
        else:
            self.errorLabel.config(text = "No directory entered :[" +str(self.libDir)+"]")
            self.errorLabel.grid(row=100,column=1)
        self.window.title(self.window.title()+" - "+ str(self.libDir))
        self.library_menu.add_command(label ="Check for duplicates", command = self.checkDuplicates)
        self.progressMeter.grid_remove()
        
    def check_duplicates(self):
        """
        Handler for launching a duplicate files scanning in the library and retrieving the result
        """
        #Re-init GUI
        self.resultList.delete(0,END)
        self.resultList.config(width=100)
        self.resultList.insert(END,"Looking for duplicates elements into your library...")
        self.resultList.grid_remove
        self.progressMeter.grid(row=1,column=0,sticky=E+W)
        duplicates_indexes = filename.compare(self.library,self.progressMeter)
        
        
        #Display the result
        self.resultList.delete(0,END)
        self.resultList.insert(END,"--- Files with same filenames detected: ---")
        for index in duplicates_indexes:
            if isinstance(index, int):
                self.resultList.insert(END,str(index)+" "+self.library[index]["sys_info"][1]+" found in ("+self.library[index]["sys_info"][0]+")")
            else:
                self.resultList.insert(END,"")
        self.resultList.insert(END,"")
        
        duplicates_tags_indexes = filename.compare_tags(self.library,self.progressMeter)
        
        self.resultList.insert(END,"--- Files with same tags detected: ---")
        self.resultList.insert(END,"")
        marker = 1
        for index in duplicates_tags_indexes:
            if isinstance(index,int):
                if index not in duplicates_indexes:
                    self.resultList.insert(END,str(index)+" "+self.library[index]["sys_info"][1]+" found in ("+self.library[index]["sys_info"][0]+")")
                    marker = 0
                else:
                    marker = 1
            elif marker == 0:
                self.resultList.insert(END,"")
        
        if len(duplicates_indexes) + len(duplicates_tags_indexes) > 0:
            self.library_menu.add_command(label="Delete selected duplicates",command = self.deleteDuplicates)
     
    def delete_duplicates(self):
        try:
            entries = self.resultList.selection_get().split('\n')
            indexes = [] 
            for entry in entries:
                try:
                    index = int(str(entry).split(" ")[0])
                    print index
                    indexes.append(index)
                except:
                    print "error"
            
            if len(indexes) > 0:
                if tkMessageBox.askokcancel("Confirmation",
                                            "Delete the "+str(len(indexes))+
                                            " selected files?"):
                   tkMessageBox.showinfo("Delete files", str(Utils.deleteFiles(self.library,indexes)) + " file(s) successfully deleted.")
            else:
                raise EXCEPTION
                
        except:
            tkMessageBox.showerror("Error!", "No entries selected!")
            

    
    def main_window(self):
        """
        Main window initialisation, populating window
        """
        self.resultList.grid(row=0,column=0,sticky= N+S+E+W)
        self.resultList.insert(END,"Hello, please select the directory of your music library")
        return self.window
    
    
    def run(self):
        """
        Launches the GUI
        """
        self.main_window().mainloop()