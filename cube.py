import cv2
import numpy as np


Sign_Conv = {
            'green'  : 'F',
            'white'  : 'U',
            'blue'   : 'B',
            'red'    : 'R',
            'orange' : 'L',
            'yellow' : 'D'
            }


Color = {
        'red'    : (0,0,255),
        'orange' : (0,150,255),
        'blue'   : (255,0,0),
        'green'  : (0,230,0),
        'white'  : (255,255,255),
        'yellow' : (0,255,255),
        'ini': (150,150,150)
        }


State = {
            'up'   :['ini','ini','ini','ini','white','ini','ini','ini','ini',],
            'right':['ini','ini','ini','ini','red','ini','ini','ini','ini',],
            'front':['ini','ini','ini','ini','green','ini','ini','ini','ini',],
            'down' :['ini','ini','ini','ini','yellow','ini','ini','ini','ini',],
            'left' :['ini','ini','ini','ini','orange','ini','ini','ini','ini',],
            'back' :['ini','ini','ini','ini','blue','ini','ini','ini','ini',],
        }



stickers = {
        'face': [
            [200, 120], [300, 120], [400, 120],
            [200, 220], [300, 220], [400, 220],
            [200, 320], [300, 320], [400, 320]
        ],
        
        'current': [
            [20, 20], [54, 20], [88, 20],
            [20, 54], [54, 54], [88, 54],
            [20, 88], [54, 88], [88, 88]
        ],
        'preview': [
            [20, 130], [54, 130], [88, 130],
            [20, 164], [54, 164], [88, 164],
            [20, 198], [54, 198], [88, 198]
        ],
        'left': [
            [30, 280], [74, 280], [118, 280],
            [30, 324], [74, 324], [118, 324],
            [30, 368], [74, 368], [118, 368]
        ],
        'front': [
            [178, 280], [222, 280], [266, 280],
            [178, 324], [222, 324], [266, 324],
            [178, 368], [222, 368], [266, 368]
        ],
        'right': [
            [326, 280], [370, 280], [414, 280],
            [326, 324], [370, 324], [414, 324],
            [326, 368], [370, 368], [414, 368]
        ],
        'back': [
            [474, 280], [518, 280], [562, 280],
            [474, 324], [518, 324], [562, 324],
            [474, 368], [518, 368], [562, 368]
        ],
        'up': [
            [178, 128], [222, 128], [266, 128],
            [178, 172], [222, 172], [266, 172],
            [178, 216], [222, 216], [266, 216]
        ],
        'down': [
            [178, 434], [222, 434], [266, 434],
            [178, 478], [222, 478], [266, 478],
            [178, 522], [222, 522], [266, 522]
        ] 
    }

def draw_stickers(input_frame,stickers,name):
        for x,y in stickers[name]:
            cv2.rectangle(input_frame, (x,y), (x+30, y+30), (255,255,255), 2)


def draw_preview_stickers(frame,stickers):
        face=['front','back','left','right','up','down']
        for name in face:
            for x,y in stickers[name]:
                cv2.rectangle(frame, (x,y), (x+40, y+40), (255,255,255), 2)
                
def fill_stickers(input_frame,stickers,sides):    
    for side,colors in sides.items():
        num=0
        for x,y in stickers[side]:
            cv2.rectangle(input_frame,(x,y),(x+40,y+40),Color[colors[num]],-1)
            num+=1


            
def color_detect(h,s,v):
    if h < 5 and s>5 :
        return 'red'
    elif h <10 and h>=3:
        return 'orange'
    elif h <= 25 and h>10:
        return 'yellow'
    elif h>=50 and h<=70 and s>80 and v<220:
        return 'green'
    elif h <= 130 and s>70:
        return 'blue'
    elif h <= 100 and s<10 and v<200:
        return 'white'

    return 'white'

check_state=[]

if __name__=='__main__':
    
    cap=cv2.VideoCapture(0)

    preview = np.zeros((650,800,3), np.uint8)

    while True:
        hsv=[]
        current_state=[]
        ret,image=cap.read()
        input_frame = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = np.zeros(input_frame.shape, dtype=np.uint8)   

        draw_stickers(image,stickers,'face')
        draw_preview_stickers(preview,stickers)
        fill_stickers(preview,stickers,State)

        for i in range(9):
            hsv.append(input_frame[stickers['face'][i][1]+10][stickers['face'][i][0]+10])
        
        a=0
        for x,y in stickers['current']:
            color_name=color_detect(hsv[a][0],hsv[a][1],hsv[a][2])
            a+=1
            current_state.append(color_name)
        
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
        elif k ==ord('u'):
            State['up']=current_state
            check_state.append('u')
        elif k ==ord('r'):
            check_state.append('r')
            State['right']=current_state
        elif k ==ord('l'):
            check_state.append('l')
            State['left']=current_state
        elif k ==ord('d'):
            check_state.append('d')
            State['down']=current_state       
        elif k ==ord('f'):
            check_state.append('f')
            State['front']=current_state       
        elif k ==ord('b'):
            check_state.append('b')
            State['back']=current_state       

        cv2.imshow('Preview',preview)
        cv2.imshow('Input Frame',image[0:450,0:500])

    cv2.destroyAllWindows()