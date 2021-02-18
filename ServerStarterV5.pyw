## BigSpender's Discord bot
##
## v5 updated 16/02/2021

##TODO
##
## [ ] Add way to close bot
## [X] Add way to see running servers


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

from DiscordToken import MyBotToken

client = discord.Client()
version = "v5 16/02/2021"
longBS = 195617048569708545 #int
longJS = 178958435612622848
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
cmdAdminAdd = "!adminadd"
cmdAdminRemove = "!adminremove"
cmdServers = "!servers"
cmdBotStop = "!botstop"

#BigSpender and JamSandwich
#admins = [195617048569708545, 178958435612622848]

#Get admins from file.
with open (fileAdmins, 'r') as file:
    admins = file.read()

    file.close()

    #takes admins from file and converts to ints, as message.author.id is an int.
    admins = admins.split()
    admins = list(map(int, admins))
    
    now = datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S ")
    log = open(fileLog, "a")
    log.write(now)
    log.write("Loaded admins from file. \n")
    log.close()



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
    
    now = datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S ")
    log = open(fileLog, "a")
    log.write(now)
    log.write("Logged on as {0.user} {1}. \n".format(client, version))
    log.close()
    



@client.event
async def on_message(message):

    
    #skip reading message if not a command
    if not message.content.startswith(cmdCommand):
        return

    now = datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S ")
    log = open(fileLog, "a")
    guild = message.guild

    #Reply with DM if not a DM. Only responds to commands.
    if guild:
        if message.content.startswith(cmdCommand):
            log.write(now)
            log.write("Public message from {0.author}. {0.content}. \n".format(message))

            #Big Spender gets unique options.
            if message.author.id in admins:
                await message.author.send(adminMsg)
                
            else:
                await message.author.send(pubMsg)
                

    
    #skip reading message if its from the bot.
    if message.author == client.user:        
        log.write(now)
        log.write("Message from myself!? \n")
        log.close()
        return
    
    
    if message.content.startswith(cmdHelp):
        log.write(now)
        log.write("{0.author} asked for help in channel {0.channel}. \n".format(message))
        log.close()

        #send pub message to pubs and admin message to admins
        if message.author.id in admins:
            await message.author.send(adminMsg)
            
        else:
            await message.author.send(pubMsg)
            
        

    if message.content.startswith(cmdSquadStart):
        
        try:
            #don't start the server if it is already running
            sqdSrv = pgw.getWindowsWithTitle(nameSquad)[0]
            log.write(now)
            log.write("{0.author} tried to start the Squad server, but it was already running. \n".format(message))
            log.close()
            await message.author.send("The Squad server is already running.")

        except IndexError:      
            #if the server window doesn't exist, then it is not running so we can start it.
            log.write(now)
            log.write("{0.author} started the Squad server. \n".format(message))
            log.close()
            await message.author.send("Starting the Squad server.")    
            subprocess.Popen(startSquad)
            
        except Exception as e:
            log.write(now)
            log.write(e + "\n")
            return

    if message.content.startswith(cmdSquadUpdate):
        
        if message.author.id in admins:          
            
            try:
                #if the window does exist, then the server is still running so can't update it.
                sqdSrv = pgw.getWindowsWithTitle(nameSquad)[0]
                log.write(now)
                log.write("{0.author} tried to update the Squad server, but it was already running. \n".format(message))
                log.close()
                await message.author.send("The Squad server is currently running. Please close it first.")
                return
                
            except IndexError:
                #if the window doesn't exist then it is not running so we can update it.
                log.write(now)
                log.write("{0.author} updated the Squad server. \n".format(message))
                log.close()
                await message.author.send("Updating the Squad server. This may take a while depending on the size of the update.")    
                subprocess.Popen(updateSquad)
                
            except Exception as e:
                log.write(now)
                log.write(e + "\n")
                return
            
        else:
            #Only admins can update the server.
            log.write(now)
            log.write("{0.author} tried to update the Squad server. \n".format(message))
            log.close()
            await message.author.send("You cannot update the Squad server. Please ask an admin.")

            
    if message.content.startswith(cmdSquadQuit):
            
       #Only admins can close the server.        
        if message.author.id in admins:
            
            try:
                #If the window exists, then the server is running.
                sqdSrv = pgw.getWindowsWithTitle(nameSquad)[0]                
                log.write(now)
                log.write("{0.author} closed Squad server. \n".format(message))
                log.close()
                await message.author.send("Closing the Squad server.")
                sqdSrv = pgw.getWindowsWithTitle(nameSquad)[0]
                sqdSrv.restore()
                sqdSrv.activate()
                time.sleep(5)
                pag.hotkey('ctrl', 'c')
                
                
            except IndexError:
                #if the window doesn't exist, then the server is not running
                log.write(now)
                log.write("{0.author} tried to close the Squad server, but it was not running. \n".format(message))
                log.close()
                await message.author.send("The Squad server is not running.")

            except Exception as e:
                log.write(now)
                log.write(e + "\n")
                return
            
        else:
            #The user is not authorised to close the server.
            log.write(now)
            log.write("{0.author} tried to close the Squad server, but they were not authorised. \n".format(message))
            log.close()
            await message.author.send("You cannot shut down the server. Please ask an admin.")
            


    if message.content.startswith(cmdFactorioStart):
        
        #Check if its running first.
        try:
            #If the window exists, then it is already running.
            fctSrv = pgw.getWindowsWithTitle(nameFactorio)[0]
            log.write(now)
            log.write("{0.author} tried to start the Factorio server, but it was already running. \n".format(message))
            log.close()
            await message.author.send("The Factorio server is already running.")
            return
        
        except IndexError:
            #if the window doesn't exist, then the server is not running.
            log.write(now)
            log.write("{0.author} started the Factorio server. \n".format(message))
            log.close()
            await message.author.send("Starting Factorio server.")    
            subprocess.Popen(startFactorio)

        except Exception as e:
            log.write(now)
            log.write(e + "\n")
            return
            



    if message.content.startswith(cmdFactorioQuit):
        
        #Only admins can close the server
        if message.author.id in admins:

            try:
                #if the window exists, then it is running so we can close it.
                fctSrv = pgw.getWindowsWithTitle(nameFactorio)[0]
                log.write(now)
                log.write("{0.author} closed the Factorio server. \n.".format(message))
                log.close()
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
                log.write(now)
                log.write("{0.author} tried to close the Factorio server, but it was not running. \n".format(message))
                log.close()
                await message.author.send("The Factorio server is not running.")

            except Exception as e:
                log.write(now)
                log.write(e + "\n")
                return
                

        else:
            #User not authorised to close the factorio server
            log.write(now)
            log.write("{0.author} tried to close the Factorio server, but they were not authorised. \n".format(message))
            log.close()
            await message.author.send("You cannot shut down the server. Please ask an admin.")
            


    if message.content.startswith(cmdServers):
        
        log.write(now)
        log.write("{0.author} checked the servers. \n".format(message))

        #checks running servers by looking for window titles. same as other checks.

        #checking factorio
        try:
            fctSrv = pgw.getWindowsWithTitle(nameFactorio)[0]
            fctSrv = True
            
            
        except IndexError:
            fctSrv = False

        except Exception as e:
                log.write(now)
                log.write(e + "\n")
                return
            
        #checking squad
        try:            
            sqdSrv = pgw.getWindowsWithTitle(nameSquad)[0]
            sqdSrv = True
            
            
        except IndexError:
            sqdSrv = False

        except Exception as e:
                log.write(now)
                log.write(e + "\n")
                return
            
        
        #replying with server status
        if (fctSrv == True) and (sqdSrv == True):
            log.write(now)
            log.write("Both the Factorio and Squad server is running. \n")
            log.close()
            await message.author.send("Both the Factorio and Squad server is running.")
            

        elif fctSrv == True:
            log.write(now)
            log.write("The Factorio server is running. \n")
            log.close()
            await message.author.send("The Factorio server is running.")
            

        elif sqdSrv == True:
            log.write(now)
            log.write("The Squad server is running. \n")
            log.close()
            await message.author.send("The Squad server is running.")
            
        else:
            log.write(now)
            log.write("No servers running. \n")
            log.close()
            await message.author.send("No servers running.")
            
            

##    if message.content.startswith(cmdBotStop):
##        
##        #only admins can stop the bot
##        if message.author.id in admins:
##            
##            log.write(now)
##            log.write("{0.author} stopped the bot. \n".format(message))
##            log.close()
##
##            await message.author.send("Goodbye.")
##            
##            sys.exit()
##            
##
##        else:
##            log.write(now)
##            log.write("{0.user} tried to stop the bot, but they were not authorised \n".format(message))
##            log.close()
##            await message.author.send("You are not authorised to stop the bot.")
##
##
##        

##    if message.content.startswith(cmdAdminAdd):
##
##        #only admins can add another admin
##        if message.author.id in admins:
##            try:
##                #(message.content)
##                #get new admin ID from message. needs to be format !adminadd xxxxx
##                newAdmin = message.content.split()[1]
##                #print(newAdmin)               
##
##                with open('admins.txt', 'a') as file:
##                    file.write("\n" + newAdmin)
##                    file.close()
##
##                log.write(now)
##                log.write("{0.author} added a new admin {1}. \n".format(message, newAdmin))
##                
##            except Exception as e:
##                print (e)
##                return
##            
##        else:
##            #print("{0.author} is not an admin.".format(message))
##            log.write(now)
##            log.write("{0.author} tried to add an admin, but they are not an admind themselves. \n".format(message))


            
##    if message.content.startswith(cmdAdminRemove):
##
##        #only admins can add another admin
##        if message.author.id in admins:
##           
##            try:
##                #print(message.content)
##                #get removed admin ID from message. needs to be format !adminremove xxxxx.
##                #need to convert to int as admins is a list of ints. message.author.id is an int.
##                
##                remAdmin = message.content.split()[1]
##                remAdmin = int(remAdmin, 10)
##                print("Removed Admin")
##                print(remAdmin)
##                
##
##                
##                #can only remove an admin if they are already an admin!
##                if remAdmin in admins:
##                    
##                    #remove it
##                    
##                    newAdmins = admins
##                    print(newAdmins)
##                    newAdmins = newAdmins.remove(remAdmin)
##                    
##                    print("New Admins")
##                    print(newAdmins)
##
##                    
##                else:
##                    print("remAdmin is not an admin")
##                
##                
##                
##                
##            except Exception as e:
##                print (e)
##                return
##        else:
##            print("Not an admin")
     


while True:
    try:
        client.loop.run_until_complete(client.run(MyBotToken))

    except BaseException:

        #Try 5 times to reconnect, if not then close. Will wait 30 seconds between tries to reconnect.
        count = 0
        while count<5:
            
            log = open(fileLog, "a")
            now = datetime.now()
            now = now.strftime("%Y-%m-%d %H:%M:%S ")
            log.write(now)
            log.write("Lost connection to Discord, retrying. \n")
            log.close()
            time.sleep(30)
            count += 1        
            
        log = open(fileLog, "a")
        now = datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S ")
        log.write(now)
        log.write("Tried 5 times to reconnect, giving up. \n")
        log.close()
        sys.exit()
        
            

    
