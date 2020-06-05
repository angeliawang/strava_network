# This python script reads in the file all_strava.json and for each activity, pulls a request from the strava API that lists all the segments covered during that activity. It then writes those segments as well as the corresponding dates of the run into csv files and savses them locally. 
# Caution: the authorization token expires every 6 hrs and might have to be refreshed. Also, strava only permits 100 requests every 15 min, so break up the loop in line 48 as necessary.

# Time to review python yeehaw
import json
import requests
import csv
from polyline.codec import PolylineCodec # this is necessary apparently to use polylines

print("Hello world, it's been a while!\n")

activity_url = "https://www.strava.com/api/v3/activities/"
access_token = "b112e54c2caf7c9dda06c52fdae573f7d14d87e3" # EXPIRES EVERY SIX HOURS
header = {'Authorization': 'Bearer ' + access_token}
param = {'per_page': 2, 'page': 1}

my_file = "all_strava.json"

print("Reading in the JSON file")
with open(my_file, "r") as f1:
	print("Converting JSON encoded data into Python dictionary")
	my_list = json.load(f1)
	print("Decoded JSON Data From File")

	# the value attached to the "map" value is a dict itself.
	'''first_run = my_list[0]
	print(first_run['map'])
	print(type(first_run['map']))
	print(first_run['start_date']) #unicode'''

	# iterate through the json file and put all the polylines into one list
	'''all_polylines = []
	all_coords = []
	for n in range(len(my_list)):
		run_n = my_list[n]
		map_data = run_n['map']
		if map_data['summary_polyline'] is not None:
			all_polylines.append(map_data['summary_polyline'])
			decoded = PolylineCodec().decode(map_data['summary_polyline']);
			all_coords += decoded
	print(len(all_coords))
	print(len(set(all_coords)))'''

	all_ids = []
	all_segs = []
	all_dates = []
	all_unique_segs = []
	for n in range(475, len(my_list)):
		run_n = my_list[n]
		run_id = run_n['id'] # an int
		if run_id is not None:
			all_ids.append(run_id)
			my_data_set = requests.get(activity_url+str(run_id), headers=header, params=param).json()  # a dict
			seg_efforts = my_data_set['segment_efforts'] # a list

			segs = [] # specific to this one activity
			for s_i in range(len(seg_efforts)):
				one_seg = seg_efforts[s_i] # a dict
				seg_name = one_seg['name']

				# encode it as unicode before trying to append it
				# this bullshit is necessary because sometimes segment names have unusual characters
				segs.append(seg_name.encode('utf-8'))

			if segs: # if there were recorded segments
				all_dates.append(run_n['start_date'])
				all_segs.append(segs)
				all_unique_segs += segs

	with open('all_dates.csv','a') as DATES:
		wr = csv.writer(DATES)
		wr.writerows(all_dates)
	# note: you need the mode to be 'a', which will append to the file instead of truncating it
	with open('all_segs.csv','a') as SEGFILE:
		wr = csv.writer(SEGFILE)
		wr.writerows(all_segs)

	#print('\n'.join(map(str, all_segs))) 

	#TODO: For each of these IDs, pull a request from strava API to get the list of segments

'''	# OK, SO MY_LIST IS A LIST OF DICTIONARY ITEMS
	# the following will let you print out the keys of the first item
	for key, value in my_list[0].items():
		#print(key)
		print(key, ":", value)
	print("All set")'''