import requests

url = 'https://overpass-api.de/api/map?bbox=-121.5429,38.5721,-121.5174,38.5886' #West Sacramento Export from OSM
filename = 'sample.osm' 

def download_file(url, local_filename):
    """Downloads file needed to start Audit"""
    # stream = True allows downloading of large files; prevents loading entire file into memory
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
                
download_file(url, filename)
