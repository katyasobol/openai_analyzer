import openai
import pandas as pd
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

# Указываем путь к файлу
path = "file.xlsx"

# Указываем API-ключ для OpenAI
openai.api_key = os.getenv('SECRET_KEY')

df = pd.read_excel(path)

def analyze_review(review):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Rate the following review on a scale from 1 to 10, with 10 being the most positive:\n{review}\nRating:",
        temperature=0.7,
        max_tokens=1,
        n=1,
        stop=None,
    )
    rating = int(response.choices[0].text.strip())
    return rating

# прочитать файл xlsx и загрузить его содержимое в pandas DataFrame
df = pd.read_excel(path)

# добавить новый столбец с оценками тональности отзывов
df["rate"] = df["review text"].apply(analyze_review)

# сохранить DataFrame в новый файл CSV в той же директории
filename = os.path.splitext(os.path.basename(path))[0]
df_sorted = df.sort_values(by="rate", ascending=False)
df_sorted.to_csv(f"{filename}_analyzed.csv", index=False, columns=["email", "rate"])