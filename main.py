# This is where the entry point of your solution should be
import os, json, csv, re

#Cached data

all_artists_data = {}

#Task 0.1

def main():

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
            moosify_lyrics()
        case "7":
            calculate_word()
        case "8":
            get_forecast()
        case "9":
            search_song()
        case "10":
            print("Thank you for using Mooziq! Have a nice day :)")
            return 1
        case _:
            print("Invalid choice! Try again.")
    
    return 0
        
#Helpers

def get_data_from_jsons(folder_path):

    data_for_all_files = {}
    for file_name in sorted(os.listdir(folder_path)):

        with open(folder_path + "/" + file_name, "r", encoding="utf-8") as open_file:
            data_for_all_files[file_name] = json.load(open_file)
    
    return data_for_all_files


def print_artists():

    if not all_artists_data:
    
        artist_files = get_data_from_jsons("dataset/artists")

        for artist_data in artist_files.values():

            artist_name = artist_data["name"]
            artist_id = artist_data["id"]
            artist_genres = artist_data["genres"]

            all_artists_data[artist_name.lower()] = {"id": artist_id, "name": artist_name, "genres": artist_genres}

    for artist_data in all_artists_data.values():
        print(f"- {artist_data["name"]}")


def format_month_day(month, day):
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

    day = f"{int(day)}{suffix}"

    return month_formatted, day


def find_albums_for_artist(artist_id):

    matched_albums = []
    album_files = get_data_from_jsons("dataset/albums")
    all_albums = album_files[artist_id+".json"]
    for album in all_albums["items"]:
        matched_albums.append(album)
    
    return  matched_albums


def find_top_tracks_for_artist(artist_id):

    top_tracks = []
    top_track_files = get_data_from_jsons("dataset/top_tracks")
    track_data = top_track_files[artist_id + ".json"]
    for track in track_data["tracks"]:
        top_tracks.append((track["popularity"],track["name"]))

    return top_tracks


def choose_song():

    song_files = get_data_from_jsons("dataset/songs")
    songs = [song_data for song_data in song_files.values()]

    print("Available songs:")
    for i in range(len(songs)):
        print(f"{i+1}. {songs[i]["title"]} by {songs[i]["artist"]}")
    
    choice = int(input("Please select one of the following songs (number): ")) - 1

    if choice not in range(len(songs)):
        raise ValueError
    else:
        return songs[choice]


#Task 1

def list_artists():

    print("Artists found in the database:")

    print_artists()

#Task 2
def get_albums():
    
    print_artists()
    
    artist = input("Please input the name of one of the following artists: ").strip().lower()

    if artist not in all_artists_data:
        print("Artist is missing. Please try again.")
        return

    print(f"Listing all available albums from {all_artists_data[artist]["name"]}...")

    artist_id = all_artists_data[artist]["id"]
    artist_albums = find_albums_for_artist(artist_id)
    for album in artist_albums:

        title = album["name"]
        date = album["release_date"] #format date YYYY-MM-DD to "August 3rd 2020"
        date_precision = album["release_date_precision"]
        group = date.split("-") #splits into: ["YYYY", "MM", "DD"] index 0, 1, 2
        match date_precision:
            case "day":
                year = group[0]
                month = group[1]
                day = group[2]

                month_formatted, formatted_day = format_month_day(month, day)

                print(f"- \"{title}\" was released in {month_formatted} {formatted_day} {year}.")

            case "year":
                year = group[0]

                print(f"- \"{title}\" was released in {year}.")
            case _:
                print("ERROR: Precision format not recognized!")
                return

#Task 3

def get_top_tracks():
    print_artists()
    
    chosen_artist = input("Please input the name of one of the following artists: ").lower()

    if chosen_artist in all_artists_data:
        artist_id = all_artists_data[chosen_artist]["id"]

        print(f"Listing top tracks for {all_artists_data[chosen_artist]["name"]}...")

        top_tracks = find_top_tracks_for_artist(artist_id)
        for track in top_tracks:
            track_popularity = track[0]
            track_name = track[1]
            if track_popularity <= 30:
                print(f'- "{track_name}" has a popularity score of {track_popularity}. No one knows this track.')
            elif track_popularity <= 50:
                print(f'- "{track_name}" has a popularity score of {track_popularity}. Popular song.')
            elif track_popularity <= 70:
                print(f'- "{track_name}" has a popularity score of {track_popularity}. It is quite popular now!')
            elif track_popularity > 70:
                print(f'- "{track_name}" has a popularity score of {track_popularity}. It is made for the charts!')

    else:
        print("Invalid artist entered.")

#Task 4

def export_artist():

    print_artists()
    chosen_artist = input("Please input the name of one of the following artists: ")

    if chosen_artist in all_artists_data:
        
        #Create row

        artist_id = all_artists_data[chosen_artist]["id"]
        artist_name = all_artists_data[chosen_artist]["name"]
        number_of_albums = len(find_albums_for_artist(artist_id))
        top_tracks = find_top_tracks_for_artist(artist_id)
        top_track_1 = top_tracks[0][1]
        top_track_2 = top_tracks[1][1]
        genres = ",".join(all_artists_data[chosen_artist]["genres"])

        artist_data = [artist_id, artist_name, number_of_albums, top_track_1, top_track_2, genres]

        #Export

        print(f'Exporting "{artist_name}" data to CSV file...')

        if os.path.isfile("dataset/artist-data.csv"):

            artist_row = None
            csv_data = []

            with open("dataset/artist-data.csv", 'r') as file:
                csv_reader = csv.reader(file)

                for row in csv_reader:
                    if row[1].lower() == chosen_artist:
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

#Task 5

def get_albums_year():

    try:
        chosen_year = int(input("Please enter a year: "))
    except ValueError:
        print("ERROR: Year must be an integer.")
        return

    albums = []
    album_files = get_data_from_jsons("dataset/albums")
    for file_name, album_data in album_files.items():

        for album in album_data["items"]:

            if int(album["release_date"][:4]) == chosen_year:

                for name, data in all_artists_data.items():
                    if data["id"] == file_name[:-5]:
                        artist_name = name

                albums.append((album["name"],artist_name))

    if len(albums) == 0:
        print(f"No albums were released in the year {chosen_year}.")
    else:
        albums.sort()

        print(f"Albums released in the year {chosen_year}:")
        for album_name, album_artist in albums:
            print(f'- "{album_name}" by {album_artist}.')


#Task 6

def moosify_lyrics():
    
    try:
        song_data = choose_song()
    except ValueError:
        print("ERROR: Chosen index is out of range or not an integer.")
        return
    
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

    try:
        chosen_song_data = choose_song()
    except ValueError:
        print("ERROR: Chosen index is out of range or not an integer.")
        return

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
    upcoming_concerts = {}
    with open("dataset/concerts/concerts.csv", "r", encoding="utf-8") as concerts_file:
        all_concerts = csv.DictReader(concerts_file)
        print("Upcoming artists: ")
        for row in all_concerts:
            artist = row["artist"]
            year = int(row["year"])
            month = int(row["month"])
            day = int(row["day"])
            date_formatted = (f"{year}-{month:02d}-{day:02d}")
            concerts_location = row["city_code"]

            if artist.lower() not in upcoming_concerts:
                upcoming_concerts[artist.lower()] = [(date_formatted, concerts_location, artist)]
            else:
                upcoming_concerts[artist.lower()].append((date_formatted, concerts_location, artist))
        for artist in upcoming_concerts:
            print(f"- {upcoming_concerts[artist][0][2]}")
    chosen_artist = input("Please input the name of one of the following artists: ").lower()
    if chosen_artist in upcoming_concerts:
        artist_name = upcoming_concerts[chosen_artist][0][2]
    else:
        print("Error. Artist not found.")
        return

    #opening weather csv
    target_weather = []
    with open("dataset/weather/weather.csv", "r", encoding="utf-8") as weather_file:
        weather = csv.DictReader(weather_file)
        print(f"Fetching weather forecast for \"{artist_name}\" concerts...")
        print(f"{artist_name} has {len(upcoming_concerts[chosen_artist])} upcoming concert{'s' if len(upcoming_concerts[chosen_artist]) > 1 else ''}:")
        for row in weather:
            for date, city_code, artist_name in upcoming_concerts[chosen_artist.lower()]:
                if row["date"] == date and row["city_code"] == city_code:
                    target_weather.append(row)
    
    for weather in target_weather:
        min_temp = int(weather["temperature_min"])
        precipitation = float(weather["precipitation"])
        wind = float(weather["wind_speed"])
        city = weather["city"]
        
        recommendation = []
        if min_temp <= 10:
            recommendation.append("Wear warm clothes.")
        if precipitation >= 2.3 and wind < 15:
            recommendation.append("Bring an umbrella.")
        if precipitation >= 2.3 and wind >= 15:
            recommendation.append("Bring a raincoat.")
        if recommendation==[]:
            recommendation.append("Perfect weather!")

        date_groups = weather["date"].split("-")
        month = date_groups[1]
        day = date_groups[2]
        year = date_groups[0]

        month_formatted, formatted_day = format_month_day(month, day)

        print(f"- {city}, {month_formatted} {formatted_day} {year}. {" ".join(recommendation)}")


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

if __name__=="__main__":
    print(f"""Welcome to Mooziq!
Choose one of the options bellow:
""")
    run_finished = 0
    while run_finished != 1:
        run_finished = main()