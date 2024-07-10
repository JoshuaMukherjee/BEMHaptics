from controller import Controller
from pages import ID_page, Text_Page, Response_Page
from haptics_code import get_hand_to_path
from acoustools.Levitator import LevitatorController
import time, pickle, random

mat_to_world = (1, 0, 0, 0,
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
        f.write(str(controller.data["pose"]))
        f.write('\n')

def pick_img(x):
    controller = x.controller
    pose = random.randint(0,5)
    controller.data["pose"] = pose
    print(pose)
    img = controller.imgs[pose]
    print(img)

    controller.frames['scan_page'].img_label.grid_forget()
    controller.frames['scan_page'].img_label.configure(image=img)
    controller.frames['scan_page'].img_label.image = img
    controller.frames['scan_page'].img_label.grid(row = 1, column = 0, padx = 10, pady = 10) 


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
        "button_func": lambda x: pick_img(x),
        "next_page": 'scan_page'
    }, 

    {
        'text_args':{
            "text":"Orient your hand like this (as viewed from below - your palm should face down). Press the button when in place",
            "wraplength":800
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

pth = './HapticsGUI/Media/HandPositions/'
imgs = [pth+'flat_bottom.png', pth+'ok_bottom.png', pth+'peace_bottom.png', pth+'pinch_bottom.png', pth+'point_bottom.png', pth+'spiderman_bottom.png']

gui = Controller(pages, page_names, page_args,imgs=imgs)
gui.mainloop()