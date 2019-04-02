

import pickle


def loadPreparedData(input_data):
    with open(input_data, 'rb') as f:
        cityLUT = pickle.loads(f.read())        
    return cityLUT

def getLocations(ipDict, ips):
    country = [None] * len(ips)
    region = [None] * len(ips)
    city = [None] * len(ips)    
    for n in range(len(ips)):                
        ip_s = ips[n].split('.')    
        ipInt3 = int(ip_s[0])*65536 + int(ip_s[1])*256 + int(ip_s[2])        
        while True:
            try:
                country[n], region[n], city[n] = ipDict[ipInt3]                
                break
            except KeyError:
                ipInt3 -= 1
            except ValueError:                             
                ipInt4 = int(ip_s[3])                
                for n1 in range(len(ipDict[ipInt3])):                    
                    if ipInt4 >= ipDict[ipInt3][n1][0]:                       
                        country[n], region[n], city[n] = ipDict[ipInt3][n1][1]                        
                break                   
    return country, region, city    
