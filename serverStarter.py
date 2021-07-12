import credentials, config, discord
import pyautogui as pag
import pygetwindow as pgw
from discord.ext import commands
from subprocess import Popen
from datetime import datetime, time




ready = False

bot = commands.Bot(command_prefix=commands.when_mentioned_or(config.prefix))

@bot.event
async def on_ready():
    await afterReady(True)
    


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



class squad(commands.Cog, name="Squad Game Commands"):
    def __init__(self, bot):
        self.bot = bot
    
    

    @commands.command(name="sstart", brief="Starts Squad server")
    async def squadStart(self, ctx):

        allWindows = pgw.getAllTitles()

        if config.nameSquad in allWindows:
            log(f"INFO - squad - {ctx.author} tried to start the Squad server, but it was already running.")
            await ctx.send("Can't start the server, it is already running.")

        elif config.nameSquadUpdate in allWindows:
            log(f"INFO - squad - {ctx.author} tried to start the Squad server, but it was updating.")
            await ctx.send("Can't start the server, it is updating.")
        
        else:
            await ctx.send("Starting the Squad server.")  
            log(f"INFO - squad - {ctx.author} tried to start the Squad server.")
            Popen(config.startSquad)
            log(f"INFO - squad - Squad server started.")
            


    
    @commands.command(name="sstop",  brief="Stops Squad server")
    async def squadStop(self, ctx):

        allWindows = pgw.getAllTitles()

        if config.nameSquadUpdate in allWindows:
            log(f"INFO - squad - {ctx.author} tried to stop the Squad server, but it was updating.")
            await ctx.send("Can't start the Squad server, it is updating.")
        
              
        elif config.nameSquad in allWindows:
            await ctx.send("Stopping the Squad server.")
            log(f"INFO - squad - {ctx.author} tried to stop the Squad server.")
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
        
        allWindows = pgw.getAllTitles()

        if config.nameSquad in allWindows:
            log(f"INFO - squad - {ctx.author} tried to update the Squad server, but it was running.".format(ctx))
            await ctx.send("Can't update the Squad server, it is running.")

        elif config.nameSquadUpdate in allWindows:
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
            textToAppend = f"Admin={adminToAdd}:WhiskeyLancer"
            squadAdminFile = config.squadAdmins
            with open(squadAdminFile, "a") as file:
                file.write(textToAppend)
                file.close()

            log(f"INFO - squad - Added Squad admin {adminToAdd}")
            await ctx.send("Added Squad admin.")
        
        except Exception as e:
            log(f"ERROR - squad - Unable to add {adminToAdd} to admin file. {e}")
            await ctx.send("Failed to add Squad admin.")
        





class factorio(commands.Cog, name="Factorio Game Commands"):
    def __init__(self, bot):
        self.bot = bot

             

    @commands.command(name="fstart", brief = "Starts Factorio server")
    async def factorioStart(self, ctx):

        allWindows = pgw.getAllTitles()

        if config.nameFactorio in allWindows:
            log(f"INFO - factorio - {ctx.author} tried to start the Factorio server, but it was already running.")
            await ctx.send("Can't start the Factorio server, it is already running.")
        
        else:
            await ctx.send("Starting the Factorio server.")
            log(f"INFO - factorio - {ctx.author} tried to start the Factorio server.")            
            Popen(config.startFactorio)
            log(f"INFO - factorio - Started the Factorio server") 
        
    


    @commands.command(name="fstop", brief = "Stops Factorio server")
    async def factorioStop(self, ctx):
        
        allWindows = pgw.getAllTitles()
          
        if config.nameFactorio in allWindows:
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


class servers(commands.Cog, name="Server Info"):
    def __init__(self, bot):
        self.bot = bot
   


    @commands.command(name="servers", brief = "Shows server info")
    async def server(self, ctx):
        
        await ctx.trigger_typing()
        log(f"INFO - servers - {ctx.author} checked server status")
        
        allWindows = pgw.getAllTitles()
        response=""

        #squad running
        if config.nameSquad in allWindows:
            response = response + "Squad: Running\n"

        #squad updating
        elif config.nameSquadUpdate in allWindows:
            response = response + "Squad: Updating\n"

        #squad not running
        else:
            response = response + "Squad: Not Running\n"
        

        #factorio running
        if config.nameFactorio in allWindows:
            response = response + "Factorio: Running\n"

        #factorio not running
        else:
            response = response + "Factorio: Not Running\n"    

        
        log(F"INFO - servers - {response}")
        await ctx.send(response)


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



bot.add_cog(servers(bot))
bot.add_cog(squad(bot))
#bot.add_cog(factorio(bot))


bot.run(credentials.liveToken)
