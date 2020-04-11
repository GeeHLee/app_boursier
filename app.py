from flask import Flask
from web_crawl import ConnectionBoursier

app = Flask(__name__)

@app.route("/")
def home():
    conn = ConnectionBoursier()
    comp_df = conn.download()
    return comp_df.to_html()


if __name__ == '__main__':
    app.run(debug=True, port="18888", host="0.0.0.0")