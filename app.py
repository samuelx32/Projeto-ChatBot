from flask import Flask, render_template, url_for, request, redirect
import sqlite3
app = Flask(__name__)

def recebeResposta(mensagem):
    return "resposta"

@app.route("/")
def index():
    conn = sqlite3.connect('banco-chat.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM mensagens")
    resultados = cursor.fetchall()
    conn.close()

    user={'resultados': resultados, 'qtn':len(resultados)}
    

    return render_template('index.html',user=user)

@app.route('/armazenar-mensagem',methods = ['POST','GET'])
def armazena():
    mensagem = request.form['mensagem']
    resposta = recebeResposta(mensagem)

    conn = sqlite3.connect('banco-chat.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO mensagens (nome, texto) VALUES (?,?)",("user", mensagem))
    cursor.execute("INSERT INTO mensagens (nome, texto) VALUES (?,?)",("robot", resposta))
    conn.commit()
    conn.close()
      
    return redirect('/')


if __name__ == "__main__":
	app.run(debug = True, port=8080)