import sys
import json
import requests
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import QFont

TITLE = "ORAKOL"
VERSION = "0.9.0"

class QuoteBody:
    def __init__(self, text, author):
        self.text = text
        self.author = author

class Quote:
    def __init__(self, quote_body):
        self.quote_body = quote_body

def get_new_quote(quote):
    URL = "https://favqs.com/api/qotd"

    try:
        # Fazer a solicitação HTTP para a API de citações
        response = requests.get(URL)
        response.raise_for_status()

        # Analisar a resposta JSON
        data = response.json()
        quote_body = QuoteBody(data["quote"]["body"], data["quote"]["author"])
        quote.quote_body = quote_body

    except requests.exceptions.RequestException as e:
        print("Erro ao fazer a solicitação HTTP:", e)
    except json.JSONDecodeError as e:
        print("Erro ao analisar a resposta JSON:", e)

if __name__ == "__main__":
    quote = Quote(QuoteBody("", ""))

    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle(TITLE + " v." + VERSION)
    window.resize(1000, 470)

    title = QLabel(TITLE + " v." + VERSION)
    title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    font = QFont()
    font.setPointSize(45)
    font.setBold(True)
    title.setFont(font)

    quote_text = QLabel("")
    quote_text.setWordWrap(True)
    quote_font = QFont()
    quote_font.setPointSize(16)
    quote_text.setFont(quote_font)

    def on_button_click():
        get_new_quote(quote)
        quote_text.setText("\"" + quote.quote_body.text + "\"" + "\n-" + quote.quote_body.author)
        button.adjustSize()  # Redimensione o botão para o tamanho máximo necessário

    button = QPushButton("Get new quote")
    button.clicked.connect(on_button_click)

    v_box = QVBoxLayout()
    v_box.addWidget(title)
    v_box.addWidget(button)
    v_box.addWidget(quote_text)

    central_widget = QWidget()
    central_widget.setLayout(v_box)

    window.setCentralWidget(central_widget)

    window.show()
    sys.exit(app.exec())
