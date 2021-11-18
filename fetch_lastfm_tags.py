import pylast
import openpyxl
import os
import os.path
import operator

API_KEY = "dcc5bf7ecee79d43278e2b73781a9c26"  
API_SECRET = "601291923fd46dda602de733f497cc17"
USERNAME = "laazarus"
PASSWORD_HASH = pylast.md5("6w5T-FgJH8fB.fx")



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
    allGenreList = []
    genreList = []
    totalWeight = 0
    runningWeight = 0
    if(type == 'TR'):
        topItems = track.get_top_tags(limit=None)
        if(len(topItems) == 0):
            raise ValueError("No info found for this track")
        else:
            for topItem in topItems:
                allGenreList.append([topItem.item.get_name(), topItem.weight])
                #print(topItem.item.get_name(), topItem.weight)
            for i in range(0,len(allGenreList)):
                totalWeight += int(allGenreList[i][1])
            for i in range(0, len(allGenreList)):
                if(runningWeight/totalWeight <= 0.90):
                    runningWeight += int(allGenreList[i][1])
                    genreList.append([allGenreList[i][0], allGenreList[i][1]])
                else:
                    break
            return genreList
    elif(type == 'AR'):
        topArtistItems = artist.get_top_tags(limit=None)
        if(len(topArtistItems) == 0):
            raise ValueError("No info found for this artist")
        else:
            for topItem in topArtistItems:
                    allGenreList.append([topItem.item.get_name(), topItem.weight])
                    #print(topItem.item.get_name(), topItem.weight)
            for i in range(0,len(allGenreList)):
                totalWeight += int(allGenreList[i][1])
            for i in range(0, len(allGenreList)):
                if(runningWeight/totalWeight <= 0.90):
                    runningWeight += int(allGenreList[i][1])
                    genreList.append([allGenreList[i][0], allGenreList[i][1]])
                else:
                    break
            return genreList

def updateTagDictionary(tagList, dictionary,normalized_dictionary):
    totalSum = 0
    for tag in tagList:
        if dictionary.get(tag[0]) is not None:
            dictionary[tag[0]] += int(tag[1])
        else:
            dictionary[tag[0]] = int(tag[1])
    for tag in dictionary.keys():
        totalSum += dictionary[tag]
    for tag in dictionary.keys():
        normalized_dictionary[tag] = dictionary[tag] / totalSum

def findGenre(PATH):
    STARTING_ROW = 3
    ARTIST_COLUMN = 3
    TOTAL_ROWS_COLUMN = 5
    LASTFM_GENRE_COLUMN = 6
    LASTFM_INFO_COLUMN = 7
    NORMALIZED_TAG_COUNT_COLUMN = 8
    TRACK_COLUMN = 2
    for root, dirs, files in os.walk(PATH):
        for File in files:
            try:
                TAG_DICTIONARY = dict()
                NORMALIZED_TAG_DICTIONARY = dict()
                root = root.replace("\\","/")
                dataFilePath = f"{root}{File}"
                print(f"Now Querying Last.fm with all the entries in -- {dataFilePath}")
                wb = openpyxl.load_workbook(dataFilePath)
                sheet = wb.active
                totalQueried = 0
                totalQueriedByTrack = 0
                totalQueriedByArtist = 0
                lastfm_info_cell = sheet.cell(row=STARTING_ROW, column=LASTFM_INFO_COLUMN)
                totalRows = int(sheet.cell(row=STARTING_ROW, column=TOTAL_ROWS_COLUMN).value)+1
                for row in range(STARTING_ROW, totalRows):
                    try:
                        lastfm_genre_cell = sheet.cell(row=row, column=LASTFM_GENRE_COLUMN)
                        artist = sheet.cell(row=row, column=ARTIST_COLUMN).value
                        track = sheet.cell(row=row, column=TRACK_COLUMN).value
                        print(artist, track)
                        lastfm_artist = network.get_artist(artist)
                        lastfm_track = network.get_track(title=track, artist=artist)
                        lastfm_genreByTrack = findGenreByTrackOrArtist('TR', lastfm_artist, lastfm_track)
                        lastfm_genre_cell.value = f'TRACK - {lastfm_genreByTrack}'
                        #wb.save(dataFilePath)
                        totalQueried += 1
                        totalQueriedByTrack += 1
                        print(f"FOUND GENRE (TRACK) [{lastfm_artist} - {lastfm_track}] -- {lastfm_genreByTrack}")
                        updateTagDictionary(lastfm_genreByTrack, TAG_DICTIONARY, NORMALIZED_TAG_DICTIONARY)
                        if(row == totalRows - 1):
                            NORMALIZED_TAG_DICTIONARY = dict(sorted(NORMALIZED_TAG_DICTIONARY.items(), key=operator.itemgetter(1),reverse=True))
                        sheet.cell(row=STARTING_ROW, column=NORMALIZED_TAG_COUNT_COLUMN).value = f'{NORMALIZED_TAG_DICTIONARY}'
                        wb.save(dataFilePath)
                    except:
                        try:
                            lastfm_genreByArtist = findGenreByTrackOrArtist('AR', lastfm_artist, lastfm_track)
                            lastfm_genre_cell.value = f'ARTIST - {lastfm_genreByArtist}'
                            #wb.save(dataFilePath)
                            totalQueried += 1
                            totalQueriedByArtist += 1
                            print(f"FOUND GENRE (ARTIST) [{lastfm_artist} - {lastfm_track}] -- {lastfm_genreByArtist}")
                            updateTagDictionary(lastfm_genreByArtist, TAG_DICTIONARY, NORMALIZED_TAG_DICTIONARY)
                            if(row == totalRows - 1):
                                TAG_DICTIONARY = dict(sorted(NORMALIZED_TAG_DICTIONARY.items(), key=operator.itemgetter(1),reverse=True))
                            sheet.cell(row=STARTING_ROW, column=NORMALIZED_TAG_COUNT_COLUMN).value = f'{NORMALIZED_TAG_DICTIONARY}'
                            wb.save(dataFilePath)
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
                wb.save(dataFilePath)
                print("Error Opening File")
findGenre("../fingerprinter/GTZAN-Last.fm Genres/")
