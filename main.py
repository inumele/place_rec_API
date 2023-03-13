import pandas as pd
from recommendation_engine import RecommendationEngine

person_ratings = [
    (0, 4),
    (23, 3),
    (25, 5),
    (156, 1),
    (356, 1)
]

chosen_categories = [
    'кафе',
    'развлечения',
    'музей'
]

res = RecommendationEngine('people_ratings.csv', 'places.csv').get_places(
    person_ratings,
    [55.773554, 49.184842],
    chosen_categories
)
print(res.head(50))

