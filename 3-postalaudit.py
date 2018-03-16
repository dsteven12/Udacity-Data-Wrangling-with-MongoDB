import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

filename = 'sample.osm'

def count_postcodes(filename):
    """Determines how many and number of postcodes for the filename"""
    
    postcodes = {}
    for event, elem in ET.iterparse(filename, events=('start', 'end')):
        if event == 'end':
            key = elem.attrib.get('k')
            if key == 'addr:postcode':
                postcode = elem.attrib.get('v')
                if postcode not in postcodes:
                    postcodes[postcode] = 1
                else:
                    postcodes[postcode] += 1
    return postcodes


postcodes = count_postcodes(filename)
sorted_by_occurrence = [(k, v) for (v, k) in sorted([(value, key) for (key, value) in postcodes.items()], reverse=True)]

print('Postcode values and occurrence in west_sacramento.osm:\n')
pprint.pprint(sorted_by_occurrence)

def get_postcode(elem):
    """Returns True if postcode value contains a postcode, 
    or false if the element doesn't"""
    
    if elem.tag in ['node', 'way', 'relation']:
        for tag in elem.iter():
            if tag.get('k') == 'addr:postcode':
                return True, tag.get('v')
        return False, None
    return False, None


def wsac_postcode(filename, cleaned_filename):
    """Takes original file and returns a new file with cleaned postcodes specific to West Sacramento"""
    tree = ET.parse(filename)
    root = tree.getroot()
    
    for child in ['node', 'way', 'relation']:
        for elem in root.findall(child):
            has_postcode, postcode_value = get_postcode(elem)
            if has_postcode:
                if postcode_value not in ['95605', '95691', '95798', '95799', '95818', '95831', '95899']:
                    root.remove(elem)
    
    return tree.write(cleaned_filename)

def test():
    ws_postcode = 'ws_postcode.xml' #Name of "new" file
    wsac_postcode(filename, ws_postcode) 

    postcodes = count_postcodes(ws_postcode)
    sorted_by_occurrence = [(k, v) for (v, k) in sorted([(value, key) for (key, value) in postcodes.items()], reverse=True)]
    print(' ')
    print('------------------------------------------------')
    print('Postcode values and occurrence after cleaning:\n')
    pprint.pprint(sorted_by_occurrence)

    correct_first_elem = ('95691', 3483)

    assert sorted_by_occurrence[0] == correct_first_elem

if __name__ == "__main__":
    test()

