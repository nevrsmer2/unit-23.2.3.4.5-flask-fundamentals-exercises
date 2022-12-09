from flask import Flask, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from stories import story

app = Flask(__name__)
app.config['SECRET_KEY'] = "kitties"

debug = DebugToolbarExtension(app)


@app.route("/")
def ask_questions():
    """Renders the form containing the questions"""
    prompts = story.prompts
    return render_template("questions.html", prompts=prompts)


@app.route("/story")
def show_story():
    """Shows the story with the user's input"""
    text = story.generate(request.args)
    return render_template("story.html", text=text)