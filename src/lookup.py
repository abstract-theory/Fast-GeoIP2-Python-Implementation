

import pickle
import gzip

def loadPreparedData(input_data):
    with gzip.open(input_data, 'rb') as f:
        cityLUT = pickle.loads(f.read())
    return cityLUT

def getLocations(ipDict, ips):
    country = [None] * len(ips)
    region = [None] * len(ips)
    city = [None] * len(ips)
    for n in range(len(ips)):
        ip_s = ips[n].split('.')
        ipInt3 = int(ip_s[0])*65536 + int(ip_s[1])*256 + int(ip_s[2])
        ipInt4 = int(ip_s[3])

        while True:
            try:
                ip_blocks = ipDict[ipInt3]
                for ip_block in reversed(ip_blocks):
                    if ipInt4 >= ip_block[0]:
                        country[n], region[n], city[n] = ip_block[1:4]
                        break
                break
            except KeyError:
                ipInt3 -= 1

    return country, region, city

