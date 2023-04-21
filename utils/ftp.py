
class FTPDownloader:
    def __init__(self, ip, username, password):
 
 ftp = FTP(ip)
    ftp.login(user=username, passwd=password)
    
    if action == "Upload":
        ftp.storbinary(f"STOR {file.filename}", file.file)
    
    elif action == "Download":
        files = ftp.nlst()
        for file in files:
            if len(file)>3 and "." in file:
                with open(f"folder/{file}", "wb") as f:
                    ftp.retrbinary(f"RETR {file}", f.write)
        
    ftp.quit()
    
    return {"message": f"File {action}ed successfully"}