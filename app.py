import requests
from flask import Flask, request, render_template
import os
from dotenv import load_dotenv

if os.getenv("RENDER") is None:
    load_dotenv()

app = Flask(__name__)


@app.route('/', methods=['GET'])
def meteoritos():
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    data = None
    error = None

    if start_date and end_date:
        try:
            API_URL = os.getenv('API_URL')
            API_KEY = os.getenv('API_KEY')

            if not API_KEY or not API_URL:
                print('API_KEY or API_URL missing')
                error = 'API_KEY or API_URL missing'
            else:
                params = {
                    "api_key": API_KEY,
                    "start_date": start_date,
                    "end_date": end_date
                }

                response = requests.get(API_URL, params=params, timeout=10)
                response.raise_for_status()
                json_data = response.json()

                data = json_data.get("near_earth_objects")

        except requests.exceptions.RequestException as e:
            print('Request Error: ', e)
            error = str(e)
        except Exception as e:
            print('Unexpected Error: ', e)
            error = str(e)

    return render_template('index.html', data=data, error=error)



if __name__ == "__main__":
    app.run()
