import sys
from io import BytesIO
import telegram
from flask import Flask, request, send_file
from fsm import TocMachine


API_TOKEN = '392569036:AAGLhfB-lQNYvXCXEPVMEj2t7xtd5-AFMf0'
WEBHOOK_URL = 'https://7969a632.ngrok.io/hook'

app = Flask(__name__)
bot = telegram.Bot(token=API_TOKEN)
machine = TocMachine(
    states=[
        'user',
        'state0',
        'state1',   #hello
        'state2',   #Y
        'state3',   #N
        'state4',    #boy or girl
        'state5',   #getcity_ask_indoor exercise
        'state6',    #indoor_got
        'state7',
        'state8',
        'state9',
        'state10',
        'state11',
        'state12',
        'state13',
        'state14',
        'state15',
        'state16',
        'state17',
        'state18',
        'state19',
        'state20',
        'state21',
        'state22',
        'state23',
        'state24',
        'state25',
        'state_park',
        'state_no_park'
        
    ],
    transitions=[
        {
            'trigger':'advance',
            'source':'user',
            'dest':'state0',
            'conditions':'to_start'
        },
        {
            'trigger': 'advance',
            'source': ['state0','user'],
            'dest': 'state1',
            'conditions':'go_exercise'
        },
        {
            'trigger': 'advance',
            'source': ['state0','user'],
            'dest': 'state10',
            'conditions': 'play_game'
        },
        {
            'trigger':'advance',
            'source':['state0','user'],
            'dest':'state16',
            'conditions':'count_Calorie'
        },
        {
            'trigger':'advance',
            'source':'state16',
            'dest':'state17',
            'conditions':'satisfied'
        },        
        {
            'trigger':'advance',
            'source':'state17',
            'dest':'state18',
            'conditions':'get_height'
        },
        {
            'trigger':'advance',
            'source':'state16',
            'dest':'state3',
            'conditions':'not_satisfied'
        },
        {
            'trigger':'advance',
            'source':'state18',
            'dest':'state19',
            'conditions':'get_weight'
        },
        {
            'trigger':'advance',
            'source':'state19',
            'dest':'state20',
            'conditions':'get_age'
        },
        {
            'trigger':'advance',
            'source':'state20',
            'dest':'state21',
            'conditions':'get_workouttime'
        },        
        {
            'trigger':'advance',
            'source':'state21',
            'dest':'state22',
            'conditions':'get_sex'
        }, 
        {
            'trigger':'advance',
            'source':'state22',
            'dest':'state23',
            'conditions':'how_to_deal_tdee'
        },
        {
            'trigger':'advance',
            'source':'state23',
            'dest':'state24',
            'conditions':'get_food'
        },
        {
            'trigger':'advance',
            'source':['state1','state2','state3','state4','state5','state6','state7','state8','state9','state10'
            ,'state11','state12','state13','state14',
            'state15','state16','state17','state18',
            'state19','state20','state21','state22',
            'state23','state24','state25'],
            'dest':'state3',
            'conditions':'to_quit'
        },         
        {
            'trigger':'advance',
            'source':'state24',
            'dest':'state24',
            'conditions':'get_food'
        },
        {
            'trigger':'advance',
            'source':'state24',
            'dest':'state25',
            'conditions':'get_food_weight'
        },    
        {
            'trigger':'advance',
            'source':'state25',
            'dest':'state24',
            'conditions':'get_food'
        },       
        {
            'trigger': 'advance',
            'source': 'state10',
            'dest':'state11',
            'conditions': 'satisfied'
        },
        {
            'trigger': 'advance',
            'source': 'state10',
            'dest': 'state3',
            'conditions': 'not_satisfied'
        },
        {
            'trigger': 'advance',
            'source': 'state10',
            'dest': 'state10',
            'conditions': 'other_from_YorN'
        },
       
        {
            'trigger': 'advance',
            'source': 'state11',
            'dest': 'state12',
            'conditions': 'satisfied'
        },
        {
            'trigger': 'advance',
            'source': 'state11',
            'dest': 'state3',
            'conditions': 'not_satisfied'
        },
        {
            'trigger':'advance',
            'source':'state12',
            'dest':'state13',
            'conditions':'get_answer_right'
        },
        {
            'trigger':'advance',
            'source':'state12',
            'dest':'state14',
            'conditions':'get_answer_wrong'
        },
        {
            'trigger':'advance',
            'source':['state13','state15'],
            'dest':'state13',
            'conditions':'get_answer_right'
        },
        {
            'trigger':'advance',
            'source':['state13','state15'],
            'dest':'state14',
            'conditions':'get_answer_wrong'
        },
        {
            'trigger':'advance',
            'source':'state14',
            'dest':'state15',
            'conditions':'satisfied'
        },
        {
            'trigger':'advance',
            'source':'state14',
            'dest':'state12',
            'conditions':'not_satisfied'
        },

        {
            'trigger': 'advance',
            'source': 'state1',
            'dest': 'state2',
            'conditions': 'is_going_to_state2'
        },
        {
            'trigger': 'advance',
            'source': 'state1',
            'dest': 'state3',
            'conditions': 'Dont_workout'
        },
        {
            'trigger': 'advance',
            'source': 'state1',
            'dest': 'state1',
            'conditions': 'other_from_YorN'
        },
        {
            'trigger': 'advance',
            'source': 'state2',
            'dest': 'state2',
            'conditions': 'S5_to_S2'
        },
        {
            'trigger': 'advance',
            'source': 'state2',
            'dest': 'state4',
            'conditions': 'Male_Female'
        },
        {
            'trigger':'advance',
            'source':'state4',
            'dest':'state5',
            'conditions':'City_Request'
        },
        {
            'trigger':'advance',
            'source':'state4',
            'dest':'state4',
            'conditions':'S4_to_S4'
        },
        {
            'trigger':'advance',
            'source':'state5',
            'dest':'state_no_park',
            'conditions':'not_satisfied'
        },
        {
            'trigger':'advance',
            'source':'state5',
            'dest':'state_park',
            'conditions':'want_park_info'
        },        
        {
            'trigger':'advance',
            'source':['state_park','state_no_park'],
            'dest':'state7',
            'conditions':'not_satisfied'
        },
        {
            'trigger':'advance',
            'source':['state_park','state_no_park'],
            'dest':'state6',
            'conditions':'want_to_work_inside'
        },
        {
            'trigger':'advance',
            'source':'state7',
            'dest':'state6',
            'conditions':'satisfied'
        },
        {
            'trigger':'advance',
            'source':'state7',
            'dest':'state9',
            'conditions':'not_satisfied'
        },
        {
            'trigger':'advance',
            'source':'state6',
            'dest':'state8',
            'conditions':'satisfied'
        },
        {
            'trigger':'advance',
            'source':'state6',
            'dest':'state9',
            'conditions':'not_satisfied'
        },
        {
            'trigger': 'go_back',
            'source': [
            	'state8',
                'state9',
                'state3',
                'state14',
                'state13',
                'state26'
            ],
            'dest': 'user'
        }
    ],
    initial='user',
    auto_transitions=False,
    show_conditions=True,
)


def _set_webhook():
    status = bot.set_webhook(WEBHOOK_URL)
    if not status:
        print('Webhook setup failed')
        sys.exit(1)
    else:
        print('Your webhook URL has been set to "{}"'.format(WEBHOOK_URL))


@app.route('/hook', methods=['POST'])
def webhook_handler():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    machine.advance(update)
    return 'ok'


@app.route('/show-fsm', methods=['GET'])
def show_fsm():
    byte_io = BytesIO()
    machine.graph.draw(byte_io, prog='dot', format='png')
    byte_io.seek(0)
    return send_file(byte_io, attachment_filename='fsm.png', mimetype='image/png')


if __name__ == "__main__":
    _set_webhook()
app.run()
