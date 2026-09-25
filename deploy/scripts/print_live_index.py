import ftplib

def print_live_index():
    server = 'ftp.dataholics.com.mx'
    user = 'dev-WNM@warhorsenm.dataholics.com.mx'
    password = 'UILHDA=iDiaJ'
    
    print("Connecting to FTP...")
    ftp = ftplib.FTP()
    ftp.connect(server, 21, timeout=30)
    ftp.login(user, password)
    ftp.set_pasv(True)
    
    ftp.cwd('public_html')
    
    # We retrieve the index.html from the FTP and print its contents
    contents = []
    ftp.retrbinary('RETR index.html', contents.append)
    html_text = b"".join(contents).decode('utf-8')
    print("\n--- index.html on FTP server ---")
    print(html_text)
    print("---------------------------------")
    
    ftp.quit()

if __name__ == '__main__':
    print_live_index()
