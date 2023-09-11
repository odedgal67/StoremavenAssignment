import asyncio
import time

from Accessor import Accessor
from Exceptions import *
from SpotifyAccessor import SpotifyAccessor
from Utils import *

CLIENT_ID = "8034b2828f22461aa8bba70292988563"
CLIENT_SECRET = "31f0ab1df8c64fc79c2c4deb42f682cb"


class Backend:
    def __init__(self):
        self.spotify_accessor: Accessor = SpotifyAccessor(CLIENT_ID, CLIENT_SECRET)

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

        playlists = self.spotify_accessor.get_playlists(category, country_code)
        return asyncio.run(self.spotify_accessor.get_all_tracks_from_playlists(playlists))


if __name__ == '__main__':
    timer = time.time()
    backend: Backend = Backend()
    result_logs = backend.track_data('pop', 'US')
    time_took = time.time() - timer
    assert result_logs and isinstance(result_logs, list)
    assert all([isinstance(log, FeaturedSong) for log in result_logs])
    print(f'Track complete, produced {len(result_logs)} logs and took {time_took:.5} seconds')
