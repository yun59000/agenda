from functions.common import *

agenda = Agenda("nouvel Agenda")
miles = { "mile" : [{"lib":"monmile1","mile":"5"}, {"lib":"monmile2","mile":"2"} ]}
# print(miles)
agenda.addEvent("evt1", "2021-03-02", miles )#{"mile": {"lib":"monmile1","mile":"5"},"mile": {"lib":"monmile2","mile":"2"}}
agenda.printAgenda()
# ****************************Edit milestone
newdmilestone = {"mileLib" :"monmile1" ,"key":"milestone", "keyValue" :"6"}
agenda.listOfEvents[0].editEvent("milestone", newdmilestone)
newdmilestone2 = {"mileLib" :"monmile2" ,"key":"milestone", "keyValue" :"62"}
agenda.listOfEvents[0].editEvent("milestone", newdmilestone2)
# ****************************Edit
newdmilestone2 = {"mileLib" :"monmile2" ,"key":"milestone", "keyValue" :"62"}
agenda.listOfEvents[0].editEvent("milestone", newdmilestone2)
#*****************************
agenda.printAgenda()