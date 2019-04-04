
import pickle
import gzip
import csv


class prgs:
    """A class to print program progress durring loops."""

    def __init__(self, total, updates=None, loops=None):
        self.inc = 0
        self.loops = 0
        self.count = 0
        self.progress = 0
        self.end = ''
        self.fmt_str = None
        self.deci = None
        self.set(total, updates, loops)

    def set_format(self, updates):
        # deci = ceil [ log10(updates) ] - 2
        self.deci = 0
        while updates > 1:
            updates /= 10
            self.deci += 1
        self.deci = int(self.deci) - 2
        # deci can't be negative
        if self.deci < 0:
            self.deci = 0
        # total length of float string: len('100.') = 4
        total = self.deci + 4
        # 2nd order string interpolation to format output
        self.fmt_str = "\033[K\rprogress: %%%d.%df%%%%" % (total, self.deci)

    def set(self, total, updates=None, loops=None):
        if updates == 0 or loops == 0:
            print("Error: input argument must not be zero.")
            raise ValueError
        if (not updates) == (not loops):
            print("Error: you must specify exactly one of the following input variables: updates, loops.")
            raise RuntimeError
        if loops:
            self.loops = loops
            updates = total//self.loops
        else:
            # This must be an integer.
            self.loops = total//updates
            updates = total//self.loops
        # Set the minimum number of decimal places that will change on each iteration.
        self.set_format(updates)
        # 1) After the last increment, progress must straddle the 100% mark.
        # 2) By carefuly choosing "inc", the format string will auto-magically
        #    round the final progress level to exactly 100%.
        self.inc = ( 100+0.1*10**-self.deci ) / updates

    def update(self):
        self.count += 1
        if self.count == self.loops:
            self.progress += self.inc
            self.count = 0
            if self.progress >= 100:
                self.end = '\n'
            print(self.fmt_str % self.progress, end=self.end)



def createCityData(blocks_file_name, locs_file_name, output_file_name):
    blocks = loadRawCsvData(blocks_file_name)[1:]
    locs = loadRawCsvData(locs_file_name)[1:]
    refs = geoRefs(blocks)
    names = locNames(locs)
    cityLUT = ipLoc(refs, names)

    print("writing new data...")
    with gzip.open(output_file_name, 'wb') as f:
        f.write(pickle.dumps(cityLUT, pickle.HIGHEST_PROTOCOL))


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
    d = dict()
    status = prgs(len(gRefs), loops=1000)
    for ref in gRefs:
        blk = gRefs[ref]
        d[ref] = []
        for k in blk:
            try:
                locationNames = lNames[k[1]]
            except KeyError:
                locationNames = [None,None,None,]
            d[ref].append([k[0]] + locationNames)
        status.update()
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
    str_or_None = lambda s: None if s == '' else s
    status = prgs(l, loops=1000)
    for n in range(l):
        geoRef = int(locs[n][0])
        # Choose desired geographic info here. Refer to list above function.
        d[geoRef] = [
            str_or_None(locs[n][5]),
            str_or_None(locs[n][7]),
            str_or_None(locs[n][10]),
        ]
        status.update()
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
    l = len(blocks)
    dl = dict()
    status = prgs(l, loops=10000)
    for n in range(l):
        ipStr = blocks[n][0].split('/')[0]
        ip_s = ipStr.split('.')
        ip3 = int(ip_s[0])*65536 + int(ip_s[1])*256 + int(ip_s[2])
        ip4 = int(ip_s[3])
        # Choose desired data here. Index referes to notes above function.
        try:
            mm_id = int(blocks[n][1])
        except ValueError:
            mm_id = None
        try:
            dl[ip3].append([ip4, mm_id])
        except KeyError:
            dl[ip3] = [[ip4, mm_id]]
        status.update()
    return dl


