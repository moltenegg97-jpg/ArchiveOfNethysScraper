#делает запрос на полный список существ

import requests
import json

#request URL https://elasticsearch.aonprd.com/json-data/2358078df34f8d82cba6067c5455c86c.json

url = "https://elasticsearch.aonprd.com/json-data/2358078df34f8d82cba6067c5455c86c.json"

headers = {'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 OPR/125.0.0.0 (Edition std-2)'}

response = requests.get(url, headers=headers)

#проверяем успешность запроса
if response.status_code == 200:
    # 5. Парсим JSON-ответ
    data = response.json()
    print("Данные успешно получены!")
    print(len(data))
    # Здесь `data` - это Python-словарь/список с данными монстров.
    # Дальше нужно изучить его структуру.
    # Например, выведите ключи или первые элементы:
    print(data.keys()) if isinstance(data, dict) else print(data[:2])
    
else:
    print(f"Ошибка {response.status_code}: Не удалось получить данные.")

with open('monsters_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("Данные сохранены в файл 'monsters_data.json'")