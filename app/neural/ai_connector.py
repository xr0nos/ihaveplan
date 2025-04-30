import requests
from typing import Dict, List, Optional, Callable


class AiConnector:
    def __init__(self, api_key):
        self.api_url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Api-Key {api_key}"
        }
        self.model_uri = "gpt://b1gkd7sr0i2ipteg0eqg/yandexgpt-lite"
        self.default_options = {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": "2000"
        }


    def _parse_response(self, response):
        # Метод для парсинга ответа от AI

        try:
            return response['result']['alternatives'][0]['message']['text']

        except Exception:
            return None


    def send_message(self, messages):
        # Метод для отправки сообщения в AI
        prompt = {
            "modelUri": self.model_uri,
            "completionOptions": self.default_options,
            "messages": messages
        }

        try:
            response = requests.post(self.api_url, headers=self.headers, json=prompt)
            return self._parse_response(response.json())
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None







