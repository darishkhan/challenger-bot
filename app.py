#import all required libraries
import datetime
import discord
from pymongo import MongoClient
import manual


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents = intents)
CONNECTION_STRING = ""


# notifies on terminal on when bot gets active.
@client.event
async def on_ready():
  print(f"Bot is online -> {client.user}")


# listens for a message in the server.
@client.event
async def on_message(message):

  # to prevent bot from replying to itself.
  if message.author == client.user:
    return 

  # if the user asks for the manual of bot.
  if message.content.startswith('$man'):
    s=manual.printman()
    await message.channel.send(s)


  # if the user is not yet added in the database
  if message.content.startswith('$add-me'):
    # command not to be used in private
    if (message.channel.type != discord.ChannelType.private):
      dbclient = MongoClient(CONNECTION_STRING)
      db = dbclient['CSec']
      collection = db['User']
      user = collection.find_one({'id': message.author.id})
      if user == None:
        now = datetime.datetime.now()
        hacker = {
          'name': message.author.name,
          'id': message.author.id,
          'total-score': 0,
          'scores':{},
          'best-score': 0,
          'score-history': {},
          'role': 'user',
          'flags': {},
          'created-at': now
        }
        collection.insert_one(hacker)
        s = "User added!"
      else:
        s = "User already added!"
    else:
      s="This command can not be used in private messages!"
    await message.channel.send(s)


  # if user submits a flag
  if message.content.startswith('$flag'):
    print(message.channel.type)   

    # not allowed to send flag in public so that others can't see the flag
    if (message.channel.type != discord.ChannelType.private):
      await message.channel.send("This command can only be used in private messages!")
      return

    # if the channel is private, then accept the flag and check whether it is correct.
    else:
      request = message.content
      print(request)
      l = request.split(' ')
      dbclient = MongoClient(CONNECTION_STRING)
      db = dbclient['CSec']
      collection = db['Challenges']
      question_code = l[1]
      res = collection.find_one({'status':'active'},{f"problems.{question_code}.flag" : 1 ,f"problems.{question_code}.score" : 1, f"problems.{question_code}.top-hackers": 1})
      if res == None:
        await message.channel.send("Challenge not found!")
        return
      else:
        print(l)
        if( str(l[2]) == str(res['problems'][question_code]['flag'])):
          coll_users = db['User']
          coll_challenges = db['Challenges']
          res2 = coll_users.find_one({'id':message.author.id})
          if res2 == None:
            await message.channel.send("You are not registered! Please use $add-me command first.")
            return
          else:
            if(message.author.id in res['problems'][question_code]['top-hackers']):
              await message.channel.send("You have already solved this question!")
              return
            else:
              total_score = res2['total-score'] + res['problems'][question_code]['score']
              coll_users.update_one({'id':message.author.id},{'$set':{'total-score':total_score}})
              coll_challenges.update_one({'status':'active'},  {'$push':{f"problems.{question_code}.top-hackers":message.author.id}})
              await message.channel.send(f"Flag is correct! Your totalscore is {total_score}")
              return
        else:
          await message.channel.send("Incorret flag!")
          return


  # display leaderboards
  if message.content.startswith('$show-leaderboards'):
    await message.channel.send("**__Current Standings: __**")
    dbclient = MongoClient(CONNECTION_STRING)
    db = dbclient['CSec']
    collection = db['User']
    res = collection.find({}, {"total-score":1, "name":1, "_id":0})

    #storing the name in a table and sorting by score
    table=[]
    for entry in res:
      table.append([entry['total-score'], entry['name']])
    table.sort(reverse=True)
    
    # this is to print the leaderboard in the chat with proper formatting
    i=0
    for entry in table:
      i+=1
      entry[1]=entry[1].upper()+(" "*(45-len(entry[1])))
      await message.channel.send(f"`> {i} |  {entry[1]}  | {entry[0]} `")
      if(i>5):
        break

  if message.content.startswith('$my-score'):
    dbclient = MongoClient(CONNECTION_STRING)
    db = dbclient['CSec']
    coll_users = db['User']
    res2 = coll_users.find_one({'id':message.author.id})
    if res2 == None:
      await message.channel.send("You are not registered! Please use $add-me command first.")
      return
    else:
      await message.channel.send(f"{res2['name'].upper()}'s score is : {res2['total-score']}")


  # if user wants to see challenges
  if message.content.startswith('$show-challenges'):
    print("Hey!")
    dbclient = MongoClient(CONNECTION_STRING)
    db = dbclient['CSec']
    collection = db['Challenges']
    problems = collection.find_one({"status":"active"})
    if (problems != None):
      s = f'''
      __**{problems['title']}**__  `[{problems['code']}]`
      *{problems['description']}*
      Files -> {problems['files']}
      '''
      l = len(problems['problems'])
      print(l)
      for i in range(1,l+1):
        key = f"p{i}"
        problem = problems['problems'][key]
        s += f'''
        __**{problem['title']}**__  `[{key}]`
        `{problem['description']}`
        Score -> {problem['score']}
        '''
      await message.channel.send(s)
    else:
      await message.channel.send("No active challenge!")


discord_token = ''
client.run(discord_token)
