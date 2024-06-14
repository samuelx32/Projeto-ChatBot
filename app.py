from flask import Flask, render_template, url_for, request, redirect
import sqlite3
from dotenv import load_dotenv
import openai
import os
import google.generativeai as genai

load_dotenv()

API_CHAT = os.getenv('API_CHAT')
app = Flask(__name__)

def recebeResposta(mensagem):
    genai.configure(api_key=API_CHAT)
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(mensagem)
    
    return response.text

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