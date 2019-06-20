############################################################################# 
## Events contains nessesary routines for writting markers file for 
## BrainVision data format
############################################################################# 
## Copyright (c) 2018-2019, University of Liège
## Author: Nikita Beliy
## Owner: Liege University https://www.uliege.be
## Version: 0.74
## Maintainer: Nikita Beliy
## Email: Nikita.Beliy@uliege.be
## Status: developpement
############################################################################# 
## This file is part of eegBidsCreator                                     
## eegBidsCreator is free software: you can redistribute it and/or modify     
## it under the terms of the GNU General Public License as published by     
## the Free Software Foundation, either version 2 of the License, or     
## (at your option) any later version.      
## eegBidsCreator is distributed in the hope that it will be useful,     
## but WITHOUT ANY WARRANTY; without even the implied warranty of     
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the     
## GNU General Public License for more details.      
## You should have received a copy of the GNU General Public License     
## along with eegBidsCreator.  If not, see <https://www.gnu.org/licenses/>.
############################################################################


from datetime import datetime

class MarkerFile(object):
    __slots__ = ["DataFile", "__file", "__path", "__prefix", "__startTime", "__frequency", "__mkCount", "__aDate" ]

    def __init__(self, path, prefix, encoding = "ANSII"):
        self.DataFile   = prefix+"_eeg.eeg"
        self.__path     = path
        self.__prefix   = prefix
        self.__startTime= None
        self.__frequency= -1
        self.__mkCount  = 0
        self.__file = None
        self.__aDate = None

    def SetAnonymDate(self, date):
        self.__aDate = date

    def SetFrequency(self, frequency):
        self.__frequency = frequency

    def SetStartTime(self, time):
        self.__startTime = time

    def OpenFile(self, encoding):        
        if encoding == "ANSI":
            enc = "ascii"
        elif encoding == "UTF-8":
            enc = "utf_8"
        else: raise Exception("BrainVision Header: wrong encoding '{}', only 'ANSI' and 'UTF-8' are supported")
        self.__file = open(self.__path+"/"+self.__prefix+"_eeg.vmrk", "w", encoding=enc)
        self.__file.write("Brain Vision Data Exchange Marker File Version 1.0\n")

        self.__file.write("\n[Common Infos]\n")
        self.__file.write("DataFile={}\n".format(self.DataFile))

        self.__file.write("\n[Marker Infos]\n")
        
    def Write(self):
        self.__file.close()        
       
    def AddNewSegment(self, date, channel  = -1, description = ''):
        self.AddMarker("New Segment", date, 0, channel, description)
        
    def AddMarker(self, name, date, duration = 0, channel = -1, description = '' ) :
        if self.__startTime == datetime.min or self.__frequency <= 0:
            raise Exception ("Markers start time or frequency are not initialized")
        self.__mkCount += 1
        #<name>,<description>,<position>,<points>,<channel number>,<date>
        pos = int((date - self.__startTime).total_seconds()*self.__frequency)
        lenght = int(duration*self.__frequency + 0.5)
        if self.__aDate != None:
            date = self.__aDate + (date - self.__startTime)
        if lenght == 0:
            lenght = 1
        if name == "New Segment":
            self.__file.write("Mk{0}={1},{2},{3},{4},{5},{6}\n".format(
                    self.__mkCount,
                    name,description,
                    pos,lenght,
                    channel+1, 
                    date.strftime("%Y%m%d%H%M%S%f") ))
        else:
            self.__file.write("Mk{0}={1},{2},{3},{4},{5}\n".format(
                    self.__mkCount,
                    name,description,
                    pos,lenght,
                    channel+1 
                    ))
            
        
        
