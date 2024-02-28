import discord
from discord.ext import commands
import json
import os

class Data(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def getuserinfo(self, ctx):
        if not os.path.isdir("./userdata"):
            os.makedirs("./userdata")

        member = ctx.author
        userdata = {
            "member": {
                "accent_color": member.accent_color,
                "accent_colour": member.accent_colour,
                "activities": member.activities,
                "activity": member.activity,
                "avatar": member.avatar,
                "banner": member.banner,
                "bot": member.bot,
                "color": member.color,
                "colour": member.colour,
                "created_at": str(member.created_at),
                "default_avatar": member.default_avatar,
                "desktop_status": member.desktop_status,
                "discriminator": member.discriminator,
                "display_avatar": member.display_avatar,
                "display_icon": member.display_icon,
                "display_name": member.display_name,
                "dm_channel": member.dm_channel,
                "flags": member.flags,
                "global_name": member.global_name,
                "guild": member.guild,
                "guild_avatar": member.guild_avatar,
                "guild_permissions": member.guild_permissions,
                "id": member.id,
                "joined_at": str(member.joined_at),
                "mention": member.mention,
                "mobile_status": member.mobile_status,
                "mutual_guilds": member.mutual_guilds,
                "name": member.name,
                "nick": member.nick,
                "pending": member.pending,
                "premium_since": str(member.premium_since),
                "public_flags": member.public_flags,
                "raw_status": member.raw_status,
                "resolved_permissions": member.resolved_permissions,
                "roles": [x.name for x in member.roles if x.name != "@everyone"],
                "status": member.status,
                "system": member.system,
                "timed_out_until": str(member.timed_out_until),
                "web_status": member.web_status
            }
        }

        filedir = f'{os.getcwd}/userdata/{member.id}.txt'
        await ctx.send(filedir)
        with open(filedir, 'w') as file:
            file.write(json.dumps(userdata))
        
        await ctx.send(file=lambda: discord.File(f"./userdata/{member.id}.txt"))

        os.remove(f"./userdata/{member.id}.txt")
        
        

async def setup(bot):
    await bot.add_cog(Data(bot))