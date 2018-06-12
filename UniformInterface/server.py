from flask import Flask,render_template,session,request, jsonify, Response, redirect , url_for
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

    user1 = entities.User( email='ed', fullname='Ed Jones', password='hola123')
    curso1=entities.Curso(name='Fisica', user=user1)
    nota1=entities.Nota( variable="pc1", nota=15, porcentaje=20, curso=curso1)
    curso2 = entities.Curso( name='Mate', user=user1)
    user2 = entities.User(  email='jb', fullname='Je Belli', password='bye123')
    curso3 = entities.Curso( name='Fisica', user=user2)
    nota3=entities.Nota(variable="pc1", nota=12, porcentaje=20, curso=curso3)
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

@app.route('/add/<idd>', methods=['POST'])
def add(idd):
    data = request.form
    print(idd)
    session = db.getSession(engine)
    curso=entities.Curso(name=data['curso'], user_id=idd)
    user = session.query(entities.User).filter_by(id=idd)
    print(user[0].fullname)
    session.add(curso)
    session.commit()
    return render_template("Cursos.html", user=user[0])


@app.route('/curso/<id>/<name>', methods=['GET'])
def get_cursos(id,name):
    session = db.getSession(engine)
    cursos = session.query(entities.Curso).filter(entities.Curso.user_id == id,entities.Curso.name == name)
    for curso in cursos:
        js = json.dumps(curso, cls=connector.AlchemyEncoder)
        return  Response(js, status=200, mimetype='application/json')

    message = { "status": 404, "message": "Not Found"}
    return Response(message, status=404, mimetype='application/json')


@app.route('/nota/<id>/<variable>', methods=['GET'])
def get_notas(id,variable):
    session = db.getSession(engine)
    notas = session.query(entities.Nota).filter(entities.Nota.curso_id == id,entities.Nota.variable == variable)
    for nota in notas:
        print(nota.variable)
        js = json.dumps(nota, cls=connector.AlchemyEncoder)
        return  Response(js, status=200, mimetype='application/json')

    message = { "status": 404, "message": "Not Found"}
    return Response(message, status=404, mimetype='application/json')
if __name__ == '__main__':
    app.run(port=80)
