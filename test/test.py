import json
from os import path
import datetime

filename = '../data/event.json'
listObj = []

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
          print("key found")
          self.new = False
          return True
        else:
          print("key not found")
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
    dateTimeObj = datetime.datetime.now()
    timestampStr = dateTimeObj.strftime("%Y%m%d%H%M%S")
    i= 1
    lastIndex = self.getLastRecordIndex()
    index = str(int(lastIndex) + 1)
    y = { "event" + index :{
          "lib" : self.lib + index ,
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

  def editEvent(self, lib, key, value):
    with open(self.filename,'r') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
    for elmt in file_data:
      values_view = elmt.keys()
      value_iterator = iter(values_view)
      first_key = next(value_iterator)
      print(first_key)
      
      if elmt[first_key]["lib"] == lib:
        # print("trouvé")
        # print("OldKey: "+key+" OldValue: "+elmt[first_key][key])
        # print("a changer key :"+key + " value: "+value)
        elmt[first_key][key] = value
        # write_json(file_data)
        with open(self.filename,'r+') as file:        
          # Sets file's current position at offset.
          file.seek(0)
          # convert back to json.
          json.dump(file_data, file, indent = 4, separators=(',',': '))
          print('Successfully edit the JSON file')
      # for k, v in elmt[first_key].items():
      #   print("keys: "+str(k)+ " value: "+str(v))

    # if file_data["lib"] == value:

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
mon_evet = MyAgendaEvent("nouvel event","description","2021-12-24",[1,8,2])
# print(mon_evet.lib)
# print(mon_evet.listOfMilestonesObj.originalDate)
# print(mon_evet.listOfMilestonesObj.milestonesInDays)
# print(mon_evet.listOfMilestonesObj.milestonesAsDate)
# print(mon_evet.listOfMilestonesObj.milestonesAsStrDate)

new_data = mon_evet.createEvent()
# print(mon_evet.jsonFormAgendaEvent)

#**********************************
if mon_evet.new == True:
  write_json_add(new_data)  
  # pass
else:
  print("event already exist please change lib")
  
mon_evet.editEvent("nouvel event4","description","une autre edit descrp")
#controle unicité json lib                                 *******************OK
#transform function def milestone to really add milestone to a date **********OK with obj 
#add def to add milestone to the JSON Object               *******************OK
#edit one param at a time                                  *******************OK