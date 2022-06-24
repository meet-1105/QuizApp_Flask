from flask import render_template, flash, redirect, request, url_for, json, session, jsonify
from sqlalchemy.sql.functions import user

from Quiz import app, forms
# from flask_login import  LoginManager, logout_user
import requests


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
            print('%%%', data)

            url = '  https://434f-14-99-145-110.ngrok.io/register'

            response = requests.post(url=url, json=data)
            print('++++', response)
            if response.status_code == 200:
                return redirect('/login')
        return render_template('Main.html')

    except Exception as e:
        print(e)
        return e


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        if email == 'admin@gmail.com' and password == '123456':
            return render_template('admin/admin_home.html')

        data = {
            "email": request.form.get("email"),
            "password": request.form.get("password"),
        }
        url = '  https://434f-14-99-145-110.ngrok.io/login'
        response = requests.post(url=url, json=data)
        print(response)

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
# @login_required
def quiz():
    if session['logged_in'] == True:
        data = {"data": request.args.get("subject")}
        print("%&&%", data)
        response = requests.get(url='  https://434f-14-99-145-110.ngrok.io/quiz', json=data)
        qa_list = response.json()
        qa_list_data = qa_list.get('data')
        print("&&&",qa_list_data)
        length=len(qa_list_data)
        print("***8",length)

        return render_template('quiz1.html', qa_list=qa_list_data,length=length)
    return redirect('/login')


@app.route('/quiz_taken', methods=['GET', 'POST'])
def quiz_taken():
    import ast
    try:
        if request.method == 'POST':
            # for getting all the ids from the quiz template
            question_ids = [i.split("-")[1] for i in request.form.keys()]
            # for getting all the select option values from the quiz template
            selected_options = [x for x in request.form.values()]
            pay_load = {

                "questions": question_ids,
                "selected_option": selected_options
            }
            url = '  https://434f-14-99-145-110.ngrok.io/taken_quiz'

            response = requests.post(url=url, json=pay_load)
            data = response.json()
            data = json.loads(str(data["data"]))
            # data = json.loads(data)
        return render_template('result.html', data=data, question_id=question_ids)

    except Exception as e:
        print(e)
        return e


@app.route('/colors')
def colors():
    response = requests.post(url='  https://434f-14-99-145-110.ngrok.io/quiz')
    data = response.json()
    print("%%%", data)
    return render_template('page.html', data=data)

@app.route("/result")
def result():
    response = requests.post(url='  https://434f-14-99-145-110.ngrok.io/result')

    return render_template('result.html')


@app.route("/quiz_history")
def quiz_history():
    response = requests.post(url='  https://434f-14-99-145-110.ngrok.io/result')
    data = response.json()
    print("%%%", data)
    return render_template('quiz_history.html', data=data)


@app.route("/view_all_que")
def view_all_que():
    response = requests.post(url='  https://434f-14-99-145-110.ngrok.io/view_que')
    qa_list = json.loads(response.text)
    qa_list_data = qa_list.get('data')
    return render_template('admin/view_que.html', qa_list=qa_list_data)


@app.route("/home", methods=['POST', 'GET'])
def home():
    if session['logged_in'] == True:
        username = session["username"]
        if request.method == "POST":
            # subject = request.form.get('subject', "All")
            subject = request.form.getlist('subjects')
            return redirect(f"/quiz?subject={subject}")
        return render_template('home1.html', username=username)
    return redirect('/login')
@app.route("/admin_home")
def admin_home():
    if session['logged_in'] == True:
        return render_template('admin/admin_home.html')
    return redirect('/login')


@app.route("/logout")
def logout():
    session['logged_in'] = ""

    return redirect('/login')


@app.route("/add_que", methods=['GET', 'POST'])
def add_que():
    try:
        form = forms.Add_queForm(request.form)
        if request.method == 'POST':
            data = {
                "sub_name": form.sub_name.data,
                "question": form.question.data,
                "option1": form.option1.data,
                "option2": form.option2.data,
                "option3": form.option3.data,
                "option4": form.option4.data,
                "correct_option": form.correct_opt.data
            }

            url = '  https://434f-14-99-145-110.ngrok.io/add'
            response = requests.post(url=url, json=data)

        return render_template('admin/add_que.html')
    except Exception as e:
        print(e)

        return e


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    try:
        data = {"id": id}
        url = '  https://434f-14-99-145-110.ngrok.io /edit'
        response = requests.post(url=url, json=data)
        qa_list = response.json()
        data_list = qa_list.get('data')
        return render_template('admin/que_edit.html', qa_data=data_list)

    except Exception as e:
        print(e)
        return e


@app.route('/update', methods=['GET', 'POST'])
def update():
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
            # print('%%%', pay_load)
            url = '  https://434f-14-99-145-110.ngrok.io/update'
            response = requests.post(url=url, json=pay_load)
        return redirect('/view_all_que')
    except Exception as e:
        print(e)
        return e


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    data = {"id": id}
    response = requests.post(url='  https://434f-14-99-145-110.ngrok.io/delete', json=data)

    return redirect('/view_all_que')
