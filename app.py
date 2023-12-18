from flask import g, Flask, render_template, request, redirect, url_for, flash,abort
app = Flask(__name__)
@app.route('/')
def hello():
    return "<p>Hello</p>"
