from controller import Controller
from pages import ID_page, Text_Page, Response_Page
from haptics_code import get_hand_to_path
from acoustools.Levitator import LevitatorController
import time, pickle

mat_to_world = (-1, 0, 0, 0,
                    0, 1, 0, 0,
                    0, 0, 1, 0,
                    0, 0, 0, 1)

lev = LevitatorController(ids=(73,),matBoardToWorld=mat_to_world)
lev.set_frame_rate(200)

index = 0
REST_IDX = 2

def f(x):
    global index
    old_text = x.into_label['text']
    x.into_label['text'] = 'Scanning... \n Please Wait'
    x.update()
    while True:
        try:
            index += 1
            holograms, times, number, bem = get_hand_to_path(x.controller.data["participant_id"]+'_'+str(index), path='HapticsGUI/Media/')
            pickle.dump(times, open('./HapticsGUI/Media/Times/times_'+x.controller.data["participant_id"] + '_' + str(index),'wb'))
            
            x.controller.data['bem'] = bem
            x.controller.data['true_number'] = number

            lev.levitate(holograms, num_loops=10)
            print(number)
            break
        except Exception as e:
            print(e)
    lev.turn_off()
    print((times[-1] - times[0]) / 1e9)
    x.into_label['text'] = old_text

def write_responses(controller):
    global index
    with open('HapticsGUI\Media\Responses\\' + controller.data["participant_id"] +'_'+ str(index) + '.txt', 'w') as f:
        f.write(str(controller.data['true_number']))
        f.write('\n')
        f.write(str(controller.data['bem']))
        f.write('\n')
        f.write(str(controller.data["intensity"]))
        f.write('\n')
        f.write(str(controller.data["number"]))
        f.write('\n')


pages = [ID_page, Text_Page, Text_Page, Response_Page,Text_Page]

page_args = [
    {
            "title_label_args":{
                "text":'Haptics User Study'
            },
            "info_label_args":{
                "text":"Welcome to the Study..."
            },
            "next_page": 'text_page'
    },
    
    {
        'text_args':{
            "text":"You will have a randomly chosen number 1-9 rendered on your hand. \n You will be asked to predict which number you felt and also rank how intense the sensation was ",
            "wraplength":800
            },
        "next_page": 'scan_page'
    }, 

    {
        'text_args':{
            "text":"Press Button when hand is in place..."
            },
        "button_func": lambda x: f(x),
        "next_page": 'response_page'
        
    },
    {
         'text_args':{
            "text":"Rate Intensity & Please enter the number you belive you felt...",
            "wraplength":800
        },
         "next_page": 'scan_page',
         "extra_func":write_responses,
         "rest_page":'rest_page',
         "rest_id":REST_IDX
    },
    {
        'text_args':{
            "text":"Please take a rest"
            },
        "next_page": 'scan_page',
        "button_delay":5000
        
    },
]


page_names = ['start_page', 'text_page', 'scan_page','response_page','rest_page']


gui = Controller(pages, page_names, page_args)
gui.mainloop()