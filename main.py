# This is where the entry point of your solution should be
import os, json
#Task 0.1

#Task 1

def list_artists():
    print("Artists found in the database:")
    for artist_file in os.listdir("dataset/artists"):
        with open("dataset/artists/" + artist_file, "r", encoding="utf-8") as current_file:
            info = json.load(current_file)
        print(f"- {info["name"]}")

#Task 2

#Task 3

#Task 4

#Task 5

#Task 6

#Task 7

#Task 8

#Task 9
