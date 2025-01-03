import requests
from config import secret_answer

class LolzApi:

    def __init__(self, token: str):
        self.api_url = 'https://api.lzt.market/'

        self.session = requests.Session()
        self.session.headers = {
            'Authorization': f'Bearer {token}'
        }

    def send_money(self, amount, username):
        params = {
            'username': username,
            'amount': amount,
            'currency': 'rub',
            'secret_answer': secret_answer,
            'comment': 'Спасибо за работу!',
        }
        return self.session.post(f'{self.api_url}balance/transfer', params=params)