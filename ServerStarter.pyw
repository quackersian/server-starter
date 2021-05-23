""" 
Server Starter bot.
A custom bot for managing servers on a private home server.
Created by Big Spender#7291
v8 updated 23/05/2021
"""

import discord
from subprocess import Popen
import signal
import os
import asyncio
import time
import sys
import array
import pyautogui as pag
import pygetwindow as pgw
from datetime import datetime

from credentials import token

client = discord.Client()
version = "v8 23/05/2021"
updateSquad = [r"C:\steamcmd\squad_installandupdateBot.bat"]
startSquad = [r"C:\servers\squad_server\StartSquadServer.bat"]
startFactorio = [r"C:\servers\factorio_server\factorio_headless_x64_1.1.19\factorio\StartFactorioServer.bat"]
nameFactorio = "StartFactorioServer"
nameSquad = "C:\\servers\\squad_server\\SquadGame\\Binaries\\Win64\\SquadGameServer.exe"
nameSquadUpdate = "UpdateSquad"
fileLog = "log.txt"
fileAdmins = "admins.txt"
cmdSquadStart = "!squadstart"
cmdSquadUpdate = "!squadupdate"
cmdSquadStop = "!squadstop"
cmdSquadAdmin = "!squadadmin"
cmdFactorioStart = "!factoriostart"
cmdFactorioStop = "!factoriostop"
cmdHelp = "!help"
cmdServers = "!servers"
cmdCommand = "!"

retryCount = 1
squadProcess = ""

pubMsg = """```
!help
    Shows this message
!servers
    Shows the running servers
    
!squadstart
    Starts the Squad server
    
!factoriostart
    Starts the Factorio server``` """

adminMsg = """```
!help
    Shows this message    
!servers
    Shows the running servers
    
!squadstart
    Starts the Squad server
!squadstop
    Stops the Squad server
!squadupdate
    Updates the Squad server
    
!factoriostart
    Starts the Factorio server
!factoriostop
    Stops the Factorio server``` """



@client.event
async def on_ready():
    
    log("Logged on as {0.user} {1}.".format(client, version))
    #Get admins from file.
    with open (fileAdmins, 'r') as file:
        global admins
        admins = file.read()
        file.close()
        
        #takes admins from file and converts to ints, as message.author.id is an int.
        admins = admins.split()
        admins = list(map(int, admins))
    
        log("Loaded admins from file.")
    

@client.event
async def on_message(message):

    
    #skip reading message if not a command
    if not message.content.startswith(cmdCommand):
        return

    guild = message.guild
    allWindows = pgw.getAllTitles()

###############################################################################################################################
    
    #skip reading message if its from the bot.
    if message.author == client.user:        
        log("Message from myself!?")        
        return
    
    
    if message.content.startswith(cmdHelp):        
        log("{0.author} asked for help in channel {0.channel}.".format(message))
        

        #send pub message to pubs and admin message to admins
        if message.author.id in admins:
            await message.author.send(adminMsg)
            
        else:
            await message.author.send(pubMsg)

            
            
###############################################################################################################################
            
    #starting squad server
    if message.content.startswith(cmdSquadStart):
        
        try:
            #don't start the server if it is already running
            if nameSquad in allWindows:
                log("{0.author} tried to start the Squad server, but it was already running.".format(message))
                await message.author.send("The Squad server is already running.")
                return

            #don't start the server if it is updating   
            if nameSquadUpdate in allWindows:
                log("{0.author} tried to start the Squad server, but it was updating.".format(message))
                await message.author.send("The Squad server is currently updating, please try again later.")
                return

            #start the server if it is not already running and it is not updating.
            else:
                log("{0.author} started the Squad server.".format(message))
                await message.author.send("Starting the Squad server.")    
                squadProcess = Popen(startSquad)

            
        except Exception as e:
            log("ERROR: " + str(e))
            return


    #updating squad server
    if message.content.startswith(cmdSquadUpdate):
        
        #check if the author is an admin
        if message.author.id in admins:          
            
            try:
                #don't update the server if it is running.
                if nameSquad in allWindows:
                    log("{0.author} tried to update the Squad server, but it was already running.".format(message))
                    await message.author.send("The Squad server is currently running. Please close it first.")
                    return

                #don't update the server if it is already updating
                if nameSquadUpdate in allWindows:
                    log("{0.author} tried to update the Squad server, but it was already updating.".format(message))
                    await message.author.send("The Squad server is already updating.")
                    return

                #the server is not running and not updating, so it can be updated.
                else:
                    log("{0.author} updated the Squad server.".format(message))
                    await message.author.send("Updating the Squad server. This may take a while depending on the size of the update.")    
                    subprocess.Popen(updateSquad)
                
            except Exception as e:
                log("ERROR: " + str(e))
                return
        
        #User is not an admin, so can't update the server 
        else:
            log("{0.author} tried to update the Squad server, but they were not authorised.".format(message))
            await message.author.send("You cannot update the Squad server. Please ask an admin.")
            return


    #stopping squad server            
    if message.content.startswith(cmdSquadStop):
            
       #Only admins can close the server.        
        if message.author.id in admins:
            
            try:
                #If the window exists, then the server is running.
                if nameSquad in allWindows:                
                    log("{0.author} closed Squad server.".format(message))
                    await message.author.send("Closing the Squad server.")
                    Popen("TASKKILL /F /PIS {pid} /T".format(pid=squadProcess.pid))               

                else:
                    #if the window doesn't exist, then the server is not running
                    log("{0.author} tried to close the Squad server, but it was not running.".format(message))
                    await message.author.send("The Squad server is not running.")
                    return

            except Exception as e:
                log("ERROR: " + str(e))
                return
            
        else:
            #The user is not authorised to close the server.
            log("{0.author} tried to close the Squad server, but they were not authorised.".format(message))
            await message.author.send("You cannot shut down the server. Please ask an admin.")
            return


###############################################################################################################################

    #starting Factorio
    if message.content.startswith(cmdFactorioStart):
        
        #Check if its running first.
        try:

            #If the window exists, then it is already running.
            if nameFactorio in allWindows:                
                log("{0.author} tried to start the Factorio server, but it was already running.".format(message))
                await message.author.send("The Factorio server is already running.")
                return

            #if the window doesn't exist, then the server is not running.
            else:                
                log("{0.author} started the Factorio server.".format(message))
                await message.author.send("Starting Factorio server.")
                factorioProcess = Popen(startFactorio)

        except Exception as e:
            log("ERROR: " + str(e))
            return
            


    #stopping Factorio
    if message.content.startswith(cmdFactorioStop):
        
        #Only admins can close the server
        if message.author.id in admins:

            try:
                
                #if the window exists, then it is running so we can close it.
                if nameFactorio in allWindows:                    
                    log("{0.author} closed the Factorio server.".format(message))
                    await message.author.send("Closing the Factorio server.")
                    Popen("TASKKILL /F /PIS {pid} /T".format(pid=factorioProcess.pid)) 

                #If the window doesn't exist, then the server is not running.
                else:
                    log("{0.author} tried to close the Factorio server, but it was not running.".format(message))
                    await message.author.send("The Factorio server is not running.")
                    return

            except Exception as e:
                log("ERROR: " + str(e))
                return                

        else:
            #User not authorised to close the factorio server
            log("{0.author} tried to close the Factorio server, but they were not authorised.".format(message))
            await message.author.send("You cannot shut down the server. Please ask an admin.")
            return
            

###############################################################################################################################


    #checking running servers
    if message.content.startswith(cmdServers):
        
        log("{0.author} checked the servers.".format(message))
                
        #checks running servers by looking for window titles. same as other checks.

        try:

            #squad running
            if nameSquad in allWindows:
                sqdResponse = "Squad: Running"

            #squad updating
            elif nameSquadUpdate in allWindows:
                sqdResponse = "Squad: Updating"

            #squad not running
            else:
                sqdResponse = "Squad: Not Running"



            #factorio running
            if nameFactorio in allWindows:
                fctResponse = "Factorio: Running"

            #factorio updating
            elif nameSquadUpdate in allWindows:
                fctResponse = "Factorio: Updating"

            #factorio not running
            else:
                fctResponse = "Factorio: Not Running"


        except Exception as e:
            log("ERROR: " + str(e))
            return
            

        msgResponse = fctResponse + "\n" + sqdResponse
        logResponse = fctResponse + ". " + sqdResponse
        log(logResponse)
        await message.author.send(msgResponse)
        
###############################################################################################################################

#Logging function. Writes date, time and given text to file.
def log(text):
    
    now = datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S ")
    with open(fileLog, "a") as log:
        log.write("\n")
        log.write(now)
        log.write(text)        
        log.close()

###############################################################################################################################

def main():
    
    while True:
        try:
            client.loop.run_until_complete(client.run(token))

        except BaseException:

            #Try 5 times to reconnect, if not then close. Will wait 30 seconds between tries to reconnect.
            
            while retryCount<6:
            
                log("Lost connection to Discord, retrying. Attempt {0}.".format(retryCount))           
                time.sleep(30)
                retryCount += 1        
            
        
            log("Tried 5 times to reconnect, giving up.")
            sys.exit()
        
            

if __name__ == "__main__":
    main()
