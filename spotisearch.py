"""
Json analysis with Spotify API.
"""

import base64
import requests

CLIENT_ID = "682a8d68a9904c2290cbce40adf8e2e0"
CLIENT_SECRET = "8c250c51eab4438c99f5c849d68d4d3b"

def get_token(client_id: str, client_secret: str) -> str:
    """
    Get token from Spotify API.
    """
    url = "https://accounts.spotify.com/api/token"
    auth_base64 = str(base64.b64encode((client_id + ":" + client_secret).encode("utf-8")), "utf-8")
    data = {"grant_type": "client_credentials"}

    response = requests.post(
        url,
        data=data,
        headers={"Authorization": "Basic " + auth_base64},
        timeout=10
    )

    result = response.json()
    return result["access_token"] if "access_token" in result else None

def get_artist_id(token: str, artist_name: str) -> str:
    """
    Get artist id from Spotify API.
    """
    url = "https://api.spotify.com/v1/search"
    params = {"q": artist_name, "type": "artist"}

    response = requests.get(
        url,
        params=params,
        headers={"Authorization": "Bearer " + token},
        timeout=10
    )

    result = response.json()
    return result["artists"]["items"][0]["id"] if "artists" in result else None

def get_artist_data(token: str, artist_id: str) -> dict:
    """
    Get artist data from Spotify API.
    """
    url = f"https://api.spotify.com/v1/artists/{artist_id}"

    response = requests.get(
        url,
        headers={"Authorization": "Bearer " + token},
        timeout=10
    )

    result = response.json()
    return result

def main():
    """
    Main function.
    """
    token = get_token(CLIENT_ID, CLIENT_SECRET)
    if token is None:
        print("Error getting token.")
        return

    print("Welcome to SpotiSearch!")
    print("Please enter the name of the artist you want to search: ")
    artists_id = get_artist_id(token, input(">>> "))

    if artists_id is None:
        print("Artist not found.")
        return

    artist_data = get_artist_data(token, artists_id)

    if "error" in artist_data:
        print("Error getting artist data.")
        return

    while True:
        print(f"\nAvalable options: {', '.join(artist_data.keys())}")
        print("Enter option:")
        option = input(">>> ")

        if option in artist_data:
            artist_data = artist_data[option]

            if not isinstance(artist_data, dict):
                print(artist_data)
                break
        else:
            print("Invalid option.")
            continue

if __name__ == "__main__":
    main()
