import discord
from discord.ext import commands
import wdatabase
import os

TOKEN = os.environ.get('WLOOKUP_BOT_SECRET')


bot = commands.Bot(command_prefix='!w')

courses = wdatabase.CourseDB("courses.db")


@bot.command()
async def info(ctx):
    embed = discord.Embed(title="Info", color=0xffd54f, description="This bot looks up information for Waterloo courses. Uses the Waterloo API (v2) for course information.")

    embed.add_field(name="`!winfo`", value="Get info about this bot.", inline=True)
    embed.add_field(name="`!wlookup course`", value="Looks up information for the course of the given name, if it exists.", inline=True)
    embed.add_field(name="`!wlookup partial", value="Provides a list of courses that start with the partial course name.", inline=True)
    embed.add_field(name="`!wlookup subject`", value="Provides a list of courses in the subject, and the number of results.", inline=True)

    embed.set_footer(text="Last Updated 2020-08-31")

    await ctx.send(embed=embed)


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
