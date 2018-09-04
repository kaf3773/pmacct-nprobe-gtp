##import os and pandas modules

import os
import pandas as pd
import redis
import sys
import time
import getopt

from database_sch import resolve_ip_address

which_mno_name = " "
redis_host = "localhost"
redis_port = "6379"
#list directory contents where all csv is located in variable
directory = os.listdir(".")

#Declare empty list
newlist = []

#For loop to read in csv files

for file_names in directory:
    if file_names.endswith(".csv"):
        read = pd.read_csv(file_names)

all_unique_rows = read['IMSI'].unique()
# 1 - Connect to redis
r = redis.StrictRedis(host=redis_host, port=redis_port, db=0)

try:
    r.ping()
except Exception, err:
    print("Unable to connect to redis server '"+str(redis_host)+":"+str(redis_port)+"'")
    sys.exit(0)
 
outfile = open("imsi.txt", "w")
outfile.write("sgsn,imsi,imei,msisdn\n")
for k in all_unique_rows:
    imsi = k
    key_i_need = "gtp." + str(imsi) + ";5"
    #print key_i_need
    key_to_search = r.hgetall(key_i_need)
    #print key_to_search
    #outfile.write(str(imsi)+"\n")
    outfile.write(str(key_to_search.get("sgsn", 0))+","+str(key_to_search.get("imsi", 0))+","+str(key_to_search.get("imei",0))+","+str(key_to_search.get("msisdn", 0))+"\n")
    
outfile.close()


