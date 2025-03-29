
class BotProcessor:
    def __init__(self, ai_connector):
        """
        Инициализация класса BotProcessor
        :param ai_connector: Объект для подключения к AI
        """
        self.ai_connector = ai_connector
        

    def _call_ai(self):
        """
        Метод для вызова Yandex GPT
        """
        # Пример вызова AI
        # on_response = self.ai_connector.send_message({
        #     "text": "Сделать проект по ТПР",
        #     "user_info": "",
        #     "tasks_info": "",
        #     "user_id": 1,
        # })
        # on_response(lambda response: self._process_response(response))
        pass


    def run(self):
        """
        Запуск бота
        """
        pass
