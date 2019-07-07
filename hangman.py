#!/usr/bin/env python3

import os
import sys

from discord.ext import commands
from hangman_commands import HangmanCommands

class Hangman(commands.Bot):
    def __init__(self, command_prefix="+"):
        super().__init__(command_prefix)
        self.add_cog(HangmanCommands(self))

if __name__ == "__main__":
    try:
        token = os.environ["BOT_TOKEN"]
    except:
        print ("Bot token not found.")
        sys.exit(1)
    hangman = Hangman()
    hangman.run(token)
