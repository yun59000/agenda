from functions.common import *

agenda = Agenda("nouvel Agenda")
# miles = { "mile" : [{"lib":"monmile1","mile":"5"}, {"lib":"monmile2","mile":"2"} ]}
# agenda.addEvent("evt1", "2021-03-02", miles )#{"mile": {"lib":"monmile1","mile":"5"},"mile": {"lib":"monmile2","mile":"2"}}
# agenda.printAgenda()
# ****************************Edit milestone OK
# newdmilestone = {"mileLib" :"monmile1" ,"key":"milestone", "keyValue" :"6"}
# agenda.listOfEvents[0].editEvent("milestone", newdmilestone)
# newdmilestone2 = {"mileLib" :"monmile2" ,"key":"milestone", "keyValue" :"62"}
# agenda.listOfEvents[0].editEvent("milestone", newdmilestone2)
# ****************************Edit lib OK
# newdmilestone3 = {"mileLib" :"monmile2" ,"key":"lib", "keyValue" :"monmile3"}
# agenda.listOfEvents[0].editEvent("milestone", newdmilestone3)
# ****************************Edit lib OK
# agenda.listOfEvents[0].editEvent("startDate", "2021-05-01")
#*****************************Add milestone
# milestoneToAdd = { "mile" : [{"lib":"monmileadd","mile":"10"}, {"lib":"monmileadd2","mile":"12"} ]}
# agenda.listOfEvents[0].createMilestones(milestoneToAdd)
#*****************************
# agenda.printAgenda()

def create():
  # demander les infos
  listOfMilestoneInt = []
  err = True
  while err == True:
    evtStartDateYYYY = input("Date de début de l'evenement - Année: AAAA: ") #check date a mettre en place
    if int(evtStartDateYYYY) > 2020:
      err = False
    evtStartDateMM = input("Date de début de l'evenement - Mois: MM: ")
    if int(evtStartDateMM) > 0 and int(evtStartDateMM) < 13:
      err = False
    evtStartDateDD = input("Date de début de l'evenement - Jours: DD: ")
    if int(evtStartDateDD) > 0 and int(evtStartDateDD) < 32:
      err = False
    evtStartDate = evtStartDateYYYY + "-" + evtStartDateMM + "-" + evtStartDateDD
    lib = input("Nom de l'evenement: ")
    if lib != "":
      err = False
    description = input("Description de l'evenement: ")
    oneMoreMilestone = True
    listOfMilestones = []
    print("Vous êtes sur le point d'ajouter le/les milestones à l'évenement l'ordre à une importance")
    print("le premier milestone sera calulé a partir de la date de l'evenement")
    print("chaque autre milestone est calculé en fonction de la date du précedent ")
    while oneMoreMilestone:
        print("Milestone a ajouter: ")
        milestoneLib = input("Nom du milestone: ")
        milestoneMile = input("Delait en jours: ")
        milestoneAdd = input("un milestone suplémentaire ? (y or n): ")
        milestoneData = {"lib": milestoneLib,"mile": milestoneMile}
        listOfMilestones.append(milestoneData) 
        if milestoneAdd == "n":
            oneMoreMilestone = False
        elif milestoneAdd == "y":
            oneMoreMilestone = True
        else:
            print("mauvais choix !")      
#   miles = { "mile" : [{"lib":"monmile1","mile":"5"}, {"lib":"monmile2","mile":"2"} ]}  
  miles = { "mile" : listOfMilestones}  
  agenda.addEvent(lib, description, evtStartDate, miles )#{"mile": {"lib":"monmile1","mile":"5"},"mile": {"lib":"monmile2","mile":"2"}}
  agenda.printAgenda()
#   mon_evet = MyAgendaEvent(lib,description,evtStartDate,listOfMilestoneInt)
#   new_data = mon_evet.createEvent()
#   if mon_evet.new == True:
#     write_json_add(new_data)  
#   else:
#     print("event already exist please change lib")
  choice()

def choice():  
  choice = False
  while choice == False:
    print("Programme de gestion d'evenements calendaire")
    print("Actions : ")
    print(" 1 - Créer un évenement")#OK
    print(" 2 - Editer un évenement")
    print(" 3 - Supprimer un évenement")
    print(" 4 - Consulter les événements")
    print(" 5 - Consulter les événement à notifier")
    print(" 6 - Rechercher un événement")
    print(" 0 - exit")
    x = input('Entrer une valeur : ')
    if x == "1":
      create()
      choice = False
    elif x == "2":
      agenda.printEventslib()
      lib = input("enter event lib: ")
      event = agenda.selectEvent(lib)
      print('"lib", "description", "startDate", "milestone"')
      key = input("enter the key to modify: ")
      if key == "milestone":
          print("edit milestone: ")
          milestoneLib = input("lib du milestone a edit: ")
          print("quelle information du milestone a modifer: ")
          milestonekey = input("lib, initialDate ou milestone ? ")
          print("format de date: YYYY-MM-DD")
          milestoneNewValue = input("Nouvelle valeur ? ")
          newdmilestone3 = {"mileLib" : milestoneLib,"key": milestonekey, "keyValue" : milestoneNewValue}
          event.editEvent(key, newdmilestone3)
            # newdmilestone3 = {"mileLib" :"monmile2" ,"key":"lib", "keyValue" :"monmile3"}
            # agenda.listOfEvents[0].editEvent("milestone", newdmilestone3)
            # newdmilestone = {"mileLib" :"monmile1" ,"key":"milestone", "keyValue" :"6"}
            # agenda.listOfEvents[0].editEvent("milestone", newdmilestone)
          
      else:
        value = input("enter the new value: ")
        event.editEvent(key, value)
    #   editEvent(lib, key, value)
      choice = False 
    elif x == "3":
      lib = input("enter lib: veille de noel17 ")
    #   delEvent(lib)
      choice = True
    elif x == "4":
    #   showEvents()
      agenda.printAgenda()
      choice = False
    elif x == "5":
    #   showEvents(notify=True)
      choice = True      
    elif x == "6":
      searchLib = input("enter lib: veille de noel17 ")
    #   searchEvent(searchLib)
      choice = True
    elif x == "0":
      print("Merci à bientôt")
      exit()
    else:
      print("WIP")
      input("Press Enter")

choice()