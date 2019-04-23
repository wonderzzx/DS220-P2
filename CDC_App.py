#
#
# CDC APPLICATION FOR DS220 PROJECT 2
# GROUP 2

# TEAM LEADER:
# ISAAC RIVERA

# TEAM MEMBERS:
# DREW EDDY, JOHN DEBLASIO, ERIC ZHU, JUNKI AHN
# 
#
# THIS APPLICATION USES MONGODB ON A CLOUD SEVER AND A STITCH PROGRAM TO
# RUN A 10 QUESTION SURVEY THAT TELLS THE USER HOW THEY WILL DIE AND
# HOW TO IMPROVE RESULTS SO THAT THEY MIGHT HAVE BETTER ODDS NEXT TIME.
#
#
# KEY ASPECTS:
# - CLOUD BASED DATABASE SERVER WITH 1,200,000 RECORDS
# - PYTHON CODE TO PROMPT USER AND QUERRY DATABASE
# - DISPLAY RESULTS OF QUERRY AND TIME FOR COMPLETION
#

import random
import pymongo
from tkinter import *
from tkinter import ttk


# load
def load():
    # holds risk values
    global risk
    risk = [0, 0, 0]
    # [0] - accident
    # [1] - natural
    # [2] - homicide

    global accidentQuestionsAsked
    accidentQuestionsAsked = []
    global naturalCauseQuestionsAsked
    naturalCauseQuestionsAsked = []
    global homicideQuestionsAsked
    homicideQuestionsAsked = []


# set age function
def set_age(l, x, y, z):
    global age
    age = l[x][y][z][1]


# set gender function
def set_gender(l, x, y, z):
    global gender
    gender = l[x][y][z][1]


# set month function
def set_month(l, x, y, z):
    global month
    month = l[x][y][z][1]


def get_question():
    counter = 0
    question = []
    x = 1
    while x > 0:
        counter += 1
        if counter == 30:  # failsafe
            question = accidentQuestions[0]
            question.append("1")
            return question

        a = random.randint(0, 2)
        if a == 0:  # accident
            if len(accidentQuestionsAsked) == 7:
                continue
            b = random.randint(0, 6)
            while b in accidentQuestionsAsked:
                b = random.randint(0, 6)
            question = accidentQuestions[b]
            question.append("1")
            accidentQuestionsAsked.append(b)
            x = 0
        if a == 1:  # natural
            if len(naturalCauseQuestionsAsked) == 7:
                continue
            b = random.randint(0, 6)
            while b in naturalCauseQuestionsAsked:
                b = random.randint(0, 6)
            question = naturalCauseQuestions[b]
            question.append("7")
            naturalCauseQuestionsAsked.append(b)
            x = 0
        if a == 2:  # homicide
            if len(homicideQuestionsAsked) == 3:
                continue
            b = random.randint(0, 2)
            while b in homicideQuestionsAsked:
                b = random.randint(0, 2)
            question = homicideQuestions[b]
            question.append("3")
            homicideQuestionsAsked.append(b)
            x = 0
        else:
            continue
    return question


# (death type, list, answer number)
def add_risk(n, q, x):
    if n == 1:  # accident
        risk[0] += q[1][x][1]
    if n == 3:  # homicide
        risk[2] += q[1][x][1]
    if n == 7:  # natural
        risk[1] += q[1][x][1]


def query(m000, age0, risk0):

    # connect to mongodb through stitch with owner credentials
    # db for database to make coding similar to mongo shell
    if not m000:
        print("Invalid month.")
        return

    client = pymongo.MongoClient('localhost')
    db = client['mydatabase']
    icd10codes = db['icd10codes']
    monthCollection = db[m000]
    riskMax = max(risk0)
    if riskMax == 0:
        # return success message
        print("You have lived through your week long trip!")
        return

    riskIndex = risk0.index(riskMax)
    if riskIndex == 0:
        # accident
        data = monthCollection.find_one({"Age_Recode_12": age0, "Manner_Of_Death": "1"}, {"ICD10": 1})
        if not data:
            # print success
            print("You have lived through your week long trip!")
            return
        else:
            msg = icd10codes.find_one({"Code": data["ICD10"]})
            if not msg:
                # print success
                print("You have lived through your week long trip!")
            else:
                print("You did not survive your trip. You died by:")
                print(msg)
                print("You made a lot of accidental risk decisions, try to be more calm and practical.")
    elif riskIndex == 1:
        # natural
        data = monthCollection.find_one({"Age_Recode_12": age0, "Manner_Of_Death": "7"}, {"ICD10": 1})
        if not data:
            # print success
            print("You have lived through your week long trip!")
            return
        else:
            msg = icd10codes.find_one({"Code": data["ICD10"]})
            if not msg:
                # print success
                print("You have lived through your week long trip!")
            else:
                print("You did not survive your trip. You died by:")
                print(msg)
                print("You made a lot of health risk decisions, try to consider healthier behaviors.")
    elif riskIndex == 2:
        # homicide
        data = monthCollection.find_one({"Age_Recode_12": age0, "Manner_Of_Death": "3"}, {"ICD10": 1})
        if not data:
            # print success
            print("You have lived through your week long trip!")
            return
        else:
            msg = icd10codes.find_one({"Code": data["ICD10"]})
            if not msg:
                # print success
                print("You have lived through your week long trip!")
            else:
                print("You did not survive your trip. You died by:")
                print(msg)
                print("You made a lot of risky decisions when confronted with criminals. "
                  "\nTry to avoid confrontations and being a hero.")


# Creates interface to display questions and answers.
def main():

    notebook.add(frame1, text="Age   ")
    notebook.add(frame2, text="Gender")
    notebook.add(frame3, text="Month ")

    notebook.add(frame4, text="Sunday")
    notebook.add(frame5, text="Monday")
    notebook.add(frame6, text="Tuesday")
    notebook.add(frame7, text="Wednesday")
    notebook.add(frame8, text="Thursday")
    notebook.add(frame9, text="Friday")
    notebook.add(frame10, text="Saturday")

    notebook.add(frame11, text="Process")

    # age
    Label(frame1, text=questionsForAll[0][0]).grid(row=2, column=1)
    Button(frame1, text=questionsForAll[0][1][0][0], command=set_age(questionsForAll, 0, 1, 0)).grid(row=3, column=1)
    Button(frame1, text=questionsForAll[0][1][1][0], command=set_age(questionsForAll, 0, 1, 1)).grid(row=4, column=1)
    Button(frame1, text=questionsForAll[0][1][2][0], command=set_age(questionsForAll, 0, 1, 2)).grid(row=5, column=1)
    Button(frame1, text=questionsForAll[0][1][3][0], command=set_age(questionsForAll, 0, 1, 3)).grid(row=6, column=1)
    Button(frame1, text=questionsForAll[0][1][4][0], command=set_age(questionsForAll, 0, 1, 4)).grid(row=7, column=1)
    Button(frame1, text=questionsForAll[0][1][5][0], command=set_age(questionsForAll, 0, 1, 5)).grid(row=8, column=1)
    Button(frame1, text=questionsForAll[0][1][6][0], command=set_age(questionsForAll, 0, 1, 6)).grid(row=9, column=1)
    Button(frame1, text=questionsForAll[0][1][7][0], command=set_age(questionsForAll, 0, 1, 7)).grid(row=10, column=1)
    Button(frame1, text=questionsForAll[0][1][8][0], command=set_age(questionsForAll, 0, 1, 8)).grid(row=11, column=1)
    Button(frame1, text=questionsForAll[0][1][9][0], command=set_age(questionsForAll, 0, 1, 9)).grid(row=12, column=1)
    Button(frame1, text=questionsForAll[0][1][10][0], command=set_age(questionsForAll, 0, 1, 10)).grid(row=13, column=1)

    # gender
    Label(frame2, text=questionsForAll[1][0]).grid(row=2, column=1)
    Button(frame2, text=questionsForAll[1][1][0][0], command=set_age(questionsForAll, 1, 1, 0)).grid(row=3, column=1)
    Button(frame2, text=questionsForAll[1][1][1][0], command=set_age(questionsForAll, 1, 1, 1)).grid(row=4, column=1)

    # month
    Label(frame3, text=questionsForAll[2][0]).grid(row=2, column=1)
    Button(frame3, text=questionsForAll[2][1][0][0], command=set_month(questionsForAll, 2, 1, 0)).grid(row=3, column=1)
    Button(frame3, text=questionsForAll[2][1][1][0], command=set_month(questionsForAll, 2, 1, 1)).grid(row=4, column=1)
    Button(frame3, text=questionsForAll[2][1][2][0], command=set_month(questionsForAll, 2, 1, 2)).grid(row=5, column=1)
    Button(frame3, text=questionsForAll[2][1][3][0], command=set_month(questionsForAll, 2, 1, 3)).grid(row=6, column=1)
    Button(frame3, text=questionsForAll[2][1][4][0], command=set_month(questionsForAll, 2, 1, 4)).grid(row=7, column=1)
    Button(frame3, text=questionsForAll[2][1][5][0], command=set_month(questionsForAll, 2, 1, 5)).grid(row=8, column=1)
    Button(frame3, text=questionsForAll[2][1][6][0], command=set_month(questionsForAll, 2, 1, 6)).grid(row=9, column=1)
    Button(frame3, text=questionsForAll[2][1][7][0], command=set_month(questionsForAll, 2, 1, 7)).grid(row=10, column=1)
    Button(frame3, text=questionsForAll[2][1][8][0], command=set_month(questionsForAll, 2, 1, 8)).grid(row=11, column=1)
    Button(frame3, text=questionsForAll[2][1][9][0], command=set_month(questionsForAll, 2, 1, 9)).grid(row=12, column=1)
    Button(frame3, text=questionsForAll[2][1][10][0], command=set_month(questionsForAll, 2, 1, 10)).grid(row=13,
                                                                                                         column=1)
    Button(frame3, text=questionsForAll[2][1][11][0], command=set_month(questionsForAll, 2, 1, 11)).grid(row=14,
                                                                                                         column=1)

    # random questions
    x = 0
    # week = [day value], [death type]
    week = [['1', 0], ['2', 0], ['3', 0], ['4', 0], ['5', 0], ['6', 0], ['7', 0]]

    # sunday
    question = get_question()
    week[x][1] = question[2]
    x += 1
    Label(frame4, text=question[0]).grid(row=2, column=1)
    Button(frame4, text=question[1][0][0], command=add_risk(question[2], question, 0)).grid(row=3, column=1)
    Button(frame4, text=question[1][1][0], command=add_risk(question[2], question, 1)).grid(row=4, column=1)
    Button(frame4, text=question[1][2][0], command=add_risk(question[2], question, 2)).grid(row=5, column=1)
    if len(question[0][1]) == 4:
        Button(frame4, text=question[0][3][0][0], command=add_risk(question[2], question, 3)).grid(row=6, column=1)

    # monday
    question = get_question()
    week[x][1] = question[2]
    x += 1
    Label(frame5, text=question[0]).grid(row=2, column=1)
    Button(frame5, text=question[1][0][0], command=add_risk(question[2], question, 0)).grid(row=3, column=1)
    Button(frame5, text=question[1][1][0], command=add_risk(question[2], question, 1)).grid(row=4, column=1)
    Button(frame5, text=question[1][2][0], command=add_risk(question[2], question, 2)).grid(row=5, column=1)
    if len(question[0][1]) == 4:
        Button(frame5, text=question[1][3][0], command=add_risk(question[2], question, 3)).grid(row=6, column=1)

    # tuesday
    question = get_question()
    week[x][1] = question[2]
    x += 1
    Label(frame6, text=question[0]).grid(row=2, column=1)
    Button(frame6, text=question[1][0][0], command=add_risk(question[2], question, 0)).grid(row=3, column=1)
    Button(frame6, text=question[1][1][0], command=add_risk(question[2], question, 1)).grid(row=4, column=1)
    Button(frame6, text=question[1][2][0], command=add_risk(question[2], question, 2)).grid(row=5, column=1)
    if len(question[0][1]) == 4:
        Button(frame6, text=question[1][3][0], command=add_risk(question[2], question, 3)).grid(row=6, column=2)

    # wednesday
    question = get_question()
    week[x][1] = question[2]
    x += 1
    Label(frame7, text=question[0]).grid(row=2, column=1)
    Button(frame7, text=question[1][0][0], command=add_risk(question[2], question, 0)).grid(row=3, column=1)
    Button(frame7, text=question[1][1][0], command=add_risk(question[2], question, 1)).grid(row=4, column=1)
    Button(frame7, text=question[1][2][0], command=add_risk(question[2], question, 2)).grid(row=5, column=1)
    if len(question[0][1]) == 4:
        Button(frame7, text=question[1][3][0], command=add_risk(question[2], question, 3)).grid(row=6, column=1)

    # thursday
    question = get_question()
    week[x][1] = question[2]
    x += 1
    Label(frame8, text=question[0]).grid(row=2, column=1)
    Button(frame8, text=question[1][0][0], command=add_risk(question[2], question, 0)).grid(row=3, column=1)
    Button(frame8, text=question[1][1][0], command=add_risk(question[2], question, 1)).grid(row=4, column=1)
    Button(frame8, text=question[1][2][0], command=add_risk(question[2], question, 2)).grid(row=5, column=1)
    if len(question[0][1]) == 4:
        Button(frame8, text=question[1][3][0], command=add_risk(question[2], question, 3)).grid(row=6, column=1)

    # friday
    question = get_question()
    week[x][1] = question[2]
    x += 1
    Label(frame9, text=question[0]).grid(row=2, column=1)
    Button(frame9, text=question[1][0][0], command=add_risk(question[2], question, 0)).grid(row=3, column=1)
    Button(frame9, text=question[1][1][0], command=add_risk(question[2], question, 1)).grid(row=4, column=1)
    Button(frame9, text=question[1][2][0], command=add_risk(question[2], question, 2)).grid(row=5, column=1)
    if len(question[0][1]) == 4:
        Button(frame9, text=question[1][3][0], command=add_risk(question[2], question, 3)).grid(row=6, column=1)

    # saturday
    question = get_question()
    week[x][1] = question[2]
    x += 1
    Label(frame10, text=question[0]).grid(row=2, column=1)
    Button(frame10, text=question[1][0][0], command=add_risk(question[2], question, 0)).grid(row=3, column=1)
    Button(frame10, text=question[1][1][0], command=add_risk(question[2], question, 1)).grid(row=4, column=1)
    Button(frame10, text=question[1][2][0], command=add_risk(question[2], question, 2)).grid(row=5, column=1)
    if len(question[0][1]) == 4:
        Button(frame10, text=question[1][3][0], command=add_risk(question[2], question, 3)).grid(row=6, column=1)

    # final window

    Label(frame11, text="Process").grid(row=2, column=1)
    Button(frame11, text="Process answers", command=query(month, age, risk)).grid(row=3, column=1)
    Button(frame11, text="Quit program", command=quit).grid(row=4, column=1)

    notebook.pack()


# questions for all
questionsForAll=[['What is your age in years?',
                  [['Under 1 Year','1'],['1 - 4','2'],['5 - 14','3'],['15 - 24','4'],['24 - 34','5'],['35 - 44','6'],
                   ['45 - 54','7'],['55 - 64','8'],['65 - 74','9'],['75 - 84','10'],['85+','11']]],
                 ['What is your Gender?',
                  [['Male', 'M'], ['Female', 'F']]],
                 ['What month do you want to travel in?',
                  [['January', '101'],['February', '102'],['March', '103'],
                    ['April', '104'],['May', '105'],['June', '106'],['July', '107'],['August', '108'],
                   ['September', '109'],['October', '110'],['November', '111'],['December', '112']]]]

# list of questions to ask 1 per day

# 7 questions
accidentQuestions=[['You’re driving to work, but you’re running late, how you get there?',
        [['You drive the recommended speed limit, focused on and arrive several minutes late to work', 1],
         ['You take the scenic route, screw work, and arrive an hour late to work', 0],
         ['You drive faster than normal, and arrive just on time', 2],
         ['You race to work and get there early', 3]]],
                   ['You’re walking along a bridge and someone next to you pushes you over, the fall is about 100ft \n'
                    'into choppy water, what do you do?',
        [['Try to hold on to something on your way down to slow down', 0],
         ['Straighten your body like a pencil and go feet first in', 1],
         ['Relax your muscles and let it happen', 2],
         ['Open your arms and legs like an X to increase wind resistance', 3]]],
                   ['You’re walking down a street and notice a fire in a nearby house, nobody is nearby and you \n'
                    'can’t hear any fire truck sirens, but you hear someone yelling for help inside. What do you do?',
        [['Nothing, you like how the flames look', 0],
         ['You call 911 but keep your distance', 0],
         ['You call 911 and try to enter the house to help, but cautiously', 2],
         ['You run into the house without hesitation to save the person inside', 3]]],
                   ['When you get really hungry, how would you describe the way you eat:',
        [['Take small bites and chew at least 20 times before swallowing', 0],
         ['Take medium sized bites and chewing several times, being mindful of each bite', 1],
         ['Take decent sized bites and chewing several times but eating fast', 2],
         ['Stuffing you face as much as you can, stopping only when it’s time for a drink', 3]]],
                   ['You’re down a rarely traveled road deep in the Arizona desert and you car breaks down. The \n'
                    'sun’s beating down and you’re starting to sweat. You remember passing a gas station two hours \n'
                    'ago but haven’t seen any cars on the road since, what do you do?',
        [['Find somewhere in the shade and wait until a car passes to get help', 2],
         ['Find somewhere in the shade and wait until night to start walking either direction, \n'
         'but risk freezing on the way there', 1],
         ['Starting walking back the way you came towards the gas station', 2],
         ['Start walking the way you were driving into the unknown', 3]]],
                   ['You’re being chased in the woods by someone you don’t know. You’re running as fast as you can \n'
                    'but he is starting to catch up to you. You come across a river but its current looks incredible \n'
                    'strong. If you don’t do something, he will get to you, what do you do?',
        [['Stand your ground to face the chaser', 0],
         ['Run down the length of the river for a safer point to cross and risk him getting to you', 1],
         ['Jump in the water and try to swim across', 3]]],
                   ['You walk into your house after spending a couple of hours at the gym and notice you left the \n'
                    'gas on your oven on all day, what do you do?',
        [['Nothing, you did it on purpose, you like the smell of gas', 3],
         ['Turn the gas off, and continue going about your day', 2],
         ['Immediately leave the house and call 911', 0]]], 1]

# 7 questions
naturalCauseQuestions=[['It’s dinner time and your stomach is grumbling, so you go to a restaurant, what do you order?',
        [['A bacon cheeseburger with a side of fries', 3],
         ['Just a salad with dressing on the side', 0],
         ['A thick 12oz steak and a baked potato', 2],
         ['Salmon with a side of rice', 1]]],
                       ['You’re out at dinner and it’s time for dessert, what do you get?',
        [['Nothing, you’re too good for that', 0],
         ['Carrot cake, because somebody has to enjoy that', 1],
         ['A slice of your favorite type of pie', 2],
         ['Ice cream, a lot of ice cream', 3]]],
                       ['You have a group project you have to work on, but one of your group mates have the flu. \n'
                        'The project due date is coming soon, so it’s crunch time and the group has to meet, \n'
                        'what do you do?' ,
        [['Don’t meet up with them, getting sick isn’t worth the bad grade', 0],
         ['You go, but you go to the bathroom every 10 minutes and wash your hands and \n'
         'you sit far from the sick kid', 1],
         ['You go and don’t worry about, who cares if you get sick', 3]]],
                       ['Has anyone in your family been diagnosed with cancer in the past?',
        [['No', 0],
         ['Yes, but it wasn’t genetic', 1],
         ['Yes, and it probably was genetic', 3]]],
                       ['Your friend invites you to a party, he’s say it’s gonna get wild, what would you do?',
        [['Decline, parties aren’t your thing', 0],
         ['You go and have a few beers', 1],
         ['You go and get pretty wasted, enough to give you a good hangover the next day', 2],
         ['You get blackout drunk and wake up in a meadow', 3]]],
                       ['Do you smoke, if so how much?',
        [['No I don’t smoke', 0],
         ['Less than 5 cigarettes a day', 1],
         ['Between 5-15 cigarettes a day', 2],
         ['More than 15 cigarettes a day', 3]]],
                       ['Does anyone in your immediate family suffer from Alzheimer’s or Alzheimer’s related dementia?',
        [['No, no one in my immediate family', 0],
         ['Yes one parent, sibling or grandparent', 1],
         ['Yes more than one parent or grandparent', 2]]], 7]

# 3 Questions
homicideQuestions=[['You’re in a convenience store looking at the drinks in the back, and a hooded man walks in and \n'
                    'yells at the cashier to hand over the money. He has his hand in his coat pocket like he is \n'
                    'pointing a gun, but it might not be real, what do you do?',
        [['Nothing and wait for them to leave', 0],
         ['Call the cops and hope there isn’t a shootout', 1],
         ['Try to sneak up behind him and knock him to the ground', 4],
         ['Run at him full charge', 6]]],
                   ['You’re walking down a street at night and a guy steps in front of you holding a knife. \n'
                    'He demands you give him your wallet and phone. You look around and don’t see anyone who can \n'
                    'help you, what do you do.',
        [['Give him you stuff, it’s not worth dying over', 0],
         ['Run as fast as you can away from him, how fast can he be', 3],
         ['Hand over your things, as he reaches for him you go for the knife', 4],
         ['Lunge at him, maybe if you surprise him you can win', 6]]],
                   ['You’re walking down a street at night and pass an alley. In it you see a man trying to mug a \n'
                    'young woman, he doesn’t look like he has any weapons, but he is pretty big, what do you do?',
        [['Run away in fear and call the cops once you know you’re safe', 0],
         ['Call the cops and wait outside of the alley to help the woman if the mugger leaves', 2],
         ['Confront him and tell him to leave her alone, like in the movies', 4],
         ['Run at him and try to push him to the ground, you think you can take him', 6]]], 3]


root = Tk()
root.title('CDC Death Prediction')
# total = IntVar()  # defaults to 0

notebook = ttk.Notebook(root)

frame1 = ttk.Frame(notebook)
frame2 = ttk.Frame(notebook)
frame3 = ttk.Frame(notebook)
frame4 = ttk.Frame(notebook)
frame5 = ttk.Frame(notebook)
frame6 = ttk.Frame(notebook)
frame7 = ttk.Frame(notebook)
frame8 = ttk.Frame(notebook)
frame9 = ttk.Frame(notebook)
frame10 = ttk.Frame(notebook)
frame11 = ttk.Frame(notebook)

load()
main()

root.mainloop()

