from flask import Flask, request, render_template
import os
import sqlite3 as sql

app = Flask(__name__) #Double "_"

template_folder = os.path.join(os.path.dirname(__file__),"templates/")
app.static_folder ="static"
app.static_url_path = "/static"

#database
database = os.path.join(os.path.dirname(__file__),"database/I-BIT.db")

@app.route('/', methods=["GET"])
def home():
    return render_template("index.html")

@app.route('/signin', methods=["GET"])
def signin():
    return render_template("signin.html")

@app.route('/post-signin', methods=["POST"])
def post_signin():
    email = request.form.get("email")
    password = request.form.get("password")

    conn = sql.connect(database)
    cur = conn.cursor()
    sql_select = """
    SELECT email, password, fullname
    FROM username
    WHERE email=?
    """
    val = (email,)
    cur.execute(sql_select,val) 
    data = cur.fetchone()
    conn.close()

    if password == data[1]:
        return user()
    else:
        return signin()
    
@app.route ('/user', methods=["GET"])
def user():
    conn = sql.connect(database)
    cur = conn.cursor()
    sql_user = """
    SELECT email, password, fullname
    FROM username
    """
    cur.execute(sql_user)
    data = cur.fetchall()
    conn.close()
    return render_template('username.html', user=data)

@app.route('/delete/<email>', methods=["GET"])
def delete(email):
    conn = sql.connect(database)
    cur = conn.cursor()
    sql_delete = """
    DELETE FROM username
    WHERE email=?
    """
    val = (email,)
    cur.execute(sql_delete, val) 
    conn.commit()
    conn.close()
    return user()

@app.route('/signup', methods=["GET"])
def signup():
    return render_template("signup.html")

@app.route('/post-signup', methods=["POST"])
def post_signup():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")
 
    conn = sql.connect(database)
    cur = conn.cursor()
    sql_insert = """
    INSERT INTO username (fullname,email,password,authorize)
    VALUES(?,?,?,?)
    """
    val = (name,email,password,1)
    cur.execute(sql_insert,val)
    conn.commit()
    conn.close()

    return name + ", " + email + ", " + password

@app.route ('/register', methods=["GET"])
def register():
    name = request.args['name']
    email = request.args['email']
    return "<h1>Your name is " + name + ", Your email is " + email + "</h1>"

@app.route('/cal', methods=["GET"])
def cal():
    item = request.args['item']
    number = int(request.args['number'])
    price = float(request.args['price'])
    msg = "You have to pay "
    msg += str(number*price)
    return "You buy <h1>" + item + "</h1>," + msg

@app.route('/edit/<email>', methods=["GET"])
def edit(email):
    conn = sql.connect(database)
    cur = conn.cursor()
    sql_select = """
    SELECT fullname, email, password
    FROM username
    WHERE email=?
    """
    val = (email,)
    cur.execute(sql_select, val) 
    data = cur.fetchone()
    conn.close()
    return render_template('edit_user.html', user=data)

@app.route('/post-edit', methods=["POST"])
def post_edit():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")

    conn = sql.connect(database)
    cur = conn.cursor()
    sql_update = """
    UPDATE username
    SET fullname=?
    WHERE email=?
    """
    val = (name, email)
    cur.execute(sql_update, val)
    conn.commit()
    conn.close()
    return user()
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)