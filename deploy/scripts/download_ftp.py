import ftplib
import os

server = 'ftp.dataholics.com.mx'
user = 'dev-WNM@warhorsenm.dataholics.com.mx'
password = 'UILHDA=iDiaJ'

ftp = ftplib.FTP()
ftp.connect(server, 21, timeout=30)
ftp.login(user, password)
ftp.set_pasv(True)

ftp.cwd('/warhorse_app/app/Controllers/Api/V1')
with open('RequisicionesController_remote.php', 'wb') as f:
    ftp.retrbinary('RETR RequisicionesController.php', f.write)

ftp.quit()
