from flask import Flask

app = Flask(__name__)
@app.route("/")
def main(): 
    return "<p>Kurs programowania w Pythonie</p>"
@app.route("/wyklad12")
def wyklad():
    return "<p>Usługi sieciowe</p>"