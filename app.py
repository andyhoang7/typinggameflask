from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
import os

app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

CORS(app)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['SECRET_KEY']= 'supersecret'


#set connection with Postgres
POSTGRES = {
       'user': "thien",
       'pw': "qwerty",
       'db': "typinggame",
       'host': "localhost",
       'port': 5432,
   }
if 'DATABASE_URL' in os.environ:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL'] 
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:\
%(port)s/%(db)s' % POSTGRES



class Scores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wpm = db.Column(db.String)
    time = db.Column(db.String)
    error = db.Column(db.String)


class Excerpts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String)

@app.route('/', methods=['GET'])
def home():
    return jsonify(['Foo', 'Bar'])

@app.route('/excerpts', methods=['GET'])
def list():
    a = Excerpts.query.all()
    resp = []
    for i in a:
        resp.append({"id":i.id,
                     'body':i.body})
    return jsonify(resp)


@app.route('/postscore', methods=['GET', 'POST'])
def postscore():
    # import code; code.interact(local=dict(globals(), **locals()))

    Scores()
    score = Scores(
        wpm = request.get_json() ['wpm'],
        time = request.get_json() ['time'],
        error = request.get_json() ['errors']
    )
    db.session.add(score)
    db.session.commit()
    return jsonify(["hhuhu", "fuccccc"])
    

@app.route('/thien')
def thien():
    p=["The enormous room on the ground floor faced towards the north. Cold for all the summer beyond the panes, for all the tropical heat of the room itself, a harsh thin light glared through the windows, hungrily seeking some draped lay figure, some pallid shape of academic goose-flesh, but finding only the glass and nickel and bleakly shining porcelain of a laboratory.",
        "Wintriness responded to wintriness. The overalls of the workers were white, their hands gloved with a pale corpse-coloured rubber. The light was frozen, dead, a ghost. Only from the yellow barrels of the microscopes did it borrow a certain rich and living substance, lying along the polished tubes like butter, streak after luscious streak in long recession down the work tables.", 
        "Bent over their instruments, three hundred Fertilizers were plunged, as the Director of Hatcheries and Conditioning entered the room, in the scarcely breathing silence, the absent-minded, soliloquizing hum or whistle, of absorbed concentration.", 
        "Each of them carried a notebook, in which, whenever the great man spoke, he desperately scribbled. Straight from the horse's mouth. It was a rare privilege. The D. H. C. for Central London always made a point of personally conducting his new students round the various departments."]
    for i in p:
        new=Excerpts(body=i)
        db.session.add(new)
        db.session.commit()
    return "ok"

if __name__ == "__main__":
    app.run(debug=True, port=5005)