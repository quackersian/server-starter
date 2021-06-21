from discord.ext import commands
from subprocess import Popen
from datetime import datetime, time
import pyautogui as pag
import pygetwindow as pgw
import credentials, config, discord


ready = False

bot = commands.Bot(command_prefix = config.cmdPrefix)

@bot.event
async def on_ready():
    await afterReady(True)
    


@bot.event
async def afterReady(ready=False):
    
    if ready == True:       

        log("--------------")
        log(f"Logged in as: {bot.user}")
        log(f"Discord Version: {discord.__version__}")
        log(f"Prefix: {config.cmdPrefix}")

        log("Connected to following servers:")
        for guild in bot.guilds:
            log("- " + guild.name + " - discord.com/channels/" + str(guild.id))

        #sets bot's status to "Playing !help" where ! is prefix
        game = discord.Game(F"{config.cmdPrefix}help")
        await bot.change_presence(status=discord.Status.online, activity=game)
        
        log(f"Status changed to \"Playing {config.cmdPrefix}help\"")
    
    else:
        log("afterReady called before being ready")
        return



class squad(commands.Cog, name="Squad Game Commands"):
    def __init__(self, bot):
        self.bot = bot
    
    

    @commands.command(name="squadstart", brief="Starts Squad server")
    async def squadStart(self, ctx):

        allWindows = pgw.getAllTitles()

        if config.nameSquad in allWindows:
            log(f"{ctx.author} tried to start the Squad server, but it was already running.")
            await ctx.send("Can't start the server, it is already running.")

        elif config.nameSquadUpdate in allWindows:
            log(f"{ctx.author} tried to start the Squad server, but it was updating.")
            await ctx.send("Can't start the server, it is updating.")
        
        else:
            log(f"{ctx.author} started the Squad server.")
            await ctx.send("Starting the Squad server.")    
            Popen(config.startSquad)
            


    
    @commands.command(name="squadstop",  brief="Stops Squad server")
    async def squadStop(self, ctx):

        allWindows = pgw.getAllTitles()

        if config.nameSquadUpdate in allWindows:
            log(f"{ctx.author} tried to stop the Squad server, but it was updating.")
            await ctx.send("Can't start the Squad server, it is updating.")
        
              
        elif config.nameSquad in allWindows:
            log(f"{ctx.author}stopped the Squad server.")
            await ctx.send("Stopping the Squad server.")
            sqdSrv = pgw.getWindowsWithTitle(config.nameSquad)[0]
            sqdSrv.restore()
            sqdSrv.activate()
            time.sleep(5)
            pag.hotkey('ctrl', 'c')

        else:
            log(f"{ctx.author} tried to stop the Squad server, but it was not running.")
            await ctx.send("Can't stop the Squad server, it is not running.")    
            
    


    @commands.command(name="squadupdate", brief="Updates Squad server")
    async def squadUpdate(self, ctx):
        
        allWindows = pgw.getAllTitles()

        if config.nameSquad in allWindows:
            log(f"{ctx.author} tried to update the Squad server, but it was running.".format(ctx))
            await ctx.send("Can't update the Squad server, it is running.")

        elif config.nameSquadUpdate in allWindows:
            log(f"{ctx.author} tried to update the Squad server, but it was already updating.")
            await ctx.send("Can't update the Squad server, it is already updating.")
        
        else:
            log(f"{ctx.author} updated the Squad server.")
            await ctx.send("Updating the Squad server.")    
            Popen(config.updateSquad)



class factorio(commands.Cog, name="Factorio Game Commands"):
    def __init__(self, bot):
        self.bot = bot

             

    @commands.command(name="factoriostart", brief = "Starts Factorio server")
    async def factorioStart(self, ctx):

        allWindows = pgw.getAllTitles()

        if config.nameFactorio in allWindows:
            log(f"{ctx.author} tried to start the Factorio server, but it was already running.")
            await ctx.send("Can't start the Factorio server, it is already running.")
        
        else:
            log(f"{ctx.author} started the Factorio server.")
            await ctx.send("Starting the Factorio server.")    
            Popen(config.startFactorio)
        
    


    @commands.command(name="factoriostop", brief = "Stops Factorio server")
    async def factorioStop(self, ctx):
        
        allWindows = pgw.getAllTitles()

          
        if config.nameFactorio in allWindows:
            log(f"{ctx.author}stopped the Squad server.")
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
            log(f"{ctx.author} tried to stop the Factorio server, but it was not running.")
            await ctx.send("Can't stop the Factorio server, it is not running.")  


class servers(commands.Cog, name="Server Info"):
    def __init__(self, bot):
        self.bot = bot
   


    @commands.command(name="servers", brief = "Shows server info")
    async def server(self, ctx):
        allWindows = pgw.getAllTitles()
        response=""

        #squad running
        if config.nameSquad in allWindows:
            response.append("Squad: Running\n")

        #squad updating
        elif config.nameSquadUpdate in allWindows:
            response.append("Squad: Updating\n")

        #squad not running
        else:
            response.append("Squad: Not Running\n")
        

        #factorio running
        if config.nameFactorio in allWindows:
            response.append("Factorio: Running\n")

        #factorio not running
        else:
            response.append("Factorio: Not Running\n")
    

        log(f"{ctx.author} checked server status")
        log(response)
        await ctx.send(response)


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


bot.run(credentials.testToken)
