import sys
import os
import getopt
#from database_sch import resolve_ip_address as res
import pandas as pd

from database_sch import resolve_asn, resolve_ip_address

#read the json file
df = pd.read_json("bgp-172_21_22_20-1610.log", orient='records', lines=True)
#read in the csv file
read = pd.read_csv('imsi_zero.csv')
#readzero = read[read.sgsn != 0]
#delete all rows containing zero in the sgsn column
readzero = read.drop(read[read.sgsn == "0"].index)

outfile = open("imsi_resolved.csv", "w")
outfile.write("mno,imsi,imei,msisdn\n")
#iterate over the rows
for index, row in readzero.iterrows():
       #print row['sgsn'], row['imsi']
       sgsn_ip = str(row['sgsn'])
       #Do first lookup to see if it matches IP addresses
       mno_name = resolve_ip_address(sgsn_ip)
       if mno_name == None: 
             ip_to_use = sgsn_ip.rsplit('.',1)[0]
             asn_needed = df[df['ip_prefix'].str.contains(ip_to_use)].head(1)
             #asn_needed = df.loc[df['ip_prefix'] == ip_to_use].head(1)
             for index, as_row in asn_needed.iterrows():
                    
                    count_list_of_asn = len(as_row['as_path'].split(' '))
                    if count_list_of_asn == 1:
                           list_of_asn = resolve_asn(as_row['as_path'])
                           outfile.write(str(list_of_asn).replace(",","") + "," + str(row['imsi']) + "," + str(row['imei']) + "," + str(row['msisdn']) + "\n")
                    else:
                           list_of_asn = resolve_asn(as_row['as_path'].split(' ')[-1])
                    #print as_row['ip_prefix'], list_of_asn
                    #print list_of_asn, str(row['imsi']), str(row['imei']), str(row['msisdn'])
                           outfile.write(str(list_of_asn).replace(",","") + "," + str(row['imsi']) + "," + str(row['imei']) + "," + str(row['msisdn']) + "\n")
       else:
            #print sgsn_ip, mno_name
            #print mno_name, str(row['imsi']), str(row['imei']), str(row['msisdn'])
            outfile.write(str(mno_name) + "," + str(row['imsi']) + "," + str(row['imei']) + "," + str(row['msisdn']) +"\n") 

outfile.close()      
       
#readzero.to_csv('imsi_without_zero.csv', sep=',', encoding='utf-8', index=False)
#ipaddress = str(key_to_search["sgsn"])
#    try:
#        print ipaddress
#        which_mno_name = resolve_ip_address(str(ipaddress))
#        print which_mno_name
#        if (str(which_mno_name) <> "None"): 
#               outfile.write(str(which_mno_name)+","+str(key_to_search.get("imsi", 0))+","+str(key_to_search.get("imei",0))+","+str(key_to_search.get("msisdn", 0))+"\n")
#        elif (str(which_mno_name) == "None"):
