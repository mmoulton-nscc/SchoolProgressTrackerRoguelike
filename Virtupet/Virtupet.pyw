import sys
import random

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import QTimer, QTime, Qt
#ADD IMPORT STATEMENT FOR YOUR GENERATED UI.PY FILE HERE
import Ui_Virtupet
#      ^^^^^^^^^^^ Change this!

#CHANGE THE SECOND PARAMETER (Ui_ChangeMe) TO MATCH YOUR GENERATED UI.PY FILE
class MyForm(QMainWindow, Ui_Virtupet.Ui_MainWindow):
#                         ^^^^^^^^^^^   Change this!

    # DO NOT MODIFY THIS CODE
    def __init__(self, parent=None):
        super(MyForm, self).__init__(parent)
        self.setupUi(self)

        #main options are all the menu things
        self.mainOptions = [self.labelOption0, self.labelOption1, self.labelOption2, self.labelOption3,
        self.labelOption4, self.labelOption5, self.labelOption6]
        
        #hideables are all the GUI bits that come and go
        self.hideables = [self.labelStatsText, self.labelStatsImage, self.labelMeal, self.labelSnack,
         self.labelPoop, self.labelSick, self.labelMain]

        #intialize all the icons and background images
        self.labelOption0.setPixmap(QPixmap("{0}/sprites/feed_sprite1.png".format(sys.path[0])))
        self.labelOption1.setPixmap(QPixmap("{0}/sprites/light_sprite1.png".format(sys.path[0]))) 
        self.labelOption2.setPixmap(QPixmap("{0}/sprites/game_sprite1.png".format(sys.path[0])))
        self.labelOption3.setPixmap(QPixmap("{0}/sprites/med_sprite1.png".format(sys.path[0]))) 
        self.labelOption4.setPixmap(QPixmap("{0}/sprites/bathh_sprite1.png".format(sys.path[0])))
        self.labelOption5.setPixmap(QPixmap("{0}/sprites/scale_sprite1.png".format(sys.path[0])))
        self.labelOption6.setPixmap(QPixmap("{0}/sprites/dis_sprite1.png".format(sys.path[0])))
        self.labelAttention.setPixmap(QPixmap("{0}/sprites/attention_sprite1.png".format(sys.path[0])))
        self.labelBG.setPixmap(QPixmap("{0}/sprites/background2.png".format(sys.path[0])))
        self.labelSick.setPixmap(QPixmap("{0}/sprites/sick_sprite1.png".format(sys.path[0])))
        self.labelPoop.setPixmap(QPixmap("{0}/sprites/poop_sprite1.png".format(sys.path[0])))


        #timer. times out every 1s and connects to slot below
        self.timer = QTimer()
        self.timer.start(1000)

        #time to hatch from egg. 
        self.hatchTimer = 60

        #time to evolve from child - not implemented
        self.evolveTimer = 60000

        #initialize animation frame
        self.frame = 0

        self.resetThings()
        #try to load, else reset
        try:
            self.loadThings()
        except:
            pass

    # END DO NOT MODIFY

        # ADD SLOTS HERE
        self.actionLoad.triggered.connect(self.Load_Clicked)
        self.actionSave_and_Exit.triggered.connect(self.SaveAndExit_Clicked)
        self.actionRESET.triggered.connect(self.Reset_Clicked)
        self.pushButtonSelect.clicked.connect(self.SelectButton_Clicked)
        self.pushButtonConfirm.clicked.connect(self.ConfirmButton_Clicked)
        self.pushButtonCancel.clicked.connect(self.CancelButton_Clicked)
        self.timer.timeout.connect(self.LiveLifeTimer)

    # ADD SLOT FUNCTIONS HERE
    def Load_Clicked(self):
        self.loadThings()
    
    def SaveAndExit_Clicked(self):
        self.saveThings()
        self.exitThing()

    def Reset_Clicked(self):
        self.resetThings()

    def SelectButton_Clicked(self):
        self.selectStuff()

    def ConfirmButton_Clicked(self):
        self.confirmStuff()

    def CancelButton_Clicked(self):
        self.cancelStuff()

    def LiveLifeTimer(self):
        self.animate()
        self.statUpdates()

    #ADD HELPER FUNCTIONS HERE
    def loadThings(self):

        #load list of stats
        with open("{0}/saves/petdata.txt".format(sys.path[0]), "r") as loadFile:
            loaded = loadFile.readlines()
            #set live stats to loaded stats
            self.ageStat = int(loaded[0])
            self.hungerStat = int(loaded[1])
            self.weightStat = float(loaded[2])
            self.happyStat = int(loaded[3])
            self.disciplineStat = int(loaded[4])
            self.tiredStat = float(loaded[5])
            self.poopStat = float(loaded[6])
            self.sickStat = float(loaded[7])
            self.isFussing = bool(loaded[8])
            self.raisingMistakeStat = float(loaded[9])
            self.timeTracker = float(loaded[10])
            self.poopTimer = float(loaded[11])
            self.hungerTimer = float(loaded[12])
            self.happyTimer = float(loaded[13])
            self.ageTimer = float(loaded[14])
            self.sickTimer = float(loaded[15])
            self.fussTimer = float(loaded[16])
            self.raisingMistakeTimer = float(loaded[17])
            self.state = loaded[18].rstrip()
        self.setState(self.state)
        #self.prepStatsForPlay()
            

    def saveThings(self):

        #all stats is a list of stats in order for saving
        allStats = [self.ageStat, self.hungerStat, self.weightStat, self.happyStat, self.disciplineStat,
        self.tiredStat, self.poopStat, self.sickStat, self.isFussing, self.raisingMistakeStat, self.timeTracker,
        self.poopTimer, self.hungerTimer, self.happyTimer, self.ageTimer, self.sickTimer, self.fussTimer,
        self.raisingMistakeTimer, self.state]

        #self.prepStatsForSave()
        with open("{0}/saves/petdata.txt".format(sys.path[0]), "w") as saveFile:
            for stat in range(len(allStats)):
                saveFile.write(str(allStats[stat]) + "\n")
        #self.prepStatsForPlay
    
    # def prepStatsForSave(self):
    #     for stat in range(len(self.allStats)):
    #         self.allStats[stat] = str(self.allStats[stat])
    
    # def prepStatsForPlay(self):
    #     for stat in range(len(self.allStats)):
    #         try:
    #             self.allStats[stat] = int(self.allStats[stat])
    #         except:
    #             if self.allStats[stat] == "False":
    #                 self.allStats[stat] = False
    #             elif self.allStats[stat] == "True":
    #                 self.allStats[stat] = True

    def exitThing(self):
        exit()

    def resetThings(self):

        self.ageStat = 0
        self.hungerStat = 0
        self.weightStat = 0
        self.happyStat = 0
        self.disciplineStat = 0
        self.tiredStat = 5
        self.poopStat = 0.0
        self.sickStat = 0.0
        self.isFussing = False
        self.raisingMistakeStat = 0
        self.timeTracker = 0
        self.poopTimer = 300
        self.hungerTimer = 120
        self.happyTimer = 150
        self.ageTimer = 86400
        self.sickTimer = 180
        self.fussTimer = 450
        self.raisingMistakeTimer = 600
        self.state = "EGG"
        self.setState("EGG")

    def selectStuff(self):
        #for main screen
        if self.state == "MAIN":
            
            #for each option
            for option in range(len(self.mainOptions)):
                #set this option to the option
                thisOption = self.mainOptions[option]
                
                try:
                    #try setting the next option
                    nextOption = self.mainOptions[option+1]
                except:
                    #if next option is out of range, set next option to this option
                    nextOption = self.mainOptions[option]
                
                #check which option is enabled
                if thisOption.isEnabled():
                    #set next option to true first so if it was out of range it will be turned false right after
                    nextOption.setEnabled(True)
                    thisOption.setEnabled(False)
                    #break out of the loop when the selection has moved
                    break

                if thisOption == nextOption:
                    #if this and next are the same and it did not break out of the loop above
                    #nothing was selected, so set option 0 to true
                    self.labelOption0.setEnabled(True)

        #for food screen
        elif self.state == "FOOD":
            option1 = self.labelMeal
            option2 = self.labelSnack

            #toggle between the two
            if option1.isEnabled():
                option1.setEnabled(False)
                option2.setEnabled(True)
            else:
                option1.setEnabled(True)
                option2.setEnabled(False)
        
        #for stats screen
        elif self.state == "STATS":
            print(self.labelStatsText.text())
            if self.labelStatsText.text() == "AGE":
                self.labelStatsText.setText("WEIGHT")
                self.labelStatsImage.setText("{0}lbs".format(self.weightStat))
            elif self.labelStatsText.text() == "WEIGHT":
                self.labelStatsText.setText("DISCIPLINE")
                self.labelStatsImage.setText("{0}/5".format(self.disciplineStat))
            elif self.labelStatsText.text() == "DISCIPLINE":
                self.labelStatsText.setText("HUNGER")
                self.labelStatsImage.setText("{0}/5".format(self.hungerStat))
            elif self.labelStatsText.text() == "HUNGER":
                self.labelStatsText.setText("HAPPINESS")
                self.labelStatsImage.setText("{0}/5".format(self.happyStat))
            elif self.labelStatsText.text() == "HAPPINESS":
                self.labelStatsText.setText("AGE")
                self.labelStatsImage.setText("{0}Y".format(self.ageStat))

        #for night screen
        elif self.state == "NIGHT":
            self.setState("MAIN")

    def confirmStuff(self):
        if self.state == "MAIN":
            #for food option
            if self.labelOption0.isEnabled():
                #change state to food screen
                self.setState("FOOD")
            elif self.labelOption1.isEnabled():
                #change state to lights out
                self.setState("NIGHT")
            elif self.labelOption2.isEnabled():
                #change state to game mode
                self.setState("GAME")
                self.happyStat += 1
                self.weightStat -= 1
            elif self.labelOption3.isEnabled():
                #set state to medic
                self.setState("MEDIC")
                self.sickStat -= 1.5
            elif self.labelOption4.isEnabled():
                #set state to bath
                self.setState("BATH")
                self.poopStat -= 1.5
            elif self.labelOption5.isEnabled():
                #set state to stats
                self.setState("STATS")
            elif self.labelOption6.isEnabled():
                #set state to discipline
                self.setState("DISCIPLINE")
                if self.isFussing:
                    self.isFussing = False
                    self.disciplineStat += 1
                    self.happyStat -= 1
                else:
                    self.disciplineStat -= 1
                    self.happyStat -= 2
                    
            else:
                #set state to clock
                self.setState("CLOCK")

        #NEEDS TO BE ELIF OR IT WILL RUN IMMEDIATELY AFTER SELECTING FOOD AND AUTOFEED DEFAULT OPTION
        elif self.state == "FOOD":
            #meal effects
            if self.labelMeal.isEnabled():
                #set state to eating meal
                #setState("EATMEAL")
                self.hungerStat += 2
                self.weightStat += 1
            else:
                #set state to eating snack
                #setState("EATSNACK")
                self.happyStat += 1
                self.sickStat += 0.1
                self.weightStat += 2

            self.setState("EATING")
        
        #for night screen
        elif self.state == "NIGHT":
            self.setState("MAIN")

    def cancelStuff(self):
        #IMPORTANT
        #most states will return to main if cancel is pressed
        #HOWEVER
        #some states are designed to delay user input
        #thus we avoid using else: set state main

        #for main screen, deselect options
        if self.state == "MAIN":
            for option in range(len(self.mainOptions)):
                self.mainOptions[option].setEnabled(False)
        #for food state return to main without feeding
        elif self.state == "FOOD":
            self.setState("MAIN")
        #for night state return to main
        elif self.state == "NIGHT":
            self.setState("MAIN")
        #cancel game to main
        elif self.state == "GAME":
            self.setState("MAIN")
        #for stats state return to main
        elif self.state == "STATS":
            self.setState("MAIN")
        #for clcok return to main
        elif self.state == "CLOCK":
            self.setState("MAIN")

    def setState(self, state):
        self.hideAll(self.hideables)

        #reset animation on state change
        self.frame = 0

        if state == "MAIN" or state == "EGG" or state == "HATCHING" or state == "SHATTERING":         
            #show poop if pooped
            if self.poopStat > 0:
                self.labelPoop.setHidden(False)
            
            #show sick if sick
            if self.sickStat >= 1:
                self.labelSick.setHidden(False)
            
            #show creature
            self.labelMain.setHidden(False)

            
        
        elif state == "FOOD":
            #show food
            self.labelMeal.setHidden(False)
            self.labelSnack.setHidden(False)
        
        elif state == "NIGHT":
            #show nothinggggg
            pass

        elif state == "GAME":
            #show creature
            self.labelMain.setHidden(False)

        elif state == "STATS":
            #show stats
            self.labelStatsText.setHidden(False)
            self.labelStatsImage.setHidden(False)
            self.labelStatsText.setText("AGE")
            self.labelStatsImage.setText("{0}Y".format(self.ageStat))
        
        elif state == "CLOCK":
            #show clock
            self.labelStatsText.setHidden(False)
            self.labelStatsImage.setHidden(False)
            self.labelStatsText.setText("TIME")
            self.labelStatsImage.setText("{0}".format(QTime.currentTime().toString(Qt.DefaultLocaleLongDate)))

        #set state after else return to avoid setting state to an error
        self.state = state

    def hideAll(self, hide):
        for label in range(len(hide)):
            hide[label].setHidden(True)

    def statUpdates(self):
        #increase timetracking
        self.timeTracker += 1
        
        #hatch on time
        if self.timeTracker == self.hatchTimer:
            self.setState("HATCHING")


        #poop on time
        if self.timeTracker > self.poopTimer:
            self.poopStat += 1
            self.weightStat -= 0.5
            #next poop between 200 and 500 seconds
            self.poopTimer += random.randint(200, 500)
        #get hungry every x seconds
        if self.timeTracker > self.hungerTimer:
            self.hungerStat -= 1
            self.hungerTimer += random.randint(100, 300)
        #lose happy every x seconds
        if self.timeTracker > self.happyTimer:
            self.happyStat -= 1
            self.happyTimer += random.randint(100,300)
        #age every day
        if self.timeTracker > self.ageTimer:
            self.ageStat += 1
        #get sick over time
        if self.timeTracker > self.sickTimer:
            self.sickStat += 0.3
            self.sickTimer += (random.randint(100,300) / self.sickStat)
            if self.poopStat > 0.0:
                self.sickStat += self.poopStat

        #fuss for no reason over time
        if self.timeTracker > self.fussTimer:
            self.isFussing = True
            self.fussTimer += (random.randint(200, 300) * self.disciplineStat)

        #update screen with poop on poop
        if self.poopStat >= 1 and self.state == "MAIN":
            self.labelPoop.setHidden(False)
        
        #update screen with sick on sick
        if self.sickStat >= 1 and self.state == "MAIN":
            self.labelSick.setHidden(False)

        #if sick or poop or fussing or hungry or unhappy, trigger attention icon
        if self.hungerStat <= 1 or self.happyStat <= 1 or self.poopStat >= 1 or self.sickStat >= 1 or self.isFussing:
            self.labelAttention.setEnabled(True)
        else:
            self.labelAttention.setEnabled(False)

        #set minimums and maximums
        if self.hungerStat < 0:
            self.hungerStat = 0
        if self.hungerStat > 5:
            self.hungerStat = 5
        #happy
        if self.happyStat < 0:
            self.happyStat = 0
        if self.happyStat > 5:
            self.happyStat = 5
        #weight
        if self.weightStat < 10:
            self.weightStat = 10
        if self.weightStat > 100:
            self.weightStat = 100
        #disciplineStat
        if self.disciplineStat < 0:
            self.disciplineStat = 0
        if self.disciplineStat > 5:
            self.disciplineStat = 5
        
        #if pet needs attention
        if self.labelAttention.isEnabled():
            #countdown mistake timer
            self.raisingMistakeTimer -= 1
            #after 10 minutes of neglect, add 1 mistake and reset mistake countdown
            if self.raisingMistakeTimer <= 0:
                self.disciplineStat -= 1
                self.happyStat -= 1
                self.raisingMistakeStat += 1
                self.raisingMistakeTimer = 600
            
            #after 5 minutes of neglect, become undeciplined and unhappy
            if self.raisingMistakeTimer <= 300:
                self.disciplineStat -= 1
                self.happyStat -= 1

        if self.state == "CLOCK":
            self.labelStatsImage.setText("{0}".format(QTime.currentTime().toString(Qt.DefaultLocaleLongDate)))

    def animate(self):
        #increment frame count
        self.frame += 1
        print("animating")
        if self.state == "MAIN":
            if self.frame > 11:
                self.frame = 1
            self.labelMain.setPixmap(QPixmap("{0}/sprites/poro_sprite{1}.png".format(sys.path[0],self.frame)))
        elif self.state == "EGG":
            if self.frame > 3:
                self.frame = 1
            self.labelMain.setPixmap(QPixmap("{0}/sprites/egg_sprite{1}.png".format(sys.path[0],self.frame)))
        elif self.state == "HATCHING":
            if self.frame > 3:
                self.frame = 1
                self.setState("SHATTERING")
            self.labelMain.setPixmap(QPixmap("{0}/sprites/hatch_sprite{1}.png".format(sys.path[0],self.frame)))
        elif self.state == "SHATTERING":
            if self.frame > 2:
                self.frame = 1
                self.setState("MAIN")
            self.labelMain.setPixmap(QPixmap("{0}/sprites/shatter_sprite{1}.png".format(sys.path[0],self.frame)))

        elif self.state == "EATING":
            #not artistic enough to make an eating animation
            self.setState("MAIN")
        elif self.state == "DISCIPLINE":
            #not artistic enough to make an discipline animation
            self.setState("MAIN")
        elif self.state == "GAME":
            #not artistic enough to make an game animation
            self.setState("MAIN")
        elif self.state == "BATH":
            #not artistic enough to make an cleaning animation
            self.setState("MAIN")
        elif self.state == "MEDIC":
            #not artistic enough to make an medicating animation
            self.setState("MAIN")

    #handle x out
    def closeEvent(self, event):
        close = QMessageBox.question(self,
                                     "QUIT",
                                     "Save first?",
                                      QMessageBox.Yes | QMessageBox.No)
        if close == QMessageBox.Yes:
            self.saveThings()
            event.accept()
        else:
            event.accept()
# DO NOT MODIFY THIS CODE
if __name__ == "__main__":
    app = QApplication(sys.argv)
    the_form = MyForm()
    the_form.show()
    sys.exit(app.exec_())
# END DO NOT MODIFY