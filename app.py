import discord
from discord.ext import commands
import wdatabase
import os

TOKEN = os.environ.get('WLOOKUP_BOT_SECRET')


bot = commands.Bot(command_prefix='!w')

courses = wdatabase.CourseDB("courses.db")


@bot.command()
async def lookup(ctx, arg):
    arg = arg.upper()
    course = courses.lookup(arg)
    id = course[1]
    title = course[4]
    units = course[5]
    desc = course[6]
    level = course[7]

    if course:
        embed = discord.Embed(title=arg, color=0xffd54f)
        embed.add_field(name=title, value=desc, inline=False)
        embed.add_field(name="ID", value=id, inline=True)
        embed.add_field(name="Units", value=units, inline=True)
        embed.add_field(name="Academic Level", value=level, inline=True)

        await ctx.send(embed=embed)
    else:
        await ctx.send("Course '" + arg + "' not found")

bot.run(TOKEN)