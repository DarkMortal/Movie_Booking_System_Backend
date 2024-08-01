import json
from models import Movie, session

if __name__ == "__main__":
    with open('movies.json') as json_data:
        data = json.load(json_data)
        for i in data:
            movie = Movie(id_ = i['id'],
                          title_ = i['name'],
                          description_ = i['synopsis'],
                          genres_= i["genres"].__str__().replace("'",'''"'''),
                          image_ = i['poster_image']
                    )
            session.add(movie)
        session.commit()
        session.close()
        print("Database populated")
    