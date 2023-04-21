from ftplib import FTP
import os

class FTPDownloader:
    def __init__(self, ip, username, password):
        self.ip = ip
        self.username = username
        self.password =  password
        self.ftp = None
 
    def connect(self):
        """Establish an connection and return an FTP client object"""

        if self.ftp is None:
            self.ftp = FTP(self.ip)
            self.ftp.login(user=self.username, passwd=self.password)

        return self.ftp
        
    def download_files(self, local_path):
        ftp = self.connect()
        files = ftp.nlst()
        local_elements = os.listdir(local_path)
        for file in files:
            if self.check_file(file, local_elements):
                with open(f"{local_path}/{file}", "wb") as f:
                   ftp.retrbinary(f"RETR {file}", f.write)
            
    def check_file(self, file, local_elements):
        return len(file) > 3 and "." in file and file[0] != "." and file not in local_elements
