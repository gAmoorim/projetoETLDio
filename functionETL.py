import pandas as pd
import requests
import json

API_URL = "https://sdw-2023-prd.up.railway.app"

def extracao_users(csv_files):
    df = pd.read_csv(csv_files)

    users = []

    for user_id in df["UserID"]:
        try:
            response = requests.get(f"{API_URL}/users/{user_id}")

            if response.status_code == 200:
                users.append(response.json())
        except:
            pass

        if len(users) == 0:
            print('API está fora do ar, usando dados fictícios ')

            users = [
                {"id":1,"name":"Joao","news":[]},
                {"id":2,"name":"Thiago","news":[]},
                {"id":3,"name":"Alex","news":[]},
                {"id":4,"name":"Meire","news":[]},
                {"id":5,"name":"Nyvi","news":[]}
            ]

        return users 

def transform(users):
    for user in users:
        mensagem = f"Olá {user['name']}, Que tal começar a investir hoje?! Pequenas decisões financeiras podem construir um grande futuro!"

        user['news'].append({
            "icon":"https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
            "description":mensagem.strip()
        })
    return users    


def load(users):

    updated = []

    for user in users:

        try:
            requests.put(f"{API_URL}/users/{user['id']}", json=user)
        except:
            pass

        updated.append(user)

    with open("resultado_etl.json","w",encoding="utf-8") as f:
        json.dump(updated,f,indent=4,ensure_ascii=False)

    print("ETL finalizado. Arquivo salvo.")

users = extracao_users("SDW2023.csv")
users = transform(users)
load(users)