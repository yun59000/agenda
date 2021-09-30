import json
from os import path
import datetime
# from smtp import sendMail
from colorama import init, Fore, Back, Style

filename = '../data/event.json'
listObj = []
init(autoreset=True)

# check if file exist
def check_if_file_exist(filename):
  if path.isfile(filename) is False:
    raise Exception("File not found")

class MyMilestones:
    def __init__(self,milestonesInDays,originalDate):
      self.originalDate = originalDate
      self.milestonesInDays = milestonesInDays #list of milestones [12,120] -> 12 days, 120 days
      self.milestonesAsDate = []
      self.milestonesAsStrDate = []
      self.fullfill_milestones()

    def generate_strdate_with_milestones(self,daysToAdd):      
      date_time_obj = datetime.datetime.strptime(self.originalDate, '%Y-%m-%d')
      myMilestone = date_time_obj + datetime.timedelta(days = daysToAdd) # type date      
      return self.milestonesAsDate.append(myMilestone.strftime("%Y-%m-%d")) # type string

    def generate_date_with_milestones(self,daysToAdd):      
      date_time_obj = datetime.datetime.strptime(self.originalDate, '%Y-%m-%d')
      myMilestone = date_time_obj + datetime.timedelta(days = daysToAdd) # type date
      return self.milestonesAsStrDate.append(myMilestone)
    
    def fullfill_milestones(self):
      for milestone in self.milestonesInDays:
        # print('milestone: '+str(milestone))
        self.generate_date_with_milestones(milestone)
        self.generate_strdate_with_milestones(milestone)
      

class MyAgendaEvent:
  def __init__(self,lib,description,creationDateStr,listOfMilestones):
    self.lib = lib
    self.description = description
    self.creationDateStr = creationDateStr
    self.lastEditDateStr = ""
    # self.listOfMilestones = listOfMilestones
    self.listOfMilestonesObj = MyMilestones(listOfMilestones,creationDateStr)
    self.jsonFormAgendaEvent = ''
    self.new = True
    self.filename = '../data/event.json'
  
  def checkIfEventAlreadyExistInFile(self, key):
    with open(self.filename,'r') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        if key in file_data:
          # print("key found")
          self.new = False
          return True
        else:
          # print("key not found")
          self.new = True
          return False
        
  def getLastRecordIndex(self):
    with open(self.filename,'r') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)    
    # print(file_data[-1])    
    values_view = file_data[-1].keys()
    value_iterator = iter(values_view)
    first_key = next(value_iterator)
    lastIndex = first_key[5:]
    # print("last")
    # print(lastIndex)
    return lastIndex

  def createEvent(self):
    # dateTimeObj = datetime.datetime.now()
    # timestampStr = dateTimeObj.strftime("%Y%m%d%H%M%S")
    i= 1
    lastIndex = self.getLastRecordIndex()
    index = str(int(lastIndex) + 1)
    y = { "event" + index :{
          "lib" : self.lib,
          "index" : index,
          "description" : self.description,
          "date_ori" : self.creationDateStr,
          "date_edit" : ""}
        } 
    eventKey = "event" + index
    if self.checkIfEventAlreadyExistInFile(eventKey) == False:
      for elmt in self.listOfMilestonesObj.milestonesAsStrDate:
        y["event" + index]["date_"+ str(i) + "_milestone"] = elmt.strftime("%Y-%m-%d")
        i = i +1
      self.jsonFormAgendaEvent = y
    else:
      print("an event with that name already exist "+eventKey)
    # print("y: "+ str(y))
    return y

def editEvent(lib, key, value):
  with open(filename,'r') as file:
      # First we load existing data into a dict.
      file_data = json.load(file)
  for elmt in file_data:
    values_view = elmt.keys()
    value_iterator = iter(values_view)
    first_key = next(value_iterator)
    # print(first_key)
    
    if elmt[first_key]["lib"] == lib:
      # print("trouvé")
      # print("OldKey: "+key+" OldValue: "+elmt[first_key][key])
      # print("a changer key :"+key + " value: "+value)
      elmt[first_key][key] = value
      # write_json(file_data)
      with open(filename,'r+') as file:        
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4, separators=(',',': '))
        print('Successfully edit the JSON file')

def delEvent(lib):
  with open(filename,'r') as file:
      # First we load existing data into a dict.
      file_data = json.load(file)
  newFileData = []
  for elmt in file_data:
    values_view = elmt.keys()
    value_iterator = iter(values_view)
    first_key = next(value_iterator)
    # print(first_key)
    
    if elmt[first_key]["lib"] == lib:
      pass      
    else:
      newFileData.append(elmt)
  
  valid = input("Etes vous sûre de vouloir supprimer l'event "+ lib + " ? y or n : ")
  if valid == "y":          
    with open(filename,'w') as file:        
      # Sets file's current position at offset.
      file.seek(0)
      # convert back to json.
      json.dump(newFileData, file, indent = 4)
      print('Successfully del the event')
  else:
    choice()

#**************************
# # function to add to JSON
def write_json_add(new_data, filename='../data/event.json'):
    with open(filename,'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data.append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4, separators=(',',': '))
        print('Successfully appended to the JSON file')
# ******************************    
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
    milestones = input("Delais à appliquer en jours, séparé par un espace si plusieurs: ")
    if milestones == "":
      milestones = 0
  listOfMilestoneStr = milestones.split()
  for elmt in listOfMilestoneStr:
      listOfMilestoneInt.append(int(elmt))
  
  mon_evet = MyAgendaEvent(lib,description,evtStartDate,listOfMilestoneInt)
  new_data = mon_evet.createEvent()
  if mon_evet.new == True:
    write_json_add(new_data)  
  else:
    print("event already exist please change lib")
  choice()
  
def days_between(d1, d2):
    d1 = datetime.datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.datetime.strptime(d2, "%Y-%m-%d")
    return str(abs((d2 - d1).days))

def showEvents(filename='../data/event.json', notify=False):
    #lire    
    aujourdhui = datetime.datetime.now()
    timestampStr = aujourdhui.strftime("%Y-%m-%d")
    with open(filename,'r') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
    
    for elmt in file_data:
        values_view = elmt.keys()
        value_iterator = iter(values_view)
        first_key = next(value_iterator)
        i=0
        listOfData = []
        listOfDataToNotify = []
        for myList in elmt:
          eachList = list(elmt[first_key].items())
          # print(eachList)
          # print("event:")
          listTemp = []
          toNotify = False
          for eachItem in eachList:
            # print(eachItem[0][7:])
            if eachItem[0][7:] == "milestone":
              date_time_obj = eachItem[1]
              diffDay = days_between(timestampStr,date_time_obj)
              
              if int(diffDay) <= 15:
                toNotify = True
                listTemp.append(Fore.RED +eachItem[0]+" -> "+eachItem[1]+" ->prévu dans "+diffDay+" jours")
                listOfData.append(eachItem[0]+" -> "+eachItem[1]+" ->prévu dans "+diffDay+" jours")
              elif int(diffDay) > 15 and int(diffDay) <= 31:
                toNotify = True
                listTemp.append(Fore.YELLOW +eachItem[0]+" -> "+eachItem[1]+" ->prévu dans "+diffDay+" jours")
                listOfData.append(eachItem[0]+" -> "+eachItem[1]+" ->prévu dans "+diffDay+" jours")
              else:                
                listTemp.append(Fore.GREEN +eachItem[0]+" -> "+eachItem[1]+" ->prévu dans "+diffDay+" jours")
                listOfData.append(eachItem[0]+" -> "+eachItem[1]+" ->prévu dans "+diffDay+" jours")
            else:              
              listOfData.append("%s -> %s" % (eachItem))
              listTemp.append("%s -> %s" % (eachItem))
          if toNotify == True:
            listOfDataToNotify.append(listTemp)

          if notify == True:
            for lignes in listOfDataToNotify:
              for eachLigne in lignes:
                print(eachLigne)
              print("**************************")
              input("Press Enter notif")
              
          else:
            for lignes in listOfData:
              print(lignes)
            print("**************************")  
            input("Press Enter")
          
          i = i + 1
    choice()
    # sendMail(listOfData)    
 
def searchEvent(searchLib):
  with open(filename,'r') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
  aujourdhui = datetime.datetime.now()
  timestampStr = aujourdhui.strftime("%Y-%m-%d")
  for files in file_data:
    search = False
    for eachfile in files.values():
      # print("********search**********")
      # print(eachfile)
      for k, v in eachfile.items():
        if v == searchLib:
          search = True
          break
      listTemp = []
      if search == True:
        print("**************************")        
        for eachdata in eachfile.items():
          # print(eachdata[0]+" -> "+eachdata[1])
          #***************
          if eachdata[0][7:] == "milestone":
            date_time_obj = eachdata[1]
            diffDay = days_between(timestampStr,date_time_obj)
            
            if int(diffDay) <= 15:              
              listTemp.append(Fore.RED +eachdata[0]+" -> "+eachdata[1]+" ->prévu dans "+diffDay+" jours")              
            elif int(diffDay) > 15 and int(diffDay) <= 31:              
              listTemp.append(Fore.YELLOW +eachdata[0]+" -> "+eachdata[1]+" ->prévu dans "+diffDay+" jours")              
            else:                
              listTemp.append(Fore.GREEN +eachdata[0]+" -> "+eachdata[1]+" ->prévu dans "+diffDay+" jours")              
          else:                          
            listTemp.append("%s -> %s" % (eachdata))

      for allelmt in listTemp:
        print(allelmt)
  input("Press Enter")
  choice()

def choice():  
  choice = False
  while choice == False:
    print("Programme de gestion d'evenements calendaire")
    print("Actions : ")
    print(" 1 - Créer un évenement")
    print(" 2 - Editer un évenement")
    print(" 3 - Supprimer un évenement")
    print(" 4 - Consulter les événements")
    print(" 5 - Consulter les événement à notifier")
    print(" 6 - Rechercher un événement")
    print(" 0 - exit")
    x = input('Entrer une valeur : ')
    if x == "1":
      create()
      choice = True
    elif x == "2":
      lib = input("enter lib: veille de noel17 ")
      print('key: "lib", "description", "date_ori", "date_edit", "date_1_milestone", "date_2_milestone", "date_3_milestone", "date_4_milestone"')
      key = input("enter the key to modify: ")
      print("format de date: YYYY-MM-DD")
      value = input("enter the new value: ")
      editEvent(lib, key, value)
      choice = True 
    elif x == "3":
      lib = input("enter lib: veille de noel17 ")
      delEvent(lib)
      choice = True
    elif x == "4":
      showEvents()
      choice = True
    elif x == "5":
      showEvents(notify=True)
      choice = True      
    elif x == "6":
      searchLib = input("enter lib: veille de noel17 ")
      searchEvent(searchLib)
      choice = True
    elif x == "0":
      print("Merci à bientôt")
      exit()
    else:
      print("WIP")
      input("Press Enter")

choice()

# ToDo
# agenda
    # events
        # milestones
  
# jalon en jours dans l'objet
# check choice a l'edition
# check modif si key n'existe pas
# fonction ajouter un jalons
# fonction supprimer un jalons