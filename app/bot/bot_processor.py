
class BotProcessor:
    def __init__(self, ai_connector):
        """
        Инициализация класса BotProcessor
        :param ai_connector: Объект для подключения к AI
        """
        # ВАЖНО: при добавлении информации о пользователе в её начало вставить следующий текст:
        # Меня зовут {name}. Запомни моё свободное время и никогда не добавляй задачи на часы, когда я занят. 
        self._ai_connector = ai_connector
        

    def _call_ai(self, telegram_id: int, message_text: str):
        """
        Метод для вызова Yandex GPT
        """
        message = self._ai_connector.make_request(
            telegram_id, message_text
        )
        if message:
            self._send_message(telegram_id, message)
        # Пример вызова AI
        # on_response = self.ai_connector.send_message({
        #     "text": "Сделать проект по ТПР",
        #     "telegram_id": 1,
        # })
        # on_response(lambda response: self._process_response(response))
        pass
    

    def _send_message(self, telegram_id: int, message_text: str):
        """
        Метод для отправки сообщения пользователю
        """
        # TODO: Должно отправляться через тг
        print(f"{telegram_id}: {message_text}")


    def run(self):
        """
        Запуск бота
        """
        pass
