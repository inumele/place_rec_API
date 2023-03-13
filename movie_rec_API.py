from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import htmlgenerator as hg
from recommendation_engine import RecommendationEngine


engine = RecommendationEngine("ratings.csv", "movies.csv")
top_movies = engine.get_top_movies()


def generate_HTML(movies_list):
    divs = []
    for idx, movie_info in enumerate(movies_list):
        divs.append(
            hg.DIV(
                hg.LABEL(movie_info[0]),
                hg.LABEL(movie_info[1]),
                hg.INPUT()
            )
        )
    page = hg.HTML(
        hg.HEAD(
            hg.TITLE('Movie recommendations')
        ),
        hg.BODY(
            hg.H1('Movie recommendations'),
            hg.FORM(
                divs[0],
                divs[1],
                divs[2],
                divs[3],
                divs[4],
                action="/recommendations",
                method="post"
            )
        )
    )
    return hg.render(page, {})

app = FastAPI()

print(generate_HTML(top_movies))


# @app.get("/", response_class=HTMLResponse)
# def index()