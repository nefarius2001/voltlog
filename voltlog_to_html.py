#!/usr/bin/env python3

import random
import datetime
import tzlocal
import time
import csv
#import Adafruit_ADS1x15

#adc = Adafruit_7ADS1x15.ADS1115()
GAIN = 1

data = []

def getTimestring():
	return str(datetime.datetime.now(tzlocal.get_localzone()))
	
def readNewSample():
	sample = {}
	sample['timestring'] = 	str(datetime.datetime.now(tzlocal.get_localzone()))
	
	values = []
	for i in range(4):
		values.append(random.randint(0,20))
		#values.append(adc.read_adc(i, gain=GAIN)*4.096/32768.0)
		
	sample['values'] = values
	return sample

def data_to_csv(filename_to_save, samples_to_save):	
	with open(filename_to_save, mode='w') as myfile:
		writer = csv.writer(myfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		for sample_to_save in samples_to_save:
			writer.writerow([
				sample_to_save['values'][0],
				sample_to_save['values'][1],
				sample_to_save['values'][2],
				sample_to_save['values'][3],
				sample_to_save['timestring']
				])
				
				#["value-0"], entry["value-1"], entry["value-2"], entry["value-3"], entry["year"], entry["month"], entry["day"], entry["hour"], entry["minute"]])


def data_to_html(filename_to_save, samples_to_save):	
	with open(filename_to_save, mode='w') as myfile:
		myfile.write("<!DOCTYPE html>\n<html>
<head>
<style>
"table, th, td {border: 1px solid black;}"
</style>"
</head>
\n<body>\n<h1>My First Heading</h1>\n")
		myfile.write("<<table style="width:100%">")
		for sample_to_save in samples_to_save:
				myfile.write("<tr>")
				myfile.write("<td>")
				myfile.write(str(sample_to_save['timestring']))
				myfile.write("</td>")
				myfile.write(str(sample_to_save['values'][0]))
				myfile.write("</td>")
				myfile.write("<td>")
				myfile.write(str(sample_to_save['values'][1]))
				myfile.write("</td>")
				myfile.write("<td>")
				myfile.write(str(sample_to_save['values'][2]))
				myfile.write("</td>")
				myfile.write("<td>")
				myfile.write(str(sample_to_save['values'][3]))
				myfile.write("</td>")
				myfile.write("</tr>\n")
		myfile.write("</table>")
		myfile.write("\n</body>\n</html>\n")
	
	
	
	
	
	
filename=getTimestring()
filename = filename[:19]
filename = filename.replace(' ','_')
filename = filename.replace(':','-')
#filename = filename + ".txt"
print(filename)

samples = []
while True:
	print('sleep')
	time.sleep(1)

	try:
		print('try')
		sample = readNewSample()
		print('sample')
		print(sample)
		samples.append(sample)
		print(samples)
		print('save')
		data_to_csv (filename + ".txt", samples)
		data_to_html(filename + ".html", samples)
	except:
		raise
		print('except')
		pass
	print('done')
