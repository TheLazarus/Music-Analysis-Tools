import os
import os.path
import shutil
import subprocess

MUSIC_PATH = ''
SPLIT_PATH = ''
SPLIT_PATH2 = ''

def splitFile():
    fileNum = 1
    for root, dirs, files in os.walk(MUSIC_PATH):
        print('Looking in:',root)
        for File in files:
            try:
                root = root.replace("\\","/")
                print(root)
                print(f"ffmpeg -t 30 -i '{root}/{File.strip()}'"+f" -acodec copy '{str(SPLIT_PATH)+str(fileNum)}.mp3'")
                command = f"ffmpeg -i '{root}/{File.strip()}'"+f"-ss 00:01:30 -to 00:02:00 '{str(SPLIT_PATH)+str(fileNum)}.mp3'"
                subprocess.run(["powershell", "-Command", command], capture_output=True)
                fileNum+=1
            except:
                print("Error")
                return None
def splitParts():
    fileNum = 30
    for root, dirs, files in os.walk(MUSIC_PATH):
        print('Looking in:',root)
        for File in files:
            try:
                root = root.replace("\\","/")
                path = str(SPLIT_PATH2)+f'output_audio{fileNum}file_%05d.mp3'
                command = f"ffmpeg -i '{root}/{File}' -f segment -segment_time 30 -c copy '{path}'"
                print(command)
                subprocess.run(["powershell", "-Command", command], capture_output=True)
                fileNum+=1
            except:
                print("Error")
                return None
                

    

splitParts()