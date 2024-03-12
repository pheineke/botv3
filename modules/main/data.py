import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.ui import Button, View

import pprint, sqlite3, os
from datetime import datetime

class Data(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.allowed_users = []

        self.conn = sqlite3.connect('user_activities.db')
        self.c = self.conn.cursor()

        # Tabelle für Benutzeraktivitäten erstellen
        self.get_allowed_users()
        
        for user in self.allowed_users:
            self.c.execute(f'''CREATE TABLE IF NOT EXISTS {user} (
                            user_id INT,
                            timestamp DATETIME,
                            desktop_status TEXT,
                            mobile_status TEXT,
                            web_status TEXT,
                            game_activity TEXT,
                            name_changes INT,
                            server_name TEXT,
                            premium_status TEXT
                        )''')
            self.conn.commit()

        
        self.check_activity_changes.start()

    '''@tasks.loop(minutes=1.0)
    async def getdata(self, ctx:commands.Context):
        guild = ctx.guild

        users = [user for user in guild.members if user in self.users]
        async for users in users:
            pass'''
    
    def get_allowed_users(self):
        with open("privacy_log.txt", 'r') as file:
            liste = [int(x) for x in file.readlines()]
            self.allowed_users = liste
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self,payload:discord.RawReactionActionEvent):
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        user = await self.bot.fetch_user(payload.user_id)
        
        message_id = message.id
        user_id = user.id
        
        if message_id == 1217200712576929945:
            reaction_users = []
            for reaction in message.reactions:
                async for user in reaction.users():
                    reaction_users.append(user.id)

            with open("privacy_log.txt", 'w') as file:
                for elem in reaction_users:
                    file.write(f"{elem}\n")

            with open("privacy_log.txt", 'r') as file:
                liste = [int(x) for x in file.readlines()]
                self.allowed_users = liste

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self,payload:discord.RawReactionActionEvent):
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        user = await self.bot.fetch_user(payload.user_id)

        message_id = message.id
        
        if message_id == 1217200712576929945:
            reaction_users = []
            for reaction in message.reactions:
                async for user in reaction.users():
                    reaction_users.append(user.id)

            with open("privacy_log.txt", 'w') as file:
                for elem in reaction_users:
                    file.write(f"{elem}\n")

            with open("privacy_log.txt", 'r') as file:
                liste = [int(x) for x in file.readlines()]
                self.allowed_users = liste



    @tasks.loop(minutes=1)
    async def check_activity_changes(self):
        print(f"Works iguess\nself.allowed_users{self.allowed_users}")
        for guild in self.bot.guilds:
            for member in guild.members:
                if member.id in self.allowed_users:
                    # Überprüfen, ob sich die Aktivität des Benutzers geändert hat
                    previous_activity = self.get_previous_activity(member.id)
                    current_activity = self.get_current_activity(member)
                    if previous_activity != current_activity:
                        self.save_activity(member, current_activity)

    def get_previous_activity(self, user_id):
        self.c.execute('''SELECT * FROM user_activities WHERE user_id = ? ORDER BY timestamp DESC LIMIT 1''', (user_id,))
        previous_activity = self.c.fetchone()
        return previous_activity

    def get_current_activity(self, member):
        desktop_status = str(member.desktop_status)
        mobile_status = str(member.mobile_status)
        web_status = str(member.web_status)
        game_activity = str(member.activity.name) if member.activity else None
        name_changes = 1 if member.name != member.display_name else 0
        premium_status = 'Premium' if member.premium_since else 'Standard'
        return (member.id, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), desktop_status, mobile_status, web_status, game_activity, name_changes, premium_status)

    def save_activity(self, member, activity):
        self.c.execute('''INSERT INTO user_activities VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', activity)
        self.conn.commit()

    @commands.command()
    async def export_user_activity(self, ctx):
        # Daten aus der Datenbank abrufen
        self.c.execute('''SELECT * FROM user_activities''')
        user_activities = self.c.fetchall()

        # Dateiname für den Export
        export_file = 'user_activities_export.db'

        # Neue Datenbank erstellen und Daten einfügen
        conn_export = sqlite3.connect(export_file)
        c_export = conn_export.cursor()
        c_export.execute('''CREATE TABLE IF NOT EXISTS user_activities (
                                user_id INT,
                                timestamp DATETIME,
                                desktop_status TEXT,
                                mobile_status TEXT,
                                web_status TEXT,
                                game_activity TEXT,
                                name_changes INT,
                                
                                premium_status TEXT
                             )''')
        c_export.executemany('''INSERT INTO user_activities 
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', user_activities)
        conn_export.commit()
        conn_export.close()

        # Nachricht senden
        await ctx.send(file=discord.File(export_file))

        # Datei löschen
        os.remove(export_file)


    @commands.command(brief="[DATA] Gibt Discord Userdaten aus.")
    async def getuserinfo(self, ctx, member: discord.Member = None):
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
                "roles": member.roles,
                "status": member.status,
                "system": member.system,
                "timed_out_until": str(member.timed_out_until),
                "top_role": member.top_role,
                "voice": member.voice,
                "web_status": member.web_status
            }
        }

        pp = pprint.PrettyPrinter(indent=4)
        pp.pformat(userdata)

        filedir = f"./userdata/{member.id}.txt"
        with open(filedir, 'w') as file:
            file.write(f"{userdata}")
        
        await ctx.send(file=discord.File(filedir))
        
        

async def setup(bot):
    await bot.add_cog(Data(bot))