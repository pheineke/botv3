import json
import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.ui import Button, View

import pprint, sqlite3, os, tempfile
from datetime import datetime

class Data(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.allowed_users = []

        self.db_path = 'user_activities.db'

        self.conn = sqlite3.connect(self.db_path)
        self.c = self.conn.cursor()

        self.get_allowed_users()
        # Tabelle für Benutzeraktivitäten erstellen
        self.create_user_db()
        for userid in self.allowed_users:
            self.add_user_to_user_db(userid)

        self.create_user_tables()

        self.check_activity_changes.start()

    def get_allowed_users(self):
        with open("privacy_log.txt", 'r') as file:
            liste = [int(x) for x in file.readlines()]
            self.allowed_users = liste

    def create_user_db(self):
        self.c.execute(f'''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                member_id INTEGER
            )''')
        self.conn.commit()

    def add_user_to_user_db(self, member_id):
        # Überprüfen, ob die member_id bereits vorhanden ist
        self.c.execute("SELECT id FROM users WHERE member_id = ?", (member_id,))
        existing_id = self.c.fetchone()
        
        if existing_id:
            print("Member ID already exists")
            return  # Abbrechen, wenn die member_id bereits vorhanden ist

        # Wenn die member_id nicht vorhanden ist, fügen Sie sie hinzu
        self.c.execute("INSERT INTO users (member_id) VALUES (?)", (member_id,))
        self.conn.commit()
        

    def fetch_user_id(self, member_id):
        self.c.execute("SELECT id FROM users WHERE member_id = ?", (member_id,))
        result = self.c.fetchone()
        if result:
            return result[0]  # Rückgabe der gefundenen ID
        else:
            return None  # Falls keine Übereinstimmung gefunden wurde

    def create_user_tables(self):
        for user in self.allowed_users: #42
            id = self.fetch_user_id(user)
            self.c.execute(f'''
                CREATE TABLE IF NOT EXISTS user_00000{id} (
                    user_id INTEGER,
                    timestamp TEXT,
                    accent_color TEXT,
                    accent_colour TEXT,
                    activities TEXT,
                    activity TEXT,
                    avatar TEXT,
                    banner TEXT,
                    bot INTEGER,
                    color TEXT,
                    colour TEXT,
                    desktop_status TEXT,
                    display_avatar TEXT,
                    display_icon TEXT,
                    display_name TEXT,
                    flags TEXT,
                    global_name TEXT,
                    mention TEXT,
                    mobile_status TEXT,
                    mutual_guilds TEXT,
                    name TEXT,
                    nick TEXT,
                    premium_since TEXT,
                    public_flags TEXT,
                    raw_status TEXT,
                    resolved_permissions TEXT,
                    roles TEXT,
                    status TEXT,
                    system TEXT,
                    timed_out_until TEXT,
                    top_role TEXT,
                    voice TEXT,
                    web_status TEXT
                )
            ''')
            self.conn.commit()

    @tasks.loop(minutes=1)
    async def check_activity_changes(self):
        for guild in self.bot.guilds:
            for member in guild.members:
                if member.id in self.allowed_users:
                    previous_activity = self.get_previous_activity(member)
                    current_activity = self.get_current_activity(member)
                    if self.compare_tuples_except_index(previous_activity, current_activity, 1):
                        self.save_activity(member, current_activity)

    def compare_tuples_except_index(self, tuple1, tuple2, index_to_ignore):
        if len(tuple1) != len(tuple2):
            return False
        
        for i in range(len(tuple1)):
            if i != index_to_ignore and tuple1[i] != tuple2[i]:
                return False
        return True
    
    def get_previous_activity(self, member):
        id = self.fetch_user_id(member_id=member.id)
    # Manuell den Tabellennamen in die Abfrage einfügen
        query = f"SELECT * FROM user_00000{id} ORDER BY timestamp DESC LIMIT 1"
        self.c.execute(query)
        previous_activity = self.c.fetchone()
        return previous_activity


    def get_current_activity(self, member):
        user_id = member.id
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        accent_color = member.accent_color
        accent_colour = member.accent_colour 
        activities = [x for x in member.activities]
        activity = member.activity
        avatar = member.avatar 
        banner = member.banner 
        bot = member.bot 
        color = member.color 
        colour = member.colour 
        desktop_status = member.desktop_status 
        display_avatar = member.display_avatar 
        display_icon = member.display_icon 
        display_name = member.display_name
        flags = member.flags 
        global_name = member.global_name 
        mention = member.mention 
        mobile_status = member.mobile_status 
        mutual_guilds = member.mutual_guilds 
        name = member.name 
        nick = member.nick 
        premium_since = str(member.premium_since) 
        public_flags = member.public_flags 
        raw_status = member.raw_status 
        resolved_permissions = member.resolved_permissions 
        roles = member.roles 
        status = member.status 
        system = member.system 
        timed_out_until = str(member.timed_out_until) 
        top_role = member.top_role 
        voice = member.voice 
        web_status = member.web_status

        return (user_id,
                timestamp,
                str(accent_color),
                str(accent_colour),
                str(activities),
                str(activity),
                str(avatar),
                str(banner),
                str(bot),
                str(color),
                str(colour),
                str(desktop_status),
                str(display_avatar),
                str(display_icon),
                str(display_name),
                str(flags),
                str(global_name),
                str(mention),
                str(mobile_status),
                str(mutual_guilds),
                str(name),
                str(nick),
                str(premium_since),
                str(public_flags),
                str(raw_status),
                str(resolved_permissions),
                str(roles),
                str(status),
                str(system),
                str(timed_out_until),
                str(top_role),
                str(voice),
                str(web_status))


    def save_activity(self, member, activity):
        id = self.fetch_user_id(member_id=member.id)
        self.c.execute(f'''INSERT INTO user_00000{id} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', activity)
        self.conn.commit()


    def get_table_names(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table_names = cursor.fetchall()
        conn.close()
        return [x[0] for x in table_names]
    
    def get_table_headers(self, table_name):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name})")
        headers = cursor.fetchall()
        conn.close()
        return [header[1] for header in headers]

    @commands.command()
    async def export_user_activity(self, ctx, format_="json"):
        if not (format_ in ["db", "json"]):
            await ctx.send("Ungültiges Dateiformat: either json or db")
        else:
            # Daten aus der Datenbank abrufen
            user_activities = []
            ctx_author_id = ctx.author.id
            if ctx_author_id in self.allowed_users:
                id = self.fetch_user_id(ctx_author_id)
                for table in self.get_table_names():
                    if "user_" in table:
                        userid = table.split('_')[1]
                        if int(id) == int(userid):
                            author_table = table
                            break
                self.c.execute(f'''SELECT * FROM {author_table}''')
                
                if format_ == "json":
                    temp_dict_main = {}
                    user_activities = self.c.fetchall()
                    table_headers = self.get_table_headers(author_table)
                    for elem in user_activities:
                        for j in range(0,len(table_headers)):
                            print(elem[j])
                            print(table_headers[j])
                            temp_dict_elem = {}
                            temp_dict_elem[table_headers[j]] = elem[j]
                            temp_dict_main[j] = temp_dict_elem
                        

                    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=f".{format_}") as temp_file:
                        json.dump(temp_dict_main,temp_file, indent=2)
                    try:
                        await ctx.author.send(file=discord.File(temp_file.name))
                        await ctx.send(f"Daten wurden dir in {format_} per DM gesendet, {ctx.author.mention}")
                    finally:
                        temp_file.close()
                else:
                    user_activities.extend(self.c.fetchall())
                    # Dateiname für den Export
                    export_file = f'{ctx.author.id}_activity_export.db'

                    # Neue Datenbank erstellen und Daten einfügen
                    conn_export = sqlite3.connect(export_file)
                    c_export = conn_export.cursor()

                    c_export.execute(f'''
                            CREATE TABLE IF NOT EXISTS user_activity (
                                user_id INTEGER,
                                timestamp TEXT,
                                accent_color TEXT,
                                accent_colour TEXT,
                                activities TEXT,
                                activity TEXT,
                                avatar TEXT,
                                banner TEXT,
                                bot INTEGER,
                                color TEXT,
                                colour TEXT,
                                desktop_status TEXT,
                                display_avatar TEXT,
                                display_icon TEXT,
                                display_name TEXT,
                                flags TEXT,
                                global_name TEXT,
                                mention TEXT,
                                mobile_status TEXT,
                                mutual_guilds TEXT,
                                name TEXT,
                                nick TEXT,
                                premium_since TEXT,
                                public_flags TEXT,
                                raw_status TEXT,
                                resolved_permissions TEXT,
                                roles TEXT,
                                status TEXT,
                                system TEXT,
                                timed_out_until TEXT,
                                top_role TEXT,
                                voice TEXT,
                                web_status TEXT
                            )
                        ''')

                    for elem in user_activities:
                        c_export.execute('''INSERT INTO user_activity VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', elem)
                    conn_export.commit()
                    conn_export.close()

                    # Nachricht senden
                    await ctx.send(file=discord.File(export_file))

                    # Datei löschen
                    os.remove(export_file)
            else:
                await ctx.send("User nicht vorhanden")

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