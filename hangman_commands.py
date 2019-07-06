# Cog class for hangman commands

import random
import copy

from discord.ext import commands

import util

class HangmanCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._words = None
        self.channel_words = {}

    @property
    def words(self):
        with open("data/words.txt", "r") as word_file:
            return [word.strip().upper() for word in word_file]

    @commands.command(name="hang", aliases=["play", "h"])
    async def hang(self, context):
        channel_id = str(context.channel.id)
        word = random.choice(self.words)
        self.channel_words[channel_id] = {
                "word" : word,
                "current" : ["-"] * len(word),
                "used" : [],
                "failed" : 0,
                "ended" : False,
                "wrong_guess" : False
                }

        embed = util.create_embed(context, self.channel_words[channel_id])
        await context.send(embed=embed)

    @commands.command(name="guess", aliases=["g"])
    async def guess(self, context, *args):
        channel_id = str(context.channel.id)
        try:
            word = copy.deepcopy(self.channel_words[channel_id])
            if word["ended"]:
                raise Exception
            word["wrong_guess"] = False
        except Exception as e:
            print (e)
            await context.send("This channel has no games.")
            return

        try:
            letter = args[0][0].upper()
        except:
            await context.send("Guess what?")
            return

        if letter in word["used"]:
            await context.send("That letter was already used.")
            return

        word["used"].append(letter)

        for i,c in enumerate(word["word"]):
            if c == letter:
                word["current"][i] = letter

        if word["current"] == self.channel_words[channel_id]["current"]:
            word["failed"] += 1
            word["wrong_guess"] = True
        
        if word["failed"] > 5:
            word["ended"] = True
            embed = util.create_lose_embed(context, word)
            await context.send(embed=embed)
        elif "".join(word["current"]) == word["word"]:
            word["ended"] = True
            embed = util.create_win_embed(context, word)
            await context.send(embed=embed)
        else:
            embed = util.create_embed(context, word)
            await context.send(embed=embed)

        self.channel_words[channel_id] = copy.deepcopy(word)
        # await context.send(word)
