from flask import Flask, request, render_template, redirect, flash, session
from surveys import satisfaction_survey as survey

responses_key = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = "its_secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


@app.route('/')
def show_survey_start():

    return render_template('/survey_start.html', survey=survey)


"""redirect to question 0 on start"""


@app.route('/begin', methods=["POST"])
def start_survey():
    """Clear all session responses"""
    session[responses_key] = []

    return redirect("/questions/0")


@app.route("/answer", methods=["POST"])
def handle_question():
    """Save response and redirect to next question."""

    # get the response choice
    choice = request.form['answer']

    # add this response to the session
    responses = session[responses_key]
    responses.append(choice)
    session[responses_key] = responses

    if (len(responses) == len(survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    else:
        return redirect(f"/questions/{len(responses)}")


@app.route('/questions/<int:qid>')
def show_question(qid):
    """Display current question"""
    responses = session.get(responses_key)

    if (responses is None):

        return redirect('/')

    if (len(responses) == len(survey.questions)):

        return redirect('/complete')

    if (len(responses) != qid):
        flash(f"Invalid question id: {qid}.")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[qid]
    return render_template(
        'question.html', question_num=qid, question=question)


@app.route('/complete')
def complete():
    return render_template("completion.html")
