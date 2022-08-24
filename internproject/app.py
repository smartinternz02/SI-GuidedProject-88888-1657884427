from flask import Flask,render_template
import os
# Flask-It is our framework which we are going to use to run/serve our application.
#request-for accessing file which was uploaded by the user on our application.
from tkinter import * # Graphical User Interface package
import PIL
from PIL import ImageGrab # used to copy the contents of the screen # loading our model python file
import cv2  #opencv library
from keras.models import load_model
from keras import utils
import numpy as np
from werkzeug.utils import secure_filename
app = Flask(__name__) # initializing a flask app



@app.route('/')# route to display the home page
def home():
    return render_template('index.html')#rendering the home page


@app.route('/intro')
def intro():
    return render_template('intro.html')#rendering the intro page



@app.route('/launch',methods=['GET', 'POST'])# route to show the predictions in a web UI
def launch():
    class main:
        def __init__(self, master):
            self.master = master
            self.res = ""
            self.pre = [None, None]
            self.bs = 4.5
            self.c = Canvas(self.master,bd=3,relief="ridge", width=400, height=400, bg='white')
            self.c.pack(side=LEFT)
            f1 = Frame(self.master, padx=5, pady=5)
            Label(f1,text="Maths Tutor for shape",fg="red",font=("",15,"bold")).pack(pady=10)
            Label(f1,text="Draw a shape to get its formula",fg="red",font=("",15)).pack()
            Label(f1,text="(Circle,Square,Triangle)",fg="red",font=("",15)).pack()
            self.pr = Label(f1,text="Prediction: None",fg="red",font=("",20,"bold"))
            self.pr.pack(pady=20)
            
            Button(f1,font=("",15),fg="white",bg="red", text="Clear Canvas", 
                   command=self.clear).pack(side=BOTTOM)
    
            f1.pack(side=RIGHT,fill=Y)
            self.c.bind("<Button-1>", self.putPoint)
            self.c.bind("<ButtonRelease-1>",self.getResult)
            self.c.bind("<B1-Motion>", self.paint)
    
      
        def getResult(self,e):
            x = self.master.winfo_rootx() + self.c.winfo_x()
            y = self.master.winfo_rooty() + self.c.winfo_y()
            x1 = x + self.c.winfo_width()
            y1 = y + self.c.winfo_height()
            img = PIL.ImageGrab.grab()
            img = img.crop((x, y, x1, y1))
            basepath = os.path.dirname(__file__)
            file_path = os.path.join(basepath, 'uploads', secure_filename('img.jpg'))
            img.save(file_path)
            img = utils.load_img('uploads/img.jpg', target_size=(64,64))
            x = utils.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            model=load_model('tutormath.h5')
            preds=np.argmax(model.predict(x), axis=1)
            print(preds)
            print(model.predict(x))
            l=['circle','square','triangle']
            self.res = l[preds[0]]
            self.pr['text'] = "Prediction: "  
            if self.res == 'square':
                self.pr['text'] = self.pr['text'] + self.res + "\n Perimeter formula : 4 × side " + "\n Area formula: side^2" 
            elif self.res == 'circle':
                self.pr['text'] = self.pr['text'] + self.res + "\n Perimeter formula: 2 × pi × radius " + "\n Area formula:	pi × radius2" 
            elif self.res == 'triangle':
                self.pr['text'] = self.pr['text'] + self.res + "\n Perimeter formula: side1 + side2 + side3 " + "\n Area formula: base × height / 2"
                
                
            
            if self.res=='circle':
                image = cv2.imread('circle.png')
                cv2.imshow('circle', image)  
                key=cv2.waitKey(0)
            
                if (key & 0xFF) == ord("c"):
                    cv2.destroyWindow("circle")
            
            elif self.res=='square':
                image = cv2.imread('square.jpg')
                cv2.imshow('square', image)  
                key=cv2.waitKey(0)
            
                if (key & 0xFF) == ord("s"):
                    cv2.destroyWindow("square")
            else:
                
                image = cv2.imread('triangle.jpg')
                cv2.imshow('triangle', image)  
                key=cv2.waitKey(0)
            
                if (key & 0xFF) == ord("t"):
                    cv2.destroyWindow("triangle")
    
        def clear(self):
            self.c.delete('all')
    
        def putPoint(self, e):
            self.c.create_oval(e.x - self.bs, e.y - self.bs, e.x + self.bs, e.y + self.bs, 
                               outline='black', fill='black')
            self.pre = [e.x, e.y]
    
        def paint(self, e):
            self.c.create_line(self.pre[0], self.pre[1], e.x, e.y, width=self.bs * 2, 
                               fill='black', capstyle=ROUND,
                               smooth=TRUE)
    
            self.pre = [e.x, e.y]
    
    
    if __name__ == "__main__":
        root = Tk()
        main(root)
        root.title('Digit Classifier')
        root.resizable(0, 0)
        root.mainloop()
       # showing the prediction results in a UI
    return render_template("index.html")
     
if __name__ == "__main__":
   # running the app
    app.run(debug=False)