# app.py
from time import sleep

from flask import Flask, request, jsonify
import random
from datetime import datetime

app = Flask(__name__)


def is_valid_card(card_number: str) -> bool:
    return len(card_number) in [13, 16] and card_number.isdigit()


def is_valid_expiry(expiry_date: str) -> bool:
    try:
        expiry_date_obj = datetime.strptime(expiry_date, "%m/%y")
        return expiry_date_obj > datetime.now()
    except ValueError:
        return False


def is_valid_cvv(cvv: str) -> bool:
    return cvv.isdigit() and len(cvv) in [3, 4]


def is_valid_value(value: float) -> bool:
    return value > 0


def simulate_payment_process() -> bool:
    return random.choice([True, False])


def extract_request_data():
    data = request.json
    if not data:
        return None, {"status": "failed", "message": "Nenhum dado fornecido"}

    # Extrair campos do JSON
    card_number = data.get('card_number')
    expiry_date = data.get('expiry_date')
    cvv = data.get('cvv')
    value = data.get('value')

    return {
        "card_number": card_number,
        "expiry_date": expiry_date,
        "cvv": cvv,
        "value": value
    }, None


def validate_request_data(data):
    if not data['card_number'] or not data['expiry_date'] or not data['cvv'] or data['value'] is None:
        return {"status": "failed", "message": "Dados incompletos"}

    if not is_valid_card(data['card_number']):
        return {"status": "failed", "message": "Número de cartão inválido"}

    if not is_valid_expiry(data['expiry_date']):
        return {"status": "failed", "message": "Data de validade inválida ou expirada"}

    if not is_valid_cvv(data['cvv']):
        return {"status": "failed", "message": "CVV inválido"}

    if not is_valid_value(data['value']):
        return {"status": "failed", "message": "Valor de transação inválido"}

    # Dados válidos
    return None

def simulate_latency():
    sleep(random.randint(0,10))



@app.route('/process_payment', methods=['POST'])
def process_payment():


    simulate_latency()

    # Extração dos dados da requisição
    data, error = extract_request_data()
    if error:
        return jsonify(error), 400

    # Validação dos dados extraídos
    validation_error = validate_request_data(data)
    if validation_error:
        return jsonify(validation_error), 400

    # Simulação de processamento
    if simulate_payment_process():
        return jsonify({"status": "success", "message": "Pagamento aprovado"}), 200
    else:
        return jsonify({"status": "failed", "message": "Pagamento recusado"}), 402


if __name__ == '__main__':
    app.run(debug=True)
