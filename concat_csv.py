from glob import glob
import argparse
import csv
import sys
from os import chdir, getcwd,listdir
import time

#
#   ARGS 
#       Need the file pattern 

ap = argparse.ArgumentParser()
ap.add_argument("-w",'--working_dir',required=True)
ap.add_argument('-o', '--outfile', required=True)
ap.add_argument("-p",'--file_pattern', required=True)

args = vars(ap.parse_args())
print(args)

file_pattern = args['file_pattern']
ofname = args['outfile']
working_dir= args['working_dir']

#
#   MOVE TO WORKING DIR
#       we need to go to the correct place to process the stuff

try:
    print('starting at:' + getcwd())
    print( 'attempting to move to ' + working_dir)
    chdir(working_dir)
    print('now at: ' + getcwd())
except Exception as e:
    print('moving to workingdir did not work error -> ', e)
    sys.exit(3)


#
#   LOGS
#       Redirect stdout to the logfile. as this is usually going to be run by a scheduled task. 

#logname = time.asctime().replace(' ','_').replace(':',".") # name it after the current time
#sys.stdout = open('diag/concat_{}.txt'.format(logname), 'w')   # save the log

#
#   CONCATENATE
#       concatenate the files

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
            print('\n\n====== > Processing', fname)
            r = csv.reader(open(fname),delimiter='\t')
            print('skipping the header')
            r.__next__() # read in the header
                
            for line in r:
                print('writing ', line)
                wo.writerow(line)

except Exception as e:
    print('ERROR opening the outfile')
    print('ERROR: ',e)
