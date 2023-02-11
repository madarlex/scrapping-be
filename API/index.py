from flask import Flask, jsonify, request
from services.scrapping_tools import scrapping_tools
import logging

app = Flask(__name__)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

logger.addHandler(handler)


@app.route("/datascrapping", methods=["GET"])
def data_scrapping():
    shop_id = request.args.get('shop_id')
    country = request.args.get('country')
    data = scrapping_tools(country, shop_id)
    response = jsonify({'status': 200, "data": data})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == '__main__':
    app.run(debug=True)