#RT to UT exchange script

#import part

import ftplib 
from ftplib import FTP
import os
import zipfile
from shutil import copyfile
try:
    import zlib
    compression = zipfile.ZIP_DEFLATED
except:
    compression = zipfile.ZIP_STORED

#config part
source_path = r'\\brc-1c-01\Exchange_RT_UT\Checked'
temp_path = r'D:\Upload'

#path create part
print ('RT to UT exchange script v1.1')

while True:
    unit = input('Enter RT UNIT: ').upper()

#are unit name ok?
    if len(unit) == 3 and unit.isalpha():
        break
    else:
        print('Error in unit name', unit, ', please re-enter it')

checked_fname = '\\Message_' + unit + '_CNT.xml'
xml_path = source_path + checked_fname 
zip_path = 'D:\\Upload'  + checked_fname [:-4] + '.zip'
print('XML path:', xml_path)

#copy .zip from FTP
ftp = FTP('brc-ftp-02.bristolcapital.ru')
print(ftp.login(user='Retail', passwd='#hjpybwf12)'))
with open(zip_path, 'wb') as f:
    print(ftp.retrbinary('RETR ' + os.path.basename(zip_path), f.write))
f.close()
print(ftp.quit())

#unzip file
zf = zipfile.ZipFile(zip_path, mode='r')
zf.extractall()

#copy file to checked
copyfile(temp_path + checked_fname, xml_path)

print('All files sucсessfully copied to destanation. Run synchronization at 1C.')

#End part
input('Press ENTER to quit')
