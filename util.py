from discord import Embed

hangmen = [
        "https://upload.wikimedia.org/wikipedia/commons/8/8b/Hangman-0.png",
        "https://upload.wikimedia.org/wikipedia/commons/3/30/Hangman-1.png",
        "https://upload.wikimedia.org/wikipedia/commons/7/70/Hangman-2.png",
        "https://upload.wikimedia.org/wikipedia/commons/9/97/Hangman-3.png",
        "https://upload.wikimedia.org/wikipedia/commons/2/27/Hangman-4.png",
        "https://upload.wikimedia.org/wikipedia/commons/6/6b/Hangman-5.png",
        "https://upload.wikimedia.org/wikipedia/commons/d/d6/Hangman-6.png"
        ]

def create_embed(context, word):
    placeholder = []
    for c in word["current"]:
        if c == "-":
            placeholder.append(":large_blue_circle:")
        else:
            placeholder.append(":regional_indicator_"+c.lower()+":")

    embed = Embed()
    embed.add_field(
            name="Word",
            value="".join(placeholder),
            inline=False
            )
    embed.add_field(
            name="Guesses",
            value=" ".join(word["used"]) or "None",
            inline=False
            )
    embed.set_thumbnail(url=hangmen[word["failed"]])
    embed.color = 16727296 if word["wrong_guess"] else 1402304
    return embed

def create_win_embed(context, word):
    embed = Embed()
    embed.add_field(
            name="You win!",
            value=":thumbsup:",
            inline=True
            )
    embed.add_field(
            name="The word was:",
            value=word["word"],
            inline=True
            )
    embed.set_footer(
            text="Type {}hang to play again.".format(context.prefix)
            )
    embed.color = 5025616
    return embed

def create_lose_embed(context, word):
    embed = Embed()
    embed.add_field(
            name="You're dead.",
            value=":cry:",
            inline=True
            )
    embed.add_field(
            name="The word was:",
            value=word["word"],
            inline=True
            )
    embed.set_thumbnail(url=hangmen[-1])
    embed.set_footer(
            text="Type {}hang to play again.".format(context.prefix)
            )
    embed.color = 14494720
    return embed
