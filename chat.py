from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit
import sqlite3 as sql
app = Flask(__name__)

conn = sql.connect('database.db')
conn.execute('DROP TABLE users')

conn.execute(
    'CREATE TABLE users (username TEXT PRIMARY KEY, password TEXT)')

conn.execute(
    "INSERT INTO users VALUES ('utente1','utente1');")
conn.execute(
    "INSERT INTO users VALUES ('utente2','utente2');")
conn.execute(
    "INSERT INTO users VALUES ('utente3','utente3');")
conn.execute(
    "INSERT INTO users VALUES ('utente4','utente4');")
conn.execute(
    "INSERT INTO users VALUES ('utente5','utente5');")
conn.execute(
    "INSERT INTO users VALUES ('utente6','utente6');")

conn.commit()
conn.close()

app.config[ 'SECRET_KEY' ] = 'jsbcfsbfjefebw237u3gdbdc'
socketio = SocketIO( app )


@app.route('/')
def init():
    if session.get('username') == None:
        return redirect(url_for('index'))
    return redirect(url_for('home'))

@app.route('/login')
def index():
    return render_template('Login.html')


@app.route('/chat')
def home():   
    return render_template('Chat.html',username = session['username'])


@app.route('/loginexec', methods=['POST', 'GET'])
def loginexec():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        con = sql.connect("database.db")
        cursor = con.cursor()
        cursor.execute("select * from users where username = (?)", [username])
        for row in cursor:
            if row[0] == username and row[1] == password:
                session['username'] = row[0]
                con.close()
                return redirect(url_for('home'))
            return redirect(url_for('init'))
    return redirect(url_for('init'))

def messageRecived():
  print( 'messaggio ricevuto!' )

@socketio.on( 'my event' )
def handle_my_custom_event( json ):
  print( 'recived my event: ' + str( json ) )
  socketio.emit( 'my response', json, callback=messageRecived )

if __name__ == '__main__':
  socketio.run( app, debug = True )
