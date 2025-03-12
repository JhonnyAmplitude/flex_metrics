from fastapi import FastAPI
import requests
from fastapi.responses import StreamingResponse
from io import StringIO
from dotenv import load_dotenv
import os

app = FastAPI()

load_dotenv()

API_URL = os.getenv("API_URL")
API_token = os.getenv("API_TOKEN")
params = {
    'date1': '6daysAgo',
    'date2': 'today',
    'id': 64417021,
    "metrics": [
        "ym:s:visits",
        "ym:s:users",
        "ym:s:bounceRate",
        "ym:s:pageDepth",
        "ym:s:avgVisitDurationSeconds"
    ],
    'dimensions': 'ym:s:TrafficSource',
    'limit': 100
}

@app.get("/metrika-data/")
async def get_metrika_data():
    response = requests.get(API_URL, params=params, headers={'Authorization': f'OAuth {API_token}'})

    if response.status_code == 200:
        # Указываем разделители для разных региональных форматов в Excel
        csv_data = response.text.replace(',', ';')
        # Добавляем BOM для корректного отображения UTF-8
        data = StringIO('\ufeff' + csv_data)
        headers = {
            "Content-Disposition": "attachment; filename=metrics.csv"
        }
        return StreamingResponse(data, media_type="text/csv", headers=headers)
    else:
        return {"error": "Ошибка получения данных", "status_code": response.status_code}
