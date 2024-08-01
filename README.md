# Movie Booking System Backend
## Usage
- To get list of all movies
  - Route: `/`
  - Method: GET
- To get details of a particular movie
  - Route: `/id`
  - URL params: `id` of the movie
  - Method: GET
- To search for a movie
  - Route: `/?search=NameOfTheMovie`
  - URL params: `search` query of the movie
  - Method: GET
- Pagination of results
  - Route: `/?page=6&limit=3`
  - URL params: `page` and `limit`
  - Method: GET
## Setting up the environment
- Create the **Virtual Environment**

       virtualenv venv
- Activate the **Virtual Environment**

       source venv/bin/activate
- To run the app

       gunicorn --bind localhost:5000 wsgi:app
- To log dependencies

      pip3 freeze >> requirements.txt
***