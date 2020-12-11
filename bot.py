import os
import shutil
from asyncio import sleep

import discord
import random
import youtube_dl
from discord.utils import get

from discord.ext import commands

client = commands.Bot(command_prefix='?')
client.remove_command('help')
token = 'this is where the server token would be but due to privacy reasons, I removed mine'
listOfCommands = ["?god - prints a picture that embodies our server",
                  "?8ball - ask a question and you get an answer",
                  "?clear # - it clears # newest messages",
                  "?coinflip - flips a coin",
                  "?dm - the bot dms you something special",
                  "?msg [@] [message] - the bot dms the person your message",
                  "?spam - spams someone"]


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('with python code'))
    print("Bot is ready")


@client.event
async def on_member_join(ctx, member):
    await ctx.send((f'{member} has joined our beautiful server'))


@client.event
async def on_member_remove(ctx, member):
    await ctx.send((f'{member} is scared of us and unfortunately left'))

# @client.event
# async def on_message(message):
#     message.content = message.content.lower()
#     await client.process_commands(message)

@client.command()
async def god(ctx):
    await ctx.send(
        'https://cdn.discordapp.com/attachments/275009597759291392/322532460758040577/unknown.png')  # await makes the bot say something


@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    responses = ['Not even close baby', 'As I see it, yes.',
                 'Ask again later.',
                 'Better not tell you now.',
                 'Cannot predict now.',
                 'Concentrate and ask again.',
                 'Don’t count on it.',
                 'It is certain.',
                 'It is decidedly so.',
                 'Most likely.',
                 'My reply is no.',
                 'My sources say no.',
                 'Outlook not so good.',
                 'Outlook good.',
                 'Reply hazy, try again.',
                 'Signs point to yes.',
                 'Very doubtful.',
                 'Without a doubt.',
                 'Yes.',
                 'Yes – definitely.',
                 'You may rely on it.']
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')


@client.command()
async def clear(ctx, amount=1):
    await ctx.channel.purge(limit=amount + 1)


# @client.command()
# async def kick(ctx, member: discord.Member, *, reason=None):
#      await member.kick()

@client.command()
async def coinflip(ctx):
    flips = ['heads', 'tails']
    await ctx.send(f"Coin landed on {random.choice(flips)}")


@client.command()
async def dm(ctx):
    await ctx.author.send("Hello good sir")


@client.command()
async def msg(ctx, member: discord.Member, *, content):
    channel = await member.create_dm()
    await channel.send(content)
    await clear(ctx, 1)


@client.command()
async def spam(ctx, member: discord.Member, *, content):
    channel = await member.create_dm()
    await clear(ctx, 0)
    for i in range(10):
        await channel.send(content)
        await sleep(1)


@client.command(aliases=['help'])
async def _help(ctx):
    author = ctx.message.author
    embed = discord.Embed(colour=discord.Colour.green())
    embed.set_author(name='Help')
    embed.add_field(name='?god', value='Embodiment of our server', inline=False)
    embed.add_field(name='?8ball [question]', value='Ask a question and get an answer', inline=False)
    embed.add_field(name='?clear n', value='Clears n newest messages', inline=False)
    embed.add_field(name='?coinflip', value='Flip a coin', inline=False)
    embed.add_field(name='?dm', value='The bot dms you something special <3', inline=False)
    embed.add_field(name='?msg [@] [message]', value='Dm\'s the person[@] your message[message]', inline=False)
    embed.add_field(name='?spam', value='Spams someone', inline=False)
    embed.add_field(name='?play', value='Plays music', inline=False)
    embed.add_field(name='?pause', value='Pauses music', inline=False)
    embed.add_field(name='?resume', value='Resumes paused music', inline=False)
    embed.add_field(name='?stop', value='Stops music that\'s playing', inline=False)

    await ctx.author.send(embed=embed)

players = {}

@client.command()
async def join(ctx):
    global voice
    #channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if ctx.message.author.voice:
        channel = ctx.message.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("You are not connected to a voice channel")

@client.command()
async def leave(ctx):
    server = ctx.message.guild.voice_client
    await server.disconnect()


@client.command()
async def play(ctx, url: str):
    await join(ctx)
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            print("Removed old song file")
    except PermissionError:
        print("Trying to delete song file, but it's being played")
        await ctx.send("Error: Music is playing")
        return
    voice = get(client.voice_clients, guild=ctx.guild)
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading song now\n")
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed File: {file}")
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e:print(f"{name} has finished playing"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07 #this is the sound volume

    nname = name.rsplit("-", 2)
    await ctx.send(f"Playing {nname[0]}")
    print("Playing\n")

@client.command()
async def pause(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_playing():
        print("Music paused")
        voice.pause()
        await ctx.send("Paused")
    else:
        await ctx.send("Music isn't playing")

@client.command()
async def resume(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    if (voice and voice.is_paused()) or (voice and voice.is_stopped()):
        print("Music paused")
        voice.resume()
        await ctx.send("Resumed")
    else:
        await ctx.send("Music isn't paused")

@client.command()
async def stop(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_playing():
        print("Stopped")
        voice.stop()
        await ctx.send("Stopped")
    else:
        await ctx.send("Music isn't playing")

@client.command()
async def spam(ctx):
    for i in range(10):
        await join(ctx)
        await leave(ctx)



client.run(token)
