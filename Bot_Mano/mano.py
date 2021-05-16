import discord
from datetime import *
import time
from discord.ext import commands
from discord.ext.commands import has_permissions
from random import *
import asyncio

client = discord.Client()

# création du bot
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="*", intents=intents)

with open("warnings.txt", "r") as warn_file:
    warnings = eval(warn_file.read())
    print(warnings)
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

win_shifumi = {'ciseaux': 'papier',
               'pierre': 'ciseaux',
               'papier': 'pierre'}

emojis_a = ['1️⃣', '2️⃣', '3️⃣']
emojis_m = ['4️⃣', '5️⃣', '6️⃣']

images = ["image0.jpg", "image1.jpg", "image2.jpg", "image3.png", "image4.png", "image5.png"]

reponses = ["Biensûr que oui", "Biensûr que non", "Evidemment", "PTDRRRR jamais de la vie enculé", "Ouais ptet jsp eft",
            "Dans 10/20 ans peut être ouais", "ftg et me casse pas la tête", "Oui", "Non",
            "Aucune idée poto tu me poses une colle là", "Je crois bien ouais"]

disquettes = [" je parle allemand français anglais mais la langue que je préfère c'est la tienne",
              " tu serai pas du bon shit sa mère ?\nParce que t'es stupéfiant",
              " tu serai pas ma porte de sortie par hasard ?\nParce que tu m'exit",
              " tu serais pas tomber sous mon charmes?\nParce que t'es claqué au sol",
              " t'aimes les maths ?\nNan parce que sinon on pourrait soustraire nos vêtements et "
              " additionner nos corps...",
              " tu fais du foot?\nNan parce que t'es vraiment une frappe",
              " black friday : -100% sur les habits dans mon lit",
              " faudrait que tu sois un sablier comme ça je pourrai te retourner",
              " si j'étais un super héro j'aurai kiffe être yourman",
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
              " à quoi ça sert de dire bonne nuit si elle n'est pas aussi bonne que toi",
              " j'aimerai pas jouer à cache cache avec toi\n Parce que trouver quelqu'un comme toi c'est impossible",
              " les autre m'appellent par mon prénom  mais toi tu peux m’appeler ce soir"]

blagues = ["Quelle mamie fait peur aux voleurs ?\n**Mamie Traillette** ",
           "J'ai une blague sur les magasins\n**Mais elle a pas supermarché**",
           "Pourquoi est-ce c'est difficile de conduire dans le Nord ?\n"
           "**Parce que les voitures arrêtent PAS DE CALER**",
           "Comment est-ce que la chouette sait que son mari fait la gueule ?\n**Parce qu’HIBOUDE**",
           "Pourquoi est-ce qu'on dit que les bretons sont tous frères et sœurs ?\n**Parce qu’ils n’ont Quimper**",
           "Pourquoi est-ce qu'on met tous les crocos en prison ?\n**Parce que les crocos dealent**",
           "Comment fait-on pour allumer un barbecue breton ?\n**On utilise des breizh**",
           "Pourquoi dit-on que les poissons travaillent illégalement ?\n**Parce qu’ils n’ont pas de FISH de paie**",
           "Quel est le bar préféré des espagnols ?\n**Le Bar-celone**",
           "Que faisaient les dinosaures quand ils n'arrivaient pas à se décider?\n**Des tirageosaures**",
           "Qu'est-ce qu'un tennisman adore faire ?\n**Rendre des services**",
           "Pourquoi est-ce que les livres ont-ils toujours chaud ?\n**Parce qu’ils ont une couverture**",
           "Où est-ce que les super héros vont-ils faire leurs courses ?\n**Au supermarché**",
           "Que se passe-t-il quand 2 poissons s'énervent ?\n**Le thon monte**",
           "Quel fruit est assez fort pour couper des arbres?\n**Le ci-tron**",
           "Quel est le jambon que tout le monde déteste ?\n**Le sale ami**",
           "Que fait un cendrier devant un ascenseur ?\n**Il veut des cendres**",
           "Que dit une imprimante dans l'eau ?\n**J’ai papier**",
           "Que dit une noisette quand elle tombe à l'eau ?\n**Je me noix**",
           "Quel est le sport préféré des insectes?\n**Le criquet**",
           "Il existe un point commun entre les noirs et les crèmes. Le connaissez-vous ?\n "
           "**C’est meilleur quand c’est fouetté**",
           "Que fait un DJ djihadiste ?\n**Il fait péter le son.**",
           "Qu'est-ce qu'un enfant de chœur encore puceau ?\n**Un enfant qui court plus vite que le prêtre.**",
           "Quel est la dernière chose que Lady Di a mangé ?\n**Le tableau de bord**",
           "J'ai vu un enfant sur un vélo hier, j'ai d'abord cru que c'était le mien.\n"
           "**Alors j'ai vérifié dans le garage et il était toujours là, enchaîné, à réclamer à boire et à manger.**",
           "Comment s'appelle le cul de la schtroumpfette ?\n**La blu-ray**",
           "Moi je voudrais mourir comme mon grand-père, il est mort pendant son sommeil, il n'a rien senti."
           "Ca c'est une belle mort !\n**Je ne voudrais surtout pas mourir en paniquant, en gesticulant et en criant "
           "comme tous les autres passagers dans sa voiture.**",
           "Pourquoi New York a un désavantage aux échecs?\n**Parce qu'ils ont déjà perdu deux tours**",
           "C'est l’histoire d’un zoophile qui prends son élan",
           "Quel est le tigre qui nage le moins vite ?\n**Le petigregory**",
           "-Bonne nuit mon cœur\n-Maman laisse la lumière allumer j'ai peur du noir\n"
           "**-Mais non tkt pas il est bien attaché**",
           "Si deux sourds se battent, peut on appeler ça un malentendu ?",
           "Pourquoi les femmes aiment jouer à among us ?\n**Car là au moins elles ont le droit de vote**",
           "Qu’est ce qui est mieux que de gagner la médaille d'or aux jeux paralympiques ?\n**Marcher.**",
           "Quel est le point commun entre une meuf de 14 ans enceinte et son bébé ?\n"
           '**Les deux se disent "putain ma mère va me tuer**"',
           "Qu'y a t'il de plus merveilleux que de faire tourner un enfant sur un tourniquet?\n"
           "**C'est de l'arrêter avec une pelle**",
           "C l’histoire d’une petite fille qui n a pas de bras. \n-Toc Toc \n-C qui?\n**-Pas la petite fille**",
           "Il y a Mohamed et Rachid dans une voiture qui conduit ?\n**La police**",
           "Comment on appelle un boomerang qui reviens pas ?\n**Un chat mort**",
           "Qu est ce qui est pire que trouvé deux bébé dans un sac poubelle ?\n"
           "**En trouve un dans deux sac poubelle**",
           "Comment s'appelle une photo de famille d'un orphelin ?\n**Un selfie.**",
           "Pourquoi un orphelin ne peut pas utiliser un portable ?\n**Car il n'a pas l'option home.**",
           "Quel est le point commun entre les juifs et les chaussures ?\n**Y en avait plus en 39 qu en 45**",
           "Si tu vois un arabe tomber avec une  moto rigole pas c'est ptet la tienne",
           "Pourquoi les arabes sont toujours les vainqueurs au triathlon ?\n"
           "**Car ils viennent à pied et repartent à vélo**",
           "Quel est le point commun entre un bébé et une pizza?\n**Quand c'est noir c'est raté**",
           "La disparition des girafes est un coup monté",
           "Grâce à quoi peut-on enlever le chewing-gum dans les cheveux \n**Le cancer.**",
           "Que dit un aveugle lorsqu'on lui donne du papier de verre ?\n**« C’est écrit serré. »**",
           "Qu'est-ce qu'un dinosaure gay?\n Un tripotanus"]


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


@bot.command()
# @commands.cooldown(1, 60, commands.BucketType.user)
async def shifumi(ctx, membre: discord.Member):
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
        choice_b = ""
        choice_a = ""


@shifumi.error
async def shifumi_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"TOUT DOUX LE LOUP !", description=f"Un shifumi est déjà lancé. Réessaie dans"
                                                                     f" {error.retry_after:.0f}s.")
        await ctx.send(embed=em)


@bot.command()
@commands.cooldown(1, 60, commands.BucketType.user)
async def debat(ctx, *args):
    """   Lance un débat sur la quetion que tu as posé !   """

    global debat_question, emojis, react_id, deb
    deb = True
    count_emoji['✅'] = 0
    count_emoji['❌'] = 0
    questionl = []
    for q in args:
        questionl.append(q)
        debat_question = " ".join(questionl)
        if debat_question.endswith("?"):
            pass
        else:
            debat_question += " ?"
    react = await ctx.send(f"Le débat du jour est: \n **{debat_question}** \n \n"
                           f"Votez dès à présent grâce aux réactions !")
    react_id = react.id
    print(react_id)
    for emoji in emojis:
        await react.add_reaction(emoji)
    await asyncio.sleep(60)
    await verif_deb(msg=ctx.message.channel)


@bot.event
async def on_raw_reaction_remove(payload):
    global react_id
    print("une réaction a été retirée")
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


@debat.error
async def debat_name_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"TOUT DOUX LE LOUP !", description=f"Un débat est déjà lancé. Réessaie dans"
                                                                     f" {error.retry_after:.0f}s.")
        await ctx.send(embed=em)


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
async def join(ctx):
    """   Le bot rejoint le vocal dans lequel tu es   """

    print("la commande *join a été utilisée")
    channel = ctx.author.voice.channel
    await channel.connect()


@bot.command()
async def SHEESH(message):
    """   SHEEEEEEEESH   """

    print("SHEEEESH")
    await message.channel.send("SHEEEEEEEEEEEEEEEEEEEESH !")


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

    shuffle(blagues)
    await ctx.send(blagues[0])


@bot.command()
async def disquette(ctx, membre: discord.Member):
    """   Envoie une disquette à la personne que tu mentionnes !   """

    print("Une disquette a été envoyée !")
    pseudo = membre.mention
    shuffle(disquettes)
    shuffle(images)
    await ctx.send("dis " + pseudo + disquettes[0] + " :smirk:")
    with open(images[0], "rb") as f:
        picture = discord.File(f)
        await ctx.send(file=picture)


@bot.command()
async def voyance(ctx, *args):
    """   Répond à la question que tu lui poses   """

    print("La voyante est en entretien !")
    global reponses
    question_a = args
    print(question_a)
    question_l = []
    for q_word in question_a:
        question_l.append(q_word)
    question = " ".join(question_l)
    pseudo = ctx.message.author.name
    shuffle(reponses)
    await ctx.send(f"**{pseudo}** m'a posé la question suivante: \n*{question}* \n \n**{reponses[1]}**")


@bot.command()
@has_permissions(manage_roles=True)
async def warning(ctx, membre: discord.Member):
    """   Met un avertissement au membre mentionné   """

    print("la commande warning a été utilisée")
    pseudo = membre.mention
    ident = membre.id

    # si la personne n'a pas de warn
    if ident == ctx.message.author.id:
        await ctx.send("Tu ne peux pas te warn toi même enfin ")
    elif ident == 831261319155417128:
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
async def on_message(message):
    mentioni = f'<@!{bot.user.id}>'
    mention = f'<@{bot.user.id}>'
    with open("logs", "a", encoding='utf-8') as file:
        file.write(f"{str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))} {message.author} dans {message.channel}: "
                   f"{message.content} \n")
        file.close()
    if message.content.startswith('*'):
        await bot.process_commands(message)
    if mention in message.content or mentioni in message.content:
        await message.channel.send("Que puis-je pour vous maître ?")


@bot.event
async def on_ready():
    print("Bot Prêt")
    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Activity(type=discord.ActivityType.listening, name="TU TU... TULULU..."))


# lancement du bot
print("Lancement du bot...")

# connecter au serveur
bot.run("TOKEN")
