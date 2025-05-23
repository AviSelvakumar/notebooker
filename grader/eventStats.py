from openai import OpenAI
from django.http import HttpResponse
import json

client = OpenAI(api_key="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", base_url="https://openrouter.ai/api/v1")

class Rubric:
    def __init__(self, rubric):
        self.rubric = rubric
        self.prompt =  "A response where the " + rubric["0-1"] + "recieves a score of 0-1. A response where the " + rubric["2-3"] + "recieves a score of 2-3. A response where the " + rubric["4-5"] + "recieves a score of 4-5."

designProcessRubric = Rubric({
    '0-1': "Team shows little to no evidence of independent inquiry in their design process.",
    '2-3': "Team shows evidence of independent inquiry for some elements of their design process.",
    '4-5': "Team shows evidence of independent inquiry from the beginning stages of their design process. This includes brainstorming, testing, and exploring alternative solutions."
})

strategyRubric = Rubric({
    '0-1': "Team did not explain game strategy/strategy is not student-directed.",
    '2-3': "Team can explain their current strategy with limited evidence of game analysis.",
    '4-5': "Team can fully explain their entire game strategy including game analysis."
})

designRubric = Rubric({
    '0-1': "Team did not explain robot design, or design is not student-directed.",
    '2-3': "Team can provide a limited description of why the current robot design was chosen, but shows limited evolution",
    '4-5': "Team can fully explain the evolution of their robot design to the current design."
})

buildRubric = Rubric({
    '0-1': "Team did not explain robot build, or build is not student-directed.",
    '2-3': "Team can describe why the current robot design was chosen, but with limited explanation.",
    '4-5': "Team can fully explain their robot construction. Ownership of the robot build is evident."
})

programmingRubric = Rubric({
    '0-1': "Team did not explain programming, or programming is not student-directed.",
    '2-3': "Team can describe how the current programs work, but with limited evolution.",
    '4-5': "Team can fully explain the evolution of their programming."
})

creativeRubric = Rubric({
    '0-1': "Team has difficulty describing a creative solution or gives minimal response",
    '2-3': "Team can describe a creative solution but the answer lacks detail.",
    '4-5': "Team can describe creative aspect(s) of their robot with clarity and detail."
})

teamworkRubric = Rubric({
    '0-1': "Team cannot explain how team progress was monitored or how resources were managed.",
    '2-3': "Team can explain how team progress was monitored, and some degree of management of material and personnel resources.",
    '4-5': "Team can explain how team progress was tracked against an overall project timeline. Team can explain management of material and personnel resources."
})

class Question:
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text

questionList = [
"What does your robot do, and how does it score points?",  
"How did you develop this robot design?",  
"Which team members built the robot?",  
"What part of your robot are you most proud of? Why?",  
"Were there any other robots that inspired your robot design? How?",  
"What changes did you make to improve your design during the season?",  
"What was the most difficult challenge your team has overcome so far?",  
"Did you use any sensors? What are they used for? How do they operate in your autonomous mode? How do they operate in your driver-controlled mode?",  
"What problems did you have in working on your robot? How did your team solve them?",  
"If you had one more week to work on your robot, how would you improve it?",  
"Has your game strategy been effective? How and why?",  
"Tell us about your robot’s programming; who was the primary programmer?",  
"What were the challenges of this year’s game that you considered before designing your robot? How did you design your robot to meet those challenges?",  
"What are your goals for Driver Skills and Autonomous Coding Skills scores? What are your average scores?",
]
question = "How did you develop this robot design?"

responses = []

questionsAndResponses = {}

content = "You are a judge at a high school VEX Robotics competition interviewing competing teams. You will evaluate a team's interview based on the following rubric: In the Engineering Design Process category, " + designProcessRubric.prompt + " In the Game Strategies category, " + strategyRubric.prompt + " In the Robot Design category, " + designRubric.prompt + " In the Robot Build category, " + buildRubric.prompt + " In the Robot Programming category, " + programmingRubric.prompt + " In the Creativity / Originality category, " + creativeRubric.prompt + " In the Team and Project Management category, " + teamworkRubric.prompt

def gradeInterview(request):
    interviewJSON = request.body.decode('utf-8')
    interviewPy = json.loads(interviewJSON)
    interview = ""
    for key in interviewPy:
        if interviewPy[key] != "":
            interview += key + ": " + interviewPy[key] + "\n"
    print(interview)
    if interview == "":
        return HttpResponse(status=400)
    completion = client.chat.completions.create(
    model='google/gemini-2.0-flash-exp:free',
    extra_body={
        'models': ["google/gemini-2.0-pro-exp-02-05:free"]
    },
    messages=[
        {
            "role": "system",
            "content": "You are a helpful mentor for high school VEX Robotics students providing feedback on a practice verbal interview. You will evaluate a team's interview based on the following rubric: In the Engineering Design Process category, " + designProcessRubric.prompt + " In the Game Strategies category, " + strategyRubric.prompt + " In the Robot Design category, " + designRubric.prompt + " In the Robot Build category, " + buildRubric.prompt + " In the Robot Programming category, " + programmingRubric.prompt + " In the Creativity / Originality category, " + creativeRubric.prompt + " In the Team and Project Management category, " + teamworkRubric.prompt + " Score the interview as a whole. Use this JSON Schema: {'score':  int,\n'feedback': str}. Output only the JSON. Do not wrap the JSON codes in JSON markers. Do not use markdown. Add a blank line at the top and bottom of the JSON. Start by scoring the interview in each category, then add up the scores to get the total score. Finally, provide an overall score and feedback for the interview. Ensure answers are specific and detailed. Scores within each category can be a zero. The interview will be in the following format: 'question': 'answer'. Pick one specific score. Do not provide a range of scores."
        },
        {
        "role": "user",
        "content": interview
        }
    ],
    response_format={
        'type': 'json_schema',
        'json_schema': {
            'name': 'aiResponse',
            'strict': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'score': {
                        'type': 'int',
                        'description': 'Total grade that interview recieves. This field should only be the total score. Do not place any text here.'
                    },
                    'feedback': {
                        'type': 'string',
                        'description': 'Feedback on how to improve interview score',
                    },
                    'engineeringDesignProcess': {
                        'type': 'int',
                        'description': 'Score that interview recieves in the Engineering Design Process category'
                    },
                    'gameStrategy': {
                        'type': 'int',
                        'description': 'Score that interview recieves in the Game Strategy category'
                    },
                    'robotDesign': {
                        'type': 'int',
                        'description': 'Score that interview recieves in the Robot Design category'
                    },
                    'robotBuild': {
                        'type': 'int',
                        'description': 'Score that interview recieves in the Robot Build category'
                    },
                    'robotProgramming': {
                        'type': 'int',
                        'description': 'Score that interview recieves in the Robot Programming category'
                    },
                    'creativityOriginality': {
                        'type': 'int',
                        'description': 'Score that interview recieves in the Engineering Design Process category'
                    },
                    'teamAndProjectManagement': {
                        'type': 'int',
                        'description': 'Score that interview recieves in the Team and Project Management category'
                    }
                },
                'required': ['score', 'feedback', 'engineeringDesignProcess', 'gameStrategy', 'robotDesign', 'robotBuild', 'robotProgramming', 'creativityOriginality', 'teamAndProjectManagement']
            }
        }
    })
    processed = "".join(completion.choices[0].message.content.replace("```json", "").replace("```", "").splitlines())
    print(processed)
    return HttpResponse(processed)

def getQuestionsJSON():
    return json.dumps(questionList)


