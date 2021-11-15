import os
import os.path
import shutil
import csv

TRACK_METADATA_PATH = ''
GENRE_METADATA_PATH = ''
TRACK_ID_COLUMN = 0
TRACK_GENRE_COLUMN = 42
GENRE_ID_COLUMN = 0
GENRE_NAME_COLUMN = 3
FMA_PATH = ''
FMA_SORTED_PATH = ''

genres = {}

genre_file = open(GENRE_METADATA_PATH, newline='', encoding='utf-8')
reader = csv.reader(genre_file)

header = next(reader)
for row in reader:
    genres[row[GENRE_ID_COLUMN]] = row[GENRE_NAME_COLUMN]

tracks_file = open(TRACK_METADATA_PATH, newline='', encoding='utf-8')
reader = csv.reader(tracks_file)

track_genres = {}

header = next(reader)
for row in reader:
    split_string = row[TRACK_GENRE_COLUMN][1:-1].strip().split(",")
    track_genre_top = split_string[0]
    if(track_genre_top in genres.keys()):
        track_genres[row[TRACK_ID_COLUMN].zfill(6)] = genres[track_genre_top]

def searchFile(fileName):
    for root, dirs, files in os.walk(FMA_PATH):
        print('Looking in:',root)
        for Files in files:
            try:
                found = Files.find(fileName)
                if found != -1:
                   return f"{root}/{fileName}"
            except:
                return None

def make_and_move(track_genres):
    print("Creating Genre Folders...")
    os.chdir(FMA_SORTED_PATH)
    fileli = os.listdir()
    for genre in genres:
        genre = genres[genre]
        os.mkdir(genre)
    print("Successfully created folders!")
    for track in track_genres:
        print(f"Finding {track}.mp3")
        filePath = searchFile(track)
        if(filePath):
            filePath = filePath+'.mp3'
            print(f"Found {track}.mp3 in {filePath}")
            print(f"Now Copying {track}.mp3 ... to {FMA_SORTED_PATH}/{track_genres[track]}")
            genre_path = f"{FMA_SORTED_PATH}/{track_genres[track]}/"
            shutil.copy(filePath, genre_path)
            print(f"Successfully Copied {track}.mp3")
            
        else:
            print(f"Unable to find {track}")

    

make_and_move(track_genres)



     
   
