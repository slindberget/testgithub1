from flask import Flask, request, render_template
import datetime
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="phonedb",
    user="postgres",
    password="xxxxxx")

def read_phonelist():
    cur = conn.cursor()
    cur.execute("SELECT * FROM phonelist;")
    rows = cur.fetchall()
    cur.close()
    return rows

def read_phone(name):
    cur = conn.cursor()
    print(f"SELECT phone FROM phonelist WHERE name = '{name}';")
    cur.execute(f"SELECT phone FROM phonelist WHERE name = '{name}';")
    rows = cur.fetchall()
    cur.close()
    return rows

def add_phone(name, phone):
    cur = conn.cursor()
    cur.execute(f"INSERT INTO phonelist VALUES ('{name}', '{phone}');")
    cur.execute("COMMIT;")
    cur.close()

def delete_phone(name):
    cur = conn.cursor()
    cur.execute(f"DELETE FROM phonelist WHERE name = '{name}';")
    cur.execute("COMMIT;")
    cur.close()
    return name

app = Flask(__name__)

@app.route("/")
def start():
    now = datetime.datetime.now()
    today = [str(now.year%100), str(now.month), str(now.day)]
    if len(today[1])<2:
        today[1] = '0'+today[1]
    if len(today[2])<2:
        today[2] = '0'+today[2]
    return render_template('list.html', list=read_phonelist())

@app.route("/delete", methods = ['POST', 'GET'])
def delete_func():
    if request.method == 'POST':
        name = request.form['name']
        return render_template('delete.html', req = delete_phone(name))
    else:
        return render_template('list.html', list=read_phonelist())

@app.route("/insert", methods = ['POST', 'GET'])
def insert_func():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        return render_template('insert.html', req = add_phone(name, phone))
    else:
        return render_template('list.html', list=read_phonelist())

@app.route("/api")
def api_func():
    args=request.args
    action = args.get('action', default="Bad action", type=str)
    if action == "Bad action":
        return render_template('api_usage.html', action=action)
    if action == 'phone':
        name = args.get('name', default="No name", type=str)
        if name == "No name":
            return render_template('api_usage.html', action=action)
        phone = read_phone(name)
        if len(phone) < 1:
            return f"not found {name}"
        return phone[0][0]
    else:
        return f"Unknown action: '{action}'"

if __name__ == '__main__':
    app.run(debug=True)


###BAJSKORVAR ÄR SMARTA#