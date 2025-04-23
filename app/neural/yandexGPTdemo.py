import requests

prompt = {
    "modelUri": "gpt://b1gkd7sr0i2ipteg0eqg/yandexgpt-lite",
    "completionOptions": {
        "stream": False,
        "temperature": 0.6,
        "maxTokens": "2000"
    },
    "messages": [
        {
            "role": "system",
            "text": "Ты помощник, который создает раписание."
        },
        {
            "role": "user",
            "text": "Привет. У меня в пятницу контрольная работа по теории вероятности. Поможешь мне к ней подготовиться?"
        },
        {
            "role": "assistant",
            "text": "Привет! Как долго ты будешь готовиться к контрольной?"
        },
    ]
}


url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Api-Key AQVN0S-PrEc6lVsqi-b4n0_5qLfQZYY6j0tv_7mo"
}

response = requests.post(url, headers=headers, json=prompt)
result = response.text
print(result)