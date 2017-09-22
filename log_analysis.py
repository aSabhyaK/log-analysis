"""
Author: Sabhya Kaushal
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

def parent_folder(file):
    reverse = file[::-1];
    return reverse[reverse.index("\\")::][::-1];

def create_folder(fqn):
    try:
        #creating a folder in case it does not exist
        if not os.path.exists(fqn):
            os.makedirs(fqn);
    except:
        print("some issue with folder creation. kindly retry later.")
        sys.exit();

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

#contains the sanitized name of the file under consideration
file = config['file'].replace("/", "\\");

#in case the filename mentioned is not a file; terminate the script
if not os.path.isfile(file):
    print("kindly enter only one file name.");
    sys.exit();

#creating an output folder to store the threaded files.
output_folder = parent_folder(file) + "output\\";
if(os.path.exists(output_folder)):
    print("another subfolder named 'output' exists in the parent folder.");
    print("kindly rename it to something else and restart the script.");
    sys.exit();

create_folder(output_folder);

#creating the regex which is to be used to check whether a string starts with a valid timestamp or not
date_regex = "^2[0-9]{3}-[01][0-9]-[0123][0-9] [012][0-9]:[0-5][0-9]:[0-5][0-9],[0-9]{3}";
#compiling the pattern
pattern = re.compile(date_regex);
#reading all the lines of the file under consideration
lines = open(file, "r").readlines();
#creating a dictionary to hold the complete data
dictionary = dict();
threads_with_errors = [];

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
    thread_file_name = output_folder + "\\" + key;

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
