import json
import logging
import requests
logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
#r = requests.post('http://ec2-54-197-14-241.compute-1.amazonaws.com:8080', data = {'type': 'speech', 'emotion': 'Stand/Gestures/IDontKnow_3', 'message': 'Testing Speech'})
#r = requests.get('https://rfhqzzslrj.localtunnel.me/say', data = {'type': 'speech', 'emotion': 'Stand/Gestures/IDontKnow_3', 'message': 'Testing Speech'})
#### HELPERS
def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }
def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
def get_welcome_response():
    
    # format welcome response
    session_attributes = {}
    card_title = "Welcome"
    reprompt_text = speech_output = "Hello! My name is Andra. What is your name?"
    # If the user either does not reply to the welcome message or says something
    # that is
    should_end_session = False
    response = build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
    logger.debug(json.dumps(response, indent=2))
    return response
def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    logger.debug(json.dumps(event, indent=2))
    # create new session
    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
def on_session_started(session_started_request, session):
    """ Called when the session starts """
    logger.info("on_session_started requestId=" + session_started_request['requestId']   + ", sessionId=" + session['sessionId'])
def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
       want
       """
    logger.info("on_launch requestId=" + launch_request['requestId'] + ", sessionId=" + session['sessionId'])
    return get_welcome_response()
def log_object(object):
    logger.debug(json.dumps(object, indent=2))
def process_intent(request, intent, session):
    logger.debug("processing intent")
    logger.debug("dialogState is " + request["dialogState"])
    session_attributes = get_filled_slot(session)
    if request["dialogState"] == "STARTED":
        updatedIntent = intent
        return build_response(session_attributes, build_response_directive_with_no_intent())
    elif request["dialogState"] != "COMPLETED":
        return build_response(session_attributes, build_response_directive_with_no_intent())
    else:
        name = request["intent"]["slots"]["Name"]["value"]
        #name_resp = "Hi {}. I'd like to work with you to help you maintain a healthy level of physical activity. What activity would you like to do more over the next week?"
        #resp_txt = name_resp.format(name)        
        #r = requests.get('https://rfhqzzslrj.localtunnel.me/say', data = {'type': 'speech', 'emotion': 'Stand/Gestures/IDontKnow_3', 'message': resp_text})
        current_minutes = int(request["intent"]["slots"]["CurrentMinutes"]["value"])
        
        #new_minutes = minuteFormula()
        if current_minutes < 30:
            new_min = current_minutes + 30
            speech_output = "That's great {0}. Can we try to increase your physical activity time from {1} to {2} minutes next week. See you during our next session.".format(name,current_minutes,new_min) 
        elif current_minutes >= 30:
            new_min = current_minutes + 10
            speech_output = "That's great {0}, that's better than the national average. As a stretch goal, how about trying to increase your time from {1} to {2} minutes next week. Thank you for your time.".format(name,current_minutes,new_min)
            
        #if new_goal == "yes":
        #    speech_output = "Let's try again during our next session!"
        #else:
        #    speech_output = "Thanks for your time {0}, I feel like we have created a clear goal for you to work on this week.".format(name)
        return build_response(session_attributes, build_speechlet_response( intent['name'], speech_output, None, True))
def build_response_directive_with_no_intent():
    return \
        {
        "outputSpeech": None,
        "card": None,
        "directives": [{
            "type": "Dialog.Delegate"
        }],
        "reprompt": None,
        "shouldEndSession": False
    }
# figures out what slots have been filled
def get_filled_slot(session):
    return session
def on_intent(intent_request, session):
    logger.debug("on_intent requestId=" + intent_request['requestId'] + ", sessionId=" + session['sessionId'])
    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    # Intents:
    # SocialBot
    # Dispatch to your skill's intent handlers
    if intent_name == "SocialBotIntent":
        return process_intent(intent_request, intent, session)
        
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")
def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.
    Is not called when the skill returns should_end_session=true
    """
    logger.debug("on_session_ended requestId=" + session_ended_request['requestId'] + ", sessionId=" + session['sessionId'])
def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you and good bye!"
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))
def minuteFormula(current_minutes):
    new_minutes = 0
    
    if current_minutes < 30:
        new_minutes = current_minutes + 30
    elif current_minutes >= 30:
        new_minutes = current_minutes + 10
    else:
        pass
    
    return new_minutes
