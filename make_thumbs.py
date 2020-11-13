#!/bin/python
import argparse
import os
import re
from pathlib import Path
import subprocess
from subprocess import PIPE, run,call
import piexif
from datetime import datetime, date, time, timezone, timedelta

## A POSIX variable
#OPTIND=1         # Reset in case getopts has been used previously in the shell.

## Initialize our own variables:
#str outdir="."
#str inputfile=""
#str interval_secs=0
#str starttime=0
#endtime=0
#average=0



parser = argparse.ArgumentParser()
parser.add_argument('-f', metavar='inputfile', type=str, action='store',
                    help='inputfile', required=True)
parser.add_argument('-d', metavar='output_directory', type=str, default=".",
                    help='output_directory (. is the default)')
parser.add_argument('-i', metavar='interval_secs', type=float, action='store',
                    help='interval_secs',required=True)
parser.add_argument('-s', metavar='starttime', type=float, action='store',
                    help='starttime_secs',default=0.0)
parser.add_argument('-e', metavar='endtime', type=float, action='store',
                    help='endtime_secs',default=0.0)
args = parser.parse_args()
#args, unknown = parser.parse_known_args()
inputfile = args.f
endtime = args.e
interval_secs = args.i
starttime = args.s
print(args)


#show_help ()
#{
    #echo "   -h (show help)"
    #echo "   -f inputfile"
    #echo "   -d output_directory ('$outdir' is the default)"
    #echo "   -i interval_secs"
    #echo "   -s starttime_secs"
    #echo "   -e endtime_secs"
    #echo "   -a total_images_averaged_over_the_duration_or_start_stop_time (will override interval_secs)"
#}

#while getopts "h?f:i:s:e:a:d:" opt; do
    #case "$opt" in
    #h|\?)
        #show_help
        #exit 0
        #;;
    #f)  inputfile=$OPTARG
        #;;
    #d)  outdir=$OPTARG
        #;;
    #i)  interval_secs=$OPTARG
        #;;
    #s)  starttime=$OPTARG
        #;;
    #e)  endtime=$OPTARG
        #;;
    #a)  average=$OPTARG
        #;;
    #esac
#done

#shift $((OPTIND-1))

#[ "$1" = "--" ] && shift

#if [ -z $inputfile ]; then
   #echo We need a filename to work on
   #show_help
   #exit 1
#fi

dto = subprocess.run(['exiftool',inputfile,"-DateTimeOriginal"],capture_output=True)
print(dto)
dtom=dto.stdout.decode("utf-8").replace(':','').replace('\n','')
dtom=re.sub("Date/Time Original\s+","",dtom)
filedate=datetime.strptime(dtom,'%Y%m%d %H%M%S%z')
print(dtom, filedate)
if endtime == 0:
#https://stackoverflow.com/a/30980523/5840230

    duration = subprocess.check_output(['ffprobe', '-i', inputfile, '-show_entries', 'format=duration', '-v', 'quiet', '-of', 'csv=%s' % ("p=0")])
    print(float(duration.decode("utf-8")))	
   ### When used to calculate average interverals or end time is not defined...
    #et=run(["ffprobe",
	    #"-v", "quiet",
	    ##" -show_entries", 
	    #"format=duration", inputfile,
	    ##'-of csv="p=0" '
	    ##"| sed 's/\..*//'"
	    #],capture_output=True)
    #print(et)
    #endtime=et.stdout
    endtime=float(duration.decode("utf-8"))
    print("endtime\t",endtime)
#fi

#if [ $average -gt 0 ]; then
   #let duration=endtime-starttime
   #let interval_secs=duration/average
#fi

#if [ $interval_secs -eq 0 ]; then
   #echo We need interval in seconds to work on
   #show_help
   #exit 1
#fi


## Get the filename sans directory...
#filename=`echo $inputfile | sed 's/.*\///'`

filename=Path(inputfile).stem
print("stem\t",filename)
## Drop off the filename extesion...
#filename="${filename/.mp4/}"
#ffmpegstring =  ("ffmpeg -v quiet -i "+inputfile+" -ss "+ str(starttime) +" -t "+str(endtime)+" -f image2 -qscale 2 " + filename+"-%d.jpeg -deinterlace -r "+ str(1/interval_secs))
ffmpegstring =  "ffmpeg -i "+inputfile+" -y -ss "+ str(starttime) +" -t "+str(endtime)+" -an -qscale 0 -f image2 -r "+str(1/interval_secs)+ " -deinterlace " + filename+"-%d.jpeg"
print (ffmpegstring)
os.system(ffmpegstring)
## Create sequence and use the filename for the jpegs to avoid collision with other jpeg processing...
#ffmpeg -loglevel panic -i $inputfile -ss $starttime -t $endtime -f image2  -r 1/$interval_secs -qscale 2 $filename-%d.jpeg -deinterlace 
##fps=1/$interval_secs 

## Get a listing of the thumbnail filenames...
p = Path('.')
arr=(p.glob(filename+'*.jpeg'))
#print(list(arr))
#res =  filter(re.math("*\d*"),list(arr))
#res = filter(re.match(r'.*',arr))
fns=filename+"\-\d\d\.jpeg"
print (fns)
fn = re.compile(fns)
res = [f for f in list(arr) if fn.search(f.name)]
#for f in list(arr):
#    print(f.name+"\n")

print(list(res))
#arr=( $(ls $filename*.jpeg) )
# Number of filenames
qnt=len(list(res))
## First filename will be #1..
for i in range(1,qnt):
#while [ $i -le $qnt ]; do
    totalsec=i*interval_secs
    print(totalsec)
    timestampsecs=totalsec+starttime
    sec=(timestampsecs % 60)
    min=(timestampsecs % 3600)/60
    hour=(timestampsecs/3600)
    ##timestampsecs/3600
    filedelta=timedelta(seconds=timestampsecs)
    print(filedate+filedelta)
    thumb_filename="%s-%02d_%02d_%02.2f-%.2f.jpeg" % (filename,hour,min,sec,interval_secs)
    print(thumb_filename)
    #mv $filename-$i.jpeg $outdir/$thumb_filename
    #let i=i+1
#done
