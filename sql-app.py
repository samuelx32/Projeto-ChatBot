import sqlite3

conn = sqlite3.connect('banco-chat.db')
cursor = conn.cursor()

#cursor.execute("DROP TABLE mensagens")
cursor.execute("CREATE TABLE IF NOT EXISTS mensagens (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL, texto TEXT NOT NULL)")

# Inserir alguns dados
#cursor.execute("INSERT INTO mensagens (nome, texto) VALUES (?,?)",("robot", "Olá, como posso ajudá-lo?"))
#cursor.execute("INSERT INTO mensagens (nome, texto) VALUES (?,?)",("user", "Gostaria de saber quanto custa a mensalidade para o curso de ciência da computação"))
#cursor.execute("INSERT INTO mensagens (nome, texto) VALUES (?,?)",("robot", "A mensalidade desse curso é de 1650 reais..."))

conn.commit()


# Consultar os dados
cursor.execute("SELECT * FROM mensagens")
resultados = cursor.fetchall()
for linha in resultados:
    print(linha)
# Fechar a conexão
conn.close()