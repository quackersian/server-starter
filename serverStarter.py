from discord.ext.commands.core import command
import credentials, config, discord, urllib, json
import pyautogui as pag
import pygetwindow as pgw
from discord.ext import commands
from subprocess import Popen
from datetime import datetime, time

bot = commands.Bot(command_prefix=commands.when_mentioned_or(config.prefix))


####################################################################################################

@bot.event
async def on_ready():
    await afterReady(True)
    
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, command.CommandNotFound):
        return

@bot.event
async def afterReady(ready=False):
    now = datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S")

    if ready == True:               
        log("--------------")
        log(f"INFO - afterReady - Logged in as: {bot.user}")
        log(f"INFO - afterReady - ID: {bot.user.id}")
        log(f"INFO - afterReady - Bot Name: {config.botName}")
        log(f"INFO - afterReady - Discord Version: {discord.__version__}")
        log(f"INFO - afterReady - Script Version: {config.scriptVersion}")
        log(f"INFO - afterReady - Prefix: {config.prefix}")

        log("INFO - afterReady - Connected to following servers:")
        for guild in bot.guilds:
            log(f"INFO - afterReady - {guild.name},  {guild.id}")

        
        game = discord.Game(F"{config.prefix}help")
        await bot.change_presence(status=discord.Status.online, activity=game)
        
        log(f"INFO - afterReady - Status changed to \"Playing {config.prefix}help\"")
        print(f"{now} INFO - afterReady - {config.botName} ready.")
    
    else:
        log(f"{now} ERROR - afterReady - afterReady called before being ready")
        return

####################################################################################################

class squad(commands.Cog, name="Squad"):
    def __init__(self, bot):
        self.bot = bot
 
    
    @commands.command(name="sstart", brief="Starts Squad server")
    async def squadStart(self, ctx):

        if self.squadStatus == "server":
            log(f"INFO - squad - {ctx.author} tried to start the Squad server, but it was already running.")
            await ctx.send("Can't start the server, it is already running.")

        elif self.squadStatus == "update":
            log(f"INFO - squad - {ctx.author} tried to start the Squad server, but it was updating.")
            await ctx.send("Can't start the server, it is updating.")
        
        else:
            await ctx.send("Starting the Squad server.")  
            log(f"INFO - squad - {ctx.author} tried to start the Squad server.")
            Popen(config.startSquad)
            log(f"INFO - squad - Squad server started.")
   


    
    @commands.command(name="sstop",  brief="Stops Squad server")
    async def squadStop(self, ctx):

        if self.squadStatus == "update":
            log(f"INFO - squad - {ctx.author} tried to stop the Squad server, but it was updating.")
            await ctx.send("Can't start the Squad server, it is updating.")
        
              
        elif self.squadStatus == "server":
            log(f"INFO - squad - {ctx.author} tried to stop the Squad server.")
            await ctx.send("Stopping the Squad server.")
            sqdSrv = pgw.getWindowsWithTitle(config.nameSquad)[0]
            sqdSrv.restore()
            sqdSrv.activate()
            time.sleep(5)
            pag.hotkey('ctrl', 'c')
            log(f"INFO - squad - Squad server stopped.")
            

        else:
            log(f"INFO - squad - {ctx.author} tried to stop the Squad server, but it was not running.")
            await ctx.send("Can't stop the Squad server, it is not running.")    
            
    


    @commands.command(name="supdate", brief="Updates Squad server")
    async def squadUpdate(self, ctx):
        
        if self.squadStatus == "server":
            log(f"INFO - squad - {ctx.author} tried to update the Squad server, but it was running.".format(ctx))
            await ctx.send("Can't update the Squad server, it is running.")

        elif self.squadStatus == "update":
            log(f"INFO - squad - {ctx.author} tried to update the Squad server, but it was already updating.")
            await ctx.send("Can't update the Squad server, it is already updating.")
        
        else:
            log(f"INFO - squad - {ctx.author} updated the Squad server.")
            await ctx.send("Updating the Squad server.")    
            Popen(config.updateSquad)



    @commands.command(name="sadmin", brief="Add an admin to the squad server", help=f"Adds an admin to the squad server admin. Usage: {config.prefix}sadmin <steam64ID>")
    async def squadAddAdmin(self, ctx, adminToAdd):

        log(f"INFO - squad - {ctx.author} tried to add a new Squad admin, {adminToAdd}")
        
        await ctx.trigger_typing()
        try:
            
            playerName = str(getSteamInfo(adminToAdd))

            if playerName == "fail":
                log(f"WARNING - squadAddAdmin - playerName failed")
                await ctx.send("Unable to add Squad admin")
                return


            appendText1 = f"""//{playerName}\n"""
            appendText2 = f"Admin={adminToAdd}:WhiskeyLancer\n"

            squadAdminFile = config.squadAdmins
            with open(squadAdminFile, "a") as file:
                file.write(appendText1)
                file.write(appendText2)
                file.close()          
            


            log(f"INFO - squad - Added Squad admin {adminToAdd}, {playerName}")
            await ctx.send(f"Added Squad admin {playerName}.")
        
        except Exception as e:
            log(f"ERROR - squad - Unable to add {adminToAdd} to admin file. {e}")
            await ctx.send("Failed to add Squad admin.")


    def squadStatus(self, ctx):
        allWindows = pgw.getAllTitles()
        if config.nameSquad in allWindows:
            return "server"
        if config.nameSquadUpdate in allWindows:
            return "update"
        else:
            return None    



####################################################################################################

class factorio(commands.Cog, name="Factorio"):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="fstart", brief = "Starts Factorio server")
    async def factorioStart(self, ctx):

        if self.factorioStatus == "server":
            log(f"INFO - factorio - {ctx.author} tried to start the Factorio server, but it was already running.")
            await ctx.send("Can't start the Factorio server, it is already running.")
        
        else:
            await ctx.send("Starting the Factorio server.")
            log(f"INFO - factorio - {ctx.author} tried to start the Factorio server.")            
            Popen(config.startFactorio)
            log(f"INFO - factorio - Started the Factorio server") 
        
    


    @commands.command(name="fstop", brief = "Stops Factorio server")
    async def factorioStop(self, ctx):
          
        if self.factorioStatus == "server":
            log(f"INFO - factorio - {ctx.author} tried to stop the Factorio server")  
            await ctx.send("Stopping the Factorio server.")                      
            fctSrv = pgw.getWindowsWithTitle(config.nameFactorio)[0]
            fctSrv.restore()
            fctSrv.activate()
            time.sleep(5)
            pag.hotkey('ctrl', 'c')
            time.sleep(15)
            pag.write('y')
            pag.press('enter')
            log("INFO - factorio - Factorio server stopped.")

        else:
            log(f"INFO - factorio - {ctx.author} tried to stop the Factorio server, but it was not running.")
            await ctx.send("Can't stop the Factorio server, it is not running.")  



    def factorioStatus(self, ctx):
        allWindows = pgw.getAllTitles()
        if config.nameFactorio in allWindows:
            return "server"
        else:
            return None 


####################################################################################################

class servers(commands.Cog, name="Server Info"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="servers", brief = "Shows server info")
    async def server(self, ctx):
        count = 0
        await ctx.trigger_typing()
        log(f"INFO - servers - {ctx.author} checked server status")

        allWindows = pgw.getAllTitles()

        listOfCogs = bot.cogs

        for nameOfCog, classOfCog in listOfCogs.items():
            if nameOfCog == "Server Info":
                continue
            if nameOfCog in allWindows:
                await ctx.send(f"{nameOfCog} server is running.")
                count += 1
        
        if count == 0:
            await ctx.send("No game servers running.")
                
            
####################################################################################################

def getSteamInfo(steam64ID=None):

    if steam64ID is None:
        log(f"WARNING - getSteamInfo - No Steam64ID provided")
        return "fail"
    

    else:
        steamUrl=f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={credentials.steamToken}&steamids={steam64ID}"
        with urllib.request.urlopen(steamUrl) as url:
            
            data = json.loads(url.read().decode())
            if data is not None:
                
                playerName = data['response']['players'][-1]['personaname']                
                log(f"INFO - getSteamInfo - retrieved {playerName} from API")
                return playerName


            else:
                log(f"ERROR - getSteamInfo - no data returned from Valve API")
                return "fail"




def log(text):
        try:
            
            now = datetime.now()
            now = now.strftime("%Y-%m-%d %H:%M:%S ")
            with open(config.fileLog, "a", encoding="utf-8") as file:
                file.write("\n")
                file.write(now)
                file.write(text)        
                file.close()        
        
        except Exception as e:
            print(f"{now}ERROR - log - Unable to add to log. {e}")
            return

####################################################################################################

bot.add_cog(servers(bot))
bot.add_cog(squad(bot))
#bot.add_cog(factorio(bot))


bot.run(credentials.testToken)
