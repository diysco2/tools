'''

Data Import script
Uses Linux/Unix Rsync called from Python subprocess module

# src =  "/Users/Jozo/Dropbox/_Projects/_GitHub/MobileCO2/Projects/Workspace/rsynctest/LI820_0150/"
# dest = "/Users/Jozo/Dropbox/_Projects/_GitHub/MobileCO2/Projects/Workspace/rsynctest/dest"
# cmd = [str("rsync" +' '+ '-r ' +" "+ src +" "+ dest)]
# subprocess.call(cmd, shell=True)

'''

import os, sys, subprocess

def rsyncfiles(src, dest):
	cmd = [str("rsync " + "-r " + "-v " + src + " " + dest)]
	subprocess.call(cmd, shell=True)
	

def main():

	# Get the folder path of SD
	fpath_sensor = [os.path.join(fpath_sd,i) for i in os.listdir(fpath_sd) if i[:5] == 'LI820'][0]
	fpath_sensor = fpath_sensor+"/"
	# Determine Destination folder
	repo_path = [i for i in folders if str(i.split('/')[-1]) == str(fpath_sensor.split('/')[-2])][0]
	# Call the Rsync
	rsyncfiles(fpath_sensor, repo_path)

if __name__ == '__main__':

	fpath_sd = '/Volumes/'
	folders = [
		'/Users/Jozo/Dropbox/_Projects/ubc-micromet/DIYSCO2/private/data/LI820_0108',
		'/Users/Jozo/Dropbox/_Projects/ubc-micromet/DIYSCO2/private/data/LI820_0205',
		'/Users/Jozo/Dropbox/_Projects/ubc-micromet/DIYSCO2/private/data/LI820_0150',
		'/Users/Jozo/Dropbox/_Projects/ubc-micromet/DIYSCO2/private/data/LI820_0151',
		'/Users/Jozo/Dropbox/_Projects/ubc-micromet/DIYSCO2/private/data/LI820_1641'
		]
	main()




	