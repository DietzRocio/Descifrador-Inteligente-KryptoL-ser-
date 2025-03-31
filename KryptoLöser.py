import string
import base64
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QVBoxLayout

FRECUENCIA_ESP = "EAOSRNIDLCTUMPBGVYQHFZJXKZ"

#descifrado (César, Base64, Hex)
def cesar_descifrar(texto_cifrado, desplazamiento):
    descifrado = ""
    for caracter in texto_cifrado:
        if caracter.isalpha():
            if caracter.islower():
                descifrado += chr((ord(caracter) - ord('a') - desplazamiento) % 26 + ord('a'))
            else:
                descifrado += chr((ord(caracter) - ord('A') - desplazamiento) % 26 + ord('A'))
        else:
            descifrado += caracter
    return descifrado

def cesar_fuerza_bruta(texto_cifrado):
    resultados = "\n--- Posibles mensajes descifrados (César) ---\n"
    for desplazamiento in range(1, 26):
        resultados += f"Desplazamiento {desplazamiento}: {cesar_descifrar(texto_cifrado, desplazamiento)}\n"
    return resultados

def base64_descifrar(texto_cifrado):
    try:
        return base64.b64decode(texto_cifrado).decode('utf-8')
    except Exception:
        return "No se pudo descifrar Base64"

def hex_descifrar(texto_cifrado):
    try:
        return bytes.fromhex(texto_cifrado).decode('utf-8')
    except Exception:
        return "No se pudo descifrar Hex"

def detectar_cifrado(texto):
    texto = texto.replace(" ", "")
    if all(c.isalpha() or c.isspace() for c in texto):
        return "Posible César"
    elif all(c in "0123456789ABCDEF" for c in texto.upper()):
        return "Posible Hex"
    elif any(c in "+/=" for c in texto):
        return "Posible Base64"
    else:
        return "Cifrado desconocido"

# Interfaz con PyQt6
class CryptoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("KryptoLöser")
        self.setGeometry(100, 100, 500, 400)
        self.setStyleSheet("background-color: #F8EDEB;")  #Fondo 

        self.label = QLabel("Ingrese el texto a descifrar:", self)
        self.label.setStyleSheet("color: #6D597A; font-weight: bold;")
        
        self.text_input = QLineEdit(self)
        self.text_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #B5838D;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
                background-color: #FFDDD2;
                color: #6D597A;
            }
            QLineEdit:focus {
                border: 2px solid #E5989B;
            }
        """)

        self.decode_button = QPushButton("Descifrar", self)
        self.decode_button.setStyleSheet("""
            QPushButton {
                background-color: #FFB4A2;
                color: white;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #E5989B;
            }
        """)

        self.result_output = QTextEdit(self)
        self.result_output.setReadOnly(True)
        self.result_output.setStyleSheet("""
            QTextEdit {
                background-color: #FFFFFF;
                color: #6D597A;
                border: 1px solid #B5838D;
                border-radius: 5px;
                padding: 5px;
            }
        """)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.text_input)
        layout.addWidget(self.decode_button)
        layout.addWidget(self.result_output)
        self.setLayout(layout)
        self.decode_button.clicked.connect(self.descifrar_texto)

    def descifrar_texto(self):
        texto_cifrado = self.text_input.text()
        cifrado_detectado = detectar_cifrado(texto_cifrado)
        resultado = f"Texto cifrado detectado: {cifrado_detectado}\n"
        if cifrado_detectado == "Posible César":
            resultado += cesar_fuerza_bruta(texto_cifrado)
        elif cifrado_detectado == "Posible Base64":
            resultado += "Descifrado Base64: " + base64_descifrar(texto_cifrado)
        elif cifrado_detectado == "Posible Hex":
            resultado += "Descifrado Hex: " + hex_descifrar(texto_cifrado)
        else:
            resultado += "No se pudo identificar el cifrado."
        self.result_output.setText(resultado)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = CryptoApp()
    window.show()
    sys.exit(app.exec())
