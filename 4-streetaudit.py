"""
Your task in this exercise has two steps:
- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

filename = 'ws_postcode.xml'
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons"]

# Reflects the changes needed to standardize the street names by fixing 
# the unexpected street types to the appropriate ones in the expected list
mapping = { "pl": "Place",
            "st": "Street",
            "ave": "Avenue",
            "rd": "Road",
            "w": "West",
            "n": "North",
            "s": "South",
            "e": "East",
            "blvd":"Boulevard",
            "ic": "Interchange",
            "sr": "Drive",
            "ct": "Court",
            "ne": "Northeast",
            "se": "Southeast",
            "nw": "Northwest",
            "sw": "Southwest",
            "dr": "Drive",
            "sq": "Square",
            "ln": "Lane",
            "trl": "Trail",
            "pkwy": "Parkway",
            "ste": "Suite",
            "lp": "Loop",
            "hwy": "Highway"}


def audit_street_type(street_types, street_name):
    """Update dictionary of street names and mapping type"""
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types


def update_name(name, mapping):
    """Replace and return new name from street name mapping."""
    name_list = re.findall(r"[\w']+", name)
    end_of_street_name = len(name_list)
    
    for i in range(len(name_list)):
        word = name_list[i].lower()
        if word in mapping:
            end_of_street_name = i
            name_list[i] = mapping[word]
        
    name_list = name_list[:(end_of_street_name+1)]
    better_name = ' '.join(name_list)
    return better_name

street_types = audit(filename)

def better_street_names(filename, cleaned_filename):
    """Takes original file and returns a new file with 
    cleaned street names specific to West Sacramento"""
    tree = ET.parse(filename)
    root = tree.getroot()

    for tag in root.findall('*/tag'):
        if is_street_name(tag):
            name = tag.get('v')
            better_name = update_name(name, mapping)
            tag.set('v', better_name)

    return tree.write(cleaned_filename)

ws_street_name = 'ws_street_name.xml' #Name of "new" file
better_street_names(filename, ws_street_name)

street_types = audit(ws_street_name)

def test():
    for st_type, ways in street_types.items():
        for name in ways:
            better_name = update_name(name, mapping)
            print (name, "=>", better_name)
            if name == "Folsom Blvd":
                assert better_name == "Folsom Boulevard"
            if name == "Watt Ave.":
                assert better_name == "Watt Avenue"


if __name__ == '__main__':
    test()
