# DirectTable.py
# A directory scraping program that looks through photoscan projects and organizing their chunks into a table
# Authors: 	Winston Wu
#		Haley Emerson
#		Diego Magdaleno
#		Andrew Yeh

import xlsxwriter
import os
import datetime
import xml.etree.ElementTree
import zipfile
from glob import glob

''' global variables '''

# The resulting array that will contain data of all the chunks from the project.
all_chunks          =   []


# Location of the script / starting point; may be changed later
root_location       =   os.getcwd()
cwd                 =   os.getcwd()


# List of folder names inside each chunk; some folders have variants with '.1' behind the name.
camera              =   "thumbnails"
sparse              =   "point_cloud"
dense               =   "dense_cloud"
dense_1             =   "dense_cloud.1"
mesh                =   "model"
mesh_1              =   "model.1"
texture             =   "model"
texture_1           =   "model.1"
dem                 =   "elevation"
orthomosaic         =   "orthomosaic"
orthomosaic1        =   "orthomosaic.1"
version             =   "project.zip"

# Checks the file type; in this case, checks if a file is an '.xml' or a '.png' file; returns True if it is, and False if not.
def check_doc (file_name, type_name):
    check           =   str(file_name)
    if type_name    ==  "xml":
        doc         =   "doc.xml"
    elif type_name  ==  "png":
        doc         =   "texture.png"
    check           =   check.split('\'')

    if doc in check:
        return True
    else:
        return False


# Searches a specific zip file for the desired data given.
def search_zip_file (content):

    print(cwd)

    # Location of the file that will be parsed is based on argument passed.
    if content      ==  "camera":
        location    =   str(cwd) + "/thumbnails/thumbnails.zip"
    elif content    ==  "sparse":
        location    =   str(cwd) + "/point_cloud/point_cloud.zip"
    elif content    ==  "dense":
        location    =   str(cwd) + "/dense_cloud/dense_cloud.zip"
    elif content    ==  "dense_1":
        location    =   str(cwd) + "/dense_cloud.1/dense_cloud.zip"
    elif content    ==  "mesh":
        location    =   str(cwd) + "/model/model.zip"
    elif content    ==  "mesh_1":
        location    =   str(cwd) + "/model.1/model.zip"
    elif content    ==  "texture":
        location    =   str(cwd) + "/model/model.zip"
    elif content    ==  "texture_1":
        location    =   str(cwd) + "/model.1/model.zip"
    elif content    ==  "version":
        location    =   str(cwd) + "/project.zip"

    zip = zipfile.ZipFile(location)

    # Finding the number of images doesn't require opening files so can be done quickly.
    if content      ==  "camera":
        result      =   str(len(zip.infolist())-1)
        return result

    # Loops through the list of files in the zip file until the desired 'xml' or 'png' file is found.
    for file in zip.infolist():
        if content  ==  "texture" or content == "texture_1":

            # Returns the filesize of the 'png'
            if check_doc(file, "png"):
                result= str(file.file_size)

        else:
            # Parses through the 'doc.xml' file once found.
            if check_doc(file, "xml"):
                ofile       =   zip.open(file)
                tree        =   ET.parse(ofile)
                root        =   tree.getroot()

                # Uses the 'xml.etree.ElementTree' module to parse 'xml' files to find a specific data value.
                if content  ==  "sparse":
                    value   =   root.find("points").attrib
                    result  =   value["count"]  

                elif content    ==  "dense" or content == "dense_1":
                    for tag1 in root.findall("tiles"):
                        for tag2 in tag1.findall("tile"):
                            value   =   tag2.find("pointCount").text
                            result  =   value

                elif content    ==  "mesh" or content   ==  "mesh_1":
                    for tag in root.findall("mesh"):
                        value   =   tag.find("faceCount").text
                        result  =   value

                elif content    ==  "version":
                    value       =   root.attrib
                    value       =   str(value).split('\'')
                    result      =   value[3]
                
                ofile.close()
                break

    return result

# Function that returns an array with the desired information in the indices. 
def chunk_data_grab():

    # Placeholder array.
    chunk           =   ["N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"]

    # Grabs the project and chunk name from the current directory address.
    name            =   cwd.split('/')
    dirs            =   os.listdir(cwd)
    project_name    =   name[len(name) - 3]
    chunk_name      =   name[len(name) - 2]
    chunk[0]        =   project_name
    chunk[1]        =   chunk_name

    # If the corresponding folder type exists in the current chunk directory 'dirs', it will look for it; if not, it will ignore it and leave the index as 'N/A'
    if camera in dirs:
        chunk[2] = search_zip_file("camera")
    if sparse in dirs:
        chunk[3] = search_zip_file("sparse")
    if dense in dirs:
        chunk[4] = search_zip_file("dense")
    if dense_1 in dirs:
        chunk[4] = search_zip_file("dense_1")
    if mesh in dirs:
        chunk[5] = search_zip_file("mesh")
    if mesh_1 in dirs:
        chunk[5] = search_zip_file("mesh_1")
    if texture in dirs:
        chunk[6] = search_zip_file("texture")
    if texture_1 in dirs:
        chunk[6] = search_zip_file("texture_1")
    if dem in dirs:
        chunk[7] = "True"
    if orthomosaic in dirs:
        chunk[8] = "True"
    if orthomosaic1 in dirs:
        chunk[8] = "True"

    return(chunk)




# main function
def main():
    ''' find all files in the directory '''

    projNames = []
    # recieve input form user as to what will be the topdir to search from
    dirNameInput = str(input("Enter the directory path: "))
    while (os.path.exists(dirNameInput) is False):
        print("Error: Enter a valid path.\n")
        dirNameInput = str(input("Enter the directory path: "))
    # top argument for name in files
    topdir = dirNameInput
    # extensions to search for
    extens = ['psx']
    # list of files
    fileList = []
    # dict of found files
    found = {x: [] for x in extens}
    # directories to ignore
    ignore = []
    print("Beginning search for files in %s" % os.path.realpath(topdir))
    # walk the tree
    for dirpath, dirnames, files in os.walk(topdir):
        # remove directories in ignore
        # directory names mut match exactly
        for idir in ignore:
            if idir in dirnames:
                dirnames.remove(idir)
        # loop through the file names for current step
        for name in files:
            # split the name by '.' and get the last element
            ext = name.lower().rsplit('.',1)[-1]
            # save full name if ext matches
            if ext in extens:
                filename = os.path.splitext(name)[0]
                filesDirectory = filename + ".files"
                fDir = os.path.join(dirpath, filesDirectory)
                if (os.path.exists(fDir)):
                    found[ext].append(os.path.join(dirpath, name))
                    found[ext].append(fDir)
                    projNames.append(name)
                    fileList.append(fDir)

    ''' go through process of gathering data for each project '''

    print("Grabbing data.")
    dataLists = []
    for i in fileList:
        dataLists.append(project_data(i))    # takes the argument of the folder path

    print(dataLists) #<-------------------------------------------------------------------------------------------------------------
    
    ''' create and write to table '''
    
    print("Writing to to table")
    write_to_table(dirNameInput, dataLists)

    print("Table written. Program Complete.")

# gather data from each project and returns a list
def project_data(path_of_project):
    root_location = path_of_project

    # A snippet of code used to find immediate subdirectories.
    paths = glob('*/')

    # Code to find the version of the software used in the project through the 'doc.xml' document in the project.zip file.
    files = os.listdir(os.curdir)
    if "project.zip" in files:
        cwd = root_location
        vrsn = search_zip_file("version")

    # Main function that will grab the data from each chunk and append them to the array
    for chunks in paths:
        os.chdir(root_location + "/" + chunks + "0/")
        cwd = root_location
        indiv_chunk = chunk_data_grab()

        # Version number is added to the array here.
        indiv_chunk[9]  =   vrsn                    
        all_chunks.append(indiv_chunk)

    print(all_chunks) #<-------------------------------------------------------------------------------------------------------------
    return all_chunks

# create/write to xlsx book
def write_to_table(folder_name, data):
    # get current time 
    now = datetime.datetime.now()
    # create new workbook/worksheet
    name = str(folder_name+'-photoscan-table-'+now.strftime("%Y%m%d")+".xlsx")
    # check if a workbook with this name already exists
    if os.path.exists(folder_name+name):
        # remove the existing file
        os.remove(folder_name+name)
    book = xlsxwriter.Workbook(name)
    sheet = book.add_worksheet()
    # write headers
    Titles = ["Project", "Chunk", "Cameras", "SC # of Points", "DC # of Points", "Number of Faces", "Texture Map Size", "DEM", "Orthomosaic", "Software Version"]
    row = 1
    col = 1
    for i in Titles:
        if (col != 2):
            sheet.write(row, col, i)
        col += 1
    # reset col and row
    col = 1
    row = 2
    # iterate through the data list
    for j in data:
        col = 1
        for k in j:
            if (col is not 2):
                if (type(k) is list):
                    temp = row
                    for l in k:
                        sheet.write(row, col, l)
                        row += 1
                    row = temp
                else:
                    sheet.write(row, col, k)
            else:
                continue
            col += 1
        row += len(j)

    # close workbook
    book.close()


if __name__ == "__main__":
    main()
