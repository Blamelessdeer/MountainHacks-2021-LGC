import discord
import requests
from discord.ext import commands

class Search(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.command()
    async def search(self, ctx, *args):
        parameters = ["title", "author", "subject"]
        if args[0] in parameters:
            response = requests.get("https://www.googleapis.com/books/v1/volumes?q=" + args[0] + ":" + '\"' + str(args[1]) + '\"')
            print(args[1])
            if "items" in response.json():
                googleBooksList = response.json()['items']
                result = "```\n"
                if "title" in googleBooksList[0]["volumeInfo"]:
                    result += (str(googleBooksList[0]["volumeInfo"]["title"]) + "\n")
                if "subtitle" in googleBooksList[0]["volumeInfo"]: 
                    result += (str(googleBooksList[0]["volumeInfo"]["subtitle"]) + "\n")
                if "authors" in googleBooksList[0]["volumeInfo"]: 
                    result += (str(googleBooksList[0]["volumeInfo"]["authors"]) + "\n")
                if "publishedDate" in googleBooksList[0]["volumeInfo"]: 
                    result += (str(googleBooksList[0]["volumeInfo"]["publishedDate"]) + "\n")
                if "description" in googleBooksList[0]["volumeInfo"]: 
                    result += str(googleBooksList[0]["volumeInfo"]["description"] )
                result += "\n```"

                def check(reaction, user):
                    return user == ctx.author and str(reaction.emoji) in ['\N{WHITE HEAVY CHECK MARK}']

                embedMsg = await ctx.send(result)                
                await embedMsg.add_reaction('\N{WHITE HEAVY CHECK MARK}')
                confirmation = await self.bot.wait_for("reaction_add", check=check)
                if confirmation :    
                    #add the book to the list       
                    print("something")
            else:
                await ctx.send("No books found.")
        else:
            await ctx.send("Invalid parameters. Use: /search <type> <query>")

    


def setup(bot):
    bot.add_cog(Search(bot))