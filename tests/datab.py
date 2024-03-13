import sqlite3

conn = sqlite3.connect('test_datab.db')
c = conn.cursor()

allowed_users = ['386254372646158338','278965321094660096']
#mit buchstaben am anfang funkts
users = ["manager", "autor"]

for user in allowed_users: #42
    c.execute(f'''
        CREATE TABLE IF NOT EXISTS {user} (
            user_id INTEGER,
            timestamp DATETIME,
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
conn.commit()