'''
I made this module to address a previously described problem. The Spotify
database had artists in a "[artist1, artist2]" format, which was not ideal for
matching with the "Shazam" output. This function returns the artists in a format
that somewhat "meets half way" and trusts that the artists will be sufficiently
destinguishable from each other based on their names without '&' or ',' when paired
with the song title
'''

def sanitize_zasham(artist_name):
    artist_name = artist_name.lower()
    artist_name = artist_name.split(' &')[0].split(',')[0]
    return artist_name
