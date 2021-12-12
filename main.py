# If you are running this file for the first time, then run it first to create "congif.json" and run it againg to get the values and run the bot 
import discord #pip install discord
from discord.ext import commands

import json # to Secure the token and create a database
import os # to create a json file if not there

# Creating a json file 
if os.path.exists(os.getcwd() + "/config.json"):
    with open("./config.json") as f:
        configData=json.load(f)

else:
    # Set the token value as your token for th bot
    configTemplate = {"Token":"", "Prefix":"!"}
    # Dumping the values in the json file
    with open(os.getcwd() + "/config.json", "w+") as f:
        json.dump(configTemplate,f)   

# Creating variables
token=configData["Token"]
prefix=configData['Prefix']

bot = commands.Bot(command_prefix=prefix)
bot.remove_command("help")# Removing Default Help Command

# Online indicator
@bot.event
async def on_ready():
    print("Bot Online as Gamer's Hall Bot#4493.")

# Ping Command
@bot.command()    
async def ping(ctx):
    latency = round(bot.latency*1000,1)# Rounding off the lantency of the bot
    await ctx.send(f"Pong! {latency}ms.")
    print("Message sent!")
#Hi Command
@bot.command()    
async def hi(ctx, member):
    await ctx.send(f"Hello! {member}.")
    print("Message sent!")
#Ban Command
@bot.command()   
@commands.has_permissions(ban_members=True) #Checking for permission
async def ban(ctx,member:discord.Member,*,reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"{member} has been banned for {reason}.")
    print(f"{member} banned for {reason}.")
#Kick Command
@bot.command()   
@commands.has_permissions(kick_members=True) 
async def kick(ctx,member:discord.Member,*,reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"{member} has been kicked for {reason}.")
    print(f"{member} kicked for {reason}.")
#Unban Command
@bot.command()   
@commands.has_permissions(ban_members=True) 
async def unban(ctx,*,member):
    bannedUsers=await ctx.guild.bans()
    name,discriminator=member.split("#")

    for ban in bannedUsers:
        user=ban.user
        if (user.name,user.discriminator) == (name,discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"{user.mention} was unbanned.")
            print(f"{user.mention} was ubanned")
            return
#User Info Command            
@bot.command()            
async def userinfo(ctx):
    user = ctx.author
    embed=discord.Embed(title="User Info",description=f"Here is the info we retrived about {user}",colour=user.colour)
    embed.set_thumbnail(url=user.avatar_url)
    embed.add_field(name="Name",value=user.name,inline=True)
    embed.add_field(name="Nick Name",value=user.nick,inline=True)
    embed.add_field(name="Id",value=user.id,inline=True)
    embed.add_field(name="Status",value=user.status,inline=True)
    embed.add_field(name="Top Role",value=user.top_role.name,inline=True)
    await ctx.send(embed=embed)
    print("User info sent")
#Help Command    
@bot.command()
async def help(ctx,commandNeed=None):
   if commandNeed != None:#Checking for targeted help
       for command in bot.commands:
           if command.name.lower() == commandNeed.lower():
               paramString=""
               for param in command.clean_params:
                   paramString += param + ", "
               paramString=paramString[:-2]    
               embed=discord.Embed(title=f"Help - {command.name}")
               embed.add_field(name="Parameters",value=paramString)
               await ctx.message.delete()
               await ctx.author.send(embed=embed)
               
       print("Custom help sent!.")
   else:     
    embed=discord.Embed(title="Help")
    embed.add_field(name="!ping",value="Gets the bot latency",inline=True)
    embed.add_field(name="!help",value="Shows this message")
    embed.add_field(name="!userinfo",value="Shows your info")
    embed.add_field(name="!hi",value="Sends a hi message to the specified person, Parameters: Member",inline=True)
    embed.add_field(name="!ban",value="Bans the specified person, Permissions: Ban Permission, Parameter: Member",inline=True)
    embed.add_field(name="!unban",value="Unbans the specified person, Permissions: Ban Permission, Parameter: Member",inline=True)
    embed.add_field(name="!kick",value="Kicks the specified person, Permissions: Kick Permission, Parameter: Member",inline=True)
    embed.add_field(name="!mute",value="Mutes the specified person, Permissiona: Mute Permission, Parameter: Member ",inline=True)
    embed.add_field(name="!unmute",value="Unmutes the specified person, Permissiona: Mute Permission, Parameter: Member ",inline=True)
    await ctx.message.delete()
    await ctx.author.send(embed=embed)
    print("Help sent!.")
#Mute Command    
@bot.command()
@commands.has_permissions(manage_messages=True)
async def mute(ctx,member:discord.Member,*,reason=None):
    guild=ctx.guild
    mutedRole=discord.utils.get(guild.roles,name="Muted")
    if not mutedRole:
        mutedRole=await guild.create_role(name="Muted")
        for channel in guild.channels:
            await channel.set_permissions(mutedRole,speak=False,send_messages=False,read_message_history=False,read_message=False)
    await member.add_roles(mutedRole,reason=reason) 
    await ctx.send(f"Muted {member} for reason {reason}")    
    await member.send(f"You were muted in the server {guild.name} for {reason}")   
    print(f"Muted {member} for {reason}")    
#Unmute Command    
@bot.command()
@commands.has_permissions(manage_messages=True)
async def unmute(ctx,member:discord.Member):
    mutedRole=discord.utils.get(ctx.guild.roles,name="Muted")
    await member.remove_roles(mutedRole)
    await ctx.send(f"Unmuted {member}")    
    await member.send(f"You were unmuted in the server {ctx.guild.name}")   
    print(f"Unmuted {member}") 
# Welcome Command
@bot.command()       
async def welcome(ctx,member:discord.Member):
    embed=discord.Embed(title="Welcome",colour=member.colour)
    embed.set_thumbnail(url=member.avatar_url)
    embed.add_field(name="User",value=member)
    embed.add_field(name="Welcome to our server",value=f"Hello, {member} welcome to our server, please read the rules once and stayed Tunned to uor event and register for them")
    embed.add_field(name="Enjoy",value="Enjoy Our Server")
    await ctx.send(embed=embed)
                
# Executing the bot
bot.run(token)    