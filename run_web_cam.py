from hand_tracker import HandTracker
import cv2
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import warnings
import random
import sys
import argparse


print("you must need webcam to run this code....")
option=input("y or n... ")
if option=="n" or option!="y":
  sys.exit()

palm_model_path = "./models/palm_detection.tflite"
landmark_model_path = "./models/hand_landmark.tflite"
anchors_path = "./data/anchors.csv"

# box_shift determines 
detector = HandTracker(palm_model_path, landmark_model_path, anchors_path,
                       box_shift=0.2, box_enlarge=1.3)





def finger_det():

  print("place ur right hand with gesture shows in picture in front of web cam..... ")
  print("image will click after countdown three....")
  time.sleep(3)
  i=3
  while i>0:
    print(i)
    time.sleep(1)
    i-=1
  cap = cv2.VideoCapture(0)
  seconds = 1

  millis = seconds * 1000
  while (millis > 0):
    # Capture frame-by-frame
    ret, frame = cap.read()
    millis = millis - 10
    # Display the resulting frame
    cv2.imshow('video recording', frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        #this method holds execution for 10 milliseconds, which is why we 
        #reduce millis by 10
        break

  img=frame
  
  scale_percent = 25 # percent of original size
  width = int(img.shape[1] * scale_percent / 100)
  height = int(img.shape[0] * scale_percent / 100)
  dim = (width, height)
    
  # resize image
  img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
  img_gray = img.copy()[:,:,::-1]

  kp, box = detector(img_gray)
  x=kp[:,0].tolist()
  y=kp[:,1].tolist()

  if y[8]>y[4]:
    hand=6
  elif y[20]<y[14] and y[16]<y[10] and x[8]<x[4]:
    hand=5
  elif y[20]<y[14] and x[8]>x[4]:
    hand=4
  elif y[20]>y[14] and y[16]<y[10]:
    hand=3
  elif y[16]>y[10] and y[12]<y[8]:
    hand=2
  elif y[12]>y[8]:
    hand=1
  

  # Radius of circle
  radius = 2
    
  # Blue color in BGR
  color = (255, 0, 0)
  thickness=5 

  cv2.circle(img, (int(x[8]),int(y[8])), radius, color, thickness)
  img=cv2.circle(img, (int(x[4]),int(y[4])), radius, color, thickness)

  return hand,img

def batting(user1,user2):
  bat = user1
  bowl = user2

  if bat != bowl:
    batsman_runs=bat
    innings_score.append(bat)
    score=sum(innings_score)
  
  else:
    batsman_runs="outtttt......"
    print(batsman_runs)
    score=sum(innings_score)

  return batsman_runs,score

def gameplay_first_innings(u,o):

  i=1

  while i<=6:
    print(str(i)+" ball....")
    user,_ = finger_det()
    #user=int(input())
    oppenent = random.randint(1,6)

    
    if o==1:
      msd,score=batting(oppenent,user)
      print(oppenent_name+"  strike...",oppenent)
      print(oppenent_name+" scores "+str(sum(innings_score))+" runs.... ")
      if msd=="outtttt......":
        print("its out....catch on long on.....")
        break
    elif u==1:
      msd,score=batting(user,oppenent)
      print(oppenent_name+"  delivered...",oppenent)
      print(user_name+ " scores " +str(sum(innings_score)))
      if msd=="outtttt......":
        print("its edge .....fantasctic catch by keeper....")
        break

    i+=1
  if o==1:
    print(oppenent_name +" score "+str(sum(innings_score)))
  if u==1:
    print(user_name +" score "+str(sum(innings_score)))
  return score


def gameplay_second_innings(u,o,first_innings_score):


  i=1

  while i<=6:
    print(str(i)+" ball....")
    user,_ = finger_det()
    #user=int(input())
    oppenent = random.randint(1,6)

    if u==1:
      msd,score=batting(user,oppenent)
      print("ur score...",score)
      print(oppenent_name+"  delivers...",oppenent)
      target_runs = first_innings_score- sum(innings_score)
      if target_runs>0:
        print("you need "+str(target_runs)+ " runs to win....")
      if i==6 and sum(innings_score)==first_innings_score:
        print("Match draw!!!!")
        break


      elif sum(innings_score)>first_innings_score:
        print("you won!!!!")
        break
      elif msd=="outtttt......":
        print("its out....Caught and Bowled!!!!")
        print("you loss!!!!")
        break

    elif o==1:

      msd,score=batting(oppenent,user)
      print(oppenent_name+"  strike...",oppenent)
      target_runs = first_innings_score-sum(innings_score)
      if target_runs>0:
        print(str(oppenent_name) +" need " +str(target_runs)+ " runs to win... ")

      if i==6 and sum(innings_score)==first_innings_score:
        print("Match draw!!!!")
        break

      if sum(innings_score)>first_innings_score:
        print("you loss!!!!")
        break
      elif msd=="outtttt......":
        print("bowled.....that's a quicker....150 kmph")
        
        print("you won!!!!")
        break


    

    i+=1

  return score


warnings.filterwarnings("ignore")



print("........welcome to super over......")

user_name=input("Enter your name....")

oppenent_name=["...poonamani...","....sarapaambu....","...maaturavi...."]
num=random.randint(0,2)
oppenent_name=oppenent_name[num]

print("..."+ user_name+ "..."+"  vs  " +str(oppenent_name))


Toss = ''

while Toss != 'odd' and Toss != 'even':
    print('please enter odd or even.....?')
    Toss = input()


oppenent_chose=["bat","bowl"]
choice=random.randint(0,1)
oppenent_chose=oppenent_chose[choice]

hand,_= finger_det()
oppenent_run = random.randint(1,6)
print(oppenent_name,str(oppenent_run))
print("..."+user_name,"... "+str(hand))
total = hand+oppenent_run
user_chose=" "

if Toss == "even":
  if (total % 2) == 0:
    print("its Even u won the toss.... chose to ")
    user_chose=input("bat or bowl....")
  elif (total % 2) != 0:
    print("oppenent won the toss chose to "+str(oppenent_chose))

    

if Toss == "odd":
  if (total % 2) != 0:
    print("its odd u won the toss.... chose to ")
    user_chose=input("bat or bowl....")

  elif (total % 2) == 0:
    print("oppenent won the toss choose to "+str(oppenent_chose))



if oppenent_chose =="bat" or user_chose =="bowl":

  print("...first innings....")
  print("...get ready....")

  innings_score=[]
  print(oppenent_name+" was ready to bat !!!!!")
  print(".....just_play...")
  first_innings_score = gameplay_first_innings(0,1)
  print(oppenent_name+" finished his innings !!!!!")
  print("you have target of is "+str(first_innings_score))
  innings_score=[]
  print(user_name+" get ready to bat !!!!!")
  second_innings_score = gameplay_second_innings(1,0,first_innings_score)
  print(second_innings_score)

if oppenent_chose =="bowl" or user_chose =="bat":

  print("...first innings....")

  innings_score=[]
  print(user_name +" get ready to bat !!!!!")
  print(".....just_play...")
  first_innings_score = gameplay_first_innings(1,0)
  print(user_name +" finished his innings !!!!!")
  print("you have to defend "+str(first_innings_score)+" runs...")
  innings_score=[]
  print(oppenent_name +" get ready to bat !!!!!")
  second_innings_score = gameplay_second_innings(0,1,first_innings_score)





