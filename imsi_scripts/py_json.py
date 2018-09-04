import pandas as pd

#url = 'file://localhost/home/ntop/bgp-172_21_22_20-1610.log'

# Load the first sheet of the JSON file into a data frame
df = pd.read_json("bgp-172_21_22_20-1610.log", orient='records', lines=True)

#ippref = df['ip_prefix']
# View the first ten rows

needed = df[df['ip_prefix'].str.contains("166.181.8")]

#ippref = df.head(10)
#whatnum = pd.__version__
#print ippref

print needed
