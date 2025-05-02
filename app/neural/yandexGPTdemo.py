from ai_connector import AiConnector


class YandexGPTDemo:
    def __init__(self, connector: AiConnector):
        # Инициализация интерфейса для работы с Yandex GPT

        self.connector = connector
        self.session_history = [
            {"role": "system", "text": "Ты помощник в составлении раписания."}
        ]

    def add_message(self, role: str, text: str) -> None:
        # Метод для добавления сообщения в историю диалога

        self.session_history.append({"role": role, "text": text})

    def get_response(self, user_message: str) -> str:
        # Метод для получения ответа от AI на сообщение пользователя

        self.add_message("user", user_message)

        response = self.connector.send_message(self.session_history)
        if not response:
            return "API connection error"

        self.add_message("assistant", response)
        return response

    def clear_history(self) -> None:
        # Метод для очистки истории диалога

        self.session_history = self.session_history[:1]


if __name__ == "__main__":
    connector = AiConnector(api_key="AQVN0S-PrEc6lVsqi-b4n0_5qLfQZYY6j0tv_7mo")
    demo = YandexGPTDemo(connector)

    demo.add_message("system", "Создавай раписание со временем, когда какое действие необходимо сделать пользователю")
    demo.add_message("user", "У меня есть 3 дня и возможность заниматься каждый день по 2 часа")

    response = demo.get_response("Привет. У меня в пятницу контрольная работа по теории вероятности. Поможешь мне к ней подготовиться?")

    print(response)