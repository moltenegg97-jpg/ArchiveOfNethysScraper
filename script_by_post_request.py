#делает запрос на существ по поиску (например по уровням)

import requests
import json
import pandas as pd

url = 'https://elasticsearch.aonprd.com/aon/_search?stats=search'

min_level = 2
max_level = 3
headers = {'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 OPR/125.0.0.0 (Edition std-2)'}

json_as_text = """{
    "query": {
        "function_score": {
            "query": {
                "bool": {
                    "filter": [
                        {
                            "range": {
                                "level": {
                                    "gte": 19
                                }
                            }
                        },
                        {
                            "range": {
                                "level": {
                                    "lte": 19
                                }
                            }
                        },
                        {
                            "query_string": {
                                "query": "category:creature !category:item-bonus",
                                "default_operator": "AND",
                                "fields": [
                                    "name",
                                    "legacy_name",
                                    "remaster_name",
                                    "text^0.1",
                                    "trait_raw",
                                    "type"
                                ],
                                "minimum_should_match": 0
                            }
                        },
                        {
                            "bool": {
                                "must_not": {
                                    "exists": {
                                        "field": "remaster_id"
                                    }
                                }
                            }
                        }
                    ],
                    "must_not": [
                        {
                            "exists": {
                                "field": "item_child_id"
                            }
                        },
                        {
                            "term": {
                                "exclude_from_search": true
                            }
                        }
                    ]
                }
            },
            "boost_mode": "multiply",
            "functions": [
                {
                    "filter": {
                        "terms": {
                            "type": [
                                "Ancestry",
                                "Class",
                                "Versatile Heritage"
                            ]
                        }
                    },
                    "weight": 1.2
                },
                {
                    "filter": {
                        "terms": {
                            "type": [
                                "Trait"
                            ]
                        }
                    },
                    "weight": 1.05
                }
            ]
        }
    },
    "size": 10000,
    "sort": [
        {
            "name.keyword": {
                "order": "asc"
            }
        },
        "_doc"
    ],
    "track_total_hits": true,
    "_source": true,
    "search_after": [
        "beast tamer",
        13636
    ]
}"""
request_body = json.loads(json_as_text)

def change_creature_level(json_string, min_level, max_level):
    data = json.loads(json_string)
    data['query']["function_score"]["query"]["bool"]["filter"][0]["range"]["level"]["gte"] = min_level
    data['query']["function_score"]["query"]["bool"]["filter"][1]["range"]["level"]["lte"] = max_level

    return data

new_request = change_creature_level(json_as_text, min_level, max_level)

# 2. Отправляем POST-запрос с JSON в теле
response = requests.post(url, json=new_request, headers=headers)

if response.status_code == 200: #status code - статус ответа, например 404 page no found, 200 - вроде всё ок
    data = response.json()
    
    # Сохраняем полный ответ для анализа
    with open('full_api_response.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("Ответ сохранён в 'full_api_response.json'. Проверьте его структуру.")

    monsters_data = []
    for monster in data['hits']['hits']:
        source = monster['_source']
        monsters_data.append(source)
    
    df = pd.DataFrame(monsters_data)
    print(df[['name', 'level', 'url', 'hp', 'ac']].head())
