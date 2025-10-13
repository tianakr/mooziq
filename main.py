# This is where the entry point of your solution should be
import os, json, csv, re
#Task 0.1
def main_menu():
    welcome_menu = f"""Welcome to Mooziq!
Choose one of the options bellow:
"""
    menu = f"""1. Get All Artists
2. Get All Albums By An Artist
3. Get Top Tracks By An Artist
4. Export Artist Data
5. Get Released Albums By Year
6. Analyze Song Lyrics
7. Calculate Longest Unique Word Sequence In A Song
8. Weather Forecast For Upcoming Concerts
9. Search Song By Lyrics
10. Exit"""
    option_exit = 0
    print(welcome_menu)
    while option_exit != 10:
        print(menu)

        option = int(input("Type your option: "))

        match option:
            case 1:
                list_artists()
            case 2:
                get_albums()
            case 3:
                get_top_tracks()
            case 4:
                export_artist()
            case 5:
                get_albums_year()
            case 6:
                analyze_lyrics()
            case 7:
                calculate_word()
            case 8:
                get_forecast()
            case 9:
                search_song()
            case 10:
                option_exit = 10
                print("Thank you for using Mooziq! Have a nice day :)")
            case _:
                print("Invalid choice! Try again.")


#Task 1

#display: turns logging on and off
def list_artists(display = True, display_artists = True):
    artists = {}
    if display:
        print("Artists found in the database:")
    for artist_file in sorted(os.listdir("dataset/artists")):
        with open("dataset/artists/" + artist_file, "r", encoding="utf-8") as current_file:
            info = json.load(current_file)
            if display_artists:
                print(f"- {info["name"]}")

        artists[info["name"].lower()] = {"id":info["id"],"genres":info["genres"]}

    return artists

#Task 2
def get_albums():
    artist_id = list_artists()

    artist = input("Please input the name of an artist: ").strip()
    matched_albums = []

    if artist not in artist_id:
        print("Invalid. Try again")

    for album_file in os.listdir("dataset/albums"):
        if album_file[:-5] == artist_id[artist]["id"]:

            with open("dataset/albums/" + album_file + ".json", "r", encoding="utf-8") as all_albums:
                all_albums = json.load(album_file)

            for album in all_albums["items"]:
                matched_albums.append(album)

    
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

                if day[1] == "1":
                    suffix = "st"
                elif day[1] == "2":
                    suffix = "nd"
                elif day[1] == "3":
                    suffix = "rd"
                else:
                    suffix = "th"

                pattern = r"\b0"

                formatted_day = re.sub(pattern, "", day)

                print(f"Listing all available albums from {artist}...")
                print(f"- {title} was released in {month_formatted} {formatted_day}{suffix} {year} ")

            return matched_albums

#Task 3

#display: turns logging on and off
#chosen_artist: if a chosen_artist is given as parameter, asking for input is skipped
def get_top_tracks(display = True, chosen_artist = None):
    artists = list_artists(display=True) if display else list_artists(display=False,display_artists=False)
    
    if not chosen_artist: chosen_artist = input("Please input the name of an artist: ")

    artist_id = artists[chosen_artist.lower()]["id"]
    if artist_id == "":
        print("Invalid artist entered.")
        return

    with open("dataset/top_tracks/" + artist_id + ".json", "r", encoding="utf-8") as tracks_file:
        dictionary = json.load(tracks_file)

    if display:
        print(f"Listing top tracks for {chosen_artist}...")

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

    return sorted(tracks, reverse=True)

#Task 4

def export_artist():
    artists = list_artists(display=False)

    chosen_artist = input("Please input the name of one of the following artists: ")

    if chosen_artist.lower() in [name.lower() for name in artists.keys()]:
        
        #Create row

        artist_id = artists[chosen_artist.lower()]["id"]
        number_of_albums = len(get_albums())
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
    
    chosen_year = input("Please enter a year: ")

    albums = []
    for album_file in os.listdir("dataset/albums"):#["hjady678dtguyu67.json","ijtgrkjdem796856.json"]

        with open("dataset/albums/" + album_file, "r", encoding='utf-8') as file:
            albums_json = json.load(file)

        for album in albums_json["items"]:

            if album["release_date"][:4] == chosen_year:
                artist_names_list = []

                for artist_data in album["artists"]:
                    artist_names_list.append(artist_data["name"])

                artist_names = ", ".join(artist_names_list)
                albums.append((album["name"],artist_names))
        
    albums.sort()

    print(f"Albums released in the year {chosen_year}:")
    for album_name, album_artists in albums:
        print(f'- "{album_name}" by {album_artists}.')


#Task 6

#Task 7

#Task 8

#Task 9

#extra functions

def find_id(chosen_artist):
    artist_id = ""
    for artist_file in os.listdir("dataset/artists"):
        with open("dataset/artists/" + artist_file, "r", encoding="utf-8") as artist_file:
            info = json.load(artist_file)
        if info["name"] == chosen_artist:
            artist_id = info["id"]
    return artist_id

#Start

if __name__== "__main__":
    main_menu()