def sanitize_zasham(artist_name):
    artist_name = artist_name.lower()
    artist_name = artist_name.split(' &')[0].split(',')[0]
    return artist_name
