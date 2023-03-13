import pandas as pd
from recommendation_engine import RecommendationEngine

person_ratings = [
    (0, 1),
    (23, 1),
    (25, 1),
    (156, 1),
    (356, 5)
]

res = RecommendationEngine('people_ratings.csv', 'places.csv').get_places(person_ratings, [55.790762, 49.112765])

