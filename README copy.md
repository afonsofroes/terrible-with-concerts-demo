# terrible-with-concerts
'Find events/concerts all from one song...'

This project was lead by Harpall Singh and developed by Harpall Singh, Afonso Froes, Pedro Peralta and Marat Akhmetshin. 
Demo'd on the 17th of March 2023 during the batch 1157 & 1157 Lisbon Le Wagon Demo Day.

Terrible with concerts uses a combination of 3 APIs (ZylaLab Music Gigs & Concerts Tracker, Bandsintown, and Spotify throigh Spotipy) and an 
unsupervised nearest neighbors model from SciKit-Learn to suggest live music events happening over a date range, in a specific city, based on a recorded song.

The song is recorded through your device's built-in microphone and is recognised through Shazamio (integrated into the front end, which is sotred in a different 
repository). The artist name and song title are then fed into the Spotify API and song features are extracted. These features are used in the unsupervised NN model, 
where the distance to every song played by the artists playing in your city is calculated and an average gouped by artist is returned.

The model then returns the top 5 matches, in a dictionary which includes the artists name, when they're playing, the longitutde and latitude of the venue, and a ticket link.

All of this information can be accessed through a web API, which was used in a Streamlit app during the Demo.
