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
        
    def download_files(self, folder_path):
        newfiles = []
        ftp = self.connect()
        ftp.cwd("/tobollore")
        files = ftp.nlst()
        local_path = f"{folder_path}frombollore"
        for file in files:
            if self.check_file(file):
                with open(f"{local_path}/{file}", "wb") as f:
                   ftp.retrbinary(f"RETR {file}", f.write)
                file_size = os.path.getsize(f"{local_path}/{file}")
                file_desc = {"filename": file, "path": f"{local_path}/{file}", "size": file_size}
                newfiles.append(file_desc)
        ftp.cwd('..')
        return newfiles

    def check_file(self, file):
        return len(file) > 3 and "." in file and file[0] != "."


    def upload_file(self, file_path):
        ftp = self.connect()
        remote_path = "frombollore"
        print(f"{remote_path}/{os.path.basename(file_path)}")
        with open(file_path, "rb") as f:
            ftp.storbinary(f"STOR {remote_path}/{os.path.basename(file_path)}", f)