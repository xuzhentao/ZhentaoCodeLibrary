# Tools to clean most HDFS space below your name space.
# Author: Frank Xu
# (This is specifically for the cleaning before explore page.)

import argparse
import os
import subprocess

# Sample Call:

# python clean_personalhive.py --username frank.xu

# this is the list of users that are allowed to use this script,
# please add your name in this list if needed. 
# this is to prevent cleaning important databases.
list_trust = ['frank.xu']

########### Arg Parsing and Configuration Station ###########
parser = argparse.ArgumentParser(prog='Cleaning HDFS')
parser.add_argument('--username', help='Your User Name', default='')

args = parser.parse_args()
username = args.username.strip()
username_nodot = username.replace('.', '')

# Prevent sudo user using this.
if username_nodot == '':
    print("Please add a username here using --username flag")
    exit(1)

# first check.
if username_nodot == 'smuledata' or username_nodot == 'smule' or username_nodot == 'root':
    print("Attention: Please never try smuledata / smule using this script.")
    print("Abort !")
    exit(1)

# dual check.
if not username in list_trust:
    print(
        "Attention: Please make sure you understand this script before running this script !!!, then add your name into the 'list_trust' variable, then run it again.");
    print("Abort !")
    exit(1)
############################################
os.system('clear')

##########HDFS PART ###############
print("==========Start Removing HDFS Files==========")

set_hdfscmd = set(["hdfs dfs -rm -r /user/" + username + "/reco/PROD/training_data/*",  # MUST DO
                   "hdfs dfs -rm -r /user/" + username + "/reco/PROD/training_signals/signal=user_platform/*",
    # MUST DO.
                   "hdfs dfs -rm -r /user/" + username + "/reco/PROD/training_signals/signal=user_version/*",
    # MUST DO.
                   "hdfs dfs -rm -r /user/" + username + "/reco/PROD/training_metrics/*",  # MUST DO
                   "hdfs dfs -rm -r /user/" + username + "/reco/PROD/user_attributes/*",  # MUST DO
                   "hdfs dfs -rm -r /user/" + username + "/reco/PROD/training_data_metrics/*",  # MUST DO
                   "hdfs dfs -rm -r /user/" + username + "/reco/PROD/models/*",  # MUST DO
                   "hdfs dfs -rm -r /user/" + username + "/reco/PROD/canonical_comps_lyrics/*",
                   "hdfs dfs -rm -r /user/" + username + "/reco/PROD/active_users/*",
                   "hdfs dfs -rm -r /user/" + username + "/reco/PROD/collabfilt_lyrics_metrics/*",
                   "hdfs dfs -rm -r /user/" + username + "/reco/PROD/collabfilt_lyrics_scores/*",
                   "hdfs dfs -rm -r /user/" + username + "/reco/PROD/duplicate_comps_by_family/*",
    # "hdfs dfs -rm -r /user/" + username + "/reco/PROD/el_orc/*", #don't want to do this, since el_orc is the most button level and won't change.
                   "hdfs dfs -rm -r /user/" + username + "/reco/PROD/impressions/action/*",
                   "hdfs dfs -rm -r /user/" + username + "/reco/PROD/impressions/action_extended/*",
                   "hdfs dfs -rm -r /user/" + username + "/reco/PROD/impressions/cntry/*",
                   "hdfs dfs -rm -r /user/" + username + "/reco/PROD/impressions/ctopic/*",
                   "hdfs dfs -rm -r /user/" + username + "/reco/PROD/impressions/loc/*",
                   "hdfs dfs -rm -r /user/" + username + "/reco/PROD/impressions/ltopic/*",
                   "hdfs dfs -rm -r /user/" + username + "/reco/PROD/impressions/similar/*",
                   "hdfs dfs -rm -r /user/" + username + "/reco/PROD/incidences/*",  # MUST DO
                   "hdfs dfs -rm -r /user/" + username + "/reco/PROD/logins/*",  # MUST DO
                   "hdfs dfs -rm -r /user/" + username + "/reco/PROD/login_attributes/*",  # MUST DO
                   "hdfs dfs -rm -r /user/" + username + "/reco/PROD/user_attributes/*",  # MUST DO
                   "hdfs dfs -rm -r /user/" + username + "/reco/PROD/user_activities/*",  # MY PARTITION>

])

for hdfscmd in set_hdfscmd:
    print("\t --> Removing HDFS Files in " + hdfscmd.split(' ')[-1])
    proc = subprocess.Popen(hdfscmd, shell=True, stdout=subprocess.PIPE);
    _ = proc.stdout.read()  # wait until finishied running.

##############HIVE TABLE PART##############
print("==========Start Removing and Re-creating Hive Tables.==========")
set_db_table = ["reco_prod_" + username_nodot + "." + "training_data",
    # "reco_prod_" + username_nodot + "."	+	"training_signals",
    # "reco_prod_" + username_nodot + "."	+	"training_metrics", 			#no such hive tables
                "reco_prod_" + username_nodot + "." + "user_attributes",
    # "reco_prod_" + username_nodot + "."	+	"training_data_metrics",		#no such hive tables
                "reco_prod_" + username_nodot + "." + "canonical_comps_lyrics",
                "reco_prod_" + username_nodot + "." + "active_users",
    # "reco_prod_" + username_nodot + "."	+	"collabfilt_lyrics_metrics",	#no such hive tables
                "reco_prod_" + username_nodot + "." + "collabfilt_lyrics_scores",
                "reco_prod_" + username_nodot + "." + "duplicate_comps_by_family",
    # "reco_prod_" + username_nodot + "."	+	"el_orc",
                "reco_prod_" + username_nodot + "." + "action_impressions",
                "reco_prod_" + username_nodot + "." + "cntry_impressions",
                "reco_prod_" + username_nodot + "." + "ctopic_impressions",
    # "reco_prod_" + username_nodot + "."	+	"loc_impressions",				#no such hive tables
                "reco_prod_" + username_nodot + "." + "ltopic_impressions",
                "reco_prod_" + username_nodot + "." + "similar_impressions",
                "reco_prod_" + username_nodot + "." + "incidences",
                "reco_prod_" + username_nodot + "." + "active_users", "reco_prod_" + username_nodot + "." + "logins",
                "reco_prod_" + username_nodot + "." + "login_attributes",
                "reco_prod_" + username_nodot + "." + "user_attributes",
                "reco_prod_" + username_nodot + "." + "user_activities"]

for db_table in set_db_table:
    print("==>Table:" + db_table)
    str_query_droptable = "DROP TABLE " + db_table;
    str_query_showcreate = "SHOW CREATE TABLE " + db_table;

    cmd = "hive -e \"" + str_query_showcreate + "\""
    print("\t-->Show create with cmd:\t" + cmd)
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    str_query_create = proc.stdout.read()

    str_query_create = str_query_create.replace('\n', ' ')
    str_query_create = str_query_create.replace('`', '\`')
    cmd = "hive -e \"" + str_query_droptable + "\""
    print("\t-->Drop table with cmd:\t" + cmd)
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE);
    _ = proc.stdout.read()

    cmd = "hive -e \"" + str_query_create + "\""
    print("\t--> Recreate with cmd:\t" + cmd)
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE);
    _ = proc.stdout.read()
    print("")

print("===DONE Removing===")

str_query_repair = "MSCK REPAIR TABLE reco_prod_" + username_nodot + ".training_data"
cmd = "hive -e \"" + str_query_create + "\""
print("\t--> Repair with cmd:\t" + cmd)
_ = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read();
print("===ALL DONE====")

# Some Shell script to use under the extreme case when the table doesn't exist at the very beginining.

# hive -e "CREATE EXTERNAL TABLE \`reco_prod_frankxu.training_data\`(   \`datapoint_id\` string COMMENT 'ID of training data point',    \`feature_vector\` map<string,double> COMMENT 'attribute name-value pairs',    \`label\` double COMMENT 'data point label') PARTITIONED BY (    \`algorithm\` string COMMENT 'recommendation algorithm (key type)',    \`itemtype\` string COMMENT 'type of recommended item',    \`appfamily\` string COMMENT 'app family',    \`features\` string COMMENT 'name of feature set',    \`day\` string) ROW FORMAT DELIMITED    FIELDS TERMINATED BY '\u0001'    LINES TERMINATED BY '\n'  STORED AS INPUTFORMAT    'org.apache.hadoop.mapred.SequenceFileInputFormat'  OUTPUTFORMAT    'org.apache.hadoop.hive.ql.io.HiveSequenceFileOutputFormat' LOCATION   'hdfs://nameservice1/user/frank.xu/reco/PROD/training_data' TBLPROPERTIES (   'transient_lastDdlTime'='1534806940') "
# hive -e "CREATE TABLE \`reco_prod_frankxu.training_signals\`(   \`datapoint_id\` string COMMENT 'ID of training data point (uniquely identifies impression)',    \`attribute_id\` string COMMENT 'attribute ID (machine learning feature name)',    \`value\` double COMMENT 'attribute value',    \`ts\` bigint COMMENT 'timestamp (unused)') PARTITIONED BY (    \`algorithm\` string COMMENT 'recommendation algorithm (key type)',    \`itemtype\` string COMMENT 'type of recommended item',    \`appfamily\` string COMMENT 'app family',    \`signal\` string COMMENT 'name of signal (matches query producing signal)',    \`day\` string COMMENT 'day of impression for which signal is computed') ROW FORMAT DELIMITED    FIELDS TERMINATED BY '\u0001'    LINES TERMINATED BY '\n'  STORED AS INPUTFORMAT    'org.apache.hadoop.mapred.SequenceFileInputFormat'  OUTPUTFORMAT    'org.apache.hadoop.hive.ql.io.HiveSequenceFileOutputFormat' LOCATION   'hdfs://nameservice1/user/frank.xu/reco/PROD/training_signals' TBLPROPERTIES (   'transient_lastDdlTime'='1534806961') "
# hive -e "CREATE TABLE \`reco_prod_frankxu.user_attributes\`(   \`user_id\` bigint COMMENT 'account ID',    \`attribute_name\` string COMMENT 'attribute name (see comments for logins table)',    \`attribute_value\` string COMMENT 'attribute value') PARTITIONED BY (    \`appfamily\` string COMMENT 'app family',    \`day\` string COMMENT 'day for which attributes are computed') CLUSTERED BY (    user_id)  SORTED BY (    user_id ASC)  INTO 1 BUCKETS ROW FORMAT DELIMITED    FIELDS TERMINATED BY '\u0001'    LINES TERMINATED BY '\n'  STORED AS INPUTFORMAT    'org.apache.hadoop.mapred.SequenceFileInputFormat'  OUTPUTFORMAT    'org.apache.hadoop.hive.ql.io.HiveSequenceFileOutputFormat' LOCATION   'hdfs://nameservice1/user/frank.xu/reco/PROD/user_attributes' TBLPROPERTIES (   'transient_lastDdlTime'='1534807000') "
# hive -e "CREATE TABLE \`reco_prod_frankxu.canonical_comps_lyrics\`(   \`comp_id\` string COMMENT 'composition ID',    \`canonical_comp_id\` string COMMENT 'canonical composition ID') PARTITIONED BY (    \`appfamily\` string COMMENT 'app family',    \`day\` string COMMENT 'day (canonical compositions recomputed each day)') ROW FORMAT DELIMITED    FIELDS TERMINATED BY '\u0001'    LINES TERMINATED BY '\n'  STORED AS INPUTFORMAT    'org.apache.hadoop.mapred.SequenceFileInputFormat'  OUTPUTFORMAT    'org.apache.hadoop.hive.ql.io.HiveSequenceFileOutputFormat' LOCATION   'hdfs://nameservice1/user/frank.xu/reco/PROD/canonical_comps_lyrics' TBLPROPERTIES (   'transient_lastDdlTime'='1534807021') "
# hive -e "CREATE TABLE \`reco_prod_frankxu.active_users\`(   \`user_id\` bigint COMMENT 'account ID') PARTITIONED BY (    \`appfamily\` string COMMENT 'app family',    \`day\` string COMMENT 'day for which user active status is computed') CLUSTERED BY (    user_id)  SORTED BY (    user_id ASC)  INTO 1 BUCKETS ROW FORMAT DELIMITED    FIELDS TERMINATED BY '\u0001'    LINES TERMINATED BY '\n'  STORED AS INPUTFORMAT    'org.apache.hadoop.mapred.SequenceFileInputFormat'  OUTPUTFORMAT    'org.apache.hadoop.hive.ql.io.HiveSequenceFileOutputFormat' LOCATION   'hdfs://nameservice1/user/frank.xu/reco/PROD/active_users' TBLPROPERTIES (   'transient_lastDdlTime'='1534807043') "
# hive -e "CREATE EXTERNAL TABLE \`reco_prod_frankxu.collabfilt_lyrics_scores\`(   \`user_id\` bigint COMMENT 'account ID',    \`item_id\` string COMMENT 'item ID',    \`score\` double COMMENT 'collaborative filtering score') PARTITIONED BY (    \`itemtype\` string COMMENT 'type of item',    \`actiontype\` string COMMENT 'type of action by which taste is measured',    \`appfamily\` string COMMENT 'app family',    \`day\` string COMMENT 'date for which taste is measured (using actions prior to this date)') ROW FORMAT DELIMITED    FIELDS TERMINATED BY '\u0001'    LINES TERMINATED BY '\n'  STORED AS INPUTFORMAT    'org.apache.hadoop.mapred.SequenceFileInputFormat'  OUTPUTFORMAT    'org.apache.hadoop.hive.ql.io.HiveSequenceFileOutputFormat' LOCATION   'hdfs://nameservice1/user/frank.xu/reco/PROD/collabfilt_lyrics_scores' TBLPROPERTIES (   'transient_lastDdlTime'='1534807063') "
# hive -e "CREATE TABLE \`reco_prod_frankxu.duplicate_comps_by_family\`(   \`comp_1\` string COMMENT 'first composition (song) ID',    \`comp_2\` string COMMENT 'second composition (song) ID') PARTITIONED BY (    \`appfamily\` string COMMENT 'app family',    \`day\` string COMMENT 'day (duplicate compositions recomputed each day)') ROW FORMAT DELIMITED    FIELDS TERMINATED BY '\u0001'    LINES TERMINATED BY '\n'  STORED AS INPUTFORMAT    'org.apache.hadoop.mapred.SequenceFileInputFormat'  OUTPUTFORMAT    'org.apache.hadoop.hive.ql.io.HiveSequenceFileOutputFormat' LOCATION   'hdfs://nameservice1/user/frank.xu/reco/PROD/duplicate_comps_by_family' TBLPROPERTIES (   'transient_lastDdlTime'='1534807083') "
# hive -e "CREATE TABLE \`reco_prod_frankxu.el_orc\`(   \`ts\` bigint,    \`srvts\` bigint,    \`appvs\` string,    \`campid\` int,    \`tstid\` int,    \`grpid\` int,    \`acctid\` string,    \`plyrid\` string,    \`dvcid\` string,    \`instdate\` bigint,    \`instdays\` int,    \`userdays\` int,    \`loc\` string,    \`subsperiodnum\` int,    \`substype\` string,    \`perfs\` int,    \`registered\` string,    \`osvs\` string,    \`gender\` string,    \`birthyear\` string,    \`dvcmachn\` string,    \`event\` string,    \`target\` string,    \`context\` string,    \`value\` string,    \`k1\` string,    \`k2\` string,    \`k3\` string,    \`k4\` string,    \`k5\` string,    \`k6\` string,    \`k7\` string,    \`usrid\` string,    \`lng\` string,    \`cntry\` string,    \`usrinstdays\` string,    \`appinstdays\` string,    \`k8\` string,    \`k9\` string,    \`dc\` string,    \`cfid\` string) PARTITIONED BY (    \`app\` string,    \`day\` string) ROW FORMAT SERDE    'org.apache.hadoop.hive.ql.io.orc.OrcSerde'  STORED AS INPUTFORMAT    'org.apache.hadoop.hive.ql.io.orc.OrcInputFormat'  OUTPUTFORMAT    'org.apache.hadoop.hive.ql.io.orc.OrcOutputFormat' LOCATION   'hdfs://nameservice1/user/frank.xu/reco/PROD/el_orc' TBLPROPERTIES (   'last_modified_by'='frank.xu',    'last_modified_time'='1533623240',    'transient_lastDdlTime'='1534807119') "
# hive -e "CREATE TABLE \`reco_prod_frankxu.action_impressions\`(   \`user_id\` bigint COMMENT 'account ID of user receiving recommendation',    \`item_id\` string COMMENT 'item ID of recommended item',    \`context\` string COMMENT 'context in which recommendation was received',    \`rank\` bigint COMMENT 'position of item in list of recommendations',    \`ts\` bigint COMMENT 'timestamp at which recommendation was received') PARTITIONED BY (    \`itemtype\` string COMMENT 'type of recommended item',    \`appfamily\` string COMMENT 'app family',    \`day\` string COMMENT 'day on which impression occurred') CLUSTERED BY (    user_id)  SORTED BY (    user_id ASC)  INTO 1 BUCKETS ROW FORMAT DELIMITED    FIELDS TERMINATED BY '\u0001'    LINES TERMINATED BY '\n'  STORED AS INPUTFORMAT    'org.apache.hadoop.mapred.SequenceFileInputFormat'  OUTPUTFORMAT    'org.apache.hadoop.hive.ql.io.HiveSequenceFileOutputFormat' LOCATION   'hdfs://nameservice1/user/frank.xu/reco/PROD/impressions/action' TBLPROPERTIES (   'transient_lastDdlTime'='1534806697') "
# hive -e "CREATE TABLE \`reco_prod_frankxu.cntry_impressions\`(   \`country\` string COMMENT 'country of user receiving recommendation',    \`user_id\` bigint COMMENT 'account ID of user receiving recommendation',    \`item_id\` string COMMENT 'item ID of recommended item',    \`context\` string COMMENT 'context in which recommendation was received',    \`rank\` bigint COMMENT 'position of item in list of recommendations',    \`ts\` bigint COMMENT 'timestamp at which recommendation was received') PARTITIONED BY (    \`itemtype\` string COMMENT 'type of recommended item',    \`appfamily\` string COMMENT 'app family',    \`day\` string COMMENT 'day on which impression occurred') CLUSTERED BY (    country)  SORTED BY (    country ASC)  INTO 1 BUCKETS ROW FORMAT DELIMITED    FIELDS TERMINATED BY '\u0001'    LINES TERMINATED BY '\n'  STORED AS INPUTFORMAT    'org.apache.hadoop.mapred.SequenceFileInputFormat'  OUTPUTFORMAT    'org.apache.hadoop.hive.ql.io.HiveSequenceFileOutputFormat' LOCATION   'hdfs://nameservice1/user/frank.xu/reco/PROD/impressions/cntry' TBLPROPERTIES (   'transient_lastDdlTime'='1534806656') "
# hive -e "CREATE TABLE \`reco_prod_frankxu.ctopic_impressions\`(   \`country\` string COMMENT 'country of user receiving recommendation',    \`topic_id\` bigint COMMENT 'topic ID for which user received recommendation',    \`user_id\` bigint COMMENT 'account ID of user receiving recommendation',    \`item_id\` string COMMENT 'item ID of recommended item',    \`context\` string COMMENT 'context in which recommendation was received',    \`rank\` bigint COMMENT 'position of item in list of recommendations',    \`ts\` bigint COMMENT 'timestamp at which recommendation was received') PARTITIONED BY (    \`itemtype\` string COMMENT 'type of recommended item',    \`appfamily\` string COMMENT 'app family',    \`day\` string COMMENT 'day on which impression occurred') CLUSTERED BY (    country,    topic_id)  SORTED BY (    country ASC,    topic_id ASC)  INTO 1 BUCKETS ROW FORMAT DELIMITED    FIELDS TERMINATED BY '\u0001'    LINES TERMINATED BY '\n'  STORED AS INPUTFORMAT    'org.apache.hadoop.mapred.SequenceFileInputFormat'  OUTPUTFORMAT    'org.apache.hadoop.hive.ql.io.HiveSequenceFileOutputFormat' LOCATION   'hdfs://nameservice1/user/frank.xu/reco/PROD/impressions/ctopic' TBLPROPERTIES (   'transient_lastDdlTime'='1534806739') "
# hive -e "CREATE TABLE \`reco_prod_frankxu.ltopic_impressions\`(   \`locale\` string,    \`topic_id\` bigint,    \`user_id\` bigint,    \`item_id\` string,    \`context\` string,    \`rank\` bigint,    \`ts\` bigint) PARTITIONED BY (    \`itemtype\` string,    \`appfamily\` string,    \`day\` string) CLUSTERED BY (    locale,    topic_id)  SORTED BY (    locale ASC,    topic_id ASC)  INTO 1 BUCKETS ROW FORMAT DELIMITED    FIELDS TERMINATED BY '\u0001'    LINES TERMINATED BY '\n'  STORED AS INPUTFORMAT    'org.apache.hadoop.mapred.SequenceFileInputFormat'  OUTPUTFORMAT    'org.apache.hadoop.hive.ql.io.HiveSequenceFileOutputFormat' LOCATION   'hdfs://nameservice1/user/frank.xu/reco/PROD/impressions/ltopic' TBLPROPERTIES (   'transient_lastDdlTime'='1534806615') "
# hive -e "CREATE TABLE \`reco_prod_frankxu.similar_impressions\`(   \`item_1\` string COMMENT 'item ID from which user received recommendation',    \`user_id\` bigint COMMENT 'account ID of user receiving recommendations',    \`item_2\` string COMMENT 'item ID of recommended item',    \`context\` string COMMENT 'context in which recommendation was received',    \`rank\` bigint COMMENT 'position of item in list of recommendations',    \`ts\` bigint COMMENT 'timestamp at which recommendation was received') PARTITIONED BY (    \`itemtype\` string COMMENT 'type of recommended item',    \`appfamily\` string COMMENT 'app family',    \`day\` string COMMENT 'day on which impression occurred') CLUSTERED BY (    item_1)  SORTED BY (    item_1 ASC)  INTO 1 BUCKETS ROW FORMAT DELIMITED    FIELDS TERMINATED BY '\u0001'    LINES TERMINATED BY '\n'  STORED AS INPUTFORMAT    'org.apache.hadoop.mapred.SequenceFileInputFormat'  OUTPUTFORMAT    'org.apache.hadoop.hive.ql.io.HiveSequenceFileOutputFormat' LOCATION   'hdfs://nameservice1/user/frank.xu/reco/PROD/impressions/similar' TBLPROPERTIES (   'transient_lastDdlTime'='1534806462') "
# hive -e "CREATE TABLE \`reco_prod_frankxu.incidences\`(   \`user_id\` bigint,    \`item_id\` string,    \`ts\` bigint) PARTITIONED BY (    \`itemtype\` string,    \`actiontype\` string,    \`appfamily\` string,    \`day\` string) CLUSTERED BY (    user_id,    item_id)  SORTED BY (    user_id ASC,    item_id ASC)  INTO 1 BUCKETS ROW FORMAT DELIMITED    FIELDS TERMINATED BY '\u0001'    LINES TERMINATED BY '\n'  STORED AS INPUTFORMAT    'org.apache.hadoop.mapred.SequenceFileInputFormat'  OUTPUTFORMAT    'org.apache.hadoop.hive.ql.io.HiveSequenceFileOutputFormat' LOCATION   'hdfs://nameservice1/user/frank.xu/reco/PROD/incidences' TBLPROPERTIES (   'transient_lastDdlTime'='1534806573') "
# hive -e "CREATE TABLE \`reco_prod_frankxu.active_users\`(   \`user_id\` bigint COMMENT 'account ID') PARTITIONED BY (    \`appfamily\` string COMMENT 'app family',    \`day\` string COMMENT 'day for which user active status is computed') CLUSTERED BY (    user_id)  SORTED BY (    user_id ASC)  INTO 1 BUCKETS ROW FORMAT DELIMITED    FIELDS TERMINATED BY '\u0001'    LINES TERMINATED BY '\n'  STORED AS INPUTFORMAT    'org.apache.hadoop.mapred.SequenceFileInputFormat'  OUTPUTFORMAT    'org.apache.hadoop.hive.ql.io.HiveSequenceFileOutputFormat' LOCATION   'hdfs://nameservice1/user/frank.xu/reco/PROD/active_users' TBLPROPERTIES (   'transient_lastDdlTime'='1534807415') "
