# This is where the entry point of your solution should be
import os, json
#Task 0.1
def main_menu():
    menu = f"""Welcome to Mooziq!
    Choose one of the options below:

    1. Get All Artists
    2. Get All Albums By An Artist
    3. Get Top Tracks By An Artist
    4. Export Artist Data
    5. Get Released Albums By Year
    6. Analyze Song Lyrics
    7. Calculate Longest Unique Word Sequence In A Song
    8. Weather Forecast For Upcoming Concerts
    9. Search Song By Lyrics
    10. Exit

    """
    option_exit = 0
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
if __name__== "__main__":
    main_menu()

#Task 1

def list_artists():
    print("Artists found in the database:")
    for artist_file in os.listdir("dataset/artists"):
        with open("dataset/artists/" + artist_file, "r", encoding="utf-8") as current_file:
            info = json.load(current_file)
        print(f"- {info["name"]}")

#Task 2

#Task 3

def get_top_tracks():
    list_artists()
    
    chosen_artist = input("Please input the name of an artist: ")
    artist_id = find_id(chosen_artist)
    if artist_id == "":
        print("Invalid artist entered.")
        return

    with open("dataset/top_tracks/" + artist_id + ".json", "r", encoding="utf-8") as tracks_file:
        dictionary = json.load(tracks_file)

    print(f"Listing top tracks for {chosen_artist}...")
    for track in dictionary["tracks"]:
        if track["popularity"] <= 30:
            print(f"- '{track["name"]}' has a popularity score of {track["popularity"]}. No one knows this track.")
        elif track["popularity"] <= 50:
            print(f"- '{track["name"]}' has a popularity score of {track["popularity"]}. Popular track.")
        elif track["popularity"] <= 70:
            print(f"- '{track["name"]}' has a popularity score of {track["popularity"]}. It is quite popular now!")
        elif track["popularity"] > 70:
            print(f"- '{track["name"]}' has a popularity score of {track["popularity"]}. Is is made for the charts!")

#Task 4

#Task 5

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
