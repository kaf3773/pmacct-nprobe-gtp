#!/usr/bin/python
#
# (C) 2013 - ntop.org
#
# This is a tool used to aggregate IMSI traffic using redis
#
# Usage:
# nprobe -i <device> --gtpv1-dump-dir /tmp/ --imsi-aggregation --redis localhost --tunnel -T "%IPV4_SRC_ADDR %IPV4_DST_ADDR %IPV4_NEXT_HOP %INPUT_SNMP %OUTPUT_SNMP %IN_PKTS %IN_BYTES %FIRST_SWITCHED %LAST_SWITCHED %L4_SRC_PORT %L4_DST_PORT %TCP_FLAGS %PROTOCOL %L7_PROTO"
#
# Requirements:
#   easy_install redis
#

import redis
import sys
import time
import getopt

verbose = False
aggregation_duration = 300 # seconds

def usage():
    print "Usage:   imsiAggregator.py [-h] [-v] --redis <redis host>[:<port>] --epoch <epoch> [--outdir <dir>]\n"
    print "Example: imsiAggregator.py --redis localhost:6379 --epoch 1374904200 --outdir /tmp"
    sys.exit()
    
try:
    opts, args = getopt.getopt(sys.argv[1:], "hvr:e:o:", ["help", "verbose", "redis=", "epoch=", "outdir="])
except getopt.GetoptError:
    usage()
    sys.exit(2)

opt_redis  = ""
opt_epoch  = ""
opt_outdir = ""

for o, a in opts:
    if o == "-v":
        verbose = True
    elif o in ("-h", "--help"):
        usage()
        sys.exit()
    elif o in ("-r", "--redis"):
        opt_redis = a
    elif o in ("-e", "--epoch"):
        opt_epoch = a
    elif o in ("-o", "--outdir"):
        opt_outdir = a

if((opt_redis == "") or (opt_epoch == "")):
    usage()

r = opt_redis.split(':')
redis_host = r[0]

if(len(r) == 2):
    redis_port = int(r[1])
else:
    redis_port = 6379

if(opt_epoch == "prev"):
    epoch = int(time.mktime(time.localtime()))-aggregation_duration
elif(opt_epoch == "now"):
    epoch = int(time.mktime(time.localtime()))
elif(opt_epoch[0] == "-"):
    epoch = int(time.mktime(time.localtime()))+aggregation_duration*int(opt_epoch)
else:
    epoch = int(opt_epoch)

epoch = epoch - (epoch % aggregation_duration)

if(opt_outdir == ""):
    fname = "<standard output>"
    outfile = sys.stdout
else:
    try:
        fname = opt_outdir+"/"+str(epoch)+".imsi"
        outfile = open(fname, "w")
        print("Dumping data to "+fname+"...")
    except Exception, err:
        print("Unable to create file "+fname)
        sys.exit()

# 1 - Connect to redis
r = redis.StrictRedis(host=redis_host, port=redis_port, db=0)

try:
    r.ping()
except Exception, err:
    print("Unable to connect to redis server '"+str(redis_host)+":"+str(redis_port)+"'")
    sys.exit(0)

# 2 - Retrieve aggregations
if(verbose):
    print "Retrieving IMSI aggregations for epoch "+str(epoch)+"..."

keys = r.keys(str(epoch)+".*")

outfile.write("#\n")
outfile.write("# Timestamp\tIMSI\tGranularity\tProtocol\tPackets\tBytes\tFlows\tDuration\n")
outfile.write("#\n")

for k in keys:
    try:
        elems = r.hgetall(k)
        key_elems = k.split('.')
        #outfile.write(str(epoch)+"\t"+key_elems[1]+"\t"+str(aggregation_duration)+"\t"+key_elems[2]+"\t"+str(elems["packets"])+"\t"+str(elems["bytes"])+"\t"+str(elems["flows"])+"\t"+str(elems["duration"])+"\n")
        outfile.write(str(epoch)+"\t"+key_elems[1]+"\t"+str(aggregation_duration)+"\t"+key_elems[2]+"\t"+str(elems.get("packets", 0))+"\t"+str(elems.get("bytes", 0))+"\t"+str(elems.get("flows",0))+"\t"+str(elems.get("duration", 0))+"\n")
        r.delete(k)
    except Exception, err:
        print "Error processing key "+str(key)

if(opt_outdir <> ""):
    try:
        outfile.close()
    except Exception, err:
        print("Unable to close file "+fname)
        sys.exit()
