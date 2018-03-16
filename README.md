# Udacity-Data-Wrangling-with-MongoDB
Final Project Files for Udacity's Data Wrangling with MongoDB

Files:
Currently all python scripts are run with the sample test file.  
1-downloadosmfile - downloads open street map file for West Sacramento. 
2-mapparser - Processes map file and finds out what tags are there, how many, and develop an intuition for the data
3-postalaudit - Cleans postal codes in file, and returns only postcodes in area of West Sacramento. Creates a new file.
4-streetaudit - Cleans street names in file, and returns cleaned street names based on the provided mapping. Creates a new file. 
5-tags - Checks the "k" value for each "<tag>" and sees if they can be valid keys in MongoDB (also determines if there are other potential problems).
6-datatransform - transforms data into a list of dictionaries. 

sample.osm: https://overpass-api.de/api/map?bbox=-121.5429,38.5721,-121.5174,38.5886
west_sacramento.osm: https://overpass-api.de/api/map?bbox=-121.6653,38.4326,-121.2578,38.6906

References: 
https://www.dataquest.io/blog/jupyter-notebook-tips-tricks-shortcuts/
https://docs.google.com/document/d/1F0Vs14oNEs2idFJR3C_OPxwS6L0HPliOii-QpbmrMo4/pub
https://github.com/joelcolucci/data-wrangling-with-mongodb/blob/master/finalproject/main.py
