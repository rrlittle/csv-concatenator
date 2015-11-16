from glob import glob
import argparse
import csv
import sys
from os import chdir, getcwd,listdir, path
from shutil import move
import time


'''
    This is a little utility to concatenate csv files for use as a batch processing method. 
    Mostly for use in the task scheduler. 

    This assumes a few things. 
    1. if this is run as a task it should be run as a waisman user, not a local admin. 
    2. it should be run with "//wcs/wtp_common/data/RDoC Computer Tasks/Inquisit tasks - USE ME/HungryDonkeyTask" type paths.
        i.e. originating with the server name. Not the local map. This is because of the way windows does mapping with tasks. 
    3. this does not create the outfile. The outfile should be a csv with the same header as the other csv files we're concatenating. 
    4. this should be saved and run as a local script on the C: drive. just navigate to C:/scripts and do a git pull command if you update this. 
    5. DONT update the local version on C: 

    6. assumes there is a diag directory, to store log files
    7. assumes there is a saved directory, to store processed files
'''


# ======================
#
#   ARGS 
#       Need the file pattern 

print("Executing the program to concatenate csv assuming all the csv's mentioned in the patter has same schema.")
ap = argparse.ArgumentParser()
ap.add_argument('-w','--working_dir',required=True) 
ap.add_argument('-o', '--outfile', required=True)
ap.add_argument('-p','--file_pattern', required=True)

print("Arguments parsing done")
args = ap.parse_args()

print("arguments are parsed")

file_pattern = args.file_pattern
ofname = args.outfile
working_dir = args.working_dir

# ======================
#
#   MOVE TO WORKING  DIR 
#       we need to go to the correct place to process the stuff

try:
    print('starting at:' + getcwd())
    print( 'attempting to move to ' + working_dir)
    chdir(working_dir)
    print('now at: ' + getcwd())
except Exception as e:
    print('moving to workingdir did not work error -> ', e)
    sys.exit(3)


# ======================
#
#   LOGS
#       Redirect stdout to the logfile. as this is usually going to be run by a scheduled task. 

logname = time.asctime().replace(' ','_').replace(':',".") # name it after the current time
sys.stdout = open('diag/concat_{}.txt'.format(logname), 'w')   # save the log


# ======================
#
#   CONCATENATE
#       concatenate the files

files_with_errs = []
files_successfull = []
try:
    # open outfile specified
    with open(ofname,'a') as of:
        wo = csv.writer(of, delimiter='\t',lineterminator="\n") # write out
    
        # get the files matching file pattern
        files = glob(file_pattern)
        print('found these files.\n[\n{}\n]\n trying to append them to {}'.format('\n'.join(files), ofname))
        print('\n\n')

        # process each file
        for fname in files:
            try:
                print('====== > Processing', fname)
                r = csv.reader(open(fname),delimiter='\t')
                print('skipping the header')
                r.__next__() # read in the header
                    
                for line in r:
                    print('\twriting ', line)
                    wo.writerow(line)


                # ======================
                #
                #   MOVE PROCESSED FILES TO SAVED
                #       moves files that have been processed successfully to the saved directory

                try:
                    # move the file to the saved dir
                    move(fname, path.join('saved', fname))
                except Exception as e:
                    # if it failed for some reason. add it to the summary log statement
                    files_with_errs.append((fname, e))
                
            except Exception as e: # if there was an error processing the file.
                files_with_errs.append((fname, e))
                
            else: # if it got through completely. save the filename to successful
                    files_successfull.append(fname)



except Exception as e:
    print('ERROR opening the outfile:')
    print('==> ERROR: ',e)

if len(files_successfull) > 0:
    print('\n\n =============================\n\tFILES SAVED SUCCESSFULLY:')
    print('\n'.join(files_successfull))

if len(files_with_errs) > 0:
    print('\n\n =============================\n\tFILES with errors. Not saved:')
    print('\n'.join(files_with_errs))

