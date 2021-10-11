
import datetime

class Agenda:
    def __init__(self, lib):
        self.lib = lib
        self.listOfEvents = []
    
    def addEvent(self, lib, description, strStartdate, dictOfMilestones):
        # print(dictOfMilestones){ "mile" : [{"lib":"monmile1","mile":"5"}, {"lib":"monmile2","mile":"2"} ]}
        event = self.Event(lib, description, strStartdate, dictOfMilestones)
        self.listOfEvents.append(event)

    def printAgenda(self):
        print("*********Agenda***DEB******")
        print("lib: "+self.lib)
        self.printEvents()
        print("*********Agenda***FIN******")

    def printEvents(self):
        for eachEvent in self.listOfEvents:
            eachEvent.printEvent()
 
    def printEventslib(self):
        for eachEvent in self.listOfEvents:
            eachEvent.printEventlib()

    def selectEvent(self,lib):
        for eachEvent in self.listOfEvents:
            if eachEvent.lib == lib:
                return eachEvent


    class Event:
        def __init__(self,lib, description, strStartdate, dictOfMilestones):
            self.lib = lib
            self.strStartDate = strStartdate
            self.dictOfMilestones = dictOfMilestones
            self.description = description
            # print("---**---"+str(dictOfMilestones))
            self.listOfMilestonesObjects = []
            self.createMilestones(self.dictOfMilestones)#{ "mile" : [{"lib":"monmile1","mile":"5"}, {"lib":"monmile2","mile":"2"} ]}

        def editEvent(self, keyToChange, editedValue):
            if keyToChange == "milestone":
                #dict {"lib" :"" ,"key":"initialDate", "keyValue" :""} ou {"lib" :"" , "key":"milestone", "keyValue" : ""}
                self.editMilestone(editedValue)
            elif keyToChange == "lib":
                self.lib = editedValue
            elif keyToChange == "startDate":                
                if checkifValueIsDate(editedValue):
                    print("date check OK")
                    self.strStartDate = editedValue
                    self.checkAndUpdateMilestones()
                else:
                    print("date check KO")

        def createMilestones(self, dictOfMilestones):#{ "mile" : [{"lib":"monmile1","mile":"5"}, {"lib":"monmile2","mile":"2"} ]}
            # print("---**---"+str(dictOfMilestones))
            index = 0
            oldMile = 0
            for eachMilestone in dictOfMilestones["mile"]:
                # print("---**---"+str(eachMilestone))
                tempDate = datetime.datetime.strptime(self.strStartDate, "%Y-%m-%d") + datetime.timedelta(days = oldMile)
                # startDate = datetime.datetime.strptime(self.strStartDate, "%Y-%m-%d")
                newMilestone = self.Milestone(eachMilestone["lib"] , eachMilestone["mile"], tempDate, index)
                self.listOfMilestonesObjects.append(newMilestone)
                oldMile = int(eachMilestone["mile"])
                index += 1
            self.checkAndUpdateMilestones()
        
        def editMilestone(self,dictValues):
        #{"mileLib" :"" ,"key":"initialDate", "keyValue" :""} ou {"mileLib" :"" , "key":"milestone", "keyValue" : ""}
            keyToModify = dictValues["key"]        
            for milestone in self.listOfMilestonesObjects:                
                if dictValues["mileLib"] == milestone.lib:
                    if keyToModify == "initialDate":    
                        print("dictvalue: "+dictValues["keyValue"])                    
                        d1 = dictValues["keyValue"]
                        milestone.initialDate = datetime.datetime.strptime(d1, "%Y-%m-%d")
                        milestone.generate_date_with_milestones(int(milestone.milestone))
                        self.checkAndUpdateMilestones()                       
                    elif keyToModify == "milestone" : #recalculer les dates
                        # print("dictvalue: "+dictValues["keyValue"])
                        milestone.milestone = dictValues["keyValue"]                        
                        milestone.generate_date_with_milestones(int(milestone.milestone))
                        self.checkAndUpdateMilestones()
                    elif keyToModify == "lib":
                        print("dictvalue: "+dictValues["keyValue"])
                        milestone.lib = dictValues["keyValue"]
                else:
                    print("no milestone with that lib: "+dictValues["mileLib"])

        def checkAndUpdateMilestones(self):            
            #constituer un dict avec {milestone:"", date:""
            nbElem = len(self.listOfMilestonesObjects) 
#            datetime.datetime.strptime(self.strStartDate, "%Y-%m-%d")
            #Check and update the first milestone
            self.listOfMilestonesObjects[0].initialDate = datetime.datetime.strptime(self.strStartDate, "%Y-%m-%d")
            self.listOfMilestonesObjects[0].calculatedMilestone = datetime.datetime.strptime(self.strStartDate, "%Y-%m-%d") + datetime.timedelta(self.listOfMilestonesObjects[0].milestone)
            #check and update all others milestones of this event
            for i  in range(nbElem -1):                
                print("*****************Avant************Mile -1 date: "+str(self.listOfMilestonesObjects[i].initialDate  ))
                print("*****************Avant************Mile -1 mile: "+str(self.listOfMilestonesObjects[i].milestone  ))                
                print("*****************Avant************Mile -1 datecalc: "+str(self.listOfMilestonesObjects[i].calculatedMilestone  ))
                print("*****************Avant************Mile courant date: "+str(self.listOfMilestonesObjects[i+1].initialDate  ))
                print("*****************Avant************Mile courant mile: "+str(self.listOfMilestonesObjects[i+1].milestone  ))
                print("*****************Avant************Mile courant datecalc: "+str(self.listOfMilestonesObjects[i+1].calculatedMilestone  ))                
                if self.listOfMilestonesObjects[i+1].initialDate != self.listOfMilestonesObjects[i].calculatedMilestone :
                    self.listOfMilestonesObjects[i+1].initialDate = self.listOfMilestonesObjects[i].calculatedMilestone 
                    self.listOfMilestonesObjects[i+1].calculatedMilestone = self.listOfMilestonesObjects[i+1].generate_date_with_milestones(int(self.listOfMilestonesObjects[i+1].milestone))
                    print("*****************Après************Mile -1 date: "+str(self.listOfMilestonesObjects[i].initialDate  ))
                    print("*****************Après************Mile -1 mile: "+str(self.listOfMilestonesObjects[i].milestone  ))
                    print("*****************Après************Mile -1 datecalc: "+str(self.listOfMilestonesObjects[i].calculatedMilestone  ))
                    print("*****************Après************Mile courant date: "+str(self.listOfMilestonesObjects[i+1].initialDate  ))
                    print("*****************Après************Mile courant mile: "+str(self.listOfMilestonesObjects[i+1].milestone  ))
                    print("*****************Après************Mile courant datecalc: "+str(self.listOfMilestonesObjects[i+1].calculatedMilestone  ))
                
        def printEvent(self):        
            print("    ---******Event***DEB******")
            print("    lib: "+ self.lib)
            print("    startDate: "+ self.strStartDate )
            self.printMilestones()
            print("    ---******Event***FIN******")

        def printEventlib(self):                    
            print("    **lib: "+ self.lib)
            print("    **startDate: "+ self.strStartDate )            

        def printMilestones(self):
            for eachMilestone in self.listOfMilestonesObjects:
                eachMilestone.printMilestone()

        class Milestone:#a revoir un seul objet pour toute la liste
            def __init__(self, lib, milestone, initialDate, index):
                self.lib = lib
                self.index = index
                self.initialDate = initialDate
                self.milestone = int(milestone)
                self.calculatedMilestone = self.generate_date_with_milestones(self.milestone)
                
            def generate_date_with_milestones(self,daysToAdd):      
                # date_time_obj = datetime.datetime.strptime(self.originalDate, '%Y-%m-%d')
                myMilestone = self.initialDate + datetime.timedelta(days = daysToAdd) # type date  
                self.calculatedMilestone  = myMilestone
                return myMilestone
            
            def printMilestone(self):
                print("        --------*Milestone***DEB******")
                print("        lib: " + self.lib)
                print("        milestone: " + str(self.milestone))
                print("        calc milestone: " + self.calculatedMilestone.strftime("%Y-%m-%d"))
                print("        --------*Milestone***FIN******")

def checkifValueIsDate(value):    
    yyyy = int(value[0:4])
    mm = int(value[5:7])
    dd = int(value[8:])
    print(yyyy)
    print(mm)
    print(dd)
    correctDate = None
    try:
        newDate = datetime.datetime(yyyy,mm,dd)
        correctDate = True
        print("date verif OK")
    except ValueError:
        correctDate = False
        print("date verif KO")
    return correctDate

    # Event
    # self.lib = lib
    # self.strStartDate = strStartdate
    # self.dictOfMilestones = dictOfMilestones
    # self.listOfMilestonesObjects = []
    #   Milestone
    #     miletone.lib = lib
    #     miletone.index = index
    #     miletone.initialDate = initialDate
    #     miletone.milestone = int(milestone)
    #     miletone.calculatedMilestone