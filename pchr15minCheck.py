#pchr15minCheck - check PCHRs files on FTP/SFTP
#lftp should be installed

import os, sys, subprocess, re

########### pchr15minChecker #############

def pchr15minChecker(IP='127.0.0.1', mode='ftp', login='user', password='password', folder='/bam/common/fam/famlogfmt/pchr/'):
    #print '-----------------'
    #print 'mode ' + mode
    #print 'login ' + login
    #print 'password ' + password
    #print 'folder ' +  folder

    lftpString = 'lftp -c "set net:max-retries 4;open -u {0},{1} {2}://{3}; ls {4}*zip"'.format(login, password, mode, IP, folder)
    #print lftpString
    
    lftpResult = os.popen(lftpString).read()
    
    try:
        minutes = [int(line[3:]) for line in lftpResult.split() if re.match('\d{2}:\d{2}',line)]
        base_minutes = [ (x*15 + min(minutes)) for x in range(0,4) ]
    except:
        print ('Connection problem! Did not get list of PCHRs!')
        return 0

    if len(minutes) < 10:
        print ('Did not get list of PCHRs!')
        return 0

    status = 1 # status = 1 - means OK - PCHRs are closed every 15 mins

    for minute in minutes:
        if minute not in base_minutes: status = 0 # status = 0 - means NOT_OK - PCHRs are closed every 15 mins
    
    return status

################ Usage ################    

def Usage():
    print ('!!!!! The usage is wrong. \nUsage examples:\npython pchr15minCheck.py 172.23.24.72\npython pchr15minCheck.py 172.23.24.72 mftp login password\npython pchr15minCheck.py 172.23.24.72 mftp login password /folder/to/pchr')
    exit()


########### MAIN #############
if __name__ == '__main__':
    
    IP = '172.23.24.72'
    mode = 'ftp'
    login = 'FtpUsr'
    password = '11111111'
    folder = '/bam/common/fam/famlogfmt/pchr/'
    
    #print sys.argv[1]
    IP = sys.argv[1]
    if not re.match('\d+.\d+.\d+.\d+', IP): Usage() 
    if len(sys.argv) > 2:
        mode = sys.argv[2]
        #print 'mode ' + mode
        login = sys.argv[3]
        #print 'login ' + login
        password = sys.argv[4]
        #print 'password ' + password

        if mode <> 'ftp' and mode <> 'sftp': Usage()

    if len(sys.argv) > 5: 
        folder = sys.argv[5]
        #print 'folder ' + folder
    
    print pchr15minChecker(IP=IP,mode=mode,login=login,password=password,folder=folder)

