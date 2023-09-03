
import time
from Exceptions import *
from FeaturedSong import FeaturedSong
from SpotifyAccessor import SpotifyAccessor
from Utils import *

CLIENT_ID = "8034b2828f22461aa8bba70292988563"
CLIENT_SECRET = "31f0ab1df8c64fc79c2c4deb42f682cb"
ITEMS_KEY = 'items'
TRACK_KEY = 'track'
ID_KEY = 'id'
NAME_KEY = 'name'
ALBUM_KEY = 'album'
ARTISTS_KEY = 'artists'
HREF_KEY = 'href'


class Backend:
    def __init__(self):
        self.spotify_accessor = SpotifyAccessor(CLIENT_ID, CLIENT_SECRET)

    def build_song(self, playlist_id: str, playlist, playlist_index: int, current_track, track_index: int) -> FeaturedSong:
        """
        Builds a new FeaturedSong object containing all the data provided
        """
        track_id = current_track[ID_KEY]
        track_name = current_track[NAME_KEY]
        playlist_name = playlist[NAME_KEY]
        artist_names = get_artist_names(current_track)
        fields_dict = build_required_fields_dict(track_id=track_id, track_name=track_name, playlist_name=playlist_name, playlist_id=playlist_id, playlist_index=playlist_index, track_index=track_index, artist_names=artist_names)

        if is_track_in_album(current_track):
            fields_dict = update_params_with_album(fields_dict, current_track)

        song: FeaturedSong = FeaturedSong(**fields_dict)

        return song

    def track_data(self, category: str, country_code: str = "") -> List[FeaturedSong]:
        """
        Returns a flat list of featured songs under category and country provided.
        May raise KeyError Exception for invalid playlists or tracks responses from API

        :param category: category
        :param country_code: Optional - default to "" which doesn't specify any country
        :return: Flat list of featured songs
        """
        if self.spotify_accessor.is_invalid_category(category):
            raise InvalidCategoryException(category)
        featured_songs: List[FeaturedSong] = list()
        playlists = self.spotify_accessor.get_playlists(category, country_code)

        for playlist_index, playlist in enumerate(playlists):
            playlist_id = playlist[ID_KEY]
            playlist_href = playlist[HREF_KEY]
            playlist_tracks = self.spotify_accessor.get_playlist_tracks(playlist_href)

            for track_index, track in enumerate(playlist_tracks):
                current_track = track[TRACK_KEY]
                current_song: FeaturedSong = self.build_song(playlist_id, playlist, playlist_index, current_track, track_index)
                featured_songs.append(current_song)

        return featured_songs


if __name__ == '__main__':
    timer = time.time()
    backend: Backend = Backend()
    result_logs = backend.track_data('pop', 'US')
    time_took = time.time() - timer
    assert result_logs and isinstance(result_logs, list)
    assert all([isinstance(log, FeaturedSong) for log in result_logs])
    print(f'Track complete, produced {len(result_logs)} logs and took {time_took:.5} seconds')
