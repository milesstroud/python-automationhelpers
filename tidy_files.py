###########   
# IMPORTS #   
###########

import glob
import shutil

#Defining functions to handle each file type
#Python files
def python_mover():
    #Using glob wildcard to find all .py files in my Documents folder
    source_file='/Documents/*.py'
    #To be moved to:
    dest_file="/Documents/Python's_Landing"
    #Returns list of files using .py ending
    file_list=glob.glob(source_file)
    #Iterate over that returned list, moving each to the proper landing
    for file in file_list:
        shutil.move(file, dest_file)


#Repetition is the mother of learning. Let's do it again!

#PDF Files
def pdf_mover():
    source_file='/Documents/*.pdf'
    dest_file="/Documents/PDF's_Landing"
    file_list=glob.glob(source_file)
    for file in file_list:
        shutil.move(file, dest_file)

#txt Files
def txt_mover():
    source_file='/Documents/*.txt'
    dest_file="/Documents/txt's_Landing"
    file_list=glob.glob(source_file)
    for file in file_list:
        shutil.move(file, dest_file)

#Word Files
def word_mover():
    #Doing something a little funky since there are two file types
    #Separate glob wildcard extensions for each file type
    source_file='/Documents/*.docx'
    source_file2='/Documents/*.doc'
    #All going to the same place
    dest_file="/Documents/Word's_Landing"
    #Return a list of matching files with each file type
    file_list=glob.glob(source_file)
    file_list2=glob.glob(source_file2)
    file_list = file_list + file_list2 #Concatenate the lists to one
    for file in file_list:
        shutil.move(file, dest_file)

#CSV Files
def csv_mover():
    source_file='/Documents/*.csv'
    dest_file="/Documents/CSV's_Landing"
    file_list=glob.glob(source_file)
    for file in file_list:
        shutil.move(file, dest_file)

#All image file types
def image_mover():
    source_file='/Documents/*.jpeg'
    source_file2='/Documents/*.png'
    source_file3='/Documents/*.jpg'
    dest_file="/Documents/Image's_Landing"
    file_list=glob.glob(source_file)
    file_list2=glob.glob(source_file2)
    file_list3=glob.glob(source_file3)
    file_list = file_list + file_list2 + file_list3 
    for file in file_list:
        shutil.move(file, dest_file)

#Excel Files
def excel_mover():
    source_file='/Documents/*.xlsx'
    source_file2='/Documents/*.xls'
    dest_file="/Documents/Excel's_Landing"
    file_list=glob.glob(source_file)
    file_list2=glob.glob(source_file2)
    file_list = file_list + file_list2
    for file in file_list:
        shutil.move(file, dest_file)

#MP4 Files
def mp4_mover():
    source_file='/Documents/*.mp4'
    dest_file="/Documents/MP4's_Landing"
    file_list=glob.glob(source_file)
    for file in file_list:
        shutil.move(file, dest_file)

#Calling all of the functions!
python_mover()
pdf_mover()
txt_mover()
word_mover()
csv_mover()
image_mover()
excel_mover()
mp4_mover()
