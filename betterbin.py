import pysftp
import os
from time import sleep
import stepper
from dotenv import load_dotenv

load_dotenv()

STEPS_PAPER = -1200 # big motor
STEPS_PLASTIC = 1200
STEPS_RESIDUAL = 0
STEPS_BOX = 100 # small motor

class Sftp:
    def __init__(self, hostname, username, password, port=22):
        self.connection = None
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port

    def connect(self):
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None

        try:
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
            print(f"connected to {self.hostname} as user {self.username}")

    def disconnect(self):
        self.connection.close()
        print(f"disconnected from {self.hostname}")

    def upload(self, source_local_path, remote_path):
        try:
            self.connection.put(source_local_path, remote_path)
            print(f"uploaded {source_local_path} to {self.hostname}")

        except Exception as err:
            raise Exception(err)

    def download(self, remote_path, target_local_path):
        try:
            self.connection.get(remote_path, target_local_path)
            print(f"downloaded {remote_path} from {self.hostname}")

        except Exception as err:
            raise Exception(err)

    def listdir(self, remote_path):
        return self.connection.listdir(remote_path)

sftp = Sftp('192.168.0.147', 'finn', os.environ.get('ENVY_PWD'))
sftp.connect()
currentPos = 1200

try:
    while True:
        if input() == 'next':
            os.system('raspistill -o img.jpg')
            sftp.upload('img.jpg', '/home/finn/prg/better-bin-pc/img.jpg')
            os.system('touch cmpl_upload')
            sftp.upload('cmpl_upload', '/home/finn/prg/better-bin-pc/cmpl_upload')

            ml_finished = False
            while not ml_finished:
                directory = sftp.listdir('/home/finn/prg/better-bin-pc/')
                if 'cmpl_ml' in directory:
                    ml_finished = True

            sftp.download('/home/finn/prg/better-bin-pc/solution.txt', 'solution.txt')

            file = open('solution.txt')
            category = file.readline()
            print(f'Image classified as {category}')

            if (category == 'paper'):
                stepper.doSteps(1, STEPS_PAPER - currentPos, 0.005)
                currentPos = STEPS_PAPER
            elif (category == 'plastic'):
                stepper.doSteps(1, STEPS_PLASTIC - currentPos, 0.005)
                currentPos = STEPS_PLASTIC
            else:
                stepper.doSteps(1, STEPS_RESIDUAL - currentPos, 0.005)
                currentPos = STEPS_RESIDUAL
            
            stepper.doSteps(2, 500, 0.01)
            stepper.doSteps(2, -500, 0.01)
            print(f"Current position: {currentPos}")

except KeyboardInterrupt:
    sftp.disconnect()
