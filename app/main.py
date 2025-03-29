
from bot.bot_processor import BotProcessor
from neural.ai_connector import AIConnector

if __name__ == "__main__":
    ai_connector = AIConnector()
    bot = BotProcessor(ai_connector)

    bot.run()
