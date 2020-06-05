# strava_network
final project PHYS465

all_strava.json is the file containing all personal activiites as late as June 3rd, 2020

strava_request.py iterates through those activities and for each of those, requests individual details from strava's API. 
This necessitates updating the access token, which expires every six hours. It will also not work for anyone but me.

read_strava.py then iterates through the segment data and builds the network. It also constructs additional csv files
that I upload to Cytoscape for visualization.
