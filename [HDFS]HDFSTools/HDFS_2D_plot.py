# Code: Plot the ROC curve from server.
# Author @ Frank Xu

#Sample call:
#python HDFS_2D_plot.py --directory /user/smuledata/reco/PROD/training_metrics_roc/algorithm=ACTION/itemtype=PERF/appfamily=SING/model=perf_model_feedback_loop_20180529/day=2018-08-08/ --outputmode 1


#install libraries:
try:
	from pywebhdfs.webhdfs import PyWebHdfsClient 	# pip install pywebhdfs
	import numpy as np 								# pip install numpy
	import matplotlib.pyplot as plt 				# pip install matplotlib.
	import argparse
except ImportError:
	print("Install necessary libraries...")
	import os
	os.system("pip install numpy")
	os.system("pip install pywebhdfs")
	os.system("pip install matplotlib") 
	os.system("pip install argparse") 


from pywebhdfs.webhdfs import PyWebHdfsClient #  pip install pywebhdfs
import numpy as np # pip install numpy
import matplotlib.pyplot as plt #pip install matplotlib.
import argparse

########### Arg Parsing and Configuration Station ###########
parser = argparse.ArgumentParser(prog='HDFS 2D Plot')
parser.add_argument('--host', help='The host address', default = 'hnn2.sf.smle.co')
parser.add_argument('--port',  help='port', default = '50070')
parser.add_argument('--username', help ='user name', default = 'frank.xu')
parser.add_argument('--pathoutputimage', help = 'the path of the output images', default = '2d_plot.png')
parser.add_argument('--directory', help = 'the directory where the PART files stays', default = '/user/smuledata/reco/PROD/training_metrics_roc/algorithm=ACTION/itemtype=PERF/appfamily=SING/model=perf_model_feedback_loop_20180529/day=2018-08-08/')
parser.add_argument('--outputmode', help = "'1' if to save, and '0' if to plot ", default = '0')
parser.add_argument('--x', help ="The x label", default = 'x label')
parser.add_argument('--y', help ="The y label", default = 'y label')
args = parser.parse_args()
str_outputimage = args.pathoutputimage #the output iamge file.
host = args.host
port = args.port
user_name = args.username
file_directory = args.directory
assert(int(args.outputmode) in {0,1})
bool_save_or_show = ['save','show'][int(args.outputmode)]
label_x = args.x
label_y = args.y
############################################

print("STEP 0: Configurations.")
if file_directory[-1] != '/':
	file_directory += '/'

print("STEP 1: Connecting to server and fatch data.")
hdfs = PyWebHdfsClient(host=host,port=port, user_name=user_name)  # your Namenode IP & username here
list_filenames = [i['pathSuffix'] for i in hdfs.list_dir(file_directory)['FileStatuses']['FileStatus']]


list_tuple_data = []
for filename in list_filenames:
	if not (filename[:4].lower() == 'part'):
		continue
	filepath = file_directory + filename
	list_tuple_data_part = [[float(j) for j in i.split("")] for i in hdfs.read_file(filepath).split('\n') if i != ""]
	list_tuple_data += list_tuple_data_part
		
	print("\t-->  Reading from file part:  " + filename + ",\t #Records = " + str(len(list_tuple_data_part)))

print("STEP 3: Image plotting.")
nd2_X = np.array(list_tuple_data)
plt.plot(nd2_X[:,0], nd2_X[:,1],'.-')
plt.grid()
plt.xlabel(label_x)
plt.ylabel(label_y)
plt.title("Receiver operating characteristic")

if bool_save_or_show == 'save':
	print("STEP 4: Result saved as " + "'" + str_outputimage + "'")
	plt.savefig(str_outputimage)
	plt.close()
elif bool_save_or_show == 'show':
	print("STEP 4: Plot the result " + "'" + str_outputimage + "', Please wait with patience ^_^ ")
	plt.show()
	plt.close()






