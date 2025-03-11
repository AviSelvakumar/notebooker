from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

class Question:
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text

questionList = [
Question("What does your robot do, and how does it score points?"),  
Question("How did you develop this robot design?"),  
Question("Which team members built the robot?"),  
Question("What part of your robot are you most proud of? Why?"),  
Question("Were there any other robots that inspired your robot design? How?"),  
Question("What changes did you make to improve your design during the season?"),  
Question("What was the most difficult challenge your team has overcome so far?"),  
Question("Did you use any sensors? What are they used for? How do they operate in your autonomous mode? How do they operate in your driver-controlled mode?"),  
Question("What problems did you have in working on your robot? How did your team solve them?"),  
Question("If you had one more week to work on your robot, how would you improve it?"),  
Question("Has your game strategy been effective? How and why?"),  
Question("Tell us about your robot’s programming; who was the primary programmer?"),  
Question("What were the challenges of this year’s game that you considered before designing your robot? How did you design your robot to meet those challenges?"),  
Question("What are your goals for Driver Skills and Autonomous Coding Skills scores? What are your average scores?"),
]

class InterviewForm(FlaskForm):
    questions = []
    for i, question in enumerate(questionList):
        questions.append(TextAreaField(question.text, validators=[DataRequired()]))