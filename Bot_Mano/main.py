import discord
from datetime import *
import time
from discord.ext import commands
from discord.ext.commands import has_permissions
from random import *
import asyncio
import json

client = discord.Client()

# création du bot
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="*", intents=intents)

with open("extra.json", "r", encoding='utf-8') as f:
    data = json.load(f)

with open("warnings.txt", "r") as warn_file:
    warnings = eval(warn_file.read())
    warn_file.close()

print(str(datetime.now()))

deb = False
roulette = False
shifumi_t = False
already_play_a = True
already_play_m = True

a = 0
nb_players = 0

playerlist = []
players = []
membre_l = []
vote = []

starter_rr = ()

liaison = {}

auteur_shif = ""
membre_shif = ""
debat_question = ""
membrestr = ""
choice_a = ""
choice_b = ""

react_id = int
msg_start_id = int

emojis = ['✅', '❌']
count_emoji = {'✅': 0, '❌': 0}

dat_shifumi = data["shifumi"]
emojis_a = dat_shifumi["emojis_a"]
emojis_m = dat_shifumi["emojis_m"]
win_shifumi = dat_shifumi["win_shifumi"]

images = data["images"]


@bot.command()
@commands.cooldown(1, 60, commands.BucketType.user)
async def rassemblement(ctx):
    """   Envoie un message mentionnant toutes les personnes du serveur !   """

    global membrestr, membre_l
    membres_b = ctx.guild.members
    for membrel in membres_b:
        if membrel.bot:
            pass
        else:
            membre_l.append(membrel.mention)
            membrestr = " \n".join(membre_l)
    await ctx.send(f'AVENGERS RASSEMBLEMENT !\n{membrestr}')
    temp = await ctx.send("C'est bon y'a tout le monde chef")
    await asyncio.sleep(2)
    await temp.delete()
    membrestr = ""
    membre_l = []


@rassemblement.error
async def rassemblement_name_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"ARRÊTE DE SPAMMER", description=f"Tu pourras réutiliser cette "
                                                                   f"commande dans"
                                                                   f" {error.retry_after:.0f}s.")
        await ctx.send(embed=em)


@bot.command()
# @commands.cooldown(1, 60, commands.BucketType.user)
async def shifumi(ctx, membre: discord.Member):
    """Permet de faire un shifumi avec la personne que tu mentionnes !"""
    global msg_start_id, shifumi_t, auteur_shif, membre_shif, liaison, already_play_m, already_play_a
    membre_shif = membre
    auteur_shif = ctx.message.author
    objects = ['pierre', 'papier', 'ciseaux']
    shuffle(objects)
    nb_liaison = 0
    if auteur_shif == membre_shif:
        await ctx.send(" Tu ne peux pas jouer solo ! \n"
                       "C'est bizarre de vouloir jouer tout seul quand même :face_with_raised_eyebrow:")
    elif membre_shif.bot:
        await ctx.send("Tu ne peux pas jour aveec un robot ! \n"
                       "C'est bizarre de vouloir jouer avec un bot quand même :face_with_raised_eyebrow:")
    elif shifumi_t:
        await ctx.send("Une partie est déjà lancée ! \n Attends qu'elle se finisse avant d'en relancer une !")
    else:
        shifumi_t = True
        msg_start = await ctx.send(f"Une partie commence entre {auteur_shif.mention} et {membre_shif.mention}")
        msg_start_id = msg_start.id
        await ctx.send("Vérifiez vos DM pour savoir à quoi correspondent vos mentions !")
        already_play_a = False
        already_play_m = False

        for emoji_a in emojis_a:
            liaison[emoji_a] = objects[nb_liaison]
            await msg_start.add_reaction(emoji_a)
            nb_liaison += 1

        shuffle(objects)
        nb_liaison = 0

        for emoji_m in emojis_m:
            liaison[emoji_m] = objects[nb_liaison]
            await msg_start.add_reaction(emoji_m)
            nb_liaison += 1

        await auteur_shif.send(f"Voici à quoi correspondent vos réactions !\n{emojis_a[0]}: {liaison['1️⃣']}"
                               f"\n{emojis_a[1]}: {liaison['2️⃣']}"
                               f"\n{emojis_a[2]}: {liaison['3️⃣']}")
        await membre_shif.send(f"Voici à quoi correspondent vos réactions !\n{emojis_m[0]}: {liaison['4️⃣']}"
                               f"\n{emojis_m[1]}: {liaison['5️⃣']}"
                               f"\n{emojis_m[2]}: {liaison['6️⃣']}")


async def verif_shifumi(auteur_, emoji, canal):
    global membre_shif, auteur_shif, liaison, shifumi_t, already_play_a, already_play_m, choice_a, choice_b
    if shifumi_t:
        if auteur_ == auteur_shif:
            if already_play_a:
                pass
            else:
                if emoji in emojis_a:
                    await auteur_shif.send(f'Tu as choisi {liaison[emoji]}')
                    choice_a = liaison[emoji]
                    already_play_a = True

        elif auteur_ == membre_shif:
            if already_play_m:
                pass
            else:
                if emoji in emojis_m:
                    await membre_shif.send(f"Tu as choisi {liaison[emoji]}")
                    choice_b = liaison[emoji]
                    already_play_m = True

        await asyncio.sleep(1)
        if already_play_a == True and already_play_m == True:
            shifumi_t = False
            if choice_a == choice_b:
                await canal.send(f"Il y a égalité ! Vous avez tous les deux choisi {choice_b}")
            elif win_shifumi[choice_a] == choice_b:
                await canal.send(f'{auteur_shif.name} a remporté la partie !\n Il a choisi {choice_a} alors que '
                                 f'{membre_shif.name} a choisi {choice_b}')
            else:
                await canal.send(f'{membre_shif.name} a remporté la partie !\n Il a choisi {choice_b} alors que '
                                 f'{auteur_shif.name} a choisi {choice_a}')
    else:
        pass


@shifumi.error
async def shifumi_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"TOUT DOUX LE LOUP !", description=f"Un shifumi est déjà lancé. Réessaie dans"
                                                                     f" {error.retry_after:.0f}s.")
        await ctx.send(embed=em)


@bot.command(pass_context=True)
@commands.has_permissions(manage_roles=True)
async def goulag(ctx, membre: discord.Member):
    """Envoie la personne que tu mentionnes au goulag !"""
    mention = membre.mention
    role = discord.utils.get(membre.guild.roles, name="Goulag")
    if role in membre.roles:
        await membre.remove_roles(role)
        await ctx.send(f"{mention} est revenu du goulag en vie !")
    else:
        await membre.add_roles(role)
        await ctx.send(f"{mention} à été envoyé au goulag !\n Puisses le sort lui être favorable")
        await membre.send("Bordel mec ! Qu'est-ce que tu fous au goulag ! \n T'es dans la sauce maintenant mec, "
                          "j'espère que tu vas t'en sortir vivant quand même")


@bot.command()
async def otage(ctx, membre: discord.Member):
    """Prends en otage la personne mentionnée !"""
    sauveur_h = []
    for sauveur in ctx.guild.members:
        if sauveur.bot:
            pass
        else:
            sauveur_h.append(sauveur)
    sauveur_d = sauveur_h[randint(0, len(sauveur_h) - 1)]
    role = discord.utils.get(membre.guild.roles, name="otage")
    await ctx.send(f" OH NON !\n{ctx.message.author.name} à pris {membre.name} en otage ! seul {sauveur_d.mention}"
                   f" peut la sauver !")
    await membre.add_roles(role)


@goulag.error
async def error_goulag(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Tu peux pas envoyer de gens au goulag enculé")


@bot.command()
async def debat(ctx, *args):
    """   Lance un débat sur la quetion que tu as posé !   """

    global debat_question, emojis, react_id, deb
    args_q = []
    if deb:
        em = discord.Embed(title=f"TOUT DOUX LE LOUP !", description=f"Un débat est déjà lancé !")
        await ctx.send(embed=em)
    else:
        deb = True
        count_emoji['✅'] = 0
        count_emoji['❌'] = 0
        questionl = []
        if not args:
            await ctx.send('Tu ne peux pas lancer de débat sans poser de question !')
        else:
            if any(str.isdigit() for str in args[-1]):
                delai = args[-1]
            else:
                delai = 60
            for arg in args:
                if arg != args[-1]:
                    args_q.append(arg)
                else:
                    pass
            for q in args_q:
                questionl.append(q)
                debat_question = " ".join(questionl)
                if debat_question.endswith("?"):
                    pass
                else:
                    debat_question += " ?"
            react = await ctx.send(f"Le débat du jour est: \n **{debat_question}** \n \n"
                                   f"Votez dès à présent grâce aux réactions !\nVous avez {delai} secondes pour voter")
            react_id = react.id
            print(react_id)
            for emoji in emojis:
                await react.add_reaction(emoji)
            await asyncio.sleep(int(delai))
            await verif_deb(msg=ctx.message.channel)


@bot.command()
async def tirage(ctx, *args):
    """Permet de faire des équipes"""

    equipe1 = []
    equipe2 = []
    equipe1str = ""
    equipe2str = ""
    nombre = 0
    joueurs = []
    for arg in args:
        joueurs.append(arg)

    shuffle(joueurs)
    for joueur in joueurs:
        if (nombre % 2) == 0:
            equipe1.append(joueur)
            equipe1str = ", ".join(equipe1)
        else:
            equipe2.append(joueur)
            equipe2str = ", ".join(equipe2)
        nombre += 1

    await ctx.send(f"L'équipe 1 est composée de {equipe1str} et l'équipe 2 est composée de {equipe2str}")
    if len(equipe1) > len(equipe2):
        await ctx.send("Le nombre de joueur est impaire il y a donc un joueur de plus dans l'équipe 1")


async def verif_deb(msg):
    global deb
    await msg.send("FIN DES VOTES")
    if count_emoji['✅'] > count_emoji['❌']:
        await msg.send("**La majorité est d'accord !**")
    elif count_emoji['✅'] < count_emoji['❌']:
        await msg.send("**La majorité désaprouve !**")
    else:
        await msg.send("**Il y a égalité ! Personne n'a réussi à se mettre d'accord !**")
    deb = False
    count_emoji['✅'] = 0
    count_emoji['❌'] = 0


@bot.command(aliases=['roulette', 'roulette_russe'])
async def rr(ctx, action=None):
    """   Lance une roulette russe !   """

    global roulette, players, nb_players, a, starter_rr
    if action == "start":
        if roulette:
            await ctx.send("Une partie est déjà lancée !")
        else:
            roulette = True
            starter_rr = ctx.message.author.name
            await ctx.send("La partie est lancée ! Rejoignez vite !")
            players.append(starter_rr)
            nb_players += 1
            playerlist.append(nb_players)
    elif action == "join":
        mention = ctx.message.author.name
        if roulette:
            if str(ctx.message.author.name) not in players:
                players.append(mention)
                nb_players += 1
                playerlist.append(nb_players)
                await ctx.send("YES ! " + str(ctx.message.author) + " viens de rejoindre la roulette russe !")
                if nb_players > 1:
                    await ctx.send(
                        "Il y a maintenant " + str(nb_players) + " joueurs qui participent à la roulette russe")
            else:
                await ctx.send("tu participes déjà à la roulette russe enculé")

        else:
            await ctx.send("Aucune partie n'est lancée")
            reset_rr()

    elif action == "membres":
        if roulette:
            if nb_players == 0:
                await ctx.send("Personne à rejoint la roulette russe -_-")
            elif nb_players == 1:
                await ctx.send(f"Pour l'insant il y un seul participant")
                await ctx.send(f"Seul {players[0]} est fidèle au poste")
            else:
                await ctx.send(f"Pour l'insant il y a {nb_players} participants")
                for part in players:
                    await ctx.send(f"-{part}")
        else:
            await ctx.send("Attends y'a même pas de partie de lancée fréro")

    elif action == "run":
        if ctx.message.author.name == starter_rr:
            if nb_players > 1:
                roulette = False
                await ctx.send("La partie commence ! qui va décéder ?")
                msg = await ctx.send("Qui vas mourir ?")

                while nb_players != a:
                    await msg.edit(content="Qui va mourir ?\n Serait-ce " + players[a] + " ?")
                    a += 1
                    time.sleep(1)

                shuffle(players)
                await msg.edit(content=f"{players[0]} est décédé(e) ! (c'est pas une grande perte)")
                reset_rr()
            else:
                if roulette:
                    await ctx.send("Tu es tout seul dans la partie !"
                                   "\n Si tu veux jouer relance une partie et ramène tes potes"
                                   "(du moins si t'en as :rolling_eyes:)")
                    reset_rr()
                else:
                    await ctx.send("Y'a pas de partie lancée t'es au courant ?")
        else:
            if roulette:
                await ctx.send(f"Uniquement la personne qui la créer la partie peut la lancer, donc c'est "
                               f"à {starter_rr} de lancer la partie")
            else:
                await ctx.print("Aucune partie n'est lancée !")

    else:
        await ctx.send("cette commande n'existe pas ! Essaie plutôt celles de cette liste\n"
                       "*``-rr start``*\n **Crée une nouvelle partie** \n \n"
                       "*``-rr join``*\n **Rejoint la partie** \n \n"
                       "*``-rr run``*\n **Lance la partie**\n \n"
                       "*``-rr membres``*\n **Nomme tous les joueurs présents dans la partie** \n \n")


def reset_rr():
    global a, nb_players, playerlist, players
    a = 0
    nb_players = 0
    playerlist = []
    players = []


@bot.command()
async def delete(message, nombre=1):
    """   Supprime le nombre de message entré !   """

    print(f"{nombre} messages supprimés")
    await message.channel.purge(limit=int(nombre) + 1)
    if nombre < 2:
        conclusion = await message.channel.send("1 message a été supprimé !")
    else:
        conclusion = await message.channel.send(f"{nombre} messages ont été supprimés !")

    await asyncio.sleep(10)
    await conclusion.delete()


@bot.command()
async def SHEESH(message):
    """   SHEEEEEEEESH   """

    print("SHEEEESH")
    await message.channel.send("SHEEEEEEEEEEEEEEEEEEEESH !")


@bot.command()
async def ping(ctx):
    """    Envoie le ping de Mano Mano   """

    if bot.latency <= 1:
        await ctx.send(f"j'ai un ping de {round(bot.latency, 3)}ms !\nEt ouais j'ai la fibre mon pote :sunglasses:")
    else:
        await ctx.send(f"On dirait que je rame...\nJ'ai un ping de {round(bot.latency, 3)}ms !")


@bot.command()
async def statut(ctx, *args):
    """   Change le statut du bot provisoirement   """

    if not args:
        await ctx.send("Tu n'as pas mis de statut dans ta commande ! Celle par défaut est restituée")
        await bot.change_presence(status=discord.Status.online,
                                  activity=discord.Activity(type=discord.ActivityType.listening,
                                                            name="TU TU... TULULU..."))
    else:
        print("Le statut a été changé !")
        perso_statusb = args
        perso_statul = []
        for q_word in perso_statusb:
            perso_statul.append(q_word)
        perso_status = " ".join(perso_statul)
        await bot.change_presence(status=discord.Status.online,
                                  activity=discord.Game(perso_status))
        await ctx.send("Le statut a été modifié pendant 10 minutes !")
        await asyncio.sleep(600)
        await bot.change_presence(status=discord.Status.online,
                                  activity=discord.Activity(type=discord.ActivityType.listening,
                                                            name="TU TU... TULULU..."))
    print("Le statut initial a été remis !")


@bot.command()
async def blague(ctx):
    """   Envoie une blague   """
    shuffle(data["blagues"])
    joke = data["blagues"]
    await ctx.send(joke[0])


@bot.command()
async def disquette(ctx, membre=None):
    """   Envoie une disquette à la personne que tu mentionnes !   """

    if not membre:
        await ctx.send('Tu dois mentionner la personne à qui tu veux dédier la disquette !')
    else:
        print("Une disquette a été envoyée !")
        if membre is discord.Member:
            membre: membre.mention
        disquettes = data["disquettes"]
        shuffle(disquettes)
        shuffle(images)
        await ctx.send("dis " + membre + disquettes[0] + " :smirk:")
        with open(images[0], "rb") as file:
            picture = discord.File(file)
            await ctx.send(file=picture)


'''@disquette.error
async def error_disquette(error, ctx):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Tu dois mentionner la personne à qui tu veux dédier la disquette !')'''


@bot.command()
async def voyance(ctx, *args):
    """   Répond à la question que tu lui poses   """

    print("La voyante est en entretien !")
    reponses = data["reponses"]
    question_a = args
    question_l = []
    for q_word in question_a:
        question_l.append(q_word)
    question = " ".join(question_l)
    pseudo = ctx.message.author.name
    shuffle(reponses)
    await ctx.send(f"**{pseudo}** m'a posé la question suivante: \n*{question}* \n \n**{reponses[1]}**")


@bot.command()
async def vald(ctx):
    """Envoie du Vald foort !"""

    channel = ctx.author.voice.channel
    guild = ctx.guild
    voice_client: discord.VoiceClient = discord.utils.get(bot.voice_clients, guild=guild)
    if voice_client is None:
        await channel.connect()
        voice_client: discord.VoiceClient = discord.utils.get(bot.voice_clients, guild=guild)

    audio_source = discord.FFmpegPCMAudio(executable="C:/Users/Megaport/Downloads/DiscordLoupGarou-master/ffmpeg.exe",
                                          source="vald-desaccorde.mp3")

    if not voice_client.is_playing():
        voice_client.play(audio_source, after=None)
        await ctx.send("C'EST PARTI POUR DU VAAAAALLLLLDDDDD !!")


''''@vald.error
async def vald_error(error, ctx):
    if isinstance(error, commands.CommandInvokeError):
        print("aaa")
        await ctx.send("Je suis déjà connecté à un salon vocal !")'''


@bot.command()
async def leave(ctx):
    """Fait quitter le bot de la voc"""

    server = ctx.message.guild.voice_client
    await server.disconnect()
    await ctx.send("J'ai compris j'me casse de la voc :smiling_face_with_tear:")


@bot.command()
async def join(ctx):
    """   Le bot rejoint le vocal dans lequel tu es   """

    print("le bot a rejoint un salon vocal")
    channel = ctx.author.voice.channel
    vc = await channel.connect()
    vc.play(discord.FFmpegPCMAudio(executable="C:/Users/Megaport/Downloads/DiscordLoupGarou-master/ffmpeg.exe",
                                   source="mano.mp3"), after=lambda e: print('done', e))
    await ctx.send("J'ARRIVE POUR METTRE LE FEU A LA VOC :fire::fire::fire: ")


@bot.command()
@has_permissions(manage_roles=True)
async def warning(ctx, membre: discord.Member):
    """   Met un avertissement au membre mentionné   """

    print("la commande warning a été utilisée")
    pseudo = membre.mention
    ident = membre.id

    # si la personne n'a pas de warn
    # if ident == ctx.message.author.id:
    #    await ctx.send("Tu ne peux pas te warn toi même enfin ")
    if ident == 831261319155417128:
        await ctx.send("Tu ne peux pas me warn !!!")
    else:
        if ident not in warnings or warnings[ident] == 0:
            warnings[ident] = 0
            warnings[ident] += 1
            await membre.send("Tu as reçu ton premier warn ! \n Je ne te félicite pas... "
                              "\n Attention à bien respecter les règles du serveur la prochaine fois !")
            print(f"{pseudo} s'est pris un warn, il en a désormais {warnings[ident]}")
            await ctx.send(f"Oh non !{pseudo} a été warn  par {ctx.message.author} ! ({warnings[ident]}/3)")

        elif warnings[ident] == 1:
            warnings[ident] += 1
            await ctx.send(f"Oh non !{pseudo} a été warn par {ctx.message.author} ! ({warnings[ident]}/3)")
            await membre.send("C'est ton deuxième warn attention ! Ne t'avises plus de recommencer ou tu seras exclu !")

        else:
            if ctx.message.author.guild_permissions.kick_members:
                warnings[ident] = 0
                await membre.kick()
                await ctx.send(f"Malheureusement {pseudo} a été exclu du serveur par {ctx.message.author}"
                               f" parce qu'il a enfreint les règles du serveur à de trop nombreuses reprises")
                await membre.send("Tu as été expulsé du server ! Comme qui dirait qui fait le malin "
                                  "tombe dans le ravin")
            else:
                await ctx.send(f"Attention {ctx.message.author} tu n'as pas la permission d'expulsé des gens de ce "
                               f"serveur ! \n Donc {pseudo} restera à {warnings[ident]} warn pour l'instant")

        with open("warnings.txt", "w+") as file:
            file.write(str(warnings) + "\n")
            file.close()


@warning.error
async def on_command_error(error, ctx):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Tu n'es pas la permission d'expulser quelqu' un !")


@bot.event
async def on_raw_reaction_add(payload):
    global react_id, msg_start_id
    emoji = payload.emoji.name
    message = payload.message_id
    cannal = payload.channel_id
    auteur_ = payload.member
    canal = bot.get_channel(id=cannal)
    if deb:
        if message == react_id:
            count_emoji[emoji] += 1
            print(count_emoji)
            print(count_emoji['✅'])
            print(count_emoji['❌'])
    else:
        pass
    if shifumi_t:
        if message == msg_start_id:
            await verif_shifumi(auteur_, emoji, canal)


@bot.event
async def on_raw_reaction_remove(payload):
    global react_id
    emoji = payload.emoji.name
    message = payload.message_id
    if deb:
        if message == react_id:
            count_emoji[emoji] -= 1
            print(count_emoji)
            print(count_emoji['✅'])
            print(count_emoji['❌'])
    else:
        pass


@bot.event
async def on_message(message):
    mentioni = f'<@!{bot.user.id}>'
    mention = f'<@{bot.user.id}>'
    with open("logs", "a", encoding='utf-8') as file:
        file.write(f"{str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))} {message.author} dans {message.channel}: "
                   f"{message.content} \n")
        file.close()
    if "🖕" in message.content:
        await warning(ctx=await bot.get_context(message), membre=message.author)
        await message.delete()
    if message.author.id == 235088799074484224 and message.channel != 830555906461794325:
        await message.delete()
    if "!fs" in message.content and message.channel != 830555906461794325:
        await message.delete()
    if message.content.startswith('*'):
        await bot.process_commands(message)
    if mention in message.content or mentioni in message.content:
        if message.author.id == 570280053515091970:
            await message.channel.send("Que puis-je pour vous Grand Dictateur Suprême ?")
        else:
            await message.channel.send("Que puis-je pour vous maître ?")


@bot.event
async def on_ready():
    print("Bot Prêt")
    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Activity(type=discord.ActivityType.listening, name="TU TU... TULULU..."))


print("Lancement du bot...")
# lancement du bot

bot.run(TOKEN)
# connecter au serveur
