from flask import render_template, flash, redirect, request, url_for, json, session, jsonify, Flask
from Quiz import forms
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'


@app.route('/register', methods=['GET', 'POST'])
def register():
    try:
        if request.method == 'POST':
            # login_user(user)
            data = {
                "username": request.form.get("username"),
                "email": request.form.get("email"),
                "password": request.form.get("password"),
                "contact_no": request.form.get("contact_no"),
            }
            url = 'http://05f3-14-99-145-110.ngrok.io/register'

            response = requests.post(url=url, json=data)
            if response.status_code == 200:
                return redirect('/login')
        return render_template('Main.html')

    except Exception as e:
        return e


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        if email == 'admin@gmail.com' and password == '123456':
            session['logged_in'] = True
            return redirect('/admin_home')
        data = {
            "email": request.form.get("email"),
            "password": request.form.get("password"),
        }
        url = 'http://05f3-14-99-145-110.ngrok.io/login'
        response = requests.post(url=url, json=data)
        if response.status_code == 200:
            status = json.loads(response.text)['status']
            if status == "True":
                username = json.loads(response.text)['username']
                session["username"] = username
                session['logged_in'] = True
                return redirect('/home')
            else:
                flash("Incorrect username/password!")
                return redirect('/login')
        else:
            flash("Incorrect username/password!")
    return render_template('Main.html')


@app.route("/")
def index():
    return render_template('Main.html')


@app.route("/index1")
def index1():
    username = session["username"]
    return render_template('layout1.html', username=username)


@app.route("/quiz", methods=['POST', 'GET'])
def quiz():
    if session['logged_in']:
        subject = request.args.get("subject")
        data = {"data": subject}
        print("data", data)
        response = requests.get(url='http://05f3-14-99-145-110.ngrok.io/quiz', json=data)
        qa_list = response.json()
        qa_list_data = qa_list.get('data')
        return render_template('quiz.html', qa_list=qa_list_data, subject=subject)
    return redirect('/login')


@app.route('/quiz_taken', methods=['GET', 'POST'])
def quiz_taken():
    try:
        if request.method == 'POST':
            # for getting all the ids from the quiz template
            question_ids = [i.split("-")[1] for i in request.form.keys()]
            # for getting all the select option values from the quiz template
            selected_options = [x for x in request.form.values()]
            dict = {}
            for key in question_ids:
                for value in selected_options:
                    dict[key] = value
                    selected_options.remove(value)
                    break
            url = 'http://05f3-14-99-145-110.ngrok.io/taken_quiz'

            response = requests.post(url=url, json=dict)
            data = response.json()
            data = json.loads(str(data["data"]))
        return render_template('result.html', data=data, question_id=question_ids)

    except Exception as e:
        return e


@app.route("/result")
def result():
    response = requests.post(url='http://05f3-14-99-145-110.ngrok.io/result')
    return render_template('result.html')


@app.route("/quiz_history")
def quiz_history():
    response = requests.post(url='http://05f3-14-99-145-110.ngrok.io/result')
    data = response.json()
    return render_template('quiz_history.html', data=data)


@app.route("/view_all_que", methods=['GET', 'POST'])
def view_all_que():
    if session['logged_in']:
        if request.method == 'POST':
            subject = str(request.form.getlist('subjects'))

            data = {"data": subject}
            response = requests.post(url='http://05f3-14-99-145-110.ngrok.io/view_que', json=data)
            qa_list = json.loads(response.text)
            print("@@@@", qa_list)
            if qa_list:
                qa_list_data = qa_list.get('data')
                return render_template('admin/view_que.html', qa_list=qa_list_data)

        return render_template('admin/sub_selection.html')
    return redirect('/login')


@app.route("/home", methods=['POST', 'GET'])
def home():
    if session['logged_in']:
        username = session["username"]
        if request.method == "POST":
            # subject = request.form.get('subject', "All")
            subject = request.form.getlist('subjects')
            if subject:
                return redirect(f"/quiz?subject={subject}")
            else:
                flash("Please select a subject!!")
        return render_template('home1.html', username=username)
    return redirect('/login')


@app.route("/admin_home")
def admin_home():
    if session['logged_in']:
        return render_template('admin/admin_home.html')
    return redirect('/login')


@app.route("/logout")
def logout():
    session['logged_in'] = ""

    return redirect('/login')


@app.route("/user_result" , methods=['GET','POST'])
def user_result():
    response = requests.post(url='http://05f3-14-99-145-110.ngrok.io/admin_result')
    data = response.json()
    return render_template('user_result.html', data=data)


@app.route("/add_que", methods=['GET', 'POST'])
def add_que():
    if session['logged_in']:
        try:
            form = forms.Add_queForm(request.form)
            if request.method == 'POST':
                data = {
                    "sub_name": form.subjects.data,
                    "question": form.question.data,
                    "option1": form.option1.data,
                    "option2": form.option2.data,
                    "option3": form.option3.data,
                    "option4": form.option4.data,
                    "correct_option": form.correct_opt.data
                }
                print("???", data)
                url = 'http://05f3-14-99-145-110.ngrok.io/add'
                response = requests.post(url=url, json=data)
            return render_template('admin/add_que.html')
        except Exception as e:
            return e
    return redirect('/login')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if session['logged_in']:
        try:
            data = {"id": id}
            url = 'http://05f3-14-99-145-110.ngrok.io/edit'
            response = requests.post(url=url, json=data)
            qa_list = response.json()
            data_list = qa_list.get('data')
            return render_template('admin/que_edit.html', qa_data=data_list)

        except Exception as e:
            return e
    return redirect('/login')


@app.route('/update', methods=['GET', 'POST'])
def update():
    if session['logged_in']:
        try:
            form1 = forms.EditqueForm()
            if request.method == 'POST':
                pay_load = {
                    "id": form1.id.data,
                    "subject": form1.subject.data,
                    "question": form1.question.data,
                    "option1": form1.option1.data,
                    "option2": form1.option2.data,
                    "option3": form1.option3.data,
                    "option4": form1.option4.data,
                    "correct_opt": form1.correct_opt.data

                }
                url = 'http://05f3-14-99-145-110.ngrok.io/update'
                response = requests.post(url=url, json=pay_load)
            return redirect('/view_all_que')

        except Exception as e:
            return e
    return redirect('/login')


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    if session['logged_in']:
        data = {"id": id}
        response = requests.post(url='http://05f3-14-99-145-110.ngrok.io/delete', json=data)

        return redirect('/view_all_que')
    return redirect('/login')
