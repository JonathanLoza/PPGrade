from flask import Flask,render_template,session,request, jsonify, Response, redirect , url_for
from Web.model import entities
from sqlalchemy import or_, and_
from Web.database import connector
import json


app = Flask(__name__)
app.secret_key = "secretkey"
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


@app.route('/signin')
def signin():
    return render_template('Sign.html')


@app.route('/cursitos/<id>')
def cursitos(id):
    session = db.getSession(engine)
    user=session.query(entities.User).filter(entities.User.id==id).first()
    return render_template('Cursos.html', user=user)

@app.route('/mobile_login', methods = ['POST'])
def mobile_login():
    obj = request.get_json(silent=True)
    print(obj)
    email = obj['email']
    password = obj['password']
    sessiondb = db.getSession(engine)
    user = sessiondb.query(entities.User).filter(
        and_(entities.User.email == email, entities.User.password == password )
    ).first()
    if user != None:
        session['logged'] = user.id
        return Response(json.dumps({'response': True, "id": user.id, "fullname": user.fullname}, cls=connector.AlchemyEncoder), mimetype='application/json')
    else:
        return Response(json.dumps({'response': False}, cls=connector.AlchemyEncoder), mimetype='application/json')


@app.route('/addcurso', methods = ['POST'])
def addcurso():
    obj = request.get_json(silent=True)
    print(obj)
    user_id = obj['user_id']
    name = obj['name']
    sessiondb = db.getSession(engine)
    curso = entities.Curso(name=name, user_id=int(user_id))
    sessiondb.add(curso)
    sessiondb.commit()
    return Response(json.dumps({'response': True}, cls=connector.AlchemyEncoder), mimetype='application/json')


@app.route('/addnota', methods = ['POST'])
def addnota():
    obj = request.get_json(silent=True)
    print(obj)
    curso_id = obj['curso_id']
    nota = obj['nota']
    variable=obj['variable']
    porcentaje=obj['porcentaje']
    sessiondb = db.getSession(engine)
    nota=entities.Nota(variable=variable, nota=nota, porcentaje=porcentaje, curso_id=curso_id)
    sessiondb.add(nota)
    sessiondb.commit()
    return Response(json.dumps({'response': True}, cls=connector.AlchemyEncoder), mimetype='application/json')


@app.route('/crear', methods=['POST'])
def crearuser():
    data=request.form
    session = db.getSession(engine)
    user=entities.User(email=data['email'],fullname=data['fullname'], password=data['password'])
    session.add(user)
    session.commit()
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
    session = db.getSession(engine)
    curso=entities.Curso(name=data['curso'], user_id=idd)
    user = session.query(entities.User).filter_by(id=idd)
    session.add(curso)
    session.commit()
    return render_template("Cursos.html", user=user[0])


@app.route('/nota/<id>/<curso>')
def nota(id,curso):
    session = db.getSession(engine)
    user = session.query(entities.User).filter_by(id=id).first()
    curso=session.query(entities.Curso).filter(entities.Curso.name == curso ,entities.Curso.user_id==id).first()
    resultado = 0
    for nota in curso.notas:
        resultado += nota.nota * nota.porcentaje / 100
    return render_template("Notas.html",user=user,curso=curso,resultado="{0:.2f}".format(resultado))


@app.route('/add/<id>/<curso>/', methods=['POST'])
def crearnota(id,curso):
    data=request.form
    session = db.getSession(engine)
    user = session.query(entities.User).filter_by(id=id).first()
    curso=session.query(entities.Curso).filter(entities.Curso.name == curso ,entities.Curso.user_id==id).first()
    nota=entities.Nota(variable=data['variable'], nota=data['nota'], porcentaje=data['porcentaje'],curso_id=curso.id)
    session.add(nota)
    session.commit()
    resultado = 0
    for nota in curso.notas:
        resultado += nota.nota * nota.porcentaje / 100
    return render_template("Notas.html",user=user,curso=curso, resultado="{0:.2f}".format(resultado))


@app.route('/delete/<id>/<curso>/<variable>')
def eliminar(id,curso,variable):
    session = db.getSession(engine)
    user = session.query(entities.User).filter_by(id=id).first()
    curso1 = session.query(entities.Curso).filter(entities.Curso.name == curso, entities.Curso.user_id == id).first()
    nota=session.query(entities.Nota).filter(entities.Nota.curso_id==curso1.id, entities.Nota.variable==variable).first()
    session.delete(nota)
    session.commit()
    resultado = 0
    for nota in curso1.notas:
        resultado += nota.nota * nota.porcentaje / 100
    return render_template("Notas.html",user=user,curso=curso1, resultado="{0:.2f}".format(resultado))


@app.route('/curso/<id>/<name>', methods=['GET'])
def get_curso(id,name):
    session = db.getSession(engine)
    cursos = session.query(entities.Curso).filter(entities.Curso.user_id == id,entities.Curso.name == name)
    for curso in cursos:
        js = json.dumps(curso, cls=connector.AlchemyEncoder)
        return  Response(js, status=200, mimetype='application/json')

    message = { "status": 404, "message": "Not Found"}
    return Response(message, status=404, mimetype='application/json')

@app.route('/cursos/<id>', methods=['GET'])
def get_cursos(id):
    sessiondb = db.getSession(engine)
    cursos = sessiondb.query(entities.Curso).filter(entities.Curso.user_id == id)
    data=[]
    for curso in cursos:
        data.append(curso)
    return Response(json.dumps({'response': data}, cls=connector.AlchemyEncoder), mimetype='application/json')


@app.route('/notas/<id>', methods=['GET'])
def getnotas(id):
    sessiondb = db.getSession(engine)
    resultado = 0
    notas = sessiondb.query(entities.Nota).filter(entities.Nota.curso_id == id)
    data=[]
    for nota in notas:
        resultado += nota.nota * nota.porcentaje / 100
        data.append(nota)
    final = "{0:.2f}".format(resultado)
    return Response(json.dumps({'response': data, "final": final}, cls=connector.AlchemyEncoder), mimetype='application/json')


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


@app.route('/total/<cursos>')
def total(cursos):
    resultado=0
    for nota in cursos:
        resultado+=nota.nota*nota.porcentaje/100
    print(resultado)
    return str(resultado)


if __name__ == '__main__':
    app.run()
