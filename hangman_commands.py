# Cog class for hangman commands

import random
import copy

import discord
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

    @commands.Cog.listener()
    async def on_ready(self):
        print ("Logged in as {}.".format(self.bot.user))
        await self.bot.change_presence(
                activity=discord.Game(
                    name="{}hangman with humans.".format(
                        self.bot.command_prefix
                        )
                    )
                )

    @commands.command(name="hangman", aliases=["play", "h", "hang"])
    async def hang(self, context):
        channel_id = str(context.channel.id)
        word = random.choice(self.words)
        self.channel_words[channel_id] = {
                "word" : word,
                "current" : ["-"] * len(word),
                "used" : [],
                "failed" : 0,
                "ended" : False,
                "wrong_guess" : False,
                "hints" : 2
                }

        embed = util.create_embed(context, self.channel_words[channel_id])
        await context.send(embed=embed)

    @commands.command(name="guess", aliases=["g"])
    async def guess(self, context, *args):
        await self._guess(context, *args)

    @commands.command(name="hint")
    async def hint(self, context):
        channel_id = str(context.channel.id)
        word = self.get_word(context)
        if not word:
            await context.send("This channel has no ongoing games.")
            return

        pos = -1
        for i,c in enumerate(word["current"]):
            if word["current"][i] == "-":
                pos = i
                break

        if pos < 0 or word["hints"] <= 0:
            await context.send("No more hints for you.")
            return

        word["hints"] -= 1
        self.channel_words[channel_id] = copy.deepcopy(word)

        await self._guess(context, [word["word"][pos]])


    async def _guess(self, context, *args):
        channel_id = str(context.channel.id)
        # try:
            # word = copy.deepcopy(self.channel_words[channel_id])
            # if word["ended"]:
                # raise Exception
            # word["wrong_guess"] = False
        # except Exception as e:
            # print (e)
            # await context.send("This channel has no ongoing games.")
            # return
        word = self.get_word(context)
        if not word:
            await context.send("This channel has no ongoing games.")
            return

        try:
            letter = args[0][0].upper()
        except:
            await context.send("What's your guess?")
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

    def get_word(self, context):
        channel_id = str(context.channel.id)
        try:
            word = copy.deepcopy(self.channel_words[channel_id])
            if word["ended"]:
                raise Exception
            word["wrong_guess"] = False
            return word
        except Exception as e:
            print (e)
            return False
