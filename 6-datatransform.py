import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json

"""
Your task is to wrangle the data and transform the shape of the data
into the model we mentioned earlier. The output should be a list of dictionaries
that look like this:
{
"id": "2406124091",
"type: "node",
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}
You have to complete the function 'shape_element'.
We have provided a function that will parse the map file, and call the function with the element
as an argument. You should return a dictionary, containing the shaped data for that element.
We have also provided a way to save the data in a file, so that you could use
mongoimport later on to import the shaped data into MongoDB.
Note that in this exercise we do not use the 'update street name' procedures
you worked on in the previous exercise. If you are using this code in your final
project, you are strongly encouraged to use the code from previous exercise to
update the street names before you save them to JSON.
In particular the following things should be done:
- you should process only 2 types of top level tags: "node" and "way"
- all attributes of "node" and "way" should be turned into regular key/value pairs, except:
    - attributes in the CREATED array should be added under a key "created"
    - attributes for latitude and longitude should be added to a "pos" array,
      for use in geospacial indexing. Make sure the values inside "pos" array are floats
      and not strings.
- if the second level tag "k" value contains problematic characters, it should be ignored
- if the second level tag "k" value starts with "addr:", it should be added to a dictionary "address"
- if the second level tag "k" value does not start with "addr:", but contains ":", you can
  process it in a way that you feel is best. For example, you might split it into a two-level
  dictionary like with "addr:", or otherwise convert the ":" to create a valid key.
- if there is a second ":" that separates the type/direction of a street,
  the tag should be ignored, for example:
<tag k="addr:housenumber" v="5158"/>
<tag k="addr:street" v="North Lincoln Avenue"/>
<tag k="addr:street:name" v="Lincoln"/>
<tag k="addr:street:prefix" v="North"/>
<tag k="addr:street:type" v="Avenue"/>
<tag k="amenity" v="pharmacy"/>
  should be turned into:
{...
"address": {
    "housenumber": 5158,
    "street": "North Lincoln Avenue"
}
"amenity": "pharmacy",
...
}
- for "way" specifically:
  <nd ref="305896090"/>
  <nd ref="1719825889"/>
should be turned into
"node_refs": ["305896090", "1719825889"]
"""

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = ["version", "changeset", "timestamp", "user", "uid"]
ATTRIB = ["id", "visible", "amenity", "cuisine", "name", "phone"]

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

def shape_element(element):
    """
    Parse, validate and format node and way xml elements.
    Return list of dictionaries
    Keyword arguments:
    element -- element object from xml element tree iterparse
    """
    if element.tag == 'node' or element.tag == 'way':

        # Add empty created dictionary and k/v = type: node/way
        node = {'created': {}, 'type': element.tag}

        # Update pos array with lat and lon
        if 'lat' in element.attrib and 'lon' in element.attrib:
            node['pos'] = [float(element.attrib['lat']), float(element.attrib['lon'])]

        # Deal with node and way attributes
        for k in element.attrib:

            if k == 'lat' or k == 'lon':
                continue
            if k in CREATED:
                node['created'][k] = element.attrib[k]
            else:
                # Add direct key/value items of node/way
                node[k] = element.attrib[k]

        # Deal with second level tag items
        for tag in element.iter('tag'):
            k = tag.attrib['k']
            v = tag.attrib['v']

            # Search for problem characters in 'k' and ignore them
            if problemchars.search(k):
                # Add to array to print out later
                continue
            elif k.startswith('addr:'):
                address = k.split(':')
                if len(address) == 2:
                    if 'address' not in node:
                        node['address'] = {}
                    node['address'][address[1]] = v
            else:
                node[k] = v

        # Add key/value node ref from way
        node_refs = []
        for nd in element.iter('nd'):
            node_refs.append(nd.attrib['ref'])

        if len(node_refs) > 0:
            node['node_refs'] = node_refs

        return node
    else:
        return None


def process_map(file_in, pretty=False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2) + "\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data


def test():
    # NOTE: if you are running this code on your computer, with a larger dataset,
    # call the process_map procedure with pretty=False. The pretty=True option adds
    # additional spaces to the output, making it significantly larger.
    data = process_map('ws_street_name.xml', True)
    pprint.pprint(data[0])

    correct_first_elem = {'created': {'changeset': '24424949',
             'timestamp': '2014-07-29T16:03:00Z',
             'uid': '1660455',
             'user': 'juergenb22',
             'version': '6'},
             'id': '90250658',
             'pos': [38.571071, -121.5154289],
             'type': 'node'}

    assert data[0] == correct_first_elem
    

if __name__ == "__main__":
    test()
