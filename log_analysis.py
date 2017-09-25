"""
1. create the configuration file which contains the address of a log file.
2. create an output folder which will contain the thread based files.
3. loop over the file under consideration and create a map with the thread id
    as the key and the list of all the associated statements as value.
"""
import json;
import sys;
import os;
import re;
from pathlib import Path;

#fetching the parent folder name from the given file name
def get_parent_name(file):
    reverse = file[::-1];
    return reverse[reverse.index("\\")::][::-1];

#extracting the file name (sans the exception)
def get_file_name(file_name):
    reverse = file_name[::-1];
    try:
        return reverse[reverse.index(".") + 1::][::-1];
    except:
        return file_name;

#listing the files (no directories) present within the specified directory dir_ 
def list_files(dir_):
    #all the files
    all_ = os.listdir(dir_);
    #empty array to contain some of them
    some_ = [];

    for one in all_:
        if os.path.isfile(dir_ + "\\" + one):
            some_.append(one);

    return some_;

#creating a folder
def create_folder(fqn):
    try:
        #creating a folder in case it does not exist
        if not os.path.exists(fqn):
            os.makedirs(fqn);
    except:
        print("some issue with folder creation. kindly retry later.")
        sys.exit();

#creating a file
def create_file(fqn):
    try:
        #opening a file for appending, so if the file exists, data gets appended to it, otherwise it just gets created
        file = Path(fqn);
        #if the file exists, clear the contents
        #if not, open for appending
        if(file.exists()):
            open(fqn, 'a').close();
        else:
            open(fqn, 'a');

    except:
        print("some issue with file creation. kindly retry later.");
        sys.exit();

#reading the configuration file to extract relevant data
with open('conf.json', 'r') as f:
    config = json.load(f);

#contains the sanitized name of the folder under consideration
folder = config['folder'].replace("/", "\\");

#in case the specified name does not belong to a directory
if not os.path.isdir(folder):
    print("kindly enter the folder name whose log files are supposed to be analysed");
    sys.exit();

#creating the regular expression which is to be used to check whether a string starts with a valid timestamp or not
date_regex = "^2[0-9]{3}-[01][0-9]-[0123][0-9] [012][0-9]:[0-5][0-9]:[0-5][0-9],[0-9]{3}";
#compiling the regular expression
pattern = re.compile(date_regex);
#extracting only the log files within the specified folder
log_files = list_files(folder);

#iterating over list of all the log files
for file in log_files:
    file_fqn = folder + "\\" + file;
    print("processing file: " + file_fqn);
    
    #creating an output folder for each of the log files
    output_folder_fqn = folder + "\\output_" + get_file_name(file);
    create_folder(output_folder_fqn);
    
    #reading all the lines of the file under consideration
    lines = open(file_fqn, "r").readlines();
    #creating a dictionary to hold the complete data
    dictionary = dict();
    #creating a list which is supposed to contain those thread ids which have at least one ERROR statement within them
    threads_with_errors = [];

    #iterating over the log file under consideration
    for line in lines:
        #in case the line is empty, or does not match the date regex; skip the further steps
        if not line or not pattern.match(line):
            continue;
        
        opening_square_bracket_index = line.index("[");
        closing_square_bracket_index = line.index("]");

        #extracting the thread id from the line being iterated on
        thread_id = line[opening_square_bracket_index + 1:closing_square_bracket_index];
        
        #in case the thread id does not exist in the dictionary
        if thread_id not in dictionary:
            dictionary[thread_id] = [];

        #in case it does, in which case the line being iterated on is added to the associated list
        else:
            array = dictionary[thread_id];
            array.append(line);
            dictionary[thread_id] = array;

        """
        checking if the line being iterated on is an error type log or not;
        in case it is, add it to the list containing such thread ids.
        the reason that we are not simply checking if the substring "ERROR"
        occurs in the log statement is because there might be cases where the 
        substring might occur later in the string and the statement might not 
        be even an ERROR type log.
        """

        if line[closing_square_bracket_index + 2] == "E":
            threads_with_errors.append(thread_id);

    #iterating over all the keys in the dictionary
    for key in dictionary.keys():
        #creating the thread specific analysis file
        thread_file_name = output_folder_fqn + "\\" + key;

        if(key in threads_with_errors):
            thread_file_name += "_error";
        
        thread_file_name += ".txt";

        print(thread_file_name + " being created.");
        create_file(thread_file_name);

        #populating the specified file
        print(thread_file_name + " being populated.");
        with open(thread_file_name, 'a') as f:
            for line in dictionary[key]:
                f.write(line + "\n");
