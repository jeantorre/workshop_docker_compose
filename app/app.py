import os

import psycopg2
import streamlit as st


def conectar_banco():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
    )


def criar_tabela():
    conn = conectar_banco()
    cur = conn.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS mensagens (
        mensagem TEXT)
    """
    )
    conn.commit()
    cur.close()
    conn.close()


def adicionar_mensagem(mensagem):
    conn = conectar_banco()
    cur = conn.cursor()
    cur.execute("INSERT INTO mensagens (mensagem) VALUES (%s)", (mensagem,))
    conn.commit()
    cur.close()
    conn.close()


def ver_mensagem():
    conn = conectar_banco()
    cur = conn.cursor()
    cur.execute("SELECT mensagem FROM mensagens")
    mensagens = cur.fetchall()
    cur.close()
    conn.close()
    return mensagens


def main():
    st.title("Quadro de Mensagens")
    criar_tabela()

    mensagem = st.text_input("Adicionar nova mensagem: ")

    if st.button("Enviar"):
        if mensagem.strip():
            adicionar_mensagem(mensagem)
            st.success("Mensagem adicionada!")

    st.subheader("Mensagens")
    mensagens = ver_mensagem()
    mensagens.reverse()
    for mensagem in mensagens:
        st.write(mensagem[0])


if __name__ == "__main__":
    main()
