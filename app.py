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

    if course:
        cid = course[1]
        title = course[4]
        units = course[5]
        desc = course[6]
        level = course[7]

        embed = discord.Embed(title=arg, color=0xffd54f)
        # embed.set_thumbnail(url='https://uwaterloo.ca/brand/sites/ca.brand/files/styles/body-500px-wide/public/uploads/images/university-of-waterloo-vertical-logo.png?itok=9KCQdLsy')
        embed.add_field(name=title, value=desc, inline=False)
        embed.add_field(name="ID", value=cid, inline=True)
        embed.add_field(name="Units", value=units, inline=True)
        embed.add_field(name="Academic Level", value=level, inline=True)

        await ctx.send(embed=embed)
    elif course_list:=courses.lookup_partial(arg):
        search_len = len(course_list)
        course_list = [course[8] for course in course_list]
        course_list = course_list[0:20]

        output = ""
        for course in course_list:
            output += course + ", "

        output = output[0:-2]
        if search_len > len(course_list):
            output += "..."

        embed = discord.Embed(title="Searches for " + arg, color=0xffd54f)
        embed.add_field(name="Results", value=output, inline=False)
        embed.add_field(name="Total Results", value=search_len)

        await ctx.send(embed=embed)
    else:
        await ctx.send("Course '" + arg + "' not found")


bot.run(TOKEN)
