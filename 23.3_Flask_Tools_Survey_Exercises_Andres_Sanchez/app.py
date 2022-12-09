from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from survey_instances import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "KittiesRock!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

RESPONSES = []

@app.route("/")
def show_survey_start():
    """Renders survey's start page"""

    return render_template("survey_start.html", survey=survey)


@app.route("/begin", methods=["POST"])
def start_survey():
    """Redirects user to questions page /0"""

    return redirect("/questions/0")


@app.route("/answer", methods=["POST"])
def handle_question():
    """Appends user's response to RESPONSES [] and redirects to next question or to /complete page if all questions have been answered"""

    # Extracts the yes/no answer from form
    choice = request.form['answer']
    # Apends choices values to RESPONSES []
    RESPONSES.append(choice)

    if (len(RESPONSES) == len(survey.questions)):
        RESPONSES.clear()
        # Compares number or user's responses in RESPONSES [] to number of survery questions in [].  If equal redirects user to confirmation page (/completion).  Else, it redirects user to next question (/question/X).
        
        return redirect("/complete")

    else:
        return redirect(f"/questions/{len(RESPONSES)}")


@app.route("/questions/<int:question_id>")
def show_question(question_id):
    """Shows the current question"""

    if (RESPONSES is None):
        # Redirects to / if user tries skipping to questions before strating survey

        return redirect("/")

    if (len(RESPONSES) == len(survey.questions)):
        # Redirects user to /complete if all questions answered
            #Set responses [] to empty

        return redirect("/complete")

    if (len(RESPONSES) != question_id):
        # Redirects user to current questin if attempting to access questions out of order
        flash(f"Invalid question id: {question_id}.")
        return redirect(f"/questions/{len(RESPONSES)}")

# Sets survey question to variable to render it in HTML template
    question = survey.questions[question_id]
    return render_template(
        "question.html", question_num=question_id,  question=question, survey=survey)


@app.route("/complete")
def complete():
    """Renders comletion confirmation page when user completes survery."""
    
    return render_template("completion.html", survey=survey)


