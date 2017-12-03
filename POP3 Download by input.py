#!C:/Python27/python.exe

import poplib
import getpass
import StringIO, email   #stringIO £¬ mail
import os   #System move
import re   
import base64   #base64 Coding

print "POP downloader"
popsrv = raw_input('please input your mail server IP or Domain£º ')
addr = raw_input('please input your mail address£º')
passwd = getpass.getpass('Please input your password£º')




server=poplib.POP3(popsrv)
server.user(addr)
server.pass_(passwd)
emailNum,emailSize=server.stat()    #connect to the server and show stat
print 'email number is %d and size is %d'%(emailNum,emailSize)
filexc = os.path.exists(r"./mail/%s/"%addr)
if filexc is False:
    os.makedirs(r"./mail/%s/"%addr) #mkdir

    
for i in range(0,emailNum,1):
    emailrsp,emailmsg,emailsiz = server.retr(emailNum)  #download mails
#to find the title of mail
    for lines in emailmsg:
        titleprobe = re.match('Subject: ',lines)   #Subject: .*?\n
        if titleprobe is not None:
               orgtitle = lines.replace('Subject: ','')

#if english title
    gbflag = re.match('\w',orgtitle,1)
    if gbflag is not None:
        title = orgtitle
        print 'English Title'
            

                       
#if Chinese title find out it's what kind of code like GBK GB2312 or UTF-8
    if gbflag is None:
        schgb = orgtitle.find('=?GB2312?B?')+orgtitle.find('=?gb2312?B?')
        schutf = orgtitle.find('utf-8')+orgtitle.find('UTF-8')
        schgbk = orgtitle.find('=?gbk?B?')+orgtitle.find('=?GBK?B?')

            
        orgtitle = orgtitle.replace('?=','')
        orgtitle = orgtitle.replace('=?gb2312?B?','')
        orgtitle = orgtitle.replace('=?GB2312?B?','')
        orgtitle = orgtitle.replace('=?GB2312?b?','')
        orgtitle = orgtitle.replace('=?gb2312?b?','')
            
        orgtitle = orgtitle.replace('=?utf-8?B?','')
        orgtitle = orgtitle.replace('=?UTF-8?B?','')
        orgtitle = orgtitle.replace('=?utf-8?b?','')
        orgtitle = orgtitle.replace('=?UTF-8?b?','')
            
        orgtitle = orgtitle.replace('=?gbk?B?','')
        orgtitle = orgtitle.replace('=?GBK?B?','')
        orgtitle = orgtitle.replace('=?gbk?b?','')
        orgtitle = orgtitle.replace('=?GBK?b?','')


#the title of the mail often code by base64 ,try to decode	
            
        if schgb!=-2 and schutf==-2 and schgbk==-2:
            try:
                print 'gb2312 decode'
                orgtitle = base64.b64decode(orgtitle)
            except:
                pass


        elif schgb==-2 and schutf!=-2 and schgbk==-2:    
            try:
                orgtitle = base64.b64decode(orgtitle)
                print 'utfcode decode'
            except:
                pass
                
                
        elif schgb==-2 and schutf==-2 and schgbk!=-2:
            try:
                print 'gbkcode decode'
                orgtitle = base64.b64decode(orgtitle)
            except:
                pass
				
        elif schgb==-2 and schutf==-2 and schgbk==-2:
            orgtitle = 'notitle'
                

    orgtitle = orgtitle.replace(':','£º')
    orgtitle = orgtitle.replace('_','')
    orgtitle = orgtitle.replace('/','')
    orgtitle = orgtitle.replace("\\",'')
    orgtitle = orgtitle.replace("\\",'')
    orgtitle = orgtitle.replace('*','$')
    orgtitle = orgtitle.replace('?','£¿')
    orgtitle = orgtitle.replace('<','¡¶')
    orgtitle = orgtitle.replace('>','¡·')
    orgtitle = orgtitle.replace('|','')
    orgtitle = orgtitle.replace('"','¡°')
    orgtitle = orgtitle.replace(',','£¬')
    orgtitle = re.sub('[\/:*?"<>|]','-',orgtitle)
          

    print 'found title:"%s")'%orgtitle
    title = orgtitle
                
#put the name of mail into the xx.eml file's name

    try:
        fp = open("./mail/%s/(%d)"%(addr,emailNum)+title +".eml",'w')
        #fp = open('./mail/%s/(%d)%s.eml'%(addr,emailNum,title),'w')
            
    except IOError:
        print 'maybe utf8 error'

        try:
            title = title.decode('UTF-8')
        except UnicodeDecodeError:
            print 'Title may include error symbol'
            title = 'Unknow title'
            fp = open("./mail/%s/(%d)"%(addr,emailNum)+title +".eml",'w')
            for eachLine in emailmsg:   #output the data into .eml files
                fp.write('%s\n'%eachLine)

                
        else:
            print 'utf-8 encode done'
            fp = open("./mail/%s/(%d)"%(addr,emailNum)+title +".eml",'w')
            for eachLine in emailmsg:   #output the data into .eml files
                fp.write('%s\n'%eachLine)

    except:
        print 'unknow error'
        title = 'Unknow title'
        fp = open("./mail/%s/(%d)"%(addr,emailNum)+title +".eml",'w')
        for eachLine in emailmsg:   #output the data into .eml files
            fp.write('%s\n'%eachLine)


    else:
        for eachLine in emailmsg:   #output the data into .eml files
            fp.write('%s\n'%eachLine)

    fp.close()
    print '"%s" has download %d mails remain'%(title,emailNum)
    emailNum=emailNum-1
    print '-------------------------------------------------------------------'
    

print 'finished'
raw_input('press any button to quit')
