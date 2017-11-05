from typing import List
from collections import OrderedDict

BASE_QUESTION = "Over the past 2 weeks, how often have you been bothered by any of the following problems?"

QUESTIONS = OrderedDict([
    ('Q1', "Little interest or pleasure in doing things"),
    ('Q2', "Feeling down, depressed or hopeless"),
    ('Q3', "Trouble falling asleep, staying asleep, or sleeping too much"),
    ('Q4', "Feeling tired or having little energy"),
    ('Q5', "Poor appetite or overeating"),
    ('Q6', "Feeling bad about yourself - or that you’re a failure or have let yourself or your family down"),
    ('Q7', "Trouble concentrating on things, such as reading the newspaper or watching television"),
    ('Q8', "Moving or speaking so slowly that other people could have noticed. Or, the opposite - being so  dgety or restless that you have been moving around a lot more than usual"),
    ('Q9', "Thoughts that you would be better off dead or of hurting yourself in some way"),
    ('Q10', "If you checked off any problems, how difcult have those problems made it for you to do your work, take care of things at home, or get along with other people?")
])

SCORES = {
    'Not at all': 0,
    'Several Days': 1,
    'More Than Half the Days': 2,
    'Nearly Every Day': 3,
}

ANSWERS = {question_key: list(SCORES.keys())[0] for question_key in QUESTIONS.keys()}

def output(answers: List[str]) -> str:
    # Step 1
    if SCORES[answers['Q1']] >= 2 and SCORES[answers['Q2']] >= 2:
        print(score)
        # Step 2
        if sum(1 for (question_key, answer) in answers if SCORES[answer] >= 2 ) + (1 if SCORES[answers['Q9']] >= 1 else 0) >= 5:
            # Step 3
            if SCORES[answers['Q10']] >= 1:
                score = 0
                for (question_key, question) in QUESTIONS.items():
                    score += SCORES[answers[question_key]]

                if score < 5:
                    mental_assessment = 'Healthy'
                elif 5 <= score <= 9:
                    mental_assessment = 'Minimal Symptoms'
                elif 10 <= score <= 14:
                    mental_assessment = 'Minor depression'
                elif 15 <= score <= 19:
                    mental_assessment = 'Major depression, moderately severe'
                elif score >= 20:
                    mental_assessment = 'Major Depression, severe'
                else:
                    raise Exception('Unexpected score: {0}'.format(score))
            else:
                mental_assessment = 'Healthy'
        else:
            mental_assessment = 'Healthy'
    else:
        mental_assessment = 'Healthy'

    return mental_assessment

if  __name__ == '__main__':
    print(output(ANSWERS))
