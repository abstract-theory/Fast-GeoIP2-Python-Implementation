===================================================
Maxmind GeoIP Python API Reimplementation
===================================================

Overview
------------------------
This is an alternative Python implementation of Maxmind's GeoIP Python API. By pre-computing a data structure and loading it into memory, IP geo-location look-ups are accelerated. The number of IPs geo-located per second is increased. This is particularly helpful when doing bulk location look-up, such as that needed for server log analysis. The below benchmarks compares the two APIs and shows a speed increase that starts at 111 when N=1 and then appears level off around a factor of 41 when N=10,000.

=============== =========================
 number of IPs   ratio of IPs per second
=============== =========================
    1                   110.6
    10                  49.18
    100                 51.8
    1000                41.8
    10000               41.2
=============== =========================



Pre-computing
------------------------
You must first obtain version 2 of Maxmind's database in CSV format. The file used for this algorithm was GeoLite2-City-CSV_20190326.zip [1]. Presuming the source and data are in the same directory, the new dataset can be pre-computed by running:

.. code-block:: python

    import precompute
    
    blocks = '/path/GeoLite2-City-Blocks-IPv4.csv'
    locs = '/path/GeoLite2-City-Locations-en.csv'
    output = '/path/ip_locations.pickle'

    precompute.createCityData(blocks, locs, output)    
    
When pickled, the new data set uses around 50MB.


Looking up a location
------------------------

Below is some example code for looking up IP address location. The input IP addresses MUST be contained in a list.

.. code-block:: python

    import lookup
    
    input_data = 'ip_locations.pickle'
    ip_city = lookup.loadPreparedData(input_data)    
    ips = ['1.0.0.0', '1.0.0.0',]
    countries, subdivisions, cities = wsc.getLocations(ip_city, ips)

References
------------------------
[1] https://dev.maxmind.com/geoip/geoip2/geolite2/
