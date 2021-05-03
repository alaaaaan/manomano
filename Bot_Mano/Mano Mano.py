heroku buildpacks:set heroku/python
python -V
Python 3.9.4

import discord

# on importe la fonction get
# from discord.utils import get

# ajouter un composant de discord.py
from discord.ext import commands

from random import *

# on importe le module "time"
# import time
client = discord.Client()

# création du bot
bot = commands.Bot(command_prefix="*")

with open("warnings.txt", "r") as warn_file:
    warnings = eval(warn_file.read())
    print(warnings)
    warn_file.close()


# détecter quand le bot est prêt ("allumé")
@bot.event
async def on_ready():
    print("Bot Prêt")
    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Activity(type=discord.ActivityType.listening, name="TU TU... TULULU..."))


@bot.command()
async def delete(message, nombre):
    await message.channel.purge(limit=int(nombre) + 1)


# creer la commande warning
@bot.command()
@commands.has_permissions(administrator=True)
async def warning(ctx, membre: discord.Member):
    pseudo = membre.mention
    ident = membre.id

    # si la personne n'a pas de warn
    if ident not in warnings:
        warnings[ident] = 0
        print("Vous n'avez eu aucun avertissement")

    print(warnings[ident])
    warnings[ident] += 1
    print("ajout de l'avertissement", ident, warnings[ident], "/3")

    # vérifier si le membre a 3 warn
    if warnings[ident] >= 3:
        # on remet le compteur a 0:
        warnings[ident] = 0
        # message
        await membre.send("Vous avez été éjecté du serveur ! Trop d'avertissements !")
        await ctx.send(f"Oh non ! {pseudo} a été exclu parce qu'il n'a pas respecté les règles du serveur "
                       f"à plusieurs reprisent !")
        # éjecter la personne
        await membre.kick()
    else:
        await ctx.send(f"{pseudo} Tu as reçu une alerte ! Attention à bien respecter les règles !")

    with open("warnings.txt", "w+") as file:
        file.write(str(warnings) + "\n")
        file.close()

disquettes = [" je parle allemand français anglais mais la langue que je préfère c'est la tienne",
              " tu serai pas du bon shit sa mère ? parce que t'es stupéfiant",
              " tu serai pas ma porte de sortie par hasard ? parce que tu m'exit",
              " tu serais pas tomber sous mon charmes?\nParce que t'es claqué au sol",
              " t'aimes les maths ? nan parce que sinon on pourrait soustraire nos vêtements et "
              " additionner nos corps...",
              " tu fais du foot? nan parce que t'es vraiment une frappe",
              " black friday : -100% sur les habits dans mon lit",
              " faudrait que tu sois un sablier comme ça je pourrai te retourner",
              " si j'avais été un super héro j'aurai kiffe être yourman",
              " si chez flunch on peut fluncher, ça te dit d'aller chez Nike ?",
              " ça te dirait pas de devenir chauffeur de bus ? \nNan comme ça tu pourrais me prendre matin midi soir",
              " le plus important dans un couple c'est de SEXprimer et de commuNIQUER",
              " j'aimerai pas te croiser pendant le ramadan parce que tu me donnes faim tellement t'es a croquer",
              " j'ai envie d'être une ps4 pour que tu m'allumes jour et nuit",
              " ça te dis de faire du parachute tous les deux ? \nComme ça on pourra s'envoyer en l'air",
              " tu sais que y'a le couvre feu ? parce que il est 23h et t'es tjr dans ma tête",
              " tu t'appellerai pas Gérard ? \nParce que Gérard-ment vu une personne comme toi",
              " viens on joue a among us et a chaque fois qu'on est crewmate on s'embrasse ?",
              " tu serais pas la mère d'Eren ? \nParce que t'es à croquer",
              " tu serais pas une série netflix ?\n Parce que j'ai bien envie de te terminer en 1 jour",
              " j'ai une question à soulever...\nTu veux être la question ?",
              " à quoi ça sert de dire bonne nuit si elle n'est pas aussi bonne que toi"]

images = ["image0.jpg", "image1.jpg", "image2.jpg", "image3.png", "image4.png", "image5.png"]


@bot.command()
async def disquette(ctx, membre: discord.Member):
    pseudo = membre.mention
    shuffle(disquettes)
    shuffle(images)
    await ctx.send("dis " + pseudo + disquettes[0] + " :smirk:")
    with open(images[0], "rb") as f:
        picture = discord.File(f)
        await ctx.send(file=picture)


# vérifier l'erreur
@warning.error
async def on_command_error(ctx, error):
    # detecter cette erreur
    if isinstance(error, commands.MissingPermissions):
        # envoyer un message
        await ctx.send("Tu n'es pas modérateur petit chenapan")


# lancement du bot
print("Lancement du bot...")

# connecter au serveur
bot.run(TOKEN)
