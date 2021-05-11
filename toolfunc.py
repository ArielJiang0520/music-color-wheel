import pickle
import pandas
import math
import heapq

def getClosestSong(r, g, b, df):
    minDis = float("inf")
    minIdx = -1
    for i in range(len(df)):
        dis = math.sqrt((r - df['R'][i]) ** 2 + (g - df['G'][i]) ** 2 + (b - df['B'][i]) ** 2)
        if dis < minDis:
            minIdx = i
            minDis = dis
    # print(df.loc[minIdx])
    return df.loc[minIdx].to_dict()

def getGenreTopN(genre, df, N):
    mask = df.genre.apply(lambda x: genre in x)
    top = df[mask].nlargest(N, ['popularity'])
    # print(top)
    return top.to_dict()  

def getArtistColor(artist, df):
    r, g, b = 0, 0, 0
    songs = df.loc[df.artist == artist]
    leng = len(songs)
    for i in range(leng):
        r += songs['R'][i]
        g += songs['G'][i]
        b += songs['B'][i]
    return (int(r//leng), int(g//leng), int(b//leng))

if __name__ == "__main__":
    color_df = pickle.load(open("color_df.p", "rb"))
    print(getClosestSong(218, 116, 101, color_df))
    print(getGenreTopN('british soul', color_df, 10))
    print(getArtistColor('Adele', color_df))