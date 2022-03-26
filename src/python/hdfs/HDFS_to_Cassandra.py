# Code: Plot the ROC curve from server.
# Author @ Frank Xu

# Sample call:
# python HDFS_to_Cassandra.py --directory /user/smuledata/reco/PROD/training_metrics_roc/algorithm=ACTION/itemtype=PERF/appfamily=SING/model=perf_model_feedback_loop_20180529/day=2018-08-08/ --outputmode 1

# install libraries:
try:
    from pywebhdfs.webhdfs import PyWebHdfsClient  # pip install pywebhdfs
    from cassandra.cluster import Cluster
    import argparse

except ImportError:
    print("Install necessary libraries...")
    import os

    os.system("pip install pywebhdfs")
    os.system("pip install cassandra")
from cassandra.cluster import Cluster
from pywebhdfs.webhdfs import PyWebHdfsClient  # pip install pywebhdfs

########### Arg Parsing and Configuration Station ###########
parser = argparse.ArgumentParser(prog='HDFS to Cassandra Data Migrater')
parser.add_argument('--hdfshost', help='The host address', default='hn1.oak.smle.co')
parser.add_argument('--hdfsport', help='port', default='9870')
parser.add_argument('--username', help='user name', default='frank.xu')
parser.add_argument('--directory', help='the directory where the PART files stays',
                    default="/user/smuledata/reco/PROD/models/algorithm=ACTION/itemtype=PERF/appfamily=SING/model=perf_model_20150828_explorebyactionastrainingdata_negCF_V2/day=2019-05-02")
parser.add_argument('--casshost', help='The host address for cassandra', default='hn1.oak.smle.co')
parser.add_argument('--cassdb', help='The database name for cassandra', default='reco_prod')
parser.add_argument('--casstbl', help='The table name for Cassandra', default='')

args = parser.parse_args()

hdfshost = args.hdfshost
hdfsport = int(args.hdfsport)

casshosts = args.casshost.split("::")  # separated with "::"
cassdb = args.cassdb
casstbl = args.casstbl

user_name = args.username
file_directory = args.directory
#############################################################


######################## hdfs reading #######################
hdfs = PyWebHdfsClient(host=hdfshost, port=hdfsport, user_name=user_name)  # your Namenode IP & username here
data = hdfs.read_file(path)

# cassandra writing
cluster = Cluster(casshosts)
session = cluster.connect()
session.execute("USE reco_prod")

session.execute("""
       INSERT INTO ml_models (day, itemtype, algorithm, modelname, appfamily, binarymodel)
       VALUES (%(day)s, %(itemtype)s, %(algorithm)s, %(modelname)s, %(appfamily)s, %(binarymodel)s)
    """, {'day': '2019-05-02', 'itemtype': 'PERF', 'algorithm': 'ACTION',
          'modelname': 'perf_model_20150828_explorebyactionastrainingdata_negCF_V2', 'appfamily': 'SING',
          'binarymodel': data})

# show result of the reco_prod.models.
res = session.execute("""SELECT * FROM reco_prod.ml_models""").current_rows
print("total rows = " + str(len(res)))

import pprint

pprint.pprint(res)
