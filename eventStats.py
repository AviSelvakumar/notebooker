from openai import OpenAI

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
question = Question("How did you develop this robot design?")

responses = []

questionsAndResponses = {}
"""
for i, question in enumerate(questionList):
    response = input(question.text + " ")
    responses.append(response)

for i, question in enumerate(responses):
    questionsAndResponses[questionList[i]] = responses[i]

userInterview = ""

for question in questionsAndResponses:
    userInterview += question.text + ": " + questionsAndResponses[question] + "\n"

print(userInterview)"

print(content)

if response == 'debug':
    response = "In the drivetrain, we decied to reuse our drivetrain from last year with a 36:48 gear ratio as it saved us time and was still suitable for this year's game, providing enough torque to push other robots in defensive situations and enough speed to quickly reach positive and negative corners before other robots. Building a new drivetrain would have cost us time that we don't have. In order to grab the mobile goal, we decided to go with a pneumatic clamp as pneumatics are both fast and powerful. A motor with enough torque to clamp onto the mobile goal would have required our robot to stop moving for a while to clamp on since it is slower. In order to intake rings, we decided to use flexwheels and a conveyor belt system to move rings onto the mobile goal. We considered using a 'hood' system to push rings onto the mobile goal, but we decied against it as it required us to tune our mobile goal clamp to be more precice."
"""

content = "You are a judge at a high school VEX Robotics competition interviewing competing teams. You will evaluate a team's interview based on the following rubric: In the Engineering Design Process category, " + designProcessRubric.prompt + " In the Game Strategies category, " + strategyRubric.prompt + " In the Robot Design category, " + designRubric.prompt + " In the Robot Build category, " + buildRubric.prompt + " In the Robot Programming category, " + programmingRubric.prompt + " In the Creativity / Originality category, " + creativeRubric.prompt + " In the Team and Project Management category, " + teamworkRubric.prompt

def gradeInterview(interview):
    completion = client.chat.completions.create(
    model="google/gemini-2.0-pro-exp-02-05:free",
    messages=[
        {
            "role": "system",
            "content": "You are a judge at a high school VEX Robotics competition interviewing competing teams. You will evaluate a team's interview based on the following rubric: In the Engineering Design Process category, " + designProcessRubric.prompt + " In the Game Strategies category, " + strategyRubric.prompt + " In the Robot Design category, " + designRubric.prompt + " In the Robot Build category, " + buildRubric.prompt + " In the Robot Programming category, " + programmingRubric.prompt + " In the Creativity / Originality category, " + creativeRubric.prompt + " In the Team and Project Management category, " + teamworkRubric.prompt
        },
        {
        "role": "user",
        "content": interview
        }
    ])
    return completion.choices[0].message.content