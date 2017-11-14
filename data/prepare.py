import os
import cv2

video_files = os.listdir("_data/running/")


def extract(data):
	path = "_data/"
	#base = path + data["fileName"].split('_')[1] + "/frames/"

	#if not(os.path.exists(base)):
	#	os.makedirs(base)

	label = data["fileName"].split("_")[1]

	video_name = path + data["fileName"].split('_')[1] + "/" + data["fileName"] + "_uncomp.avi"

	vidcap = cv2.VideoCapture(video_name)
	success, image = vidcap.read()

	count = 0
	success = True
	return_data = []

	while success:
		success, image = vidcap.read()
		if(count > int(data["start"]) and count < int(data["end"])-10):
			#cv2.imwrite(base + "/" + data["fileName"] + "_%d.jpg" %count, image)
			return_data.append({"image":image, "label":label})
		elif(count > int(data["end"])-10):
			break
		count = count + 1

	return return_data
	#extract farme data["start"] ~ data["end"] in videon_name
	#form -> frame\tlabel

def write(data):
	try:
		with open("_data/data.csv", "w") as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
			writer.writeheader()
			for d in data:
				writer.writerow(d)
	except IOError as (errno, strerror):
		print("I/O error")


#_data/running/person01_running_d1_uncomp.avi
def prepare():
	path = "_data/"
	data_seq = "_data/frame_sequence.txt"

	form = {"fileName" : None, "start":None, "end":None}

	lines = [line.rstrip('\n').rstrip('\r').split("\t") for line in open(data_seq)]
	label = [l[0].rstrip() for l in lines]
	_frame = [l[-1].split(", ") for l in lines]
	result = []

	for f, l in zip(_frame, label):
		for ff in f:
			start = ff.split("-")[0]
			end = ff.split("-")[1]
			form = {"fileName" : l, "start":start, "end":end}
			result.append(form)

	d = []
	for data in result:
		print(data["fileName"])
		d = d + extract(data)

	write(d)