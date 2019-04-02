
import pickle
import csv
from collections import defaultdict, OrderedDict


def createCityData(blocks_file_name, locs_file_name, output_file_name):        
    blocks = loadRawCsvData(blocks_file_name)[1:]
    locs = loadRawCsvData(locs_file_name)[1:]    
    refs = geoRefs(blocks)
    names = locNames(locs)
    cityLUT3 = ipLoc(refs, names)    
    print("writing new data...")  
    data = pickle.dumps(cityLUT3)
    with open(output_file_name, 'wb') as f:
        f.write(data)


def loadRawCsvData(fn):
    print("loading file %s..." % (fn))
    with open(fn, 'r') as f:    
        blocks = list(csv.reader(f))    
    return blocks


def ipLoc(gRefs, lNames):
    '''
    maps ip address to location
    '''
    print("putting it all together...")
    count = 0
    l = len(gRefs)
    d = dict()
    count_b = 0
    for ref in gRefs:        
        blk = gRefs[ref]
        try:
            d[ref] = lNames[blk]
        except TypeError:
            d[ref] = []
            for k in blk:
                d[ref].append([k[0], lNames[k[1]]])                
        count += 1
        count_b += 1
        if count_b == 1000:
            count_b = 0
            print("\033[K\rprogress: %5.2f%%" % (100*count/l), end='')
            
    print("\033[K\rprogress: %5.2f%%" % (100*count/l))
    return d    



# 0: geoname_id,
# 1: locale_code,
# 2: continent_code,
# 3: continent_name,
# 4: country_iso_code,
# 5: country_name,
# 6: subdivision_1_iso_code,
# 7: subdivision_1_name,
# 8: subdivision_2_iso_code,
# 9: subdivision_2_name,
# 10: city_name,
# 11: metro_code,
# 12: time_zone,
# 13: is_in_european_union
def locNames(locs):
    '''
    returns dictionary that maps "geoname_id" to [country_name, subdivision_1_name, city_name].
    '''
    print("processing locations...")
    d = dict()
    l = len(locs)
    count_b = 0

    str_or_None = lambda s: None if s == '' else s
    
    for n in range(l):
        geoRef = int(locs[n][0])
        # Choose desired geographic info here. Refer to list above function.
        d[geoRef] = [
            str_or_None(locs[n][5]),
            str_or_None(locs[n][7]),
            str_or_None(locs[n][10]),
        ]
        count_b += 1
        if count_b == 999:
            count_b = 0
            print("\033[K\rprogress: %5.2f%%" % (100*n/l), end='')
            
    print("\033[K\rprogress: %5.2f%%" % (100*n/l))
    return d


# 0: network,
# 1: geoname_id,
# 2: registered_country_geoname_id,
# 3: represented_country_geoname_id,
# 4: is_anonymous_proxy,
# 5: is_satellite_provider,
# 6: postal_code,
# 7: latitude,
# 8: longitude,
# 9: accuracy_radius
def geoRefs(blocks):
    '''
    returns dictionary that maps IP address (as an integer) to "geoname_id"
    '''
    print("processing blocks...")    
    d3 = dict()    
    l = len(blocks)
    count_b = 0
    count = 0
    
    dl = defaultdict(lambda: list())    
    
    for n in range(l):                
        ipStr = blocks[n][0].split('/')[0]
        ip_s = ipStr.split('.')    
        ip3 = int(ip_s[0])*65536 + int(ip_s[1])*256 + int(ip_s[2])
        ip4 = int(ip_s[3])
        try:
            # Choose desired data here. Index referes to notes above function.
            dl[ip3].append([ip4, int(blocks[n][1])])
        except ValueError:
            # exception if block has no data
            pass

        if count_b == 9999:
            count_b = 0
            print("\033[K\rprogress: %5.2f%%" % (100*count/l), end='')
        count_b += 1            
        count += 1
    print("\033[K\rprogress: %5.2f%%" % (100*count/l))
    
    print("processing more blocks...")    
    l = len(dl)
    count_b = 0
    count = 0                
    for ipl in dl:
        if len(dl[ipl]) == 1 and dl[ipl][0][0] == 0:            
            blk = dl[ipl][0][1]            
            d3[ipl] = blk
        else:
            od = OrderedDict()
            for n in range(len(dl[ipl])):            
                ip4 = dl[ipl][n][0]
                blk = dl[ipl][n][1]
                od[ip4] = blk            
            od = sorted(od.items(), key=lambda x: x[0])
            d3[ipl] = od
                            
        if count_b == 9999:
            count_b = 0
            print("\033[K\rprogress: %5.2f%%" % (100*count/l), end='')
        count_b += 1
        count += 1
    print("\033[K\rprogress: %5.2f%%" % (100*count/l))
    
    return d3     


