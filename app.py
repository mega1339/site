from functools import wraps
from db_setup import db
from tables import *
from app_setup import app
import re

from flask import render_template, request, session, flash, redirect, url_for

image_path = "D:\учеба\Сайт\FlaskDemo\site\pr2\static"

app.secret_key = 'key'
get_arr = '', '', '', ''

role = False
admin = False

#@login_required
@app.route('/table', methods=['GET', 'POST'])
def recieve():
    #q = db.engine.execute('SELECT photo FROM card WHERE id = 4;')
    #print(q)

    #img = Image.open(io.BytesIO(b'\x80\x04\x95\t\x00\x00\x00\x00\x00\x00\x00\x8c\x051.jpg\x94.'))
    #img = Image.frombytes("RGBA", (200, 200), q)

    #res = db.engine.execute('SELECT * FROM card;')
    #print(*res, sep="\n")

    if request.method == "POST":
        command = request.form.get("Data")
 
         
        if ('SELECT' in command):
            show = db.engine.execute('{}'.format(command))
        else:
            db.engine.execute('{}'.format(command))
            show = ['Nothing']
 
        res = db.engine.execute('SELECT * FROM card;')
    else:
        res = db.engine.execute('SELECT * FROM card;')
        show = ['Nothing']  

    return render_template("table.html",
                            cypher = res,
                            your = show,
                            image = '{}'.format('1.jpg'))

def check(mail, login, passw, pass_c):
    if not '@' in mail:
        print('not mail')
        return False

    if re.search(r'[^a-zA-Z]', login[0]):
        print('first need a-Z')
        return False
        
    for i in range(len(login)):
        if re.search(r'[^a-zA-Z0-9_]', login[i]):
            print('not {} in login'.format(login[i]))
            return False

    if len(login) < 6:
        print('login so short')
        return False

    for i in range(len(passw)):
        if not re.search(r'[^a-z]', passw[i]):    
            break
        else:
            if i == len(passw) - 1:
                print('not a-z in login')
                return False

    for i in range(len(passw)):
        if not re.search(r'[^A-Z]', passw[i]):
            break
        else:
            if i == len(passw) - 1:    
                print('not A-Z in login')
                return False

    for i in range(len(passw)):
        if not re.search(r'[^0-9]', passw[i]):
            break
        else:    
            if i == len(passw) - 1:    
                print('not 0-9 in login')
                return False

    for i in range(len(passw)):
        if not re.search(r'[^%$#@&*^{}|/~\]\[\\]', passw[i]):
            break
        else:   
            if i == len(passw) - 1: 
                print('not %$#@&*^|/\~[]}{ in login')
                return False

    if len(passw) < 8:
        print('password so short')
        return False

    if passw != pass_c:
        print('passwords no match')
        return False
    
    return True

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('Login first')
            return redirect(url_for('login'))
    return wrap


@login_required
def check_auth():
    global role 
    role = True


@app.route('/', methods=['GET','POST'])
def home():
    global role

    image = []
    price = []
    name = []
    marks = []
    
    
    result_show = db.engine.execute('SELECT * FROM card;') 

    j = 1
    for i in result_show:     
        img = Card.query.filter_by(id = j).first()
    
        price.append(img.price)
        image.append(img.photo)
        name.append(img.name)
    
        mark_arr = img.marks.split()
        sum = 0
    
        for i in mark_arr:
            sum += int(i)

        if len(mark_arr):
            mark = round(sum/len(mark_arr))
            marks.append(mark)
        else:
            marks.append(0)
    
        j += 1
    

    return render_template("index.html",
                            role = role,
                            cards = j - 1,
                            image = image,
                            price = price,
                            name = name,
                            marks = marks)




@app.route('/admin', methods=['GET', 'POST'])
def create_card():
    global admin

    if admin:
        if request.method == "POST":
        
            type         = request.form.get("Data_type")
            name         = request.form.get("Data_name")
            description  = request.form.get("Data_description")
            manufactor   = request.form.get("Data_manufactor")
            price        = request.form.get("Data_price")
            photo        = request.files["Data_photo"]

            photo.save('{}\{}'.format(image_path, photo.filename))

            ph = '{}'.format(photo.filename)

            Card.add(type,
                    name, 
                    description,
                    manufactor,
                    price,
                    ph
                    )

        return render_template("admin.html", role = role)

    else:
        return redirect(url_for('home'))



@app.route('/register', methods=['GET', 'POST'])
def create_user():
    if request.method == "POST":
        global get_arr

        email     = request.form.get("Data_email")
        login     = request.form.get("Data_login")
        password  = request.form.get("Data_pass")
        pass_def  = request.form.get("Data_pass_def")

        get_arr = email, login, password


        user_test_mail = User.query.filter_by(email = get_arr[0]).first()
        user_test_login = User.query.filter_by(login = get_arr[1]).first()

        if check(email, login, password, pass_def) and user_test_login == None and user_test_mail == None and get_arr[0] != '':

            User.add(get_arr[0],
                     get_arr[1], 
                     get_arr[2]
                     )

            return redirect(url_for('home'))
        else:
            print('already exist')

    return render_template("register.html")


@app.route('/login', methods=['GET','POST'])
def login():
    
    res = ''
    if request.method == "POST":

        login     = request.form.get("Data_login")
        password  = request.form.get("Data_pass")

        if login == 'adminadmin'and password == 'Admin1///':
            global admin, role
            admin = True 
            role = True

            session['logged_in'] = True
            return redirect(url_for('home'))

        else:
            user_test_login = User.query.filter_by(login = login).first()
            user_test_password = User.query.filter_by(password = password).first()

            if user_test_login == None or user_test_password == None:
                res = 'no such dire... user'

            else: 
                role = True
                session['logged_in'] = True
                return redirect(url_for('home'))

    return render_template('login.html', role = role, cypher = res )


@app.route('/logout', methods=['GET','POST'])
def logout():

    global role, admin
    role = False
    admin = False

    session.pop('logged_in', None)
    
    return redirect(url_for('home'))

@app.route('/product/<id_card>', methods=['GET','POST'])
def product(id_card):
    global role

    img = Card.query.filter_by(id = id_card).first()

    if request.method == "POST":
        new_mark = request.form["Data_mark"] 
        com_new = request.form.get("Data_comment")
        com_exist = img.comments
        mark_exist = img.marks
        db.engine.execute("UPDATE card SET comments = '{}$$${}' WHERE id = {}".format(com_exist, com_new, id_card))
        db.engine.execute("UPDATE card SET marks = '{} {}' WHERE id = {}".format(mark_exist, new_mark, id_card))
    

    price = img.price
    image = img.photo
    name = img.name
    type = img.type
    description = img.description
    comments = img.comments.split('$$$')
    manufactor = img.manufactor


    mark_arr = img.marks.split()
    sum = 0

    for i in mark_arr:
        sum += int(i)

    if len(mark_arr):
        mark = round(sum/len(mark_arr))
        marks = mark
    else:
        marks = 0

    res = db.engine.execute('SELECT * FROM card WHERE id = {};'.format(id_card))

    global admin

    return render_template("product.html",
                           role = role,
                           edit = False,
                           admin = admin,
                           cypher = res,
                           image = image,
                           price = price,
                           name = name,
                           type = type,
                           manufactor = manufactor,
                           comments = comments,
                           description = description, 
                           marks = marks,
                           id_card = id_card)




@app.route('/product/edit/<id_card>', methods=['GET','POST'])
def product_edit(id_card):
    global role

    img = Card.query.filter_by(id = id_card).first()

    price = img.price
    image = img.photo
    name = img.name
    type = img.type
    description = img.description
    comments = img.comments.split('$$$')
    manufactor = img.manufactor

    mark_arr = img.marks.split()
    sum = 0

    for i in mark_arr:
        sum += int(i)

    if len(mark_arr):
        mark = round(sum/len(mark_arr))
        marks = mark
    else:
        marks = 0

    global admin

    if admin:
        if request.method == "POST":
            
            type         = request.form.get("Data_type")
            name         = request.form.get("Data_name")
            description  = request.form.get("Data_description")
            manufactor   = request.form.get("Data_manufactor")
            price        = request.form.get("Data_price")
            photo        = request.files["Data_photo"]

            photo.save('{}\{}'.format(image_path, photo.filename))

            ph = '{}'.format(photo.filename)

            db.engine.execute('''UPDATE card SET type = '{}',
                                                name = '{}',
                                                description = '{}',
                                                manufactor = '{}',
                                                price = {},
                                                photo = '{}' 
                        WHERE id = {};'''.format(type,
                                                name, 
                                                description,
                                                manufactor,
                                                price,
                                                ph, 
                                                id_card))
        
            return redirect(url_for('home'))
    else:

        return redirect(url_for('home'))
                    

    return render_template("product.html",
                           role = role,
                           admin = admin,
                           edit = True,
                           image = image,
                           price = price,
                           name = name,
                           type = type,
                           manufactor = manufactor,
                           comments = comments,
                           description = description, 
                           marks = marks,
                           id_card = id_card)





if __name__ == '__main__':

    app.run(debug = True)
