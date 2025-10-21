# This is where the entry point of your solution should be
import re
import utils
import parsing_data as pd

#Task 0.1
def main():

    all_artists_data = pd.update_artists()
    print(f"""Welcome to Mooziq!
Choose one of the options bellow:
""")
    
    option = ""
    while option != "10":

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
                list_artists(all_artists_data)
            case "2":
                get_albums(all_artists_data)
            case "3":
                get_top_tracks(all_artists_data)
            case "4":
                export_artist(all_artists_data)
            case "5":
                get_albums_year(all_artists_data)
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
            case _:
                print("Invalid choice! Try again.")
        
#Task 1
def list_artists(all_artists_data):
    print("Artists found in the database:")
    utils.print_artists(all_artists_data)

#Task 2
def get_albums(all_artists_data):
    utils.print_artists(all_artists_data)
    artist = input("Please input the name of one of the following artists: ").strip().lower()

    if artist not in all_artists_data:
        print("Artist is missing. Please try again.")
    else:
        print(f"Listing all available albums from {all_artists_data[artist]["name"]}...")

        artist_id = all_artists_data[artist]["id"]
        artist_albums = pd.find_albums_for_artist(artist_id)
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
                    month_formatted, formatted_day = utils.format_month_day(month, day)
                    print(f"- \"{title}\" was released in {month_formatted} {formatted_day} {year}.")
                case "year":
                    year = group[0]
                    print(f"- \"{title}\" was released in {year}.")
                case _:
                    print("ERROR: Precision format not recognized!")

#Task 3

def get_top_tracks(all_artists_data):
    utils.print_artists(all_artists_data)
    chosen_artist = input("Please input the name of one of the following artists: ").lower()
    if chosen_artist in all_artists_data:

        artist_id = all_artists_data[chosen_artist]["id"]
        print(f"Listing top tracks for {all_artists_data[chosen_artist]["name"]}...")
        top_tracks = pd.find_top_tracks_for_artist(artist_id)
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

def export_artist(all_artists_data):

    utils.print_artists(all_artists_data)
    chosen_artist = input("Please input the name of one of the following artists: ").lower()

    if chosen_artist in all_artists_data:
        
        #Create row
        artist_id = all_artists_data[chosen_artist]["id"]
        artist_name = all_artists_data[chosen_artist]["name"]
        number_of_albums = len(pd.find_albums_for_artist(artist_id))
        top_tracks = pd.find_top_tracks_for_artist(artist_id)
        top_track_1 = top_tracks[0][1]
        top_track_2 = top_tracks[1][1]
        genres = ",".join(all_artists_data[chosen_artist]["genres"])

        artist_data = {"artist_id":artist_id, "artist_name":artist_name, "number_of_albums":number_of_albums}
        artist_data_rest = {"top_track_1":top_track_1, "top_track_2":top_track_2, "genres":genres}
        artist_data.update(artist_data_rest)

        #Export
        print(f'Exporting "{artist_name}" data to CSV file...')
        csv_header = ["artist_id","artist_name","number_of_albums","top_track_1","top_track_2","genres"]
        if pd.is_existing("dataset/artist-data.csv"):

            csv_data = pd.read_csv("dataset/artist-data.csv")
            artist_found = False
            i = 0
            for row in csv_data:
                if row["artist_name"].lower() == chosen_artist:
                    csv_data[i] = artist_data
                    artist_found = True
                i += 1

            if artist_found:
                pd.write_to_csv("dataset/artist-data.csv", csv_data, csv_header)
                print("Data successfully updated.")
            else:
                csv_data.append(artist_data)
                pd.write_to_csv("dataset/artist-data.csv", csv_data, csv_header)
                print("Data successfully appended.")
        else:
            pd.write_to_csv("dataset/artist-data.csv", [artist_data], csv_header)
            print("Data successfully appended.") 
    else:
        print(f"Error: {chosen_artist} not found in artists list.")

#Task 5

def get_albums_year(all_artists_data):

    try:
        chosen_year = int(input("Please enter a year: "))
    except ValueError:
        print("ERROR: Year must be an integer.")
        return

    albums = []
    album_files = pd.get_data_from_jsons("dataset/albums")
    for file_name, album_data in album_files.items():
        for album in album_data["items"]:
            if int(album["release_date"][:4]) == chosen_year:
                artist_name = utils.find_artist_name_by_id(all_artists_data, file_name[:-5])
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
        song_data = pd.choose_song()
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
        pd.update_folder("./moosified")
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
        chosen_song_data = pd.choose_song()
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

        if word in current_seq:
            if len(current_seq) > longest_seq:
                longest_seq = len(current_seq)
                current_seq = current_seq[current_seq.index(word)+1:]
            else:
                current_seq = current_seq[current_seq.index(word)+1:]

        current_seq.append(word)
        
    print(f"The length of the longest unique sequence in {chosen_song_data["title"]} is {longest_seq}")
            
#Task 8
def get_forecast():
    #list concerts
    upcoming_concerts = {}
    all_concerts = pd.read_csv("dataset/concerts/concerts.csv")

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
    

        #opening weather csv
        concerts_amount = len(upcoming_concerts[chosen_artist])
        print(f"Fetching weather forecast for \"{artist_name}\" concerts...")
        print(f"{artist_name} has {concerts_amount} upcoming concert{'s' if concerts_amount > 1 else ''}:")

        target_weather = []
        weather = pd.read_csv("dataset/weather/weather.csv")

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

            month_formatted, formatted_day = utils.format_month_day(month, day)

            print(f"- {city}, {month_formatted} {formatted_day} {year}. {" ".join(recommendation)}")
    else:
        print("Error. Artist not found.")


#Task 9

def search_song():
    if not pd.is_existing("dataset/inverted_index.json"):
        
        inverted_index = {}
        song_files = pd.get_data_from_jsons("dataset/songs")
        for info in song_files.values():
            lyrics = re.sub("[\',!\(\)?.\[\]]", "",info["lyrics"])
            
            for word in re.split(r"\s", lyrics.lower()):
                if word not in inverted_index.keys():
                    inverted_index[word] = [info["title"]]
                elif info["title"] not in inverted_index[word]:
                    inverted_index[word].append(info["title"])
                    
        pd.write_to_json("dataset/inverted_index.json", inverted_index)
    
    search = input("Please type the lyrics you'd like to search for: ").lower()
    raw_input = re.sub("  ", " ", re.sub("[\',!\(\)?.\[\]]","", search))

    info = pd.read_from_single_json("dataset/inverted_index.json")
    
    query_result = {}
    for word in raw_input.split():
        if info.get(word) != None:
            for song in info[word]:
                if song not in query_result.keys():
                    query_result[song] = 1
                else:
                    query_result[song] = query_result[song] + 1
    
    print(f"Listing matches for '{raw_input}'...")
    for result in query_result.keys():
        print(f"- {result} with a score of {query_result[result]}")


#Start

if __name__=="__main__":
    main()