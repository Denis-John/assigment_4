# Name:  
# Student Number:  





# Importing the required modules.
import tkinter
import tkinter.messagebox
import json
import random
import tkinter.font as TKFont
class ProgramGUI:
    
   
    def __init__(self):
        # This is the constructor of the class.
        # It is responsible for loading and reading the data from the text file and creating the user interface.
        # See the "Constructor of the GUI Class of fruit_test.py" section of the assignment brief. 
        
        self.main=tkinter.Tk()#creating main window
        self.main.title("Fruit Test")#setting the name of the window
        self.buttonClicked=False
        self.timer=tkinter.IntVar()
        self.correct_questions=0 #intializing the number of correct questions
        self.incorrect_questions=0 #initializing the number of incorrect questions
        self.number_of_question=0 #initializing the total number of questions
        
    
        try:
            f=open("data.txt","r")#opening the data.txt file in read mode
            self.data=json.loads(f.read())
        except ValueError:
            tkinter.messagebox.showerror("Error","Missing/invalid message")
            self.main.destroy()
            return
        if len(self.data)<2:#if length of data is less than 2 display not enough fruit message
            tkinter.messagebox.showerror("Error","Not Enough Fruit")
            self.main.destroy()
            return
            
            
       
        self.components=["calories", "fibre","sugar","vitamin_c"]#creating list containing names of fruits
        self.main.geometry("320x130")#setting the size of the window
        fontobject=TKFont.Font(size=10)

        self.top=tkinter.Frame(self.main)#creating a frame for packing the timer
        self.middle=tkinter.Frame(self.main)#creating frame for question label
        self.bottom=tkinter.Frame(self.main)#creating frame for true and false button
        self.Score=tkinter.Frame(self.main)#creating a frame for score label
        self.label=tkinter.Label(self.top,textvariable=self.timer,font=fontobject)#creating the timer label
        self.label.pack()#packing the timer label
        self.question=tkinter.Label(self.middle,width=50,font=fontobject)#creating the question label
        self.question.pack()#packing question label
        self.score=tkinter.Label(self.Score,font=fontobject)#creating the score label
        self.score.pack()#packing the score label
        #creating the true and false button and sending true or false value to checkAnswer() function
        self.tbutt=tkinter.Button(self.bottom,text="True",command=self.clickTrue,fg="blue",bg="white",font=7)
        self.fbutt=tkinter.Button(self.bottom,text="False",command=self.clickFalse,fg="blue",bg="white",font=7)
        self.tbutt.pack(side="left",padx=10)#packing the true button on the left side
        self.fbutt.pack(side="right") #setting the false button on the right side of the frame
        #packing the four frames
        self.top.pack()
        self.middle.pack()
        self.bottom.pack()
        self.Score.pack()
        #calling the showquestion
        self.showQuestion() 
        
        tkinter.mainloop()
        


    def showQuestion(self):
        # This method randomly selects two fruit and a nutritional component and displays them as a True/False question.
        # See Point 1 of the "Methods in the GUI class of fruit_test.py" section of the assignment brief.
        sampled_fruit=random.sample(self.data,2)#sampling two fruits randomly
        sampled_nutritional=random.choice(self.components)#selecting nutritional component
        #setting the question text
        if sampled_nutritional=="vitamin_c":
             text="100 grams of "+sampled_fruit[0]["name"]+" contains more Vitamin C \n than 100 grams of "+sampled_fruit[1]["name"]
        else:
            text="100 grams of "+sampled_fruit[0]["name"]+" contains more "+sampled_nutritional+" \n than 100 grams of "+sampled_fruit[1]["name"]
        
        self.question.configure(text=text)#configuring the question label with question text
        self.timer.set(7)
        self.updateTimer()
        self.fruit1=sampled_fruit[0]["name"]#obtaining the name of first fruit
        self.nutritional_component=sampled_nutritional
        self.fruit1_nutritional_component=sampled_fruit[0][self.nutritional_component]#obtaining the nutritional component of the first fruit
        self.fruit2=sampled_fruit[1]["name"]#obtaining the name of the second fruit
        self.fruit2_nutritional_component=sampled_fruit[1][self.nutritional_component]#obtaining the nutritional component of the second fruit
       
    #if true button is pressed set self.buttonClicked=True and call the function self.checkAnswer(True)
    def clickTrue(self):
        self.buttonClicked=True
        self.checkAnswer(True)
    #if False button is pressed set self.buttonClicked=True and call the function self.checkAnswer(False)   
    def clickFalse(self):
        self.buttonClicked=True
        self.checkAnswer(False)
    #This function will update the clock and show an error message if the user does not answer within 6 seconds
    def updateTimer(self):
        if not self.buttonClicked:#if buttonClicked is False
            self.timer.set(self.timer.get()-1)# decrease the counter by 1
            if self.timer.get()==0:#if timer ==0,show message showbox 
                    tkinter.messagebox.showerror("Error","Ooops!,You have \nran out of time")
                    self.showQuestion()

            else:
                self.timerID=self.main.after(1000,self.updateTimer)#calling the update timer fucntion after 1 sec
        else:
            self.main.after_cancel(self.timerID)#cancelling function call incase any button is pressed
            self.buttonClicked=False #changing the status of self.buttonClicked
    
            
    def checkAnswer(self, answer):
        
        # This method determines whether the user clicked the correct button and shows a Correct/Incorrect messagebox.
        # See Point 2 of the "Methods in the GUI class of fruit_test.py" section of the assignment brief.
        self.number_of_question+=1#updating the name of questions
        
        #checking if answer is false and if user selected false button
        self.percentage=abs(self.fruit1_nutritional_component-self.fruit2_nutritional_component)#nutritional difference of fruit components
        a=self.fruit1_nutritional_component<self.fruit2_nutritional_component
        b=(answer==False)
        result=a&b
        #checking if answer is true and user selected true button      
        if (self.fruit1_nutritional_component>self.fruit2_nutritional_component) & answer==True:
            text="You got it Correct \n "+self.fruit1+" has "+str(self.percentage)+" % more " + str(self.nutritional_component) +" than "+self.fruit2
            tkinter.messagebox.showinfo("Correct",text)
            self.correct_questions+=1 #updating the number of correct questions
            
        
           
        elif result:
            text="You got it Correct \n "+self.fruit2+" has "+str(self.percentage)+" % more " + str(self.nutritional_component) +" than "+self.fruit1
            tkinter.messagebox.showinfo("Correct",text)
            self.correct_questions+=1 #updating the number of incorrect questions
            
            
        else:
            
            if self.fruit2_nutritional_component<self.fruit1_nutritional_component:
                text="You got it wrong\n "+self.fruit1+" has "+str(self.percentage)+ "% more " +str(self.nutritional_component) +" than "+self.fruit2
                tkinter.messagebox.showerror("Incorrect",text)
                self.incorrect_questions+=1 #updating the number of incorrect questions
            else:
               
                text="You got it wrong\n "+self.fruit2+" has "+str(self.percentage)+ "% more " +str(self.nutritional_component) +" than "+self.fruit1
                tkinter.messagebox.showerror("Incorrect",text)
                self.incorrect_questions+=1 #updating the number of incorrect questions
           
        
            
        self.showQuestion() 
        
        text="You have scored  "+str(self.correct_questions)+" out of "+str(self.number_of_question)+" questions"
        self.score.configure(text=text)#displaying the number of correct questions
            
            




# Create an object of the ProgramGUI class to begin the program.
gui = ProgramGUI()
