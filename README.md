# log-analysis

This Python script looks into a log file with the log statements having a general format as:

__2017-08-19 09:45:18,923 [7484] DEBUG some_log_statement_here__
  
and creates an output folder in the same parent directory, containing files where all the information is segregated based on the thread ids. Like for instance, in the case above, a file called 7484.txt.
And the threads which contain at least one ERROR type statement are named as <thread_id>_error.txt.

The fully qualified name of the file which needs to be analysed is supposed to be mentioned in the configuration file: conf.json.

More often than not, we are forced to manually analyse multiple threads at the same time, looking for culprit threads which blocked a particular flow from going its natural way. And pouring over a single humongous log file is certainly not an ideal way to do that.  

_Believe me, I do realize that this is not some rocket-science level code, just something that I whipped up to make my life easier.
Hope it eases yours too._

## Planned updates:
1. to be able to manage multiple log files at the same time.
2. to be able to specify the log types belonging to each thread, so that in case the user is not interested in getting the INFO level logs from one particular thread, she/ he is able to do that.
3. to be able to run on any platform.
4. to be able to specify one/ multiple search terms to be searched within all the log files.

---

## Update 1:

It is now possible to specify just the folder name, and have it contain multiple log files within itself.
The script will create folders as per each of the log file, and put the thread specific files within them.
The skeleton of configuration file has been modified accordingly (have a look at the revision history of conf.json in case interested).

---

## Update 2:

It is now possible to specify the list of expected logging levels in the configuration file. Here are the possible logging levels, in the decreasing order of severity:  
FATAL > ERROR > WARN > INFO > DEBUG > TRACE  

Now, here is what the configuration file looks like:  
```javascript
{  
    "folder": "D:\\logs",  
    "log_types": [  
        "ERROR",  
        "INFO",  
        "DEBUG"  
    ]  
}  
```
  
So, against the key log_types, the user can specify an array of the log types which she/ he wants to be considered. In case the value corresponding to the key "log_types" is missing or is empty, all the possible log types are considered.
