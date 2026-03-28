import requests
from flask import Flask, request, render_template, jsonify
import os
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)


@app.route('/', methods=['GET'])
def meteoritos():
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    if start_date and end_date:
        try:
            API_URL = os.getenv('API_URL')
            API_KEY = os.getenv('API_KEY')

            params = {
                "api_key": API_KEY,
                "start_date": start_date,
                "end_date": end_date
            }

            response = requests.get(API_URL, params=params).json()
            data = response["near_earth_objects"]

            return render_template('index.html', data=data), 200

        except Exception as e:
            return jsonify({'Error': e})
    else:
        return jsonify('Null statements'), 500




if __name__ == "__main__":
    app.run(debug=True)
