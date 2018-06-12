from flask import Flask,render_template,session,request, jsonify, Response
from model import entities
from database import connector
import json




app = Flask(__name__)
db = connector.Manager()

cache = {}
engine = db.createEngine()

@app.route('/')
def hello_world():
    return render_template('login.html')

@app.route('/dologin',  methods = ['POST'])
def do_login():

    data = request.form
    session = db.getSession(engine)
    users = session.query(entities.User)
    for user in users:
        if user.email == data['email'] and user.password == data['password']:
            return render_template('Cursos.html', user=user)

    return render_template('login.html')


@app.route('/setUsers')
def set_user():

    user1 = entities.User(id=1, email='ed', fullname='Ed Jones', password='hola123')
    curso1=entities.Curso(id=1, name='Fisica')
    nota1=entities.Nota(id=1, variable="pc1", nota=15, porcentaje=20)
    curso1.notas=[nota1]
    curso2 = entities.Curso(id=2 , name='Mate')
    user1.cursos=[curso1,curso2]
    user2 = entities.User(id=2, email='jb', fullname='Je Belli', password='bye123')
    session = db.getSession(engine)
    session.add(user1)
    session.add(user2)
    session.commit()
    return 'Created users'


@app.route('/users', methods = ['GET'])
def get_users():
    key = 'getUsers'
    if key not in cache.keys():
        session = db.getSession(engine)
        dbResponse = session.query(entities.User)
        cache[key] = dbResponse;
        print("From DB")
    else:
        print("From Cache")

    users = cache[key];
    response = []
    for user in users:
        response.append(user)
    return json.dumps(response, cls=connector.AlchemyEncoder)

@app.route('/users/<id>', methods = ['GET'])
def get_user(id):
    session = db.getSession(engine)
    users = session.query(entities.User).filter(entities.User.id == id)
    for user in users:
        js = json.dumps(user, cls=connector.AlchemyEncoder)
        return  Response(js, status=200, mimetype='application/json')

    message = { "status": 404, "message": "Not Found"}
    return Response(message, status=404, mimetype='application/json')


@app.route('/users/<id>', methods = ['DELETE'])
def remove_user(id):
    session = db.getSession(engine)
    users = session.query(entities.User).filter(entities.User.id == id)
    for user in users:
        session.delete(user)
    session.commit()
    return "DELETED"


@app.route('/users', methods = ['POST'])
def create_user():
    c = json.loads(request.form['values'])
    print(c)
    user = entities.User(
        id=c['id'],
        email=c['email'],
        fullname=c['fullname'],
        password=c['password']
    )
    session = db.getSession(engine)
    session.add(user)
    session.commit()
    return 'Created users'

#@app.route('/add', methods='POST')
#def agregarcurso():
 #   curso= entities.Curso(id=user.id)

if __name__ == '__main__':
    app.run(debug=True)
