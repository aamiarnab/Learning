import os

def rename_files():
    #Get the list of files              
    file_list = os.listdir(r"C:\Aami\Learning\Python\udacity\prank")

    os.chdir (r"C:\Aami\Learning\Python\udacity\prank")
    
    #for each file, rename filename
    for file_name in file_list:
        bfile_name = file_name.encode("UTF-8")
        #print (bfile_name)

        new_file = bfile_name.translate(None, b"0123456789")
        #print (new_file.decode("UTF-8"))

        os.rename(file_name, new_file.decode("UTF-8"))

rename_files()
