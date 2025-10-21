import os, json, csv

def update_artists():

    artist_files = get_data_from_jsons("dataset/artists")

    all_artists_data = {}
    for artist_data in artist_files.values():

        artist_name = artist_data["name"]
        artist_id = artist_data["id"]
        artist_genres = artist_data["genres"]

        all_artists_data[artist_name.lower()] = {"id": artist_id, "name": artist_name, "genres": artist_genres}

    return all_artists_data


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
    if not is_existing(path):
            os.makedirs(path)


def is_existing(path):
    return os.path.exists(path)
    

def read_from_single_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def get_data_from_jsons(folder_path):
    data_for_all_files = {}
    for file_name in sorted(os.listdir(folder_path)):
        data_for_all_files[file_name] = read_from_single_json(folder_path + "/" + file_name)
    
    return data_for_all_files


def read_csv(file_path):

    csv_data = []
    with open(file_path, 'r', encoding="utf-8") as file:
        for row in csv.DictReader(file):
            csv_data.append(row)
    
    return csv_data
