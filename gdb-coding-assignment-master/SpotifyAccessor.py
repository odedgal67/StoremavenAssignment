from http import HTTPStatus
from typing import List
import requests
from Exceptions import *


ACCESS_TOKEN_URL = "https://accounts.spotify.com/api/token"
ACCESS_TOKEN_KEY = "access_token"
GET_CATEGORIES_URL = "https://api.spotify.com/v1/browse/categories"
CATEGORIES_KEY = 'categories'
ITEMS_KEY = 'items'
NAME_KEY = 'name'
TRACKS_KEY = 'tracks'
COUNTRY_KEY = 'country'
PLAYLISTS_KEY = 'playlists'


class SpotifyAccessor:
    def __init__(self, client_id: str, client_secret: str):
        self.access_token: str = ""
        self.client_id: str = client_id
        self.client_secret: str = client_secret
        self.__get_access_token(self.client_id, self.client_secret)
        self.valid_categories = self.__get_all_categories()

    def __get_header_with_token(self):
        """
        Builds a header for http request with current access token
        """
        return {"Authorization": f"Bearer {self.access_token}"}

    def __get_access_token(self, client_id: str, client_secret: str) -> None:
        """
        Updates access_token field if token request is successful or raises exception if fails

        :param client_id: client's id
        :param client_secret: client's secret
        """

        body = {'grant_type': "client_credentials"}
        response = requests.post(ACCESS_TOKEN_URL, data=body, auth=(client_id, client_secret))
        if response.status_code == HTTPStatus.OK:  # Successful response
            self.access_token = self.__extract_token_from_response(response)
        else:
            raise HttpResponseException(response.status_code, response.text)

    def __extract_token_from_response(self, response) -> str:
        """
        :param response: http response from api
        :return: token string or empty string if failed
        """
        json_response = response.json()  # Not wrapped in try catch because we want to raise error if json is bad

        if ACCESS_TOKEN_KEY not in json_response:
            raise ExtractTokenException()
        return json_response[ACCESS_TOKEN_KEY]

    def __get_all_categories(self) -> List[str]:
        categories_names: List[str] = list()
        response = requests.get(GET_CATEGORIES_URL, headers=self.__get_header_with_token())
        json_data = response.json()
        categories = json_data[CATEGORIES_KEY][ITEMS_KEY]
        for category in categories:
            name = str.lower(category[NAME_KEY])
            categories_names.append(name)
        return categories_names

    def __check_response_code(self, response) -> None:
        """
        Raises exception if response code is not OK
        """
        if response.status_code != HTTPStatus.OK:
            raise HttpResponseException(response.status_code, response.text)

    def is_invalid_category(self, category: str):
        """
        Checks if the given category is a valid category from spotify categories list
        :return: Boolean
        """
        return category.lower() not in self.valid_categories

    def get_playlist_tracks(self, playlist_href):
        """
        :param playlist_href: Playlist url
        :return: All tracks in playlist
        """
        playlist_response = requests.get(playlist_href, headers=self.__get_header_with_token())
        tracks = playlist_response.json()[TRACKS_KEY][ITEMS_KEY]
        return tracks

    def get_playlists(self, category, country):
        """
        Returns all playlists from the requested category and country. Notice country could be empty string for all countries
        :param category: Category of songs requested
        :param country: Country of songs requested. All countries if empty string
        :return: List of playlists from "category" in "country"
        """
        # Build http request params
        headers = self.__get_header_with_token()
        params = {"q": category, "type": "category"}
        if country:
            params[COUNTRY_KEY] = country
        get_playlists_url = f"https://api.spotify.com/v1/browse/categories/{category}/playlists"

        # Send request
        response = requests.get(get_playlists_url, headers=headers, params=params)

        # Extract playlists from response
        self.__check_response_code(response)
        category_data = response.json()
        playlists = category_data[PLAYLISTS_KEY][ITEMS_KEY]

        return playlists
