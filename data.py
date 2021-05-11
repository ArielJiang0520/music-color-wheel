import pandas as pd
import numpy as np
import pickle
import os
from itertools import chain
from collections import defaultdict
from sklearn.metrics.pairwise import cosine_similarity


class Dataset:
    def __init__(self, df):
        self.df = df

        self.GENRE_POOL = sorted(list(
            set(chain.from_iterable(df['genre'].tolist()))
        ))
        self.ARTIST_POOL = sorted(df['artist'].tolist())

        self.CM = np.array(
            list(zip(df['R'].tolist(), df['G'].tolist(), df['B'].tolist()))
        )
        sorted_ids = df.sort_values(by=['popularity'], ascending=False).index

        self.GENRES_TO_IDS = defaultdict(list)
        for id_ in sorted_ids:
            for g in df.at[id_, 'genre']:
                self.GENRES_TO_IDS[g].append(id_)
        
        self.ARTISTS_TO_IDS = defaultdict(list)
        for id_ in sorted_ids:
            self.ARTISTS_TO_IDS[df.at[id_, 'artist']].append(id_)
    
    def get_all_genres(self):
        """ return all genres in the database as a sorted list """
        return self.GENRE_POOL

    def get_all_artists(self):
        """ return all artists in the database as a sorted list """
        return self.ARTIST_POOL

    def get_closest_song(self, r: float, g: float, b: float):
        """ 
        given three floating points r, g, b
        returns a dictionary
        """
        query = np.array([r, g, b]).reshape(1, -1)
        song_id = np.argsort(-cosine_similarity(query, self.CM).flatten())[0]

        return self.df.iloc[song_id].to_dict()

    def get_songs_for_genre(self, genre, top_n):
        """ return top n songs in this genre sorted by popularity 
        returns a list of records (a list of dictionary)
        """
        return self.df.iloc[
            self.GENRES_TO_IDS[genre][:top_n]
        ].to_dict('records')
    
    def get_songs_for_artist(self, artist, top_n):
        """ return top n songs by this artist sorted by popularity 
        returns a list of records (a list of dictionary)
        """
        return self.df.iloc[
            self.ARTISTS_TO_IDS[artist][:top_n]
        ].to_dict('records')

    def get_average_color_for_artist(self, artist):
        """ return the mean color of all the songs by this artist """
        
        a_df = self.df.iloc[self.ARTISTS_TO_IDS[artist]]
        mean_color = (np.array(a_df[['R', 'G', 'B']].sum(axis=0)) / len(a_df)).astype(int)

        return {'R': mean_color[0], 'G': mean_color[1], 'B': mean_color[2]}

    def get_average_color_for_genre(self, genre):
        """ return the mean color of this genre """

        g_df = self.df.iloc[self.GENRES_TO_IDS[genre]]
        mean_color = (np.array(g_df[['R', 'G', 'B']].sum(axis=0)) / len(g_df)).astype(int)

        return {'R': mean_color[0], 'G': mean_color[1], 'B': mean_color[2]}
    


if __name__ == '__main__':
    color_df = pickle.load(open('color_df.p', 'rb'))
    db = Dataset(color_df)

    print(db.get_closest_song(0, 255, 255))
    """
    {'artist': 'Rihanna', 'title': 'Bitch Better Have My Money', 'popularity': 76.0, 'R': 10, 'G': 198, 'B': 198, 'genre': ['barbadian pop', 'dance pop', 'pop', 'post-teen pop', 'urban contemporary']}
    """

    print(db.get_songs_for_genre('pop', 3))
    """
    [{'artist': 'Justin Bieber', 'title': 'Peaches', 'popularity': 100.0, 'R': 84, 'G': 126, 'B': 172, 'genre': ['canadian pop', 'pop', 'post-teen pop']}, 
    {'artist': 'Olivia Rodrigo', 'title': '\u200bdrivers license', 'popularity': 96.0, 'R': 187, 'G': 88, 'B': 139, 'genre': ['pop', 'post-teen pop']}, 
    {'artist': 'Kali Uchis', 'title': '\u200btelepatía', 'popularity': 95.0, 'R': 162, 'G': 106, 'B': 140, 'genre': ['colombian pop', 'pop']}]
    """

    print(db.get_songs_for_artist('Adele', 3))
    """
    [{'artist': 'Adele', 'title': 'Someone Like You', 'popularity': 78.0, 'R': 133, 'G': 62, 'B': 213, 'genre': ['british soul', 'pop', 'pop soul', 'uk pop']}, 
    {'artist': 'Adele', 'title': 'Rolling in the Deep', 'popularity': 76.0, 'R': 193, 'G': 63, 'B': 177, 'genre': ['british soul', 'pop', 'pop soul', 'uk pop']}, 
    {'artist': 'Adele', 'title': 'Set Fire to the Rain', 'popularity': 75.0, 'R': 167, 'G': 116, 'B': 157, 'genre': ['british soul', 'pop', 'pop soul', 'uk pop']}]
    """

    print(db.get_average_color_for_artist('Adele'))
    """
    {'R': 145, 'G': 89, 'B': 172}
    """

    print(db.get_average_color_for_genre('pop'))
    """
    {'R': 144, 'G': 110, 'B': 147}
    """