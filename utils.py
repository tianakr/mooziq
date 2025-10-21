
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
 

def find_artist_name_by_id(all_artists_data, artist_id):
    for data in all_artists_data.values():
        if data["id"] == artist_id:
            return data["name"]