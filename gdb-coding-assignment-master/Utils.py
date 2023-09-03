
from typing import List

ALBUM_KEY = 'album'
ARTISTS_KEY = 'artists'
NAME_KEY = 'name'
TRACK_ID_KEY = 'track_id'
TRACK_NAME_KEY = 'track_name'
PLAYLIST_NAME_KEY = 'playlist_name'
PLAYLIST_ID_KEY = 'playlist_id'
PLAYLIST_RANK_KEY = 'playlist_rank'
TRACK_RANK_KEY = 'track_rank'
ARTISTS_NAMES_KEY = 'artist_names'
TOTAL_TRACKS_KEY = 'total_tracks'


def is_track_in_album(track) -> bool:
    """
    Checks whether song is part of an album or not
    :param track: Track to check
    :return: Boolean
    """
    return ALBUM_KEY in track


def get_artist_names(track) -> List[str]:
    """
    Returns a list of all the artists in the given track
    """
    artist_names: List[str] = list()
    artists = track[ARTISTS_KEY]
    for artist in artists:
        artist_names.append(artist[NAME_KEY])
    return artist_names


def build_required_fields_dict(track_id, track_name, playlist_name, playlist_id, playlist_index, track_index, artist_names) -> dict:
    """
    Builds and returns a dict containing all the mandatory fields of FeaturedSong
    """
    fields_dict = dict()
    fields_dict[TRACK_ID_KEY] = track_id
    fields_dict[TRACK_NAME_KEY] = track_name
    fields_dict[PLAYLIST_NAME_KEY] = playlist_name
    fields_dict[PLAYLIST_ID_KEY] = playlist_id
    fields_dict[PLAYLIST_RANK_KEY] = playlist_index
    fields_dict[TRACK_RANK_KEY] = track_index
    fields_dict[ARTISTS_NAMES_KEY] = artist_names

    return fields_dict


def update_params_with_album(fields_dict: dict, track) -> dict:
    """
    Update fields_dict with album info for a specific track
    :param fields_dict: dict to update
    :param track: track to update from
    :return: updated dict
    """
    album = track[ALBUM_KEY]
    album_name = album[NAME_KEY]
    album_tracks = album[TOTAL_TRACKS_KEY]
    fields_dict['album_name'] = album_name
    fields_dict['album_tracks'] = album_tracks
    return fields_dict
