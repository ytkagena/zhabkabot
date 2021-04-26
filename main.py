import json
import os
import youtube_dl
import discord
import ffmpeg
from random import randrange, choice
from discord.ext import commands
from set import settings
from SETTINGS import *
import requests

bot = commands.Bot(command_prefix=settings['prefix'])


class RandomThings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='помощь')
    async def help(self, ctx):
        await ctx.send('Доступные команды: жребий, число, кости, котик, подбодри, кмн, анекдот, панда, мем, обнимашки')

    @commands.command(name='кости')
    async def roll_dice(self, ctx, count):
        res = [choice(dashes) for _ in range(int(count))]
        await ctx.send(" ".join(res))

    @commands.command(name='число')
    async def my_randint(self, ctx, min_int, max_int):
        num = randrange(int(min_int), int(max_int))
        await ctx.send(num)

    @commands.command(name='жребий')
    async def new_bet(self, ctx, word):
        bet = choice(bets)
        await ctx.send(bet)
        if bet == word:
            await ctx.send('вы выиграли')
        else:
            await ctx.send('вы проиграли')

    @commands.command(name='привет')
    async def hello(self, ctx):
        await ctx.send('Приветствую тебя')

    @commands.command(name='пока')
    async def bye(self, ctx):
        await ctx.send('До скорой встречи')

    @commands.command(name='подбодри')
    async def sad(self, ctx):
        sad = choice(sadness)
        await ctx.send(sad)

    @commands.command(name='анекдот')
    async def funny(self, ctx):
        fun = choice(jokes)
        await ctx.send(fun)

    @commands.command(name='кмн')
    async def kmn(self, ctx, word):
        bot_word = choice(kmn)
        await ctx.send(bot_word)
        if word == 'камень' and bot_word == 'ножницы' or word == 'ножницы' and bot_word == 'бумага' or word == 'бумага'\
            and bot_word == 'камень':
                await ctx.send('вы выиграли')
        elif word == bot_word:
            await ctx.send('ничья')
        else:
            await ctx.send('бот победил')

    @commands.command(name='котик')
    async def cat(self, ctx):
        response = requests.get('https://some-random-api.ml/img/cat')
        json_data = json.loads(response.text)

        embed = discord.Embed(color=0xff9900, title='Бодрящий котик')
        embed.set_image(url=json_data['link'])
        await ctx.send(embed=embed)

    @commands.command(name='панда')
    async def panda(self, ctx):
        response = requests.get('https://some-random-api.ml/img/panda')
        json_data = json.loads(response.text)

        embed = discord.Embed(color=0xff9900, title='Панда')
        embed.set_image(url=json_data['link'])
        await ctx.send(embed=embed)

    @commands.command(name='мем')
    async def meme(self, ctx):
        response = requests.get('https://some-random-api.ml/meme')
        json_data = json.loads(response.text)

        embed = discord.Embed(color=0xff9900, title='Meme')
        embed.set_image(url=json_data['image'])
        await ctx.send(embed=embed)

    @commands.command(name='обнимашки')
    async def hug(self, ctx):
        response = requests.get('https://some-random-api.ml/animu/hug')
        json_data = json.loads(response.text)

        embed = discord.Embed(color=0xff9900, title='Обнимашки')
        embed.set_image(url=json_data['link'])
        await ctx.send(embed=embed)

    @commands.command(name='эхо')
    async def echo(self, ctx, *, content: str):
        await ctx.send(content)

    @commands.command(name='вероятность')
    async def chance(self, ctx):
        num = randrange(0, 100)
        await ctx.send('Вероятность этого: {} %!'.format(num))

    @commands.command(name='реверс')
    async def reverse(self, ctx, *, content: str):
        await ctx.send(content[::-1])

    @commands.command(name='сервер')
    async def fetchServerInfo(self, context):
        guild = context.guild

        await context.send(f'Имя сервера: {guild.name}')
        await context.send(f'Количество участников: {len(guild.members)}')

    @commands.command(name='предсказание')
    async def prediction(self, ctx, *, question):
        await ctx.send(f'Ваш вопрос: {question}\nОтвет на него: {choice(responses)}')

    @commands.command(name='очистка')
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount)


@bot.event
async def on_message(ctx, message):
    for i in ban_words:
        if i in message.content.lower():
            await ctx.channel.purge(limit=1)
            await message.channel.send("нельзя так выражаться")
        await bot.process_commands(message)


@bot.command()
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send('Пользователь успешно кикнут')


@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send('Пользователь успешно забанен')


@bot.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Разбанен {user.mention}')
            return


@bot.event
async def on_message(message):
    if message.content.lower() == "привет":
        await message.channel.send("приветствую")
    await bot.process_commands(message)


@bot.event
async def on_message(message):
    if message.content.lower() == "пока":
        await message.channel.send("хорошего дня")
    await bot.process_commands(message)


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game('Minecraft'))


@bot.event
async def on_member_join(member):
    print(f'{member} присоединился к серверу')


@bot.event
async def on_member_remove(member):
    print(f'{member} ушел с сервера')


@bot.command()
async def play(ctx, url : str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Подождите, пока музыка доиграет")
        return

    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='Основной')
    await voiceChannel.connect()
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))


@bot.command()
async def leave(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("Бот не подключен к голосовому каналу.")


@bot.command()
async def pause(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("На данный момент ничего не играет.")


@bot.command()
async def resume(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("Аудио не на паузе.")


@bot.command()
async def stop(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    voice.stop()


bot.add_cog(RandomThings(bot))
bot.run(settings['token'])
