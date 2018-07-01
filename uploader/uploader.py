import abc
import ftplib
import ftputil
import ftputil.file_transfer
import paramiko
import socket
import os
import ftputil.tool
from ftputil.error import PermanentError, FTPOSError, FTPIOError
from paramiko.ssh_exception import NoValidConnectionsError

from .choices import ConnectionType


class Uploader(metaclass=abc.ABCMeta):
    @staticmethod
    def factory(info):
        if info.connection == ConnectionType.FTP:
            return FTPUploader(info)
        if info.connection == ConnectionType.SFTP:
            return SFTPUploader(info)
        if info.connection == ConnectionType.FTPS:
            return FTPSUploader(info)

    def __init__(self, info):
        self.username = info.username
        self.password = info.password
        self.host = info.host_address
        self.port = info.port
        self.client = None
        self.progress_callback = None
        self.retry_callback = None
        self.last_percent = 0
        self.retry = 0
        self.MAX_RETRIES = 3

    def set_progress_callback(self, cb):
        self.progress_callback = cb

    def set_retry_callback(self, cb):
        self.retry_callback = cb

    @abc.abstractmethod
    def connect(self):
        pass

    @abc.abstractmethod
    def upload(self, local, remote):
        pass

    @abc.abstractmethod
    def download(self, remote, local):
        pass

    @abc.abstractmethod
    def delete(self, path):
        pass

    @abc.abstractmethod
    def cd(self, directory):
        pass

    @abc.abstractmethod
    def pwd(self):
        pass

    @abc.abstractmethod
    def exists(self, file):
        pass


class FTPUploader(Uploader):
    def __init__(self, info):
        super().__init__(info)
        self.data_written = 0
        self.local_file_size = 0

    def connect(self):
        try:
            self.client = ftputil.FTPHost(self.host, self.username, self.password, self.port,
                                          session_factory=FTPPortSession)
        except PermanentError as ex:  # Connection issue
            if ex.errno == 530:
                raise AuthenticationFailure("Invalid credentials provided -- Please contact an Admin")

    def upload(self, local, remote):
        self.local_file_size = os.stat(local).st_size
        self.data_written = 0
        try:
            target = ftputil.tool.as_unicode(remote)
            source_file, target_file = self._upload_files(local, target)
            self.client.copyfileobj(source_file.fobj(), target_file.fobj(), callback=self.__progress_callback,
                                    max_chunk_size=10 * 64 * 1024)
        except FTPIOError as ex:
            raise TransmissionError(base_error=ex)

    def _upload_files(self, source_path, target_path):  # taken from ftputil hosts.py file
        source_file = ftputil.file_transfer.LocalFile(source_path, "rb")
        target_file = ftputil.file_transfer.RemoteFile(self.client, target_path, "wb")
        return source_file, target_file

    def download(self, remote, local):
        try:
            self.client.download(remote, local)
        except FTPIOError as ex:
            raise TransmissionError(base_error=ex)

    def delete(self, path):
        self.client.remove(path)

    def cd(self, directory):
        self.client.chdir(directory)

    def pwd(self):
        return self.client.getcwd()

    def exists(self, file):
        return self.client.path.exists(file)

    def __progress_callback(self, block):
        self.data_written += len(block)
        percent = round((self.data_written / self.local_file_size) * 100)
        if self.last_percent != percent:
            self.last_percent = percent
            if self.progress_callback is not None:
                self.progress_callback(percent)


class FTPSUploader(FTPUploader):
    def __init__(self, info):
        super().__init__(info)

    def connect(self):
        try:
            self.client = ftputil.FTPHost(self.host, self.username, self.password, self.port,
                                          session_factory=FTPTLSPortSession)
        except PermanentError as ex:  # Connection issue
            if ex.errno == 530:  # invalid username / pass
                raise AuthenticationFailure(base_error=ex)
            raise ex
        except FTPOSError as ex:
            if ex.args[0] == -2 or ex.args[0] == 113:  # Trouble connecting
                raise ConnectionFailure(base_error=ex)
            raise ex



class SFTPUploader(Uploader):

    def __init__(self, info):
        super().__init__(info)
        self.sftp = None
        self.channel = None

    def connect(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.client.connect(self.host, self.port, username=self.username, password=self.password,
                                look_for_keys=False)
            transport = self.client.get_transport()
            transport.default_window_size = paramiko.common.MAX_WINDOW_SIZE
            # transport.packetizer.REKEY_BYTES = pow(2, 40)  # 1TB max, this is a security degradation!
            # transport.packetizer.REKEY_PACKETS = pow(2, 40)  # 1TB max, this is a security degradation!
        except paramiko.AuthenticationException as ex:
            raise AuthenticationFailure()
        except paramiko.SSHException as ex:
            raise paramiko.SSHException(ex)
        except NoValidConnectionsError as ex:
            raise ConnectionFailure(ex)
        except socket.gaierror as ex:
            raise ConnectionFailure(ex)

        try:
            self.sftp = self.client.open_sftp()
            self.channel = self.sftp.get_channel()
            self.channel.settimeout(10.0)
        except paramiko.SSHException as ex:
            raise paramiko.SSHException(ex)

    def cd(self, directory):
        self.sftp.chdir(directory)

    def delete(self, path):
        self.sftp.remove(path)

    def download(self):
        pass

    def exists(self, file):
        pass

    def pwd(self):
        pass

    def upload(self, local, remote):
        return self.__upload(local, remote)

    def __upload(self, local, remote):
        try:
            self.sftp.put(local, remote, callback=self.__progress_callback, confirm=True)
            return True
        except socket.timeout:

            if self.retry < self.MAX_RETRIES:
                print("WE RETRYING")
                self.retry += 1
                if self.retry_callback is not None:
                    self.retry_callback(f"Retrying upload attempt {self.retry} of {self.MAX_RETRIES}")

                return self.__upload(local, remote)
        except:
            print("something else went wrong!")

    def __progress_callback(self, uploaded, total):
        percent = round((uploaded / total) * 100)
        if self.last_percent != percent:
            self.last_percent = percent
            if self.progress_callback is not None:
                self.progress_callback(percent)


class FTPPortSession(ftplib.FTP):
    def __init__(self, host, userid, password, port):
        ftplib.FTP.__init__(self)
        self.connect(host, port)
        self.login(userid, password)


class FTPTLSPortSession(ftplib.FTP_TLS):
    def __init__(self, host, userid, password, port):
        ftplib.FTP_TLS.__init__(self)
        self.connect(host, port)
        self.login(userid, password)
        self.prot_p()


# Exceptions

class CustomBaseException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.base_error = kwargs['base_error']


class AuthenticationFailure(CustomBaseException):
    pass


class ConnectionFailure(CustomBaseException):
    pass


class TransmissionError(CustomBaseException):
    pass