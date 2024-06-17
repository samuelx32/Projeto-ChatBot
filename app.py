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
    prompt = f"""(Função: Servir de apoio aos funcionários e estudantes da UCB podendo utilizar essas informações ou fornecidas na internet), 
    (Cursos: Medicina Veterinária, Agronomia, Zootecnia, Direito, Administração, Ciências Contábeis, Engenharia de Software, Arquitetura, Psicologia, Ciência da Computação,e mais),
    (horário de funcionamento da coordenação: Segunda-feira: 8h às 12h e 19h às 21h30min,Terça-feira: 19h às 21h30min, Quarta-feira: 8h às 12h e 19h às 21h30min, Quinta-feira: 8h às 12h e 19h às 21h30min),
    (Local da coordenação de TI: Bloco D, sala D-210, Campus Taguatinga),
    (Coordenadora dos cursos de TI: Hially Rabelo Vaguetti),
    (Seu email institucional é: Todas as comunicações por e-mail são feitas por meio do e-mail institucional. (SEUNOME@a.ucb.br)),
    (Sobre a biblioteca virtual: A Minha Biblioteca é uma base de livros eletrônicos que oferece acesso a milhares de livros técnicos, científicos e profissionais das principais editoras acadêmicas do país),
    (Onde eu abro chamado: Sispred),
    (Como eu solicito instalação de software: Sispred),
    (Como trancar o curso:Caso deseje realizar o trancamento do seu curso, é necessário formalizar o pedido no ATENDE.),
    (Como reservar laboratórios: Enviar e-mail solicitando a reserva),
    (Qual o padrão de senha: Caracter especial, número e letra minúsculo e maiuscula),
    (Campus Taguatinga: Câmpus Taguatinga QS 07 - Lote 01 - EPCT - Taguatinga, Brasília/DF - CEP: 71966-700),
    (Campus Ceilândia: Câmpus Ceilândia St. N QNN 31 - Ceilândia, Brasília - DF, 72225-310 Telefone: 3356-9202),
    (Horário de funcionamento da biblioteca: Segunda à sexta-feira, das 8h às 21h45. Sábado, das 8h15 às 14h.),
    (Como calcular sua nota: pegue sua nota N1 e multiplique por 0.4 depois pege a sua nota N2 e multiplique por 0.5 depois pegue sua nota do PPD, aí é só somar tudo)
    (N1: Nota 1),
    (N2: Nota 2),
    (PPD: Programa Protagonismo Discente);
    Você é um chatbot help desk da Universidade católica de brasília, com base nesses dados ou nos disponíveis na internet, responda esse texto a seguir: {mensagem}"""
    chat = model.start_chat(history=[])
    response = chat.send_message(prompt)
    
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