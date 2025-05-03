import requests
from typing import Dict, List


class AiConnector:
    def __init__(self, api_key):
        # Запросы к нейронке
        self._api_url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        self._headers = {
            "Content-Type": "application/json",
            "Authorization": f"Api-Key {api_key}"
        }
        self._model_uri = "gpt://b1gkd7sr0i2ipteg0eqg/yandexgpt-lite"
        self._default_options = {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": "2000"
        }
        # Истории запросов пользователей
        self._user_histories: Dict[int, Dict[str, str]] = {}
        self._system_prompt = {
            "role": "system", 
            "text": "Создавай раписание со временем, "
                    "когда какое действие необходимо сделать пользователю"
        }


    def _add_message(self, telegram_id: int, role: str, text: str) -> None:
        """Метод для добавления сообщения в историю диалога"""
        if telegram_id not in self._user_histories:
            self._user_histories[telegram_id] = []
        self._user_histories[telegram_id].append({"role": role, "text": text})


    def _parse_response(self, response):
        """Метод для парсинга ответа от AI"""
        try:
            return response['result']['alternatives'][0]['message']['text']
        except Exception:
            return None


    def _send_message(self, messages):
        """Метод для отправки сообщения в AI"""
        prompt = {
            "modelUri": self._model_uri,
            "completionOptions": self._default_options,
            "messages": [self._system_prompt] + messages
        }

        print("PROMPT: ", prompt)

        try:
            response = requests.post(self._api_url, headers=self._headers, json=prompt)
            return self._parse_response(response.json())
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None
        

    def make_request(self, telegram_id: int, message_text: str):
        print("MAKE REQUEST")
        """Метод для создания запроса к AI"""
        if telegram_id not in self._user_histories:
            self._user_histories[telegram_id] = []

        self._add_message(telegram_id, "user", message_text)
        response = self._send_message(self._user_histories[telegram_id])

        print(f"RESPONSE: {response}")
        
        if not response:
            return None
        
        self._add_message(telegram_id, "assistant", response)
        # Удаляем старые сообщения, если их больше 6
        if len(self._user_histories[telegram_id]) > 6:
            self._user_histories[telegram_id] = self._user_histories[telegram_id][-6:]

        # TODO: Парсинг струкруты ответа
        return response
