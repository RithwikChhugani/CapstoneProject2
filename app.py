from string import ascii_uppercase
from PIL import Image, ImageTk
import cv2
import operator
from keras.models import model_from_json
import tkinter as tk

class Charcha:

    def __init__(self):
        self.screen=cv2.VideoCapture(0)
        self.onscreen_sign=None
        self.onscreen_sign_next=None
        self.mypath="C:/Users/Pratiksha Sharma/Downloads/Sign-Language-to-Text-master/model/"

        self.json_file = open(self.mypath+"mainpy.json", "r")
        self.model_json = self.json_file.read()
        self.json_file.close()
        self.loaded_model = model_from_json(self.model_json)
        self.loaded_model.load_weights(self.mypath+"mainpy.h5")

        self.ct = {}
        self.ct['blank'] = 0
        self.blank_flag = 0
        for i in ascii_uppercase:
            self.ct[i] = 0
        print("Loading...")
        self.root = tk.Tk()
        self.root.title("Charcha Talks - Sign Language to Text")
        self.root.protocol('WM_DELETE_WINDOW', self.silence)
        self.root.geometry("900x1100")
        self.frame = tk.Label(self.root)
        self.frame.place(x = 135, y = 10, width = 640, height = 640)
        self.frame_2 = tk.Label(self.root)
        self.frame_2.place(x = 460, y = 95, width = 310, height = 310)

        self.T = tk.Label(self.root)
        self.T.place(x=31,y = 17)
        self.T.config(text = "Charcha Talks - Sign Language to Text",font=("Helvetica",28,"italic"))
        self.frame_3 = tk.Label(self.root)
        self.frame_3.place(x = 500,y=640)
        self.T1 = tk.Label(self.root)
        self.T1.place(x = 10,y = 640)
        self.T1.config(text="Alphabet :",font=("Helvetica",28,"italic"))
        self.frame_4 = tk.Label(self.root)
        self.frame_4.place(x = 220,y=700)
        self.T2 = tk.Label(self.root)
        self.T2.place(x = 10,y = 700)
        self.T2.config(text ="Word :",font=("Helvetica",28,"italic"))
        self.frame_5 = tk.Label(self.root)
        self.frame_5.place(x = 350,y=760)
        self.T3 = tk.Label(self.root)
        self.T3.place(x = 10,y = 760)
        self.T3.config(text ="Sentence :",font=("Helvetica",28,"italic"))

        self.button1=tk.Button(self.root, command=self.eventOne,height = 0,width = 0)
        self.button1.place(x = 26,y=890)
        self.button2=tk.Button(self.root, command=self.eventTwo,height = 0,width = 0)
        self.button2.place(x = 325,y=890)
        self.button3=tk.Button(self.root, command=self.eventThree,height = 0,width = 0)
        self.button3.place(x = 625,y=890)
        self.button4=tk.Button(self.root, command=self.eventFour,height = 0,width = 0)
        self.button4.place(x = 125,y=950)
        self.button5=tk.Button(self.root, command=self.eventFive,height = 0,width = 0)
        self.button5.place(x = 425,y=950)
        self.str=""
        self.word=""
        self.current_symbol="Empty"
        self.photo="Empty"
        self.spiral()

    def eventOne(self):
        predicts = self.word
        if (len(predicts) > 0):
            self.word = ""
            self.str += " "
            self.str += predicts[0]

    def eventTwo(self):
        predicts = self.word
        if (len(predicts) > 1):
            self.word = ""
            self.str += " "
            self.str += predicts[1]

    def eventThree(self):
        predicts = self.word
        if (len(predicts) > 2):
            self.word = ""
            self.str += " "
            self.str += predicts[2]

    def eventFour(self):
        predicts = self.word
        if (len(predicts) > 3):
            self.word = ""
            self.str += " "
            self.str += predicts[3]

    def eventFive(self):
        predicts = self.word
        if (len(predicts) > 4):
            self.word = ""
            self.str += " "
            self.str += predicts[4]

    def infer(self,input_img):
        input_img = cv2.resize(input_img, (128,128))
        result = self.loaded_model.predict(input_img.reshape(1, 128, 128, 1))
        prediction={}
        prediction['blank'] = result[0][0]
        ix = 1
        for i in ascii_uppercase:
            prediction[i] = result[0][ix]
            ix += 1

        prediction = sorted(prediction.items(), key=operator.itemgetter(1), reverse=True)
        self.current_symbol = prediction[0][0]

        if(self.current_symbol == 'blank'):
            for i in ascii_uppercase:
                self.ct[i] = 0
        self.ct[self.current_symbol] += 1
        if(self.ct[self.current_symbol] > 60):
            for i in ascii_uppercase:
                if i == self.current_symbol:
                    continue
                tmp = self.ct[self.current_symbol] - self.ct[i]
                if tmp < 0:
                    tmp *= -1
                if tmp <= 20:
                    self.ct['blank'] = 0
                    for i in ascii_uppercase:
                        self.ct[i] = 0
                    return
            self.ct['blank'] = 0
            for i in ascii_uppercase:
                self.ct[i] = 0
            if self.current_symbol == 'blank':
                if self.blank_flag == 0:
                    self.blank_flag = 1
                    if len(self.str) > 0:
                        self.str += " "
                    self.str += self.word
                    self.word = ""
            else:
                if(len(self.str) > 16):
                    self.str = ""
                self.blank_flag = 0
                self.word += self.current_symbol

    def silence(self):
        print("Phew... That went well!")
        self.root.destroy()
        self.screen.release()
        cv2.destroyAllWindows()

    def spiral(self):
        ok, frame = self.screen.read()
        if ok:
            cv2image = cv2.flip(frame, 1)
            x1 = int(0.5*frame.shape[1])
            y1 = 10
            x2 = frame.shape[1]-10
            y2 = int(0.5*frame.shape[1])
            cv2.rectangle(frame, (x1-1, y1-1), (x2+1, y2+1), (255,0,0) ,1)
            cv2image = cv2.cvtColor(cv2image, cv2.COLOR_BGR2RGBA)
            self.onscreen_sign = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=self.onscreen_sign)
            self.frame.imgtk = imgtk
            self.frame.config(image=imgtk)
            cv2image = cv2image[y1:y2, x1:x2]
            gray = cv2.cvtColor(cv2image, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray,(5,5),2)
            th3 = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,2)
            ret, res = cv2.threshold(th3, 70, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
            self.infer(res)
            self.onscreen_sign_next = Image.fromarray(res)
            imgtk = ImageTk.PhotoImage(image=self.onscreen_sign_next)
            self.frame_2.imgtk = imgtk
            self.frame_2.config(image=imgtk)
            self.frame_3.config(text=self.current_symbol,font=("Helvetica", 28, "italic"))
            self.frame_4.config(text=self.word,font=("Helvetica", 28, "italic"))
            self.frame_5.config(text=self.str,font=("Helvetica", 28, "italic"))
            predicts=self.word
            if(len(predicts) > 0):
                self.button1.config(text=predicts[0],font = ("Helvetica", 14, "italic"))
            else:
                self.button1.config(text="")
            if(len(predicts) > 1):
                self.button2.config(text=predicts[1],font = ("Helvetica", 14, "italic"))
            else:
                self.button2.config(text="")
            if(len(predicts) > 2):
                self.button3.config(text=predicts[2],font = ("Helvetica", 14, "italic"))
            else:
                self.button3.config(text="")
            if(len(predicts) > 3):
                self.button4.config(text=predicts[3],font = ("Helvetica", 14, "italic"))
            else:
                self.button4.config(text="")
            if(len(predicts) > 4):
                self.button4.config(text=predicts[4],font = ("Helvetica", 14, "italic"))
            else:
                self.button4.config(text="")
        self.root.after(30, self.spiral)

print("Getting Chatty? Starting Charcha!")
print("Namashkar!")
print("G'day Mate!")
print("Howdy!")
print("Kia ora!")
print("Kaya!")
print("Hello!")
rpg = Charcha()
rpg.root.mainloop()
