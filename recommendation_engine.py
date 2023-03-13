import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn import preprocessing
import math


def distance(point1, point2):
    return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

def to_list(inp):
    res = [float(coord) for coord in inp[1:len(inp)-1].split(', ')]

    return res


class RecommendationEngine:
    def __init__(self, ratings_file, places_file):
        self.ratings_inp = pd.read_csv(ratings_file, sep=';')
        self.places = pd.read_csv(places_file, sep=';')
        self.ratings = pd.merge(self.places.drop(columns='rating'), self.ratings_inp)
        self.user_ratings = pd.pivot_table(self.ratings, index='person_id', columns='place_id', values='rating')
        self.user_ratings = self.user_ratings.dropna(thresh=5, axis=1).fillna(0)
        print(self.user_ratings)
        self.item_similarity = cosine_similarity(self.user_ratings.T)
        self.item_similarity_df = pd.DataFrame(self.item_similarity, index=self.user_ratings.columns,
                                               columns=self.user_ratings.columns)

    def get_similar_places(self, place_id, user_rating):
        similar_score = self.item_similarity_df[place_id] * (user_rating - 2.5)
        similar_score = similar_score.sort_values(ascending=False)
        return similar_score

    def get_places(self, user_ratings, user_coords):
        similar_places = pd.DataFrame()
        place_ids = []
        for place, rating in user_ratings:
            place_ids.append(place)
            arr = pd.Series(self.get_similar_places(place, rating))
            similar_places = pd.concat([similar_places, arr.to_frame().T], ignore_index=True, axis=0)

        recs = pd.DataFrame(similar_places.sum().sort_values(ascending=False), columns=['sim_kf'])
        recs = pd.merge(recs, self.places[['place_id', 'coords']], on='place_id').set_index('place_id')
        recs['coords'] = recs['coords'].apply(to_list)
        recs['distance'] = recs['coords'].apply(distance, args=[user_coords])

        min_max_scaler = preprocessing.MinMaxScaler()
        recs[['sim_kf', 'distance']] = min_max_scaler.fit_transform(recs[['sim_kf', 'distance']])

        print(recs.sort_values(by='distance').head(100))

        recs['sim_kf'] = recs['sim_kf'] - recs['distance']
        recs = recs.drop(columns=['coords', 'distance']).sort_values(by='sim_kf', ascending=False)

        print(recs.sort_values(by='sim_kf', ascending=False).head(100))

        recommendations = recs.index.tolist()

        res = pd.DataFrame()
        for id_ in recommendations:
            row = self.places.loc[self.places['place_id'] == id_]
            res = pd.concat([res, row], ignore_index=True)

        return res
