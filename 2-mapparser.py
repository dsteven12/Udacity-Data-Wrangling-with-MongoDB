"""
Your task is to use the iterative parsing to process the map file and
find out not only what tags are there, but also how many, to get the
feeling on how much of which data you can expect to have in the map.
Fill out the count_tags function. It should return a dictionary with the
tag name as the key and number of times this tag can be encountered in
the map as value.
Note that your code will be tested with a different data file than the 'example.osm'
"""

import xml.etree.cElementTree as ET
import pprint

def count_tags(filename):
    """Returns a dictionary of tags and totals."""
    tags = {}

    for event, elem in ET.iterparse(filename):
        if elem.tag in tags: 
            tags[elem.tag] += 1
        else:                
            tags[elem.tag] = 1
    return tags

def test(): 
    tags = count_tags('sample.osm')
    pprint.pprint(tags)
    assert tags == { 'bounds': 1,
                     'member': 5718,
                     'meta': 1,
                     'nd': 7989,
                     'node': 9871,
                     'note': 1,
                     'osm': 1,
                     'relation': 69,
                     'tag': 23424,
                     'way': 1212 }

if __name__ == "__main__":
    test()
