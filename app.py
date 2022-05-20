# კოდის მეშვეობით იქმნება ბაზა, რომელშიც მოცემულია ერთ-ერთ ვებგვერდზე დარეგისტრირებული იუზერების მონაცემები,
# სახელი, პაროლი, მინიჭებული აიდი, საცხოვრებელი ადგილი -> როგორც სტრინგები;
# აიდი და ასაკი ინტეჯერები, და არის თუარა ადმინi. .
# POSTMAN ის დახმარებით ხერხდება ბაზის შევსება და მასზე მოქმედები.
# 5000 პორტზე კი index.html  გამოაქვს ბაზიდან ყველა სია....
# სრული კოდი: github::::/ https://github.com/papitokarlo/Users.git
# +====================================================================================================
# ზურა ბეგაძე/ 
# linkdn::: ///  https://www.linkedin.com/in/zura-begadze/
# github::::/ https://github.com/papitokarlo
# gmail:::/   begadze.zura@gmail.com

from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash


app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisissecret'  # თუ დაგჭირდებათ და რამეში გამოგადეგაბთ აქ არის <3 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///User.db'
db = SQLAlchemy(app)

# ბაზას ვქმით ისე რა გამოვა :დ
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    live = db.Column(db.String(60))
    admin = db.Column(db.Boolean)
    age = db.Column(db.Integer)


# get მეთოდი მთლიანი სიის სანახავად 
@app.route('/user', methods=['GET'])
def get_all_users():
    users = User.query.all()
    output = []

    for user in users:
        data = {}
        data['public_id'] = user.public_id
        data['name'] = user.name
        data['password'] = user.password
        data['admin'] = user.admin
        data['age'] = user.age
        data['live']=user.live
        output.append(data)

    return jsonify({'users' : output})
    
# GET  კონკრეტული უსერის სანახავად 
@app.route('/user/<public_id>', methods=['GET'])
def get_one_user( public_id):

    user = User.query.filter_by(public_id=public_id).first() # ფილტრავს და მერე წვდომა აქვს

    if not user:
        return jsonify({'message' : 'No user found!'})

    data = {}
    data['public_id'] = user.public_id
    data['name'] = user.name
    data['password'] = user.password
    data['admin'] = user.admin
    data['age'] = user.age
    data['live'] = user.live

    return jsonify({'user' : data})

# # POST ით ვამატებთ ბაზაში ახალ ელემენტს რათქმაუნდა ეს ყვეაფერი რააც ზევით ეწერა პოსტმენით კეთდება 
@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, live=data['live'], age=data['age'], admin=False)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message' : 'New user created!'})

# PUT მეთოდით ხდება რაღაც ფილდის დააფდეითება
@app.route('/user/<public_id>', methods=['PUT'])
def promote_user(public_id):
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message' : 'No user found!'})

    user.admin = True   # ბაზაში admin ფილდი ბულეანფილდი იყო და მნიშვნელობა ფოლს ქონდა აქედან შეეცვაა და თრუა რა
    db.session.commit()
    return jsonify({'message' : 'The user has been updated!'})

#დელეტე მეთოდი კიდე შლის მონაცემს აიდის მიხეედვით
@app.route('/user/<public_id>', methods=['DELETE'])
def delete_user(public_id):
    user = User.query.filter_by(public_id=public_id).first()  

    if not user:
        return jsonify({'message' : 'No user found!'})
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message' : 'The user has been deleted!'})


#ვებ გვერდის ჩატვირთვა და ბაზის ყველა მონაცემის ჩვენება 
@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST' :
        return 'YOU DONT HAVE ACCESS RIGHTS'
    else:
        persons= User.query.order_by(User.age).all()
        counter = len(persons)
        return render_template("index.html", persons = persons, counter = counter)



if __name__ == '__main__':
    app.run(debug=True)
