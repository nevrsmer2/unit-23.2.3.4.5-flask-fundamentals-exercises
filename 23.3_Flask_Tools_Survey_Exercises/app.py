from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from survey_instances import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

RESPONSES_KEY = "responses"


@app.route("/")
def show_survey_start():
    """Renders survey's start page"""

    return render_template("survey_start.html", survey=survey)


@app.route("/begin", methods=["POST"])
def start_survey():
    """Redirects user to questions page /0"""

    '''[] for collecting user responses'''
    session[RESPONSES_KEY] = []

    return redirect("/questions/0")


@app.route("/answer", methods=["POST"])
def handle_question():
    """Appends user's response to session [] and redirects to next question or to /complete page if all questions have been answered"""


    # Extracts the yes/no answer from form
    choice = request.form['answer']

    # Appends user's response (choice) to session []
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(survey.questions)):
        # Compares number or user's responses in [] to number of survery questions in [].  If equal redirects user to confirmation page (/completion).  Else, it redirects user to next question (/question/X).
        
        return redirect("/complete")

    else:
        return redirect(f"/questions/{len(responses)}")


@app.route("/questions/<int:question_id>")
def show_question(question_id):
    """Shows the current question"""
    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        # Redirects to / if user tries skipping to questions before strating survey

        return redirect("/")

    if (len(responses) == len(survey.questions)):
        # Redirects user to /complete if all questions answered
        return redirect("/complete")

    if (len(responses) != question_id):
        # Redirects user to current questin if attempting to access questions out of order
        flash(f"Invalid question id: {question_id}.")
        return redirect(f"/questions/{len(responses)}")

# Sets survey question to variable to render it in HTML template
    question = survey.questions[question_id]
    return render_template(
        "question.html", question_num=question_id, question=question, survey=survey)


@app.route("/complete")
def complete():
    """Renders comletion confirmation page when user completes survery."""

    return render_template("completion.html", survey=survey)