# incidences mover

import subprocess

# directory.
username = "frank.xu"
list_item_action = [("PERF", "LISTEN"), ("COMP", "LISTEN"), ("ACCT", "SOCIAL"), ("COMP", "RECCOMPLETE")]
daterange = ["2018-07-01", "2018-08-29"]
appfamily = "SING"

for itemtype, actiontype in list_item_action:

    dir_source = "/user/smuledata/reco/PROD/incidences/itemtype=" + itemtype + "/actiontype=" + actiontype + "/appfamily=" + appfamily + "/"
    dir_target = "/user/" + username + "/reco/PROD/incidences/itemtype=" + itemtype + "/actiontype=" + actiontype + "/appfamily=" + appfamily + "/"

    # check if source directory exist:
    cmd_ls = "hdfs dfs -ls " + dir_source;
    list_date = [j.split('=')[1] for j in [i.split('/')[-1] for i in subprocess.Popen(cmd_ls, shell=True,
                                                                                      stdout=subprocess.PIPE).stdout.read().split(
        '\n') if len(i) != 0] if j[:3] == 'day']
    list_date = [dd for dd in list_date if dd >= daterange[0] and dd <= daterange[1]]

    cmd_ls = "hdfs dfs -ls " + dir_source;
    if len(subprocess.Popen(cmd_ls, shell=True, stdout=subprocess.PIPE).stdout.read()) == 0:
        print("Source folder doesn't exist, so skip to the next signal!")
        continue
    else:
        cmd_mkdir = "hdfs dfs -mkdir -p " + dir_target
        print("\t-->\tExecute: " + cmd_mkdir)
        _ = subprocess.Popen(cmd_mkdir, shell=True, stdout=subprocess.PIPE).stdout.read()

    for date in list_date:
        dir_source_folder = dir_source + "day=" + date
        dir_target_folder = dir_target
        cmd_copy = "hdfs dfs -cp " + dir_source_folder + " " + dir_target_folder
        print("\t-->\tExecute: " + cmd_copy)
        _ = subprocess.Popen(cmd_copy, shell=True, stdout=subprocess.PIPE).stdout.read()
