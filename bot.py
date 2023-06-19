import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import random
import json

# sets the prefix (e.g. if prefix = "!", then the help command is "!help")
prefix = "!"
# set intents (ver 1.5)
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=prefix, intents=intents)

# so I don't leak my token to github...
load_dotenv()
TOKEN = os.getenv("TOKEN")


# runs the bot
def run_bot():
    bot.run(TOKEN)


# command !make:
# - create your own question to add to the bot's question list
@bot.command()
async def make(ctx):
    with open("archive.json") as f:
        questions = json.load(f)
    await ctx.send("What is the question that would you like to add?")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    q = await bot.wait_for("message", check=check)
    await ctx.send("What is the answer to your question?")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    a = await bot.wait_for("message", check=check)
    if q.content[-1:] != "?":
        question = q.content + "?"
    else:
        question = q.content
    questions.append([question.lower().capitalize(), a.content.lower().capitalize()])
    with open("archive.json", "w") as f:
        json.dump(questions, f, indent=2)
    await ctx.send("Your question has been added.")


# command !quiz:
# take a quiz of 5 random questions pulled from the bot's question list, and get given a score
@bot.command()
async def quiz(ctx):
    with open("archive.json") as f:
        questions = json.load(f)
    score = 0
    x = 1
    no_dupes = []
    while x < 6 and x < len(questions) and len(no_dupes) < len(questions):
        rand = random.randint(0, len(questions) - 1)
        while rand in no_dupes:
            rand = random.randint(0, len(questions) - 1)
        no_dupes.append(rand)
        await ctx.send("**Question " + str(x) + ":** " + questions[rand][0])

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        response = await bot.wait_for("message", check=check)
        if response.content.lower().capitalize() == questions[rand][1]:
            await ctx.send("**Correct!**")
            score += 1
        else:
            await ctx.send("**Incorrect...**")
            await ctx.send("The correct answer is: *" + questions[rand][1] + "*")
        x += 1
    await ctx.send("That's the end of the quiz!")
    score_calc = (score / (x - 1)) * 100
    await ctx.send("Your score: **" + str(score_calc) + "%** (" + str(score) + " out of " + str((x - 1)) + ")")
    await ctx.send("Thank you for participating! Feel free to add questions of your own by typing **!make**.")
