import sys
from database_sch import resolve_ip_address as res

mnoname = res(sys.argv[1])
print mnoname
