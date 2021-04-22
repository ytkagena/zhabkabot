import discord
from random import randrange, choice
from discord.ext import commands
from set import settings
from SETTINGS import *
import requests
import json

bot = commands.Bot(command_prefix=settings['prefix'])


class RandomThings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='помощь')
    async def help(self, ctx):
        await ctx.send('Доступные команды: жребий, число, кости, котик, подбодри, кмн, привет, пока')

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


@bot.event
async def ready():
    print('Bot Online!')


bot.add_cog(RandomThings(bot))
bot.run(settings['token'])
