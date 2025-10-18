import os, json

def get_data_from_jsons(folder_path):

    data_for_all_files = {}
    for file_name in sorted(os.listdir(folder_path)):

        with open(folder_path + "/" + file_name, "r", encoding="utf-8") as open_file:
            data_for_all_files[file_name] = json.load(open_file)
    
    return data_for_all_files


def update_artists():

    artist_files = get_data_from_jsons("dataset/artists")

    all_artists_data = {}
    for artist_data in artist_files.values():

        artist_name = artist_data["name"]
        artist_id = artist_data["id"]
        artist_genres = artist_data["genres"]

        all_artists_data[artist_name.lower()] = {"id": artist_id, "name": artist_name, "genres": artist_genres}

    return all_artists_data


def print_artists(all_artists_data):
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
    

def update_folder(path):

    if not os.path.exists(path):
            os.makedirs(path)


def is_file(path):
    os.path.isfile(path)