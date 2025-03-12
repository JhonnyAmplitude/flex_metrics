from fastapi import FastAPI
import requests
from fastapi.responses import StreamingResponse
from io import StringIO

app = FastAPI()

API_URL = 'https://api-metrika.yandex.ru/stat/v1/data.csv'
API_token = 'y0__xDOv9UeGOf0NSCdltHAEuH0WBTuKpjd6EcSRsWjGXqaC-3J'
params = {
    'date1': '6daysAgo',
    'date2': 'today',
    'id': 64417021,
    'metrics': 'ym:s:visits,ym:s:users',
    'dimensions': 'ym:s:TrafficSource',
    'limit': 100
}

@app.get("/metrika-data/")
async def get_metrika_data():
    response = requests.get(API_URL, params=params, headers={'Authorization': f'OAuth {API_token}'})

    if response.status_code == 200:
        # Преобразуем полученные данные в поток для ответа
        data = StringIO(response.text)
        return StreamingResponse(data, media_type="text/csv")
    else:
        return {"error": "Failed to retrieve data", "status_code": response.status_code}
