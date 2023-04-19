import os
import re
import paramiko

class SFTPDownloader:
    def __init__(self, hostname, port, username, password):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.ssh_transport = None
        self.current_dir = None
        self.sftp = None

    def connect(self):
        """Establish an SSH connection and return an SFTP client object"""
        if self.ssh_transport is None or not self.ssh_transport.is_active():
            self.ssh_transport = paramiko.Transport((self.hostname, self.port))
            self.ssh_transport.connect(username=self.username, password=self.password)
        
        if self.sftp is None or self.sftp.sock.closed:
            self.sftp = paramiko.SFTPClient.from_transport(self.ssh_transport)
        
        return self.sftp
    
    def download_files(self, local_path):
        sftp = self.connect()
        remote_path = f"{local_path.split('/')[-1]}"
        local_path = f"{local_path}/pending/"     
        if "trufa" in sftp.listdir() and remote_path in sftp.listdir("trufa"):
            if self.current_dir != f"trufa/{remote_path}":
                sftp.chdir('../..')
                sftp.chdir(f"trufa/{remote_path}")
                self.current_dir = f"trufa/{remote_path}"

            downloaded_files = set()
            suffixes = ["txt", "json", "xml"]
            for file in sftp.listdir():
                if file not in downloaded_files and re.search(fr"\.({'|'.join(suffixes)})$", file):
                    remote_file_path = file
                    local_file_path = os.path.join(local_path, file)
                    sftp.get(remote_file_path, local_file_path)
                    downloaded_files.add(file)
    
    def upload_files(self, local_dir, remote_dir):
        sftp = self.connect()
        try:
            sftp.chdir('../..')
            sftp.chdir(remote_dir)
        except IOError:
            sftp.mkdir(remote_dir)
            sftp.chdir(remote_dir)

        target_file = local_dir.split("/")[-1]
        sftp.put(local_dir, target_file)
        
    def close(self):
        """Close the SSH connection"""
        if self.sftp is not None:
            self.sftp.close()
            self.sftp = None
        
        if self.ssh_transport is not None:
            self.ssh_transport.close()
            self.ssh_transport = None