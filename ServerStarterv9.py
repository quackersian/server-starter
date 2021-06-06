""" 
Server Starter bot.
A custom bot for managing servers on a private home server.
Created by Big Spender#7291
v9 updated 06/06/2021
"""

from os import name, read
import discord
from discord.ext import commands
from subprocess import Popen
import time
import sys
from discord.ext.commands.core import command
import pyautogui as pag
import pygetwindow as pgw
from datetime import datetime

import pyautogui as pag
import pygetwindow as pgw
from datetime import datetime
from credentials import token
import config #import cmdPrefix, fileLog, nameSquad, nameSquadUpdate, startSquad


ready = False

bot = commands.Bot(command_prefix = config.cmdPrefix)

@bot.event
async def on_ready():
    await afterReady(True)
    


@bot.event
async def afterReady(ready=False):
    
    if ready == True:
        

        log("--------------")
        log("Logged in as: {}".format(bot.user))
        log("Discord Version: {}".format(discord.__version__))
        log("Prefix: {}".format(config.cmdPrefix))

        log("Connected to following servers:")
        for guild in bot.guilds:
            log("- " + guild.name + " " + str(guild.id))
            
        game = discord.Game("{}help".format(config.cmdPrefix))
        await bot.change_presence(status=discord.Status.online, activity=game)
        
        log("Status changed to \"Playing {}help\"".format(config.cmdPrefix))
    


class squad(commands.Cog, name="Squad Game Commands"):
    def __init__(self, bot):
        self.bot = bot

    def log(text):
        try:            
            now = datetime.now()
            now = now.strftime("%Y-%m-%d %H:%M:%S ")
            with open(config.fileLog, "a") as file:
                file.write("\n")
                file.write(now)
                file.write(text)        
                file.close()            
            
        except Exception as e:
            print("ERROR: " + str(e))
            return     
    

    @commands.command(name="squadstart", brief="Starts Squad server")
    async def squadStart(self, ctx):

        allWindows = pgw.getAllTitles()

        if config.nameSquad in allWindows:
            log("{0.author} tried to start the Squad server, but it was already running.".format(ctx))
            await ctx.send("Can't start the server, it is already running.")

        elif config.nameSquadUpdate in allWindows:
            log("{0.author} tried to start the Squad server, but it was updating.".format(ctx))
            await ctx.send("Can't start the server, it is updating.")
        
        else:
            log("{0.author} started the Squad server.".format(ctx))
            await ctx.send("Starting the Squad server.")    
            Popen(config.startSquad)
            


    
    @commands.command(name="squadstop",  brief="Stops Squad server")
    async def squadStop(self, ctx):

        allWindows = pgw.getAllTitles()

        if config.nameSquadUpdate in allWindows:
            log("{0.author} tried to stop the Squad server, but it was updating.".format(ctx))
            await ctx.send("Can't start the Squad server, it is updating.")
        
              
        elif config.nameSquad in allWindows:
            log("{0.author}stopped the Squad server.".format(ctx))
            await ctx.send("Stopping the Squad server.")
            sqdSrv = pgw.getWindowsWithTitle(config.nameSquad)[0]
            sqdSrv.restore()
            sqdSrv.activate()
            time.sleep(5)
            pag.hotkey('ctrl', 'c')

        else:
            log("{0.author} tried to stop the Squad server, but it was not running.".format(ctx))
            await ctx.send("Can't stop the Squad server, it is not running.")    
            
    


    @commands.command(name="squadupdate", brief="Updates Squad server")
    async def squadUpdate(self, ctx):
        
        allWindows = pgw.getAllTitles()

        if config.nameSquad in allWindows:
            log("{0.author} tried to update the Squad server, but it was running.".format(ctx))
            await ctx.send("Can't update the Squad server, it is running.")

        elif config.nameSquadUpdate in allWindows:
            log("{0.author} tried to update the Squad server, but it was already updating.".format(ctx))
            await ctx.send("Can't update the Squad server, it is already updating.")
        
        else:
            log("{0.author} updated the Squad server.".format(ctx))
            await ctx.send("Updating the Squad server.")    
            Popen(config.updateSquad)



class factorio(commands.Cog, name="Factorio Game Commands"):
    def __init__(self, bot):
        self.bot = bot

    def log(text):
        try:            
            now = datetime.now()
            now = now.strftime("%Y-%m-%d %H:%M:%S ")
            with open(config.fileLog, "a") as file:
                file.write("\n")
                file.write(now)
                file.write(text)        
                file.close()            
            
        except Exception as e:
            print("ERROR: " + str(e))
            return 
              

    @commands.command(name="factoriostart", brief = "Starts Factorio server")
    async def factorioStart(self, ctx):

        allWindows = pgw.getAllTitles()

        if config.nameFactorio in allWindows:
            log("{0.author} tried to start the Factorio server, but it was already running.".format(ctx))
            await ctx.send("Can't start the Factorio server, it is already running.")
        
        else:
            log("{0.author} started the Factorio server.".format(ctx))
            await ctx.send("Starting the Factorio server.")    
            Popen(config.startFactorio)
        
    


    @commands.command(name="factoriostop", brief = "Stops Factorio server")
    async def factorioStop(self, ctx):
        
        allWindows = pgw.getAllTitles()

          
        if config.nameFactorio in allWindows:
            log("{0.author}stopped the Squad server.".format(ctx))
            await ctx.send("Stopping the Squad server.")
            fctSrv = pgw.getWindowsWithTitle(config.nameFactorio)[0]
            fctSrv.restore()
            fctSrv.activate()
            time.sleep(5)
            pag.hotkey('ctrl', 'c')
            time.sleep(15)
            pag.write('y')
            pag.press('enter')

        else:
            log("{0.author} tried to stop the Factorio server, but it was not running.".format(ctx))
            await ctx.send("Can't stop the Factorio server, it is not running.")  


class servers(commands.Cog, name="Server Info"):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="servers", brief = "Shows server info")
    async def server(self, ctx):
        allWindows = pgw.getAllTitles()

        #squad running
        if config.nameSquad in allWindows:
            sqdResponse = "Squad: Running"

        #squad updating
        elif config.nameSquadUpdate in allWindows:
            sqdResponse = "Squad: Updating"

        #squad not running
        else:
            sqdResponse = "Squad: Not Running"
        

        #factorio running
        if config.nameFactorio in allWindows:
            fctResponse = "Factorio: Running"

        #factorio not running
        else:
            fctResponse = "Factorio: Not Running"
    

        msgResponse = fctResponse + "\n" + sqdResponse
        logResponse = fctResponse + ". " + sqdResponse
        log("{0.author} checked server status".format(ctx))
        log(logResponse)
        await ctx.send(msgResponse)



def log(text):
    try:
        
        now = datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S ")
        with open(config.fileLog, "a") as file:
            file.write("\n")
            file.write(now)
            file.write(text)        
            file.close()
        
        
    except Exception as e:
        print("ERROR: " + str(e))
        return


bot.add_cog(servers(bot))
bot.add_cog(squad(bot))
bot.add_cog(factorio(bot))


bot.run(token)
