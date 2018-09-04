import sys

import MySQLdb as mdb

#### Change the username,password and the database name in which your keys are loaded here

try:
   con = mdb.connect('localhost', 'root', 'entumi3774', 'pmacct');
except Exception, err:
    print err

def resolve_ip_address(the_ip):
         ip_address = "%" + the_ip + "%"
         #print "The ip i get in resolve is" + ip_address
         cur = con.cursor()
         cur.execute("select mno_name,ip_prefix FROM claro_central WHERE ip_prefix LIKE ('%s')" % (ip_address))
         numrows = int(cur.rowcount)
         #print numrows
         i = 0
         for i in range(numrows):
               row = cur.fetchone()
               mno_name = str(row[0])
         #return str(row[0])
               #print mno_name
               return mno_name
         i = i + 1
         
def resolve_asn(the_asn):
         asn = the_asn
         #print "The ip i get in resolve is" + ip_address
         cur = con.cursor()
         cur.execute("select mno,asn FROM grx_asn_info WHERE asn = ('%s')" % (asn))
         numrows = int(cur.rowcount)
         #print numrows
         i = 0
         for i in range(numrows):
               row = cur.fetchone()
               mno_name = str(row[0])
         #return str(row[0])
               #print mno_name
               return mno_name
         i = i + 1
##### Change the name of the table into which your keys are loaded in the SQL statement.
#country = "NEDE"
#cur.execute("SELECT * FROM rtd_sig_linkset WHERE country = '%s'" % (country))
#cur.execute("SELECT lsn,customer,country FROM addnew_rrd_nm_lnkset")
def main():
    which_ip = sys.argv[1]
    #print which_ip
    resolve_ip_address(which_ip)

if __name__ == "__main__":
    main()
