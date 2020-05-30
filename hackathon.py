############### Written by Sarvesh Somasundaram, Arul Sharma, Taha Haveliwala, and Abduallah Shahid ###############

#Importing our libraries
import tkinter as tk #Used for graphical interface
import pandas as pd #Used to manipulate 

class Application(tk.Frame): #Creating frame for GUI
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    
    def create_widgets(self):
        #List of states used for items in drop-down list
        STATES = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']
        finalScores = []
        image = tk.PhotoImage(file="Mainland.png")
        img = image.subsample(4, 4)
        image2 = tk.PhotoImage(file="Hawaii.png")
        img2 = image2.subsample(6, 6)
        image3 = tk.PhotoImage(file="Alaska.png")
        img3 = image3.subsample(5, 5)
        for state in STATES:
            df = pd.read_csv("data.csv") #reading data from csv and creating a DataFrame to add the items to
            stateValue = df.loc[df['State'] == state] #takes out the row from the DataFrame in which the selected state is in

            stayAtHomeVal = stateValue.iat[0,1]
            stayAtHomeValWeighted = stayAtHomeVal*0.2
            businessesOpen = stateValue.iat[0,2]
            businessesOpenWeighted = businessesOpen*0.06 #weighted the lowest at 0.06 because businesses aren't a major impact on safety
            gatheringsOfPeople = stateValue.iat[0,3]
            gatheringsOfPeopleWeighted = gatheringsOfPeople*0.15
            confirmedCases = stateValue.iat[0,4]
            confirmedCasesWeighted = confirmedCases*0.3 #Weighted the highest at 0.3 because number of cases in the state is a major factor
            totalTests = stateValue.iat[0,5]
            totalTestsWeighted = totalTests*0.29 #Weighted almost the same as confirmed cases because total tests done should in theory balance out with the total cases
            
            #Calculating the final score by adding the weighted values
            finalScore = stayAtHomeValWeighted + businessesOpenWeighted + gatheringsOfPeopleWeighted + confirmedCasesWeighted + totalTestsWeighted

            finalScores.append(finalScore) #Adds the final scores to list for later use

        #creating a tkinter variable for dro down list
        variable = tk.StringVar(self)
        variable.set(STATES[0]) # default value
        
        #Creating the drop down list
        self.w = tk.OptionMenu(self,variable, *STATES)
        self.w.pack()

        #function that is used to calculate how safe it is to go outside on a scale from 0 to 1 and display COVID-19 statistics for chosen state
        def calculateSafetyLevel():
            finalScore = 0
            if self.label:
                self.label.destroy() #destroys label object each time a new state is clicked, to update the display
                self.label1.destroy()
            df = pd.read_csv("data.csv") #reading data from csv and creating a DataFrame to add the items to
            stateValue = df.loc[df['State'] == variable.get()] #takes out the row from the DataFrame in which the selected state is in 
            row_num = df[df['State'] == variable.get()].index.values.astype(int) #Taking the row number to get the final score value from above 
            finalScore = finalScores[row_num[0]]
            
            #Statistics for given state
            stayAtHome = str(stateValue.iat[0,6])
            businessesOpenVal = str(stateValue.iat[0,7])
            gatheringsValue = str(stateValue.iat[0,8])
            confirmedCasesVal = str(stateValue.iat[0,9])
            totalTestsVal = str(stateValue.iat[0,10])
            finalScoreString = str(finalScore)

            #Determining what level of safety a given state has based on final score
            if finalScore< 0.2:
                advise = 'Totally Safe'
            elif finalScore >= 0.2 and finalScore < 0.35:
                advise = 'Safe With Social Distancing'
            elif finalScore >= 0.35 and finalScore < 0.45:
                advise = 'Safe With Protection and Social Distancing'
            elif finalScore >= 0.45 and finalScore < 0.55:
                advise = 'Not Recommended, but OK With Protection and Social Distancing'
            elif finalScore >=0.55:
                advise = 'It Is Not Safe To Go Outside'

            #variable to feed into Label object
            sentence = '\n' + 'Numerical Safety Value: ' + finalScoreString + '\n\n' + 'Stay at home order: ' + stayAtHome + '\n\n' + 'Businesses open: ' + businessesOpenVal + '\n\n' + 'Gatherings: ' + gatheringsValue + '\n\n' + 'Confirmed cases per 100,000 people: ' + confirmedCasesVal + '\n\n' + 'Total tests done per 100,000 people: ' + totalTestsVal

            self.label1 = tk.Label(self, text = advise, bg = 'lightblue', fg ='green', font = ("Times", 18, 'bold'))
            self.label1.pack()
            self.label = tk.Label(self, text=sentence, bg = 'lightblue', fg = "green", font = "Times") 
            self.label.pack()
         

        #Confirmation button
        self.accept = tk.Button(self, text="ACCEPT", bg = "lightblue", fg='green', command = calculateSafetyLevel)
        self.accept.pack()

        #Quit Button
        self.quit = tk.Button(self, text="QUIT",bg = "lightblue", fg="red", command=self.master.destroy)
        self.quit.pack()
        self.label = tk.Label(self, text ='', bg = "lightblue").pack(side = 'bottom') #Placeholder labels
        self.label1 = tk.Label(self, text ='', bg = "lightblue").pack(side = 'bottom')
        self.panel = tk.Label(self, image = img, bg = 'lightblue')
        self.panel.photo = img
        self.panel.pack(side='bottom', fill='both', expand = 'yes')
        self.panel1 = tk.Label(self, image = img2, bg = 'lightblue')
        self.panel1.photo = img2
        self.panel1.place(relx=0.0, rely=1.0, anchor='sw')
        self.panel2 = tk.Label(self, image = img3, bg = 'lightblue')
        self.panel2.photo = img3
        self.panel2.pack(side = 'left')

root = tk.Tk()
root.geometry('2000x2000')
label_1 = tk.Label(root, text = "Is It Safe To Go Outside?", bg = "lightblue", fg = "green", font = "Verdana 32 bold") #Title
label_1.pack()
app = Application(root)
#background color
root.configure(bg='#add8e6')
app.configure(bg='#add8e6')
app.mainloop()
