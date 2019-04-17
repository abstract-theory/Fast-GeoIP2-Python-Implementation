
# pre-compute example
import precompute

blocks = '/path/GeoLite2-City-Blocks-IPv4.csv'
locs = '/path/GeoLite2-City-Locations-en.csv'
output = '/path/ip_locations.pickle.gz'

precompute.createCityData(blocks, locs, output)


# location look-up example
import lookup

input_data = '/path/ip_locations.pickle.gz'
ip_city = lookup.loadPreparedData(input_data)
ips = ['1.0.0.0', '1.0.0.0',]

countries, subdivisions1, cities = lookup.getLocations(ip_city, ips)

