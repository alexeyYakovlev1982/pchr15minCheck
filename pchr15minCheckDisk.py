#!/usr/bin/python
#pchr15minCheckDisk - check PCHRs files for 15 mins on Disk

import os, sys, subprocess, re

########### pchr15minChecker #############

def PCHRdirScan (folder, RNCPCHRfolder):
    global debug
    status = 1
    NoPCHRs = True
    try:
        PCHRfiles = os.listdir(folder + '/' + RNCPCHRfolder)
    except OSError:
        #print RNCPCHRfolder + ' is not a folder'
        return 2 # is not a folder

    if debug: print (">>>>> checking folder - " + RNCPCHRfolder)
    for PCHRfile in PCHRfiles:
        if 'PCHR' in PCHRfile:
            #print PCHRfile
            #print "file status is " + str(pchrFile15minCheckName(PCHRfile))
            NoPCHRs = False
            if pchrFile15minCheckName(PCHRfile) == 0: status = 0
    
    if NoPCHRs : status = 3       
    return status


############### pchrFile15minCheckName #################

def pchrFile15minCheckName(PCHRfileName):
    global debug
    global totalNumberOfNon15minPCHRs
    status = 0

    startMin = int(PCHRfileName[PCHRfileName.find('Log201')+13:PCHRfileName.find('Log201')+15])
    endMin = int(PCHRfileName[PCHRfileName.find('Log201')+28:PCHRfileName.find('Log201')+30])
    
    if endMin < 15: 
        endMin += 60
    
    if endMin - startMin == 15 : 
        if debug: print "               the file " + PCHRfileName + " was closed in 15 mins."
        return 1
    else:
        if debug: print "		the file " + PCHRfileName + " was not closed in 15 mins."
        totalNumberOfNon15minPCHRs += 1
        return 0

################ Usage ################    

def Usage():
    print ('!!!!! The usage is wrong. \nUsage examples:\npython pchr15minCheck.py /path/to/pchr/folder/\npython pchr15minCheck.py /path/to/pchr/folder/ debug')
    exit()


########### MAIN #############
if __name__ == '__main__':

    debug = False
    totalNumberOfNon15minPCHRs = 0

    if len(sys.argv) > 3 : Usage()
    
    if len(sys.argv) < 2: 
        folder = '/opt/raw_data/huawei/3g/pchr'
    else: folder = sys.argv[1]
    
    if len(sys.argv) == 3:
        if sys.argv[2] == 'debug': debug = True
        else: Usage()

    #print 'folder ' + folder

    pchrSubDirs = os.listdir(folder)
    
    finalStatus = 1

    for RNCPCHRfolder in pchrSubDirs:
        PCHRdirScanResult = PCHRdirScan(folder, RNCPCHRfolder)
        if PCHRdirScanResult == 0:
            if debug:  print ">>>>> The folder " + RNCPCHRfolder + " has non-15 mins PCHRs"
            finalStatus = 0
        if PCHRdirScanResult == 1:
            if debug: print ">>>>> The folder " + RNCPCHRfolder + " has fine 15 mins PCHRs"
        if PCHRdirScanResult == 2:
            if debug: print ">>>>> " + RNCPCHRfolder + " is not the folder"
        if PCHRdirScanResult == 3:
            if debug: print ">>>>> The folder " + RNCPCHRfolder + " does not have any PCHRs"

    if debug: print (finalStatus)
    if debug: print ("total number of non-15 mins PCHRs = " + str(totalNumberOfNon15minPCHRs))
    print (str(totalNumberOfNon15minPCHRs))






    #print ('END!!!')

