import pandas as pd
from recommendation_engine import RecommendationEngine

person_ratings = [
    (0, 4),
    (23, 3),
    (25, 5),
    (156, 4),
    (356, 5)
]

res = RecommendationEngine('people_ratings.csv', 'places.csv').get_places(person_ratings, [70.674798, 6.448295])
print(res.head(50))

