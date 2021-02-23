""" 
Server Starter bot.
A custom bot for managing servers on a private home server.
Created by Big Spender#7291
v7 updated 23/02/2021
"""

import discord
import subprocess
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
version = "v6 18/02/2021"
updateSquad = [r"C:\steamcmd\squad_installandupdateBot.bat"]
startSquad = [r"C:\servers\squad_server\StartSquadServer.bat"]
startFactorio = [r"C:\servers\factorio_server\factorio_headless_x64_1.1.19\factorio\StartFactorioServer.bat"]
nameFactorio = "StartFactorioServer"
nameSquad = "C:\\servers\\squad_server\\SquadGame\\Binaries\\Win64\\SquadGameServer.exe"
fileLog = "log.txt"
fileAdmins = "admins.txt"
cmdSquadStart = "!squadstart"
cmdSquadUpdate = "!squadupdate"
cmdSquadQuit = "!squadstop"
cmdFactorioStart = "!factoriostart"
cmdFactorioQuit = "!factoriostop"
cmdHelp = "!help"
cmdCommand = "!"
cmdServers = "!servers"
retryCount = 1


pubMsg = """```
!help
    Shows this message
!servers
    Shows the running servers
!squadstart
    Starts the Squad server
!factoriostart
    Starts the Factorio server
``` """


adminMsg = """```
!help
    Shows this message
!servers
    Shows the running servers
        
!squadupdate
    Updates the Squad server
!squadstart
    Starts the Squad server
!squadstop
    Closes the Squad server
!factoriostart
    Starts the Factorio server
!factoriostop
    Closes the Factorio server
    ``` """


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

    #Reply with DM if not a DM. Only responds to commands.
    if guild:
        if message.content.startswith(cmdCommand):
            log("Public message from {0.author}. {0.content}.".format(message))

            #Admins gets unique options.
            if message.author.id in admins:
                await message.author.send(adminMsg)
                
            else:
                await message.author.send(pubMsg)
                

    
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
            
        

    if message.content.startswith(cmdSquadStart):
        
        try:
            #don't start the server if it is already running
            sqdSrv = pgw.getWindowsWithTitle(nameSquad)[0]            
            log("{0.author} tried to start the Squad server, but it was already running.".format(message))
            await message.author.send("The Squad server is already running.")

        except IndexError:      
            #if the server window doesn't exist, then it is not running so we can start it.
            log("{0.author} started the Squad server.".format(message))            
            await message.author.send("Starting the Squad server.")    
            subprocess.Popen(startSquad)
            
        except Exception as e:
            log(e)
            return

    if message.content.startswith(cmdSquadUpdate):
        
        #check if the author is an admin
        if message.author.id in admins:          
            
            try:
                #if the window does exist, then the server is still running so can't update it.
                sqdSrv = pgw.getWindowsWithTitle(nameSquad)[0]
                log("{0.author} tried to update the Squad server, but it was already running.".format(message))
                await message.author.send("The Squad server is currently running. Please close it first.")
                return
                
            except IndexError:
                #if the window doesn't exist then it is not running, so we can update it.
                log("{0.author} updated the Squad server.".format(message))
                await message.author.send("Updating the Squad server. This may take a while depending on the size of the update.")    
                subprocess.Popen(updateSquad)
                
            except Exception as e:
                log(e)
                return
        
        #User is not an admin, so can't update the server 
        else:
            log("{0.author} tried to update the Squad server.".format(message))
            await message.author.send("You cannot update the Squad server. Please ask an admin.")

            
    if message.content.startswith(cmdSquadQuit):
            
       #Only admins can close the server.        
        if message.author.id in admins:
            
            try:
                #If the window exists, then the server is running.
                sqdSrv = pgw.getWindowsWithTitle(nameSquad)[0]                
                log("{0.author} closed Squad server.".format(message))
                await message.author.send("Closing the Squad server.")
                
                sqdSrv = pgw.getWindowsWithTitle(nameSquad)[0]
                sqdSrv.restore()
                sqdSrv.activate()
                time.sleep(5)
                pag.hotkey('ctrl', 'c')
                
                
            except IndexError:
                #if the window doesn't exist, then the server is not running
                log("{0.author} tried to close the Squad server, but it was not running.".format(message))
                await message.author.send("The Squad server is not running.")

            except Exception as e:
                log(e)
                return
            
        else:
            #The user is not authorised to close the server.
            log("{0.author} tried to close the Squad server, but they were not authorised.".format(message))
            await message.author.send("You cannot shut down the server. Please ask an admin.")
            


    if message.content.startswith(cmdFactorioStart):
        
        #Check if its running first.
        try:
            #If the window exists, then it is already running.
            fctSrv = pgw.getWindowsWithTitle(nameFactorio)[0]
            log("{0.author} tried to start the Factorio server, but it was already running.".format(message))
            await message.author.send("The Factorio server is already running.")
            
        
        except IndexError:
            #if the window doesn't exist, then the server is not running.
            log("{0.author} started the Factorio server.".format(message))
            await message.author.send("Starting Factorio server.")    
            subprocess.Popen(startFactorio)

        except Exception as e:
            log(e)
            return
            



    if message.content.startswith(cmdFactorioQuit):
        
        #Only admins can close the server
        if message.author.id in admins:

            try:
                #if the window exists, then it is running so we can close it.
                fctSrv = pgw.getWindowsWithTitle(nameFactorio)[0]
                log("{0.author} closed the Factorio server.".format(message))
                await message.author.send("Closing the Factorio server.")
                
                fctSrv.restore()
                fctSrv.activate()
                time.sleep(5)
                pag.hotkey('ctrl', 'c')
                time.sleep(15)
                pag.write('y')
                pag.press('enter')
                
                
            except IndexError:
                #If the window doesn't exist, then the server is not running.
                log("{0.author} tried to close the Factorio server, but it was not running.".format(message))
                await message.author.send("The Factorio server is not running.")

            except Exception as e:
                log(e)
                return
                

        else:
            #User not authorised to close the factorio server
            log("{0.author} tried to close the Factorio server, but they were not authorised.".format(message))
            await message.author.send("You cannot shut down the server. Please ask an admin.")
            


    if message.content.startswith(cmdServers):
        
        log("{0.author} checked the servers.".format(message))
                
        #checks running servers by looking for window titles. same as other checks.

        #checking factorio
        try:
            fctSrv = pgw.getWindowsWithTitle(nameFactorio)[0]
            #fctSrv = True
            fctResponse = "Factorio: Running \n"
            
        except IndexError:
            fctSrv = False
            fctResponse = "Factorio: Not running \n"

        except Exception as e:
                log(e)
                return
            
        #checking squad
        try:            
            sqdSrv = pgw.getWindowsWithTitle(nameSquad)[0]
            sqdSrv = True
            sqdResponse = "Squad: Running \n"
            
            
        except IndexError:
            sqdSrv = False
            sqdResponse = "Squad: Not running \n"

        except Exception as e:
                log.write(e)
                return
            

        response = fctResponse + sqdResponse
        log(response)
        await message.author.send(response)
        


#Logging function. Writes date, time and given text to file.
def log(text):
    
    now = datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S ")
    with open(fileLog, "a") as log:
        log.write(now)
        log.write(text)
        log.write("\n")
        log.close()



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
