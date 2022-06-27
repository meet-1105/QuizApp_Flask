import json
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_bcrypt import Bcrypt
from flask_redis import Redis

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ghjrhhrohirorthrtohi'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://ankita:12345678@192.168.1.47/quizapp"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
redis_cli = Redis(app)
bcrypt = Bcrypt(app)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        return {"status": "active", "message": "You are now in home page"}


@app.route('/register', methods=['POST'])
def register():
    response = {"status": "False", "message": "Error occurred"}
    try:
        from models import User
        data = request.get_json()
        print(data)
        hashed_password = bcrypt.generate_password_hash(data.get("password")).decode('utf-8')
        register_data = User(
            username=data.get('username'),
            email=data.get('email'),
            password=hashed_password,
            contact_no=data.get('contact_no')
        )
        print(register_data)
        db.session.add(register_data)
        db.session.commit()
        response = {"status": "True", "message": "data stored successfully"}
        return response
    except Exception as e1:
        response["message"] = "Exception occurred", str(e1)
        return response


@app.route('/login', methods=['POST'])
def login():
    from models import User
    return_response = {"status": False, "message": "Error occurred"}
    try:
        if request.method == "POST":
            data = request.get_json()
            print(data)
            email = data.get('email')
            user = User.query.filter_by(email=email).first()
            if user and bcrypt.check_password_hash(user.password, data.get('password')):
                import codecs
                from models import QA
                ques = QA.query.all()
                correct_options = json.dumps({x.id: x.correct_opt for x in ques})
                print("correct_option", correct_options)
                redis_cli.set('correct_opt', correct_options)
                redis_cli.set('id', user.id)
                redis_cli.set('username', user.username)
                print("redis get", redis_cli.get('correct_opt'))
                redis_un = codecs.decode(redis_cli.get('username'), 'UTF-8')
                return_response = {"status": "True", "message": "Logged in successfully", "flag": "1",
                                   "username": redis_un}
                return return_response

            else:
                return_response = {"status": "False", "message": "Please enter valid input"}
                return return_response
    except Exception as e1:
        return_response["message"] = "Exception occurred", str(e1)
    return return_response


@app.route('/user_profile', methods=['GET', 'POST'])
def user_profile():
    response = {"status": "False", "message": "Error occurred"}
    try:
        from models import User
        redis_id = int(redis_cli.get('id'))
        print("id", redis_id)
        user_detail = User.query.filter_by(id=redis_id).first()
        user_details = {"username": user_detail.username, "password": user_detail.password,
                        "contact_no": user_detail.contact_no, "email": user_detail.email}
        print(user_details)
        response = {"user_detail": user_details}
        data = request.get_json()
        print("data",data)
        hashed_password = bcrypt.generate_password_hash(data.get("change_password")).decode('utf-8')
        print()
        update_data = User(
            id=redis_id,
            username=data.get('username'),
            email=data.get('email'),
            password=hashed_password,
            contact_no=data.get('contact_no'),
            user_result=user_detail.user_result,
            score=user_detail.score,
        )
        local_object = db.session.merge(update_data)
        db.session.add(local_object)
        db.session.commit()
        print("dataa added!")
        return response



    except Exception as e2:
        response["message"] = "Exception occurred", str(e2)
    return response


@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    from models import QA
    try:

        data = request.get_json()
        if data.get("data") is not None:
            import random
            qes = db.session.query(QA).filter(QA.sub_name.in_(eval(data.get('data')))).order_by(func.random()).all()
            qa_list = []
            for qa in qes:
                qa_data = {'id': qa.id, 'question': qa.question,
                           'options': json.loads(qa.options)}
                qa_list.append(qa_data)
            response = {"status": "True", "message": "data stored successfully"}
            return jsonify({'response': response, "data": qa_list[:20]})

        else:

            import random
            questions = QA.query.order_by(func.random()).all()
            qa_list = []
            for qa in questions:
                qa_data = {'id': qa.id, 'sub_name': qa.sub_name, 'question': qa.question,
                           'options': json.loads(qa.options)}
                qa_list.append(qa_data)
            print(qa_list[:10])
            response = {"status": "True", "message": "data stored successfully"}
            return {'response': response, 'data': qa_list[:10]}

    except:
        return "{'error':'invalid data'}"


@app.route('/view_que', methods=['GET', 'POST'])
def view_que():
    from models import QA
    try:
        data = request.get_json()
        if data.get("data") is not None:
            questions = db.session.query(QA).filter(QA.sub_name.in_(eval(data.get('data')))).all()
            qa_list = []
            for qa in questions:
                qa_data = {'id': qa.id, 'sub_name': qa.sub_name, 'question': qa.question,
                           'options': json.loads(qa.options), 'correct_opt': qa.correct_opt}
                qa_list.append(qa_data)
            return jsonify({'status': True, 'data': qa_list})

    except Exception as e:
        return {"error": e}


@app.route("/delete", methods=['POST'])
def delete():
    try:
        from models import QA
        data = request.get_json()
        qa = QA.query.filter_by(id=data.get('id')).first()
        local_object = db.session.merge(qa)
        db.session.delete(local_object)
        db.session.commit()
        return jsonify({"Status": True, "data": "Data deleted successfully "})
    except Exception as e:
        return {"error": e}


@app.route("/edit", methods=['GET', 'POST'])
def edit():
    try:
        from models import QA
        data = request.get_json()
        qa = QA.query.filter_by(id=data.get('id')).first()
        qa_list = []
        qa_data = {'id': qa.id, 'sub_name': qa.sub_name, 'question': qa.question, 'options': json.loads(qa.options),
                   'correct_opt': qa.correct_opt}
        qa_list.append(qa_data)

        return jsonify({'status': True, 'data': qa_list})

    except Exception as e:
        return {"error": e}


@app.route("/add", methods=['POST'])
def add():
    try:

        response = {"status": "True", "message": "data added successfully"}
        if request.method == 'POST':
            from models import QA
            data = request.get_json()

            ques = data.get('question')
            sub = data.get('sub_name')
            data1 = {

                "option1": data.get('option1'),
                "option2": data.get('option2'),
                "option3": data.get('option3'),
                "option4": data.get('option4')

            }
            options = data1
            correct_opt = data.get('correct_option')
            qa = QA(question=ques, options=json.dumps(options), sub_name=sub, correct_opt=correct_opt)
            db.session.add(qa)
            db.session.commit()
            return response

    except Exception as e:
        return {"error": e}


@app.route("/update", methods=['GET', 'POST'])
def update():
    try:
        from models import QA
        data = request.get_json()
        response = {"status": "True", "message": "data updated successfully"}
        if request.method == 'POST':
            ques = data.get('question')
            sub = data.get('subject')
            data1 = {
                "option1": data.get('option1'),
                "option2": data.get('option2'),
                "option3": data.get('option3'),
                "option4": data.get('option4')
            }
            options = data1
            correct_opt = data.get('correct_opt')
            qa = QA(question=ques, options=json.dumps(options), id=data.get('id'), correct_opt=correct_opt,
                    sub_name=sub)
            local_object = db.session.merge(qa)
            db.session.add(local_object)
            db.session.commit()

        return response

    except Exception as e:
        return {"error": e}


@app.route('/taken_quiz', methods=['POST'])
def taken_quiz():
    try:
        if request.method == "POST":
            from models import User, QA
            redis_id = int(redis_cli.get('id'))
            print("redis stored id", redis_id)
            import codecs
            redis_corr = eval(codecs.decode(redis_cli.get('correct_opt'), 'UTF-8'))
            data = request.get_json()
            question1 = db.session.query(QA).filter(QA.id.in_(data.keys())).all()
            main_dict = {x.id: {'question': x.question, 'correct_opt': x.correct_opt} for x in question1}
            count = 0
            for key1, value1 in data.items():
                for key, value in redis_corr.items():
                    if key1 == key:
                        if value1 == value:
                            count = count + 1

            questions = []
            sel_opt = []
            for key, value in data.items():
                questions.append(key)
                sel_opt.append(value)

            for q in questions:
                main_dict[int(q)].update({
                    'selected_option': sel_opt[questions.index(q)]
                })
            main_dict["score"] = count
            user1 = User.query.filter_by(id=redis_id).first()
            if user1.user_result in [None, ""]:
                user1.user_result = json.dumps([main_dict])
                user1.score = count
                local_object = db.session.merge(user1)
                db.session.add(local_object)
                db.session.commit()

                return {"status": True, "data": json.dumps(main_dict)}
            else:
                old_data = json.loads(user1.user_result)
                old_data.append(main_dict)
                user1.user_result = json.dumps(old_data)
                local_object = db.session.merge(user1)
                db.session.add(local_object)
                db.session.commit()

                return {"data": json.dumps(main_dict), "score": count}

    except Exception as e:
        return {"error": e}


@app.route('/result', methods=['POST', 'GET'])
def result():
    try:
        from models import User
        redis_id = int(redis_cli.get('id'))
        print(redis_id)
        user1 = User.query.filter_by(id=redis_id).first()
        if user1.user_result in [None, ""]:
            return jsonify({"response": "No Quiz Taken Yet"})
        user_result = json.loads(user1.user_result)

        return {"response": user_result}

    except Exception as e:
        return {"error": e}


@app.route('/admin_result', methods=['POST', 'GET'])
def admin_result():
    try:
        from models import User
        user = User.query.all()
        qa_list = {}
        for qa in user:
            if qa.user_result not in [None, ""]:
                qa_list[qa.username] = eval(qa.user_result)

            else:
                pass

        return jsonify(qa_list)

    except Exception as e:
        return {"error": e}
