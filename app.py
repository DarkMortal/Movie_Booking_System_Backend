import jwt, json, os
from dotenv import load_dotenv; load_dotenv()
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_, and_
from flask import Flask, request
from models import Movie, Booking, User, session
from password_hash import check_password
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET']

allowed_origins = ['http://localhost:5173', 'https://darkmortal.github.io/']

res_to_doc = lambda x: {
        'id': x.id,
        'name': x.title,
        'synopsis': x.description,
        'poster_image': x.image,
        'genres': json.loads(x.genres)
    }

@app.route("/", methods = ['GET'])
def route_1():
    print(request.origin)
    if request.origin not in allowed_origins: return '', 403
    res = []
    page_number = request.args.get('page')
    page_size = request.args.get('limit')
    search_query = request.args.get('search')
    
    search_query = (None if search_query is None else "%{}%".format(search_query))
    page_number = (None if page_number is None else int(page_number))
    page_size = (None if page_size is None else int(page_size))

    if page_size is not None and page_number is not None:
        slice_1 = page_size * (page_number - 1)
        if slice_1 < 0: slice_1 = 0
        slice_2 = slice_1 + page_size

    if search_query is None:
        if page_size is not None and page_number is not None:
            movies = session.query(Movie).slice(slice_1, slice_2).all()
        else: movies = session.query(Movie).all()
    
    else:
        if page_size is not None and page_number is not None:
            movies = session.query(Movie).filter(or_( Movie.title.ilike(search_query),
                Movie.description.ilike(search_query), Movie.genres.ilike(search_query)
            )).slice(slice_1, slice_2).all()
        else: movies = session.query(Movie).filter(or_( Movie.title.ilike(search_query),
                 Movie.description.ilike(search_query), Movie.genres.ilike(search_query)
            )).all()
            
    for i in movies: res.append(res_to_doc(i))
    session.close()
    return res

@app.route("/<id_>", methods = ['GET'])
def route_2(id_):
    if request.origin not in allowed_origins: return '', 403
    movie = session.query(Movie).filter(Movie.id == id_).first()
    session.close()
    if movie is None:
        return 'No record found'
    return res_to_doc(movie)

@app.route("/signup", methods = ['POST'])
def route_3():
    if request.origin not in allowed_origins: return '', 403
    data = json.loads(request.data.decode("utf-8"))
    user = User(
        name = data['user_name'],
        email = data['user_email'],
        password = data['user_password']
    )
    try:
        session.add(user)
        session.commit()
    except IntegrityError:
        session.close()
        return {
            'type': "warning",
            'message': "Username or email already in use"
        }
    except Exception:
        session.close()
        return {
            'type': "error",
            'message': "There was an error"
        }
    session.close()
    return {
        'type': "success",
        'message': "Data saved successfuly"
    }

@app.route("/login", methods = ['POST'])
def route_4():
    if request.origin not in allowed_origins: return '', 403
    data = json.loads(request.data.decode("utf-8"))
    name = data['user_name']
    password = data['user_password']

    user = session.query(User).filter(User.user_name == name).first()
    if user is None:
        return {
            'type': "error",
            'message': "User doesn't exist"
        }
    if check_password(password, user.user_password_hash):

        token = jwt.encode({
            'username': user.user_name,
            'userid': user.user_id,
            # 'expiration': str(datetime.utcnow() + timedelta(seconds = 100))
        }, app.config['SECRET_KEY'], algorithm = 'HS256')

        return {
            'type': "success",
            'message': "Login successful",
            'id': user.user_id,
            'name': user.user_name,
            'token': token
        }
    else: return {
            'type': "warning",
            'message': "Invalid credentials"
        }

@app.route("/book", methods = ['POST'])
def route_5():
    if request.origin not in allowed_origins: return '', 403
    data = json.loads(request.data.decode("utf-8"))

    # check if booking already exists
    booking = session.query(Booking).filter(and_(
        Booking.user_id == data['user_id'], Booking.movie_id == data['movie_id']
    )).first()

    if booking is not None: return {
        'type': 'warning',
        'message': 'Movie already booked for this user'
    }
    
    booking  = Booking(
        u_id = data['user_id'],
        m_id = data['movie_id'],
        b_date = datetime.today().strftime('%Y-%m-%d')
    )
    try:
        session.add(booking)
        session.commit()
    except Exception:
        session.close()
        return {
            'type': 'error',
            'message': 'There was some error'
        }
    session.close()
    return {
        'type': 'success',
        'message': 'Movie booked'
    }

@app.route("/getAllBookings", methods = ['POST'])
def route_6():
    if request.origin not in allowed_origins: return '', 403
    data = json.loads(request.data.decode("utf-8"))

    # check if booking already exists
    booking = session.query(Booking).filter(Booking.user_id == data['user_id']).all()
    session.close()

    res = {}
    
    try:
        for book in booking:
            res[book.movie_id] = book.booking_date
        return res
    except Exception:
        return {
            'type': 'error',
            'message': 'There was some error'
        }

@app.route("/deleteBooking", methods = ['POST'])
def route_7():
    if request.origin not in allowed_origins: return '', 403
    data = json.loads(request.data.decode("utf-8"))

    session.query(Booking).filter(and_(
        Booking.user_id == data['user_id'], Booking.movie_id == data['movie_id']
    )).delete()

    try:
        session.commit()
    except Exception:
        session.close()
        return {
            'type': 'error',
            'message': 'There was some error'
        }
    session.close()
    return {
        'type': 'success',
        'message': 'Booking deleted'
    }

@app.route("/getUserDetails", methods = ['POST'])
def route_8():
    if request.origin not in allowed_origins: return '', 403
    data = json.loads(request.data.decode("utf-8"))

    if 'jwtAuthToken' not in data.keys():
        return '', 403
    try:
        return jwt.decode(data['jwtAuthToken'], app.config['SECRET_KEY'], algorithms = ['HS256'])
    except Exception as exc:
        print(exc)
        return '', 500