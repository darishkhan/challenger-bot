

# import datetime
import discord
# from pymongo import MongoClient
from discord.ext import commands


# import os
# token = os.environ['TOKEN']

TOKEN='MTA1NjIyMDAyMzMzMDQ0MzMxNA.GQKimB.aUGGfTuehg7A0o4gHlag0RVPW1aYaQUeovG-vA'

# client = discord.Client(intents=discord.Intents.default())
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
# CONNECTION_STRING = "mongodb+srv://darishkhan:darish155@cluster0.t4zer74.mongodb.net/?retryWrites=true&w=majority"

@bot.event
async def on_ready():
  print(f"Bot is online -> {bot.user}")


# @bot.command()
# async def ping(ctx):
#   await ctx.reply("pong")


@bot.event
async def on_message(message):
    # print(f"Yes")

    if message.author == bot.user:
        return 

    username = str(message.author)
    user_message = str(message.content)
    channel = str(message.channel)


    print(f"{username} said: {user_message} ({channel})")
    if(message.content.startswith('hi')):
        await message.channel.send('chal nikal')

    if(user_message.startswith('$man')):
      s = '''  
            ## Avilable commands :
                `$man` -> Show manual.
                `$add_me` -> Add user in database. [ nothing happens if user already added ]
                `$flag [id] [flag]` -> command for submitting flag. [ flag must be in format `njack{text}` ]
                                       this command is only accessible in private messgae/dm mode.
                `$show_leaderboard` -> show leaderboard. [ coming soon ]
                `$my_score` -> show your score. [ coming soon ]
                `$show_challenge` -> show active challenges. 
        '''
      await message.channel.send(s)

    if(user_message.startswith('$add_me')):
      if(message.channel.type == discord.ChannelType.private):
        await message.channel.send("This command can not be used in private chat.")


    if(user_message.startswith('$flag')):
      print(message.channel.type)
      if(message.channel.type != discord.ChannelType.private):
        await message.channel.send("This command can only be used in private messages!")
        return
      else: 
        await message.channel.send("OK")
        # add karo yahan pe

    if(user_message.startswith('$show_leaderboard')):
      await message.channel.send("will show leaderboard.")

    if(user_message.startswith('$my_score')):
      await message.channel.send('Your score: 0')

    if(user_message.startswith('$show_challenge')):
      await message.channel.send('Will add challenges soon!')



    


bot.run(TOKEN)













#   if message.author == client.user:
#     return 

#   if message.content.startswith('$man'):
#     s = '''  
#             ## Avilable commands :
#                 `$add-me` -> Add user in database. [ nothing happens if user already added ]
#                 `$flag [id] [flag]` -> command for submitting flag. [ flag must be in format `njack{text}` ]
#                                        this command is only accessible in private messgae/dm mode.
#                 `$showleaderboard` -> show leaderboard. [ coming soon ]
#                 `$myscore` -> show your score. [ coming soon ]
#                 `$showchallange` -> show active challange. 
#         '''
#     await message.channel.send(s)

#   if message.content.startswith('$flag'):
#     print(message.channel.type)    
#     if (message.channel.type != discord.ChannelType.private):
#       await message.channel.send("This command can only be used in private messages!")
#       return
#     else:
#       request = message.content
#       print(request)
#       l = request.split(' ')
#       dbclient = MongoClient(CONNECTION_STRING)
#       db = dbclient['CSec']
#       collection = db['challenge']
#       question_code = l[1]
#       res = collection.find_one({'status':'active'},{f"problems.{question_code}.flag" : 1 ,f"problems.{question_code}.score" : 1})
#       if res == None:
#         await message.channel.send("Challange not found!")
#         return
#       else:
#         print(l)
#         if( str(l[2]) == str(res['problems'][question_code]['flag'])):
#           coll_users = db['users']
#           res2 = coll_users.find_one({'id':message.author.id})
#           if res2 == None:
#             await message.channel.send("You are not registered!")
#             return
#           else:
#             if res2['scores'][question_code] == res['problems'][question_code]['score']:
#               await message.channel.send("You already solved this question!")
#               return
#             else:
#               total_score = res2['total_score'] + res['problems'][question_code]['score']
#               coll_users.update_one({'id':message.author.id},{'$set':{f"scores.{question_code}":res['problems'][question_code]['score'],'total_score':total_score}})
#               await message.channel.send(f"Flag is correct! Your totalscore is {total_score}")
#               return
#         else:
#           await message.channel.send("Incorret flag!")
#           return

#   if message.content.startswith('$add-me'):
#     if (message.channel.type == discord.ChannelType.private):
#       dbclient = MongoClient(CONNECTION_STRING)
#       db = dbclient['CSec']
#       collection = db['User']
#       user = collection.find_one({'id': message.author.id})
#       if user == None:
#         now = datetime.datetime.now()
#         hacker = {
#           'name': message.author.name,
#           'id': message.author.id,
#           'total-score': 0,
#           'scores':{},
#           'best-score': 0,
#           'score-history': {},
#           'role': 'user',
#           'flags': {},
#           'created-at': now
#         }
#         collection.insert_one(hacker)
#         s = "User added!"
#       else:
#         s = "User already added!"
#       await message.channel.send(s)
#     else:
#       await message.channel.send("This command can not be used in private messages!")

#   if message.content.startswith('$show_Challange'):
#     dbclient = MongoClient(CONNECTION_STRING)
#     db = dbclient['CSec']
#     collection = db['challenge']
#     problems = collection.find_one({"status": "active"})
#     if (problems != None):
#       s = f'''
#       __**{problems['title']}**__  `[{problems['code']}]`
#       *{problems['description']}*
#       Files -> {problems['files']}
#       '''
#       l = len(problems['problems'])
#       print(l)
#       for i in range(1,l+1):
#         key = f"p{i}"
#         problem = problems['problems'][key]
#         s += f'''
#         __**{problem['title']}**__  `[{key}]`
#         `{problem['description']}`
#         Score -> {problem['score']}
#         '''
#       await message.channel.send(s)
#     else:
#       await message.channel.send("No active challange!")

# client.run('OTM3MzgwNTk1MDcwMjkyMDE4.Yfa5tQ.jfoXx6JHC23mbSc5p-ZAspqEQcU')