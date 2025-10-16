# This is where the entry point of your solution should be
import os, json, csv, re
#Task 0.1
def main_menu():

    print(f"""1. Get All Artists
2. Get All Albums By An Artist
3. Get Top Tracks By An Artist
4. Export Artist Data
5. Get Released Albums By Year
6. Analyze Song Lyrics
7. Calculate Longest Unique Word Sequence In A Song
8. Weather Forecast For Upcoming Concerts
9. Search Song By Lyrics
10. Exit""")
    option = input("Type your option: ")

    match option:
        case "1":
            list_artists()
        case "2":
            get_albums()
        case "3":
            get_top_tracks()
        case "4":
            export_artist()
        case "5":
            get_albums_year()
        case "6":
            analyze_lyrics()
        case "7":
            calculate_word()
        case "8":
            get_forecast()
        case "9":
            search_song()
        case "10":
            print("Thank you for using Mooziq! Have a nice day :)")
            return False
        case _:
            print("Invalid choice! Try again.")
    
    return True
        


#Task 1

#display: turns logging on and off
def list_artists(display = True, display_artists = True, reverse = False):
    artists = {}
    if display:
        print("Artists found in the database:")
    for artist_file in sorted(os.listdir("dataset/artists")):
        with open("dataset/artists/" + artist_file, "r", encoding="utf-8") as current_file:
            info = json.load(current_file)
            if display_artists:
                print(f"- {info["name"]}")

        if reverse:
            artists[info["id"]] = {"name":info["name"],"genres":info["genres"]}
        else:
            artists[info["name"].lower()] = {"id":info["id"],"name":info["name"],"genres":info["genres"]}

    return artists

#Task 2
def get_albums(display = True, artist = None):
    
    if not display:
        artist_id = list_artists(display = False, display_artists = False)
    else:
        artist_id = list_artists(display=False)

    if artist == None:
        artist = input("Please input the name of one of the following artists: ").strip()

    matched_albums = []

    if artist.lower() not in artist_id:
        print("Invalid. Try again")
        return

    for album_file in sorted(os.listdir("dataset/albums")):
        if album_file[:-5] == artist_id[artist.lower()]["id"]:

            with open("dataset/albums/" + album_file, "r", encoding="utf-8") as opened_file:
                all_albums = json.load(opened_file)

            if display:
                print(f"Listing all available albums from {artist_id[artist.lower()]["name"]}...")

            for album in all_albums["items"]:
                matched_albums.append(album)

                if display:
                    title = album["name"]
                    date = album["release_date"] #format date YYYY-MM-DD to "August 3rd 2020"
                    group = date.split("-") #splits into: ["YYYY", "MM", "DD"] index 0, 1, 2
                    year = group[0]
                    month = group[1]
                    day = group[2]

                    month_formatted = 0

                    month_names = {
                        "01": "January",
                        "02": "February",
                        "03": "March",
                        "04": "April",
                        "05": "May",
                        "06":"June",
                        "07": "July",
                        "08": "August",
                        "09": "September",
                        "10": "October",
                        "11": "November",
                        "12": "December"
                    }

                    if month in month_names:
                        month_formatted = month_names[month]

                    if day[0] != "1":
                        if day[1] == "1":
                            suffix = "st"
                        elif day[1] == "2":
                            suffix = "nd"
                        elif day[1] == "3":
                            suffix = "rd"
                        else:
                            suffix = "th"
                    else:
                        suffix = "th"

                    pattern = r"\b0"

                    formatted_day = re.sub(pattern, "", day)

                    
                    print(f"- \"{title}\" was released in {month_formatted} {formatted_day}{suffix} {year}.")

            return matched_albums

#Task 3

#display: turns logging on and off
#chosen_artist: if a chosen_artist is given as parameter, asking for input is skipped
def get_top_tracks(display = True, chosen_artist = None):
    artists = list_artists(display=False) if display else list_artists(display=False,display_artists=False)
    
    if not chosen_artist: chosen_artist = input("Please input the name of one of the following artists: ")

    if chosen_artist.lower() in artists.keys():
        artist_id = artists[chosen_artist.lower()]["id"]
    else:
        print("Invalid artist entered.")
        return

    with open("dataset/top_tracks/" + artist_id + ".json", "r", encoding="utf-8") as tracks_file:
        dictionary = json.load(tracks_file)

    if display:
        print(f"Listing top tracks for {artists[chosen_artist.lower()]["name"]}...")

    tracks = []
    for track in dictionary["tracks"]:

        tracks.append((track["popularity"],track["name"]))

        if display:
            if track["popularity"] <= 30:
                print(f'- "{track["name"]}" has a popularity score of {track["popularity"]}. No one knows this track.')
            elif track["popularity"] <= 50:
                print(f'- "{track["name"]}" has a popularity score of {track["popularity"]}. Popular song.')
            elif track["popularity"] <= 70:
                print(f'- "{track["name"]}" has a popularity score of {track["popularity"]}. It is quite popular now!')
            elif track["popularity"] > 70:
                print(f'- "{track["name"]}" has a popularity score of {track["popularity"]}. It is made for the charts!')

    return tracks

#Task 4

def export_artist():
    artists = list_artists(display=False)

    chosen_artist = input("Please input the name of one of the following artists: ")

    if chosen_artist.lower() in [name.lower() for name in artists.keys()]:
        
        #Create row

        artist_id = artists[chosen_artist.lower()]["id"]
        number_of_albums = len(get_albums(display=False,artist=chosen_artist))
        top_tracks = get_top_tracks(display=False,chosen_artist=chosen_artist)
        top_track_1 = top_tracks[0][1]
        top_track_2 = top_tracks[1][1]
        genres = ",".join(artists[chosen_artist.lower()]["genres"])

        artist_data = [artist_id, chosen_artist.title(), number_of_albums, top_track_1, top_track_2, genres]

        #Export

        print(f'Exporting "{chosen_artist.title()}" data to CSV file...')

        if os.path.isfile("dataset/artist-data.csv"):

            artist_row = None
            csv_data = []

            with open("dataset/artist-data.csv", 'r') as file:
                csv_reader = csv.reader(file)

                for row in csv_reader:
                    if row[1].lower() == chosen_artist.lower():
                        artist_row = csv_reader.line_num - 1
                    csv_data.append(row)

            with open("dataset/artist-data.csv", 'w', newline='') as file:
                csv_writer = csv.writer(file)

                if type(artist_row) == int:
                    csv_data[artist_row] = artist_data
                    csv_writer.writerows(csv_data)
                    print("Data successfully updated.")
                else:
                    csv_data.append(artist_data)
                    csv_writer.writerows(csv_data)
                    print("Data successfully appended.")

        else:
            csv_header = ["artist_id","artist_name","number_of_albums","top_track_1","top_track_2","genres"]

            with open("dataset/artist-data.csv", "w+", newline='') as file:
                writer = csv.writer(file)
                writer.writerow(csv_header)
                writer.writerow(artist_data)
                print("Data successfully appended.")
        
    else:
        print(f"Error: {chosen_artist} not found in artists list.")
        return

#Task 5

def get_albums_year():
    
    artists = list_artists(display=False,display_artists=False,reverse=True)
    chosen_year = input("Please enter a year: ")

    albums = []
    for album_file in sorted(os.listdir("dataset/albums")):

        with open("dataset/albums/" + album_file, "r", encoding='utf-8') as file:
            albums_json = json.load(file)

        for album in albums_json["items"]:

            if album["release_date"][:4] == chosen_year:

                artist_name = artists[album_file.split(".")[0]]["name"]
                albums.append((album["name"],artist_name))
    if len(albums) == 0:
        print(f"No albums were released in the year {chosen_year}.")
        return None
    
    albums.sort()

    print(f"Albums released in the year {chosen_year}:")
    for album_name, album_artist in albums:
        print(f'- "{album_name}" by {album_artist}.')


#Task 6
lyrics = 0

def analyze_lyrics():
    songs = []
    for songs_file in sorted(os.listdir("dataset/songs")):
        with open("dataset/songs/" + songs_file, "r", encoding= "utf-8") as lyrics_file:
            all_lyrics = json.load(lyrics_file)
            songs.append(all_lyrics)

    print("Available songs:")
    for i in range(len(songs)):
        print(f"{i+1}. {songs[i]["title"]} by {songs[i]["artist"]}")
    
    index = int(input("Please select one of the following songs (number): ")) - 1
    if index not in range(len(songs)):
        print("Invalid choice.")
        return
    else:
         moosifying_lyrics(songs[index])

def moosifying_lyrics(song_data):
        
    lyrics = song_data["lyrics"]
    pattern = r"(\w+)([\!\?])|mo|Mo"
    
    if not re.findall(pattern, lyrics):
        print(f"{song_data["title"]} by {song_data["artist"]} is not moose-compatible!")
    
    else:

        replacement = r"moo\2"
    
        text = re.sub(pattern, replacement, lyrics)

        if not os.path.exists("./moosified"):
            os.makedirs("./moosified")
        
        with open(f"moosified/{song_data["title"]} Moosified.txt", "w+") as moose_file:
            moose_file.write(text)

        print(f"{song_data["title"]} by {song_data["artist"]} has been moos-ified!")
        print(f"File saved at ./moosified/{song_data["title"]} Moosified.txt")
        moose = r""" ___            ___
/   \          /   \
\_   \        /  __/
 _\   \      /  /__
 \___  \____/   __/
     \_       _/
       | @ @  \__
       |
     _/     /\
    /o)  (o/\ \__
    \_____/ /
      \____/
"""
        print(moose)


#Task 7
        
def calculate_word():

    all_songs = []
    for song_file in sorted(os.listdir("dataset/songs")):

        with open("dataset/songs/" + song_file, "r", encoding="utf-8") as file:
            song_json = json.load(file)
            all_songs.append(song_json)

    print("Available songs:")
    for i in range(len(all_songs)):
        song_data = all_songs[i]
        print(f"{i+1}. {song_data["title"]} by {song_data["artist"]}")
    
    try:
        choice = int(input("Please select one of the following songs (number): "))
    except ValueError:
        print("ERROR: Input is not a number.")
        return None

    if choice > len(all_songs) or choice < 1:
        print("ERROR: Invalid song chosen.")
        return None
    
    chosen_song_data = all_songs[choice-1]
    lyrics = chosen_song_data["lyrics"].lower()
    
    lyrics = re.sub(r"['?!.,\(\)]", "", lyrics)
    lyrics = re.sub(r"[\r\n]", " ", lyrics)
    lyrics = re.sub(r"\s+", " ", lyrics)

    longest_seq = 0
    current_seq = []
    for word in lyrics.split():

        if word not in current_seq:
            current_seq.append(word)

        elif len(current_seq) > longest_seq:
            longest_seq = len(current_seq)
            current_seq = current_seq[current_seq.index(word)+1:]
            current_seq.append(word)

        else:
            current_seq = current_seq[current_seq.index(word)+1:]
            current_seq.append(word)
        
    print(f"The length of the longest unique sequence in {chosen_song_data["title"]} is {longest_seq}")
            
#Task 8
def get_forecast():
    #list concerts
    upcoming_artists = []
    with open("dataset/concerts/concerts.csv", "r", encoding="utf-8") as concerts_file:
        all_concerts = csv.DictReader(concerts_file)
        print("Upcoming artists: ")
        for row in all_concerts:
            artist = row["artist"]
            if artist not in upcoming_artists:
                upcoming_artists.append(row["artist"])
        for artist in upcoming_artists:
            print(f"- {artist}")
    chosen_artist = input("Please input the name of one of the following artists: ")
    

    #opening weather csv
    with open("dataset/weather/weather.csv", "r", encoding="utf-8") as weather_file:
        weather = csv.DictReader(weather_file)
        print(f"Fetching weather forecast for {chosen_artist} concerts...")
        for row in weather:


#Task 9

def search_song():
    if not("inverted_index.json" in sorted(os.listdir("dataset"))):
        
        inverted_index = {}
        for song_file in sorted(os.listdir("dataset/songs")):
            with open("dataset/songs/" + song_file, "r", encoding="utf-8") as current_file:
                info = json.load(current_file)
            lyrics = re.sub("[\',!\(\)?.\[\]]", "",info["lyrics"])
            
            for word in re.split(r"\s", lyrics.lower()):
                if not(word in inverted_index.keys()):
                    inverted_index[word] = [info["title"]]
                elif not(info["title"] in inverted_index[word]):
                    inverted_index[word].append(info["title"])
                    
        with open("dataset/inverted_index.json","w") as new_file:
            json.dump(inverted_index, new_file)
    
    search = input("Please type the lyrics you'd like to search for: ").lower()
    raw_input = re.sub("  ", " ", re.sub("[\',!\(\)?.\[\]]","", search))
    with open("dataset/inverted_index.json", "r") as file:
        info = json.load(file)
    
    query_result = {}
    for word in raw_input.split():
        if info.get(word) != None:
            for song in info[word]:
                if not(song in query_result.keys()):
                    query_result[song] = 1
                else:
                    query_result[song] = query_result[song] + 1
    
    print(f"Listing matches for '{raw_input}'...")
    for result in query_result.keys():
        print(f"- {result} with a score of {query_result[result]}")
    
    return

#Start

print(f"""Welcome to Mooziq!
Choose one of the options bellow:
""")

run = True
while run:
    run = main_menu()