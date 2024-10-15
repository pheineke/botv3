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

        self.db_path = './lib/data/db/user_activities.db'

        self.conn = sqlite3.connect(self.db_path)
        self.c = self.conn.cursor()
        
        self.create_empty_text_file("./lib/data/privacy_log.txt")

        self.get_allowed_users()
        # Tabelle für Benutzeraktivitäten erstellen
        self.create_user_db()
        for userid in self.allowed_users:
            self.add_user_to_user_db(userid)

        self.create_user_tables()

        self.check_activity_changes.start()



    def create_empty_text_file(self, file_path):
        if not os.path.exists(file_path):
            try:
                with open(file_path, 'w') as file:
                    pass  # Do nothing, creating an empty file
                print(f"Empty file created: {file_path}")
            except IOError as e:
                print(f"Error: {e}")

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
            #id = self.fetch_user_id(user)
            self.c.execute(f'''
                CREATE TABLE IF NOT EXISTS user_{user} (
                    user_id INTEGER,
                    timestamp TEXT,
                    accent_color TEXT,
                    activities TEXT,
                    activity TEXT,
                    avatar TEXT,
                    banner TEXT,
                    bot INTEGER,
                    color TEXT,
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

    def drop_table(self, table_name):
        self.conn = sqlite3.connect(self.db_path)
        cursor = self.conn.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        self.conn.commit()
        
    @tasks.loop(minutes=2)
    async def check_activity_changes(self):
        for guild in self.bot.guilds:
            for member in guild.members:
                if member.id in self.allowed_users:
                    previous_activity = self.get_previous_activity(member)
                    current_activity = self.get_current_activity(member)
                    compare:bool = self.compare_tuples_except_index(previous_activity, current_activity, 1)
                    print(f"Data collector - compare: {compare}")
                    if not(compare):
                        self.save_activity(member, current_activity)

    def compare_tuples_except_index(self, tuple1, tuple2, index_to_ignore):
        if not(tuple1):
            return False
        elif len(tuple1) != len(tuple2):
            return False
        
        for i in range(len(tuple1)):
            if i != index_to_ignore and tuple1[i] != tuple2[i]:
                return False
        return True
    
    def get_previous_activity(self, member):
        #id = self.fetch_user_id(member_id=member.id)
    # Manuell den Tabellennamen in die Abfrage einfügen
        query = f"SELECT * FROM user_{member.id} ORDER BY timestamp DESC LIMIT 1"
        self.c.execute(query)
        previous_activity = self.c.fetchone()
        return previous_activity


    def get_current_activity(self, member):
        user_id = member.id
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        accent_color = member.accent_color
        activities = [x for x in member.activities]
        activity = member.activity
        avatar = member.avatar 
        banner = member.banner 
        bot = member.bot 
        color = member.color
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
                str(activities),
                str(activity),
                str(avatar),
                str(banner),
                str(bot),
                str(color),
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
        #id = self.fetch_user_id(member_id=member.id)
        self.c.execute(f'''INSERT INTO user_{member.id} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', activity)
        self.conn.commit()


    def get_table_names(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table_names = cursor.fetchall()
        return [x[0] for x in table_names]
    
    def get_table_headers(self, table_name):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name})")
        headers = cursor.fetchall()
        return [header[1] for header in headers]

    @commands.command(brief="[DATA] Exportiert deine Daten yay .export_user_activity mit nichts, json oder db")
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
                    if str(ctx_author_id) in table:
                        author_table = table
                        break
                self.c.execute(f'''SELECT * FROM {author_table}''')
                
                if format_ == "json":
                    temp_dict_main = {}
                    user_activities = self.c.fetchall()
                    table_headers = self.get_table_headers(author_table)
                    for elem in user_activities:
                        for j in range(0,len(table_headers)):
                            temp_dict_main[table_headers[j]] = elem[j]
                        

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
                                activities TEXT,
                                activity TEXT,
                                avatar TEXT,
                                banner TEXT,
                                bot INTEGER,
                                color TEXT,
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
                        c_export.execute('''INSERT INTO user_activity VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', elem)
                    conn_export.commit()
                    conn_export.close()

                    # Nachricht senden
                    await ctx.send(file=discord.File(export_file))

                    # Datei löschen
                    os.remove(export_file)
            else:
                await ctx.send("User nicht vorhanden")

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
                file.write('')
                for elem in reaction_users:
                    file.write(f"{elem}\n")

            with open("privacy_log.txt", 'r') as file:
                liste = [int(x) for x in file.readlines()]
                self.allowed_users = liste
            

            self.add_user_to_user_db(user_id)
            self.create_user_tables()
            #TODO HIER EVTL ein ephemeral
            print(f"Users {liste}")

    def get_different_elements(self, list1, list2):
        # Convert lists to sets to get unique elements
        set1 = set(list1)
        set2 = set(list2)
        
        # Get the elements that are in set1 but not in set2
        diff1 = set1 - set2
        #print(diff1)
        # Get the elements that are in set2 but not in set1
        diff2 = set2 - set1
        #print(diff2)
        # Combine the two sets of different elements
        different_elements = diff1.union(diff2)
        #print(different_elements)
        
        return list(different_elements)

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

            with open("privacy_log.txt", 'r') as file:
                liste_old = [int(x) for x in file.readlines()]
            
            print(liste_old)
            difference = self.get_different_elements(liste_old, reaction_users)
            print(f"liste_old {liste_old} diff {difference}")
            len_difference = len(difference)

            with open("privacy_log.txt", 'w') as file:
                file.write('')
                for elem in reaction_users:
                    file.write(f"{elem}\n")

            with open("privacy_log.txt", 'r') as file:
                liste = [int(x) for x in file.readlines()]
                self.allowed_users = liste
            
            if len_difference == 1:
                self.drop_table(f"user_{difference[0]}")
            elif len_difference > 1:
                for user0 in difference:
                    print(f"DATA - diff users{difference}")
                    self.drop_table(f"user_{user0}")

            #TODO HIER EVTL ein ephemeral
            print(f"Users {liste}")



    @commands.command(brief="[DATA] Gibt Discord Userdaten aus.")
    async def getuserinfo(self, ctx, member: discord.Member = None):
        userdata = {
            "member": {
                "accent_color": member.accent_color,
                "activities": member.activities,
                "activity": member.activity,
                "avatar": member.avatar,
                "banner": member.banner,
                "bot": member.bot,
                "color": member.color,
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