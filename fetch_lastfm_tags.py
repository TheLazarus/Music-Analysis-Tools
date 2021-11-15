import pylast
import openpyxl
import os
import os.path

API_KEY = ""  
API_SECRET = ""
USERNAME = ""
PASSWORD_HASH = pylast.md5("")

def setupLast(API_KEY, API_SECRET, username, password_hash):
    network = pylast.LastFMNetwork(
    api_key=API_KEY,
    api_secret=API_SECRET,
    username=username,
    password_hash=password_hash,
)

    return network

network = setupLast(API_KEY, API_SECRET, USERNAME, PASSWORD_HASH)

def findGenreByTrackOrArtist(type, artist, track):
    allGenreList = [type]
    genreList = [type]
    totalWeight = 0
    runningWeight = 0
    if(type == 'TR'):
        topItems = track.get_top_tags(limit=None)
        for topItem in topItems:
            allGenreList.append((topItem.item.get_name(), topItem.weight))
            # print(topItem.item.get_name(), topItem.weight)
        for i in range(1,len(allGenreList)):
            totalWeight += int(allGenreList[i][1])
        for i in range(1, len(allGenreList)):
            if(runningWeight/totalWeight <= 0.95):
                runningWeight += int(allGenreList[i][1])
                genreList.append(allGenreList[i][0])
            else:
                break
        return genreList[1]
    elif(type == 'AR'):
        topArtistItems = artist.get_top_tags(limit=None)
        for topItem in topArtistItems:
                allGenreList.append((topItem.item.get_name(), topItem.weight))
                # print(topItem.item.get_name(), topItem.weight)
        for i in range(1,len(allGenreList)):
            totalWeight += int(allGenreList[i][1])
        for i in range(1, len(allGenreList)):
            if(runningWeight/totalWeight <= 0.95):
                runningWeight += int(allGenreList[i][1])
                genreList.append(allGenreList[i][0])
            else:
                break
        return genreList[1]

def findGenre(PATH):
    STARTING_ROW = 3
    ARTIST_COLUMN = 3
    LASTFM_GENRE_COLUMN = 5
    LASTFM_INFO_COLUMN = 6
    TRACK_COLUMN = 2
    for root, dirs, files in os.walk(PATH):
        for File in files:
            try:
                root = root.replace("\\","/")
                dataFilePath = f"{root}{File}"
                print(f"Now Querying Last.fm with all the entries in -- {dataFilePath}")
                wb = openpyxl.load_workbook(dataFilePath)
                sheet = wb.active
                totalQueried = 0
                totalQueriedByTrack = 0
                totalQueriedByArtist = 0
                lastfm_info_cell = sheet.cell(row=STARTING_ROW, column=LASTFM_INFO_COLUMN)
                for row in range(STARTING_ROW, sheet.max_row+1):
                    
                    lastfm_genre_cell = sheet.cell(row=row, column=LASTFM_GENRE_COLUMN)
                    
                    try:
                        artist = sheet.cell(row=row, column=ARTIST_COLUMN).value
                        track = sheet.cell(row=row, column=TRACK_COLUMN).value
                        print(artist, track)
                        lastfm_artist = network.get_artist(artist)
                        lastfm_track = network.get_track(title=track, artist=artist)
                        lastfm_genreByTrack = findGenreByTrackOrArtist('TR', lastfm_artist, lastfm_track)
                        lastfm_genre_cell.value = f'TR {lastfm_genreByTrack}'
                        wb.save(dataFilePath)
                        totalQueried += 1
                        totalQueriedByTrack += 1
                        print(f"FOUND GENRE (TRACK) [{lastfm_artist} - {lastfm_track}] -- {lastfm_genreByTrack}")
                    except:
                        try:
                            lastfm_genreByArtist = findGenreByTrackOrArtist('AR', lastfm_artist, lastfm_track)
                            lastfm_genre_cell.value = f'AL {lastfm_genreByArtist}'
                            wb.save(dataFilePath)
                            totalQueried += 1
                            totalQueriedByArtist += 1
                            print(f"FOUND GENRE (ARTIST) [{lastfm_artist} - {lastfm_track}] -- {lastfm_genreByArtist}")
                        except:
                            lastfm_genre_cell.value = 'N/A'
                            wb.save(dataFilePath)
                            print("No information found")
                print(f"Total Song Genres Found - {totalQueried} / {sheet.max_row - STARTING_ROW + 1}")
                print(f"Total Song Genres Found (By Track) - {totalQueriedByTrack}")
                print(f"Total Song Genres Found (By Artist) - {totalQueriedByArtist}")
                lastfm_info_cell.value = f'Total Song Genres Found - {totalQueried} / {sheet.max_row - STARTING_ROW + 1}, Found By Track - {totalQueriedByTrack}, Found By Artist - {totalQueriedByArtist}'
                wb.save(dataFilePath)
            except:
                lastfm_genre_cell = 'N/A File Error'
                wb.save(dataFilePath)
                print("Error Opening File")
findGenre("")
