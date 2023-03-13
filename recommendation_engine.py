import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import math


def distance(point1, point2):
    return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)


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

    def get_places(self, user_ratings, coords):
        similar_places = pd.DataFrame()
        place_ids = []
        for place, rating in user_ratings:
            place_ids.append(place)
            arr = pd.Series(self.get_similar_places(place, rating))
            similar_places = pd.concat([similar_places, arr.to_frame().T], ignore_index=True, axis=0)

        recommendations = similar_places.sum().sort_values(ascending=False).index.tolist()
        # print(recommendations)
        # for i in range(5):
        #     while recommendations[i] in place_ids:
        #         del recommendations[i]

        res = pd.DataFrame()
        for id_ in recommendations:
            row = self.places.loc[self.places['place_id'] == id_]
            res = pd.concat([res, row], ignore_index=True)
        res['distance'] = res['coords'].apply(distance, args=coords)
        print(res.head())

        return res
