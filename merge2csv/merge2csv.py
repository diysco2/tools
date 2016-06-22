'''
merge2csv.py
About: 
  1. Compiles .dat files from each day to a single CSV 
  2. Compiles CSVs for a time range to a Larger CSV
Usage: 
python merge2csv.py '<folderpath to repo>' '<folderpath to workspace>' '<start:YYMMDD>' '<end:YYMMDD>'

'''
# Import libraries
import csv
import math
import os
import sys
import glob
import pandas as pd
import numpy as np
from datetime import datetime
import distutils.core
import shutil
import re

# transfer to and from directoreis
def dump(fromDir, toDir):
  distutils.dir_util.copy_tree(fromDir, toDir)

# get the directories
def getDirs(iPath):
  folders = []
  # foldernames = []
  for root, dirs, files in os.walk(iPath):
      for folder in dirs:
        folders.append(os.path.join(root, folder))
        # foldernames.append(folder)
  return folders

# Copy the selected data from the repo to the workspace temporarily
def copyselection(fromDir, toDir, startDate, endDate):
  # get subfolders in fromDir
  subFolders = os.listdir(fromDir)
  # get the range of folders based on start/end index positions
  iStart= subFolders.index(startDate)
  iEnd = subFolders.index(endDate)
  collectFolders = subFolders[ iStart : iEnd + 1 ]
  # add in folderpath
  selectedFolders = [os.path.join(fromDir, x) for x in collectFolders]
  # Copy over to workspace
  for i in xrange(len(selectedFolders)):
    dump( str(selectedFolders[i]), toDir + '/' + collectFolders[i] )
    print "copying folder FROM: " + str("'" + selectedFolders[i] + "'") + " TO: --> " + "'" + toDir + '/' + collectFolders[i] + "'"

  # TODO: include error handling only directories - not other stuff

# Merge .dat to csv & apply datetime sorting
def merge2csv(iPath):
  # List all of the files within the folder
  allFiles =[os.path.join(root, file) for root, dirs, files in os.walk(iPath) for file in files]
  # print(allFiles)
  # add each .dat file to a dataframe
  df = pd.DataFrame()
  temp = [pd.read_csv(i, index_col=None, header=None) for i in allFiles if i.endswith('.DAT') if os.path.getsize(i) > 0]

  data = df.append(temp)
  return data

# Enrich the data with the header & Apply Sorting
def enrichcsv(data, sensorid):
  data.is_copy = False
  # add headers
  # data.columns = ['date','time','gpsfix','gpsquality','lat','lon','speed','altitude','satfix','co2','tcell','pcell','vin', 'tempin', 'tempout']
  data.columns = ['date','time','gpsfix','gpsquality','lat','lon','speed','altitude','satfix','co2','tcell','pcell','vin', 'tempin', 'tempout', 'flag']
  # create a datetime column
  data['datetime'] = data['date'] + " " + data['time']
  # filter odd timestamps: everything less than the year 2020
  ts = [i for i in np.array(data['datetime']) if int(re.split('/|:| ',i)[2])  < 2020]
  data = pd.DataFrame(data[ data['datetime'].isin(ts)])
  # Round to nearest second
  data['datetime'] = pd.to_datetime(data['datetime'], format='%d/%m/%Y %H:%M:%S.%f')
  data['datetime'] = np.round(data['datetime'].astype(np.int64), -9).astype('datetime64[ns]')
  # Convert to ISO String
  data['datetime'] = map(lambda d: d.isoformat(), data.datetime)
  # Sort time Ascending
  data = data.sort(['datetime'], ascending=[True])
  # add in sensorid:
  data['sensorid'] = sensorid
  # Return enriched data
  print "CSV enriched!"

  return data

def filternull(data):
  pass

def getoname(sensorid,workspace):
  # Write the file out to a csv
  oName = [i for i in os.listdir(workspace) if os.path.isdir(os.path.join(workspace, i))]
  oName = workspace + "/" + sensorid + "_" + oName[0] + "_" + oName[-1] + ".csv"
  return oName

def rmfolders(workspace):
  [shutil.rmtree(os.path.join(root,dir)) for root, dirs, files in os.walk(workspace) for dir in dirs ]

''' ----- '''

def main():
  # # copy data to respective sensor id folder 
  # if sensorid == '0108':
  #   data_repo = fpath_0108
  #   workspace = workspace_0108
  # elif sensorid == '0205':
  #   data_repo = fpath_0205
  #   workspace = workspace_0205
  # elif sensorid == '0150':
  #   data_repo = fpath_0150
  #   workspace = workspace_0150
  # else:
  #   print "not a valid sensor id"

  # Get the repo files and the repo path based on the sd input
  for i in folders:
    if str(i.split('/')[-1][-4:]) == sensorid:
      data_repo = i
      # repo_path = i

  # Copy files from the repo to the workspace
  copyselection(data_repo, workspace, startDate, endDate)
  # merge the data from the workspace to 1 csv file
  data = merge2csv(workspace)
  # Enrich the csv
  data = enrichcsv(data, sensorid)
  # Export csv 
  oName = getoname(sensorid, workspace)
  data.to_csv(oName, index=True, index_label = 'rownum')
  print "merge2csv complete!"

  # delete unused data
  rmfolders(workspace)


if __name__ == '__main__':
  ''' ----- Set the repo path and the workspace paths ----- '''
  # fpath_0108 = '/Users/Jozo/Dropbox/projects/webpage/MobileCO2/Data/repo/Li820_0108'
  # fpath_0205 = '/Users/Jozo/Dropbox/projects/webpage/MobileCO2/Data/repo/Li820_0205'
  # fpath_0150 = '/Users/Jozo/Dropbox/projects/webpage/MobileCO2/Data/repo/Li820_0150'

  # workspace_0108 = '/Users/Jozo/Dropbox/projects/webpage/MobileCO2/Data/workspace/workspace_0108'
  # workspace_0150 = '/Users/Jozo/Dropbox/projects/webpage/MobileCO2/Data/workspace/workspace_0150'
  # workspace_0205 = '/Users/Jozo/Dropbox/projects/webpage/MobileCO2/Data/repo/Clumps'
  # ''' ----- change the sensor id ----- '''
  # # set the sensor id
  # sensorid = '0205'

  ''' ----- Set the repo path and the workspace paths ----- '''
  folders = [
  '/Users/Jozo/Dropbox/_Projects/ubc-micromet/DIYSCO2/private/data/LI820_0108',
  '/Users/Jozo/Dropbox/_Projects/ubc-micromet/DIYSCO2/private/data/LI820_0205',
  '/Users/Jozo/Dropbox/_Projects/ubc-micromet/DIYSCO2/private/data/LI820_0150',
  '/Users/Jozo/Dropbox/_Projects/ubc-micromet/DIYSCO2/private/data/LI820_0151',
  '/Users/Jozo/Dropbox/_Projects/ubc-micromet/DIYSCO2/private/data/LI820_1641'
  ]
  workspace = '/Users/Jozo/Dropbox/_Projects/ubc-micromet/DIYSCO2/private/data/Clumps'

  ''' ----- change the start and end date ----- '''
  startDate = '160318'
  endDate =  '160318'

  ''' ----- change the sensor id ----- '''
  # set the sensor id
  sensorid = '0108'
  # sensorid = '0205'
  # sensorid = '0150'
  # sensorid = '0151'
  # sensorid = '1641'

  # run main()
  main()


