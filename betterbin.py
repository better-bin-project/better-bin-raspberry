import pysftp
import os
from time import sleep
import stepper
from dotenv import load_dotenv

load_dotenv()

STEPS_1 = 100 # big motor
INTERVAL_1 = 0.05
STEPS_2 = 100 # small motor
INTERVAL_2 = 0.05

class Sftp:
    def __init__(self, hostname, username, password, port=22):
        """Constructor Method"""
        # Set connection object to None (initial value)
        self.connection = None
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port

    def connect(self):
        """Connects to the sftp server and returns the sftp connection object"""
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None

        try:
            # Get the sftp connection object
            self.connection = pysftp.Connection(
                host=self.hostname,
                username=self.username,
                password=self.password,
                port=self.port,
                cnopts=cnopts,
            )
        except Exception as err:
            raise Exception(err)
        finally:
            print(f"Connected to {self.hostname} as {self.username}.")

    def disconnect(self):
        """Closes the sftp connection"""
        self.connection.close()
        print(f"Disconnected from host {self.hostname}")

    def upload(self, source_local_path, remote_path):
        """
        Uploads the source files from local to the sftp server.
        """

        try:
            print(
                f"uploading to {self.hostname} as {self.username} [(remote path: {remote_path});(source local path: {source_local_path})]"
            )

            # Download file from SFTP
            self.connection.put(source_local_path, remote_path)
            print("upload completed")

        except Exception as err:
            raise Exception(err)

    def download(self, remote_path, target_local_path):
        """
        Downloads the file from remote sftp server to local.
        Also, by default extracts the file to the specified target_local_path
        """

        try:
            print(
                f"downloading from {self.hostname} as {self.username} [(remote path : {remote_path});(local path: {target_local_path})]"
            )

            # Download from remote sftp server to local
            self.connection.get(remote_path, target_local_path)
            print("download completed")

        except Exception as err:
            raise Exception(err)

print(os.environ.get('ENVY_PWD'))
sftp = Sftp('192.168.0.147', 'finn', os.environ.get('ENVY_PWD'))
sftp.connect()

try:
    os.system('raspistill -o img.jpg')
    sftp.upload('img.jpg', '/home/finn/prg/better-bin-pc/img.jpg')
    os.system('touch cmpl')
    sftp.upload('cmpl', '/home/finn/prg/better-bin-pc/cmpl')
    sleep(4)
    sftp.download('/home/finn/prg/better-bin-pc/solution.txt', 'solution.txt')

    file = open('solution.txt')
    category = file.readline()
    print(f'Image classified as {category}')

    if (category == 'paper'):
        pass
    elif (category == 'plastic'):
        pass
    else:
        pass

    stepper.doSteps(2, STEPS_2, INTERVAL_2)
    stepper.reverse(2)
    stepper.doSteps(2, STEPS_2, INTERVAL_2)

    sftp.disconnect()
except KeyboardInterrupt:
    sftp.disconnect()
