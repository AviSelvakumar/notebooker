from flask import Flask, render_template, request
from forms import InterviewForm
from eventStats import gradeInterview

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Define the route for the interview page
@app.route('/', methods=['GET', 'POST'])
def interview():
    form = InterviewForm()  # Create an instance of the interview form
    if form.validate_on_submit():
        responses = {}
        for question in form.questions:
            responses[question.label.text] = question.data
        interviewScript = ""
        for question in responses:
            interviewScript += question + ": " + responses[question] + "\n"
        # Here you would add your grading logic
        feedback = gradeInterview(interviewScript)
        
        return render_template('result.html', responses=responses, feedback=feedback)

    return render_template('interview.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
