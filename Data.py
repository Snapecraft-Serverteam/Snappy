import mysql.connector
import configparser
import string
import random

from Errors import PlayerFoundButNoDataError


class Database:
    def __init__(self, host: str, user: str, passwd: str, database: str):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.database = database

    def execute_query(self, query: str) -> tuple:
        database = mysql.connector.connect(host=self.host, user=self.user, passwd=self.passwd, database=self.database)
        cursor = database.cursor()
        cursor.execute(query)
        return cursor.fetchone()

    def execute_query_dict(self, query:str) -> dict:
        database = mysql.connector.connect(host=self.host, user=self.user, passwd=self.passwd, database=self.database)
        cursor = database.cursor(dictionary=True)
        cursor.execute(query)
        return cursor.fetchall()

    def insert_temp(self, mention:str, uuid:str, code:str):
        database = mysql.connector.connect(host=self.host, user=self.user, passwd=self.passwd, database=self.database)
        cursor = database.cursor()
        sql = "INSERT INTO `temp` (`discord`, `uuid`, `code`) VALUES (%s, %s, %s)"
        val = (mention, uuid, code)
        cursor.execute(sql, val)
        database.commit()

    def temp_exists_by_mention(self, mention: str) -> bool:
        return ''.join(map(str, self.execute_query("SELECT EXISTS(SELECT 1 FROM `temp` WHERE `discord`='" + mention + "')"))) == '1'

    def temp_exists_by_uuid(self, uuid: str):
        return ''.join(map(str, self.execute_query(
            "SELECT EXISTS(SELECT 1 FROM `temp` WHERE `uuid`='" + uuid + "')"))) == '1'

    def already_verified_by_mention(self, mention:str):
        return ''.join(map(str, self.execute_query(
            "SELECT EXISTS(SELECT 1 FROM `verified` WHERE `discord`='" + mention + "')"))) == '1'

    def already_verified_by_uuid(self, uuid: str):
        return ''.join(map(str, self.execute_query(
            "SELECT EXISTS(SELECT 1 FROM `verified` WHERE `uuid`='" + uuid + "')"))) == '1'

    def get_ontime(self, uuid: str, table: str) -> str:
        query_res = self.execute_query("SELECT `playtime` FROM `" + table + "` WHERE `player`='" + uuid + "' LIMIT 1")

        if not query_res:
            raise PlayerFoundButNoDataError

        return ''.join(map(str, query_res))

    def get_temp_data_by_mention(self, mention:str) -> tuple:
        return self.execute_query_dict("SELECT * FROM `temp` WHERE `discord`='" + mention + "'")[0]

    def create_temp_verfication(self, id:str, uuid: str, code: str):
        if not self.temp_exists_by_mention(id) and not self.temp_exists_by_uuid(uuid):
            if not self.already_verified_by_mention(id) and not self.already_verified_by_uuid(uuid):
                self.insert_temp(mention=id, uuid=uuid, code=code)
                return 0
            else:
                return 1  # already verified
        else:
            return 2  # already in temp

    def get_data(self):
        return self.execute_query_dict("SELECT * FROM `verified`")

    def delete_code(self, id:str, uuid:str):
        """ Useful, when the user forgot the code and wants to create a new one """
        database = mysql.connector.connect(host=self.host, user=self.user, passwd=self.passwd, database=self.database)
        cursor = database.cursor()
        sql = "DELETE FROM `temp` where `discord`=%s and `uuid`=%s LIMIT 1"
        val = (id, uuid)
        cursor.execute(sql, val)
        database.commit()


class OntimeConfig:
    config = configparser.ConfigParser()
    config.read("settings.ini")
    section = config['ontime']

    def get_db(self) -> str:
        return self.section['db']

    def get_host(self) -> str:
        return self.section['host']

    def get_user(self) -> str:
        return self.section['user']

    def get_passwd(self) -> str:
        return self.section['pw']

    def get_tables(self) -> list:
        return self.section['tables'].split(",")


class VerifyConfig:
    config = configparser.ConfigParser()
    config.read("settings.ini")
    section = config['verify']

    def get_db(self) -> str:
        return self.section['db']

    def get_host(self) -> str:
        return self.section['host']

    def get_user(self) -> str:
        return self.section['user']

    def get_passwd(self) -> str:
        return self.section['pw']


class RolesConfig:
    config = configparser.ConfigParser()
    config.read("settings.ini")
    section = config['roles']

    def get_roles(self) -> dict:
        return dict(self.section)

    def get_role(self, name) -> str:
        return self.section[name]


class CommonConfig:
    config = configparser.ConfigParser()
    config.read("settings.ini")
    section = config['guild']

    def get_guild_id(self):
        return self.section['guild_id']

    def get_verified_role(self):
        return self.section['verified_role']

    def get_general(self):
        return self.section['general']

    def get_update_interval(self):
        return self.section['update_interval']
    
    def get_brainstorm_channel(self):
        return self.section['brainstorm_channel']


class ServerlistConfig:
    config = configparser.ConfigParser()
    config.read("settings.ini")
    section = config['serverlist']

    def get_host(self):
        return self.section['host']

    def get_port(self):
        return self.section['port']

    def get_context(self):
        return self.section['context']


class TokenConfig:
    config = configparser.ConfigParser()
    config.read("token.ini")
    section = config['token']
    twitter = config['twitter']

    def get_token(self):
        return self.section['token']

    def get_twitter_tokens(self):
        return TwitterLoginInfos(
            self.twitter['apikey'],
            self.twitter['apisecret'],
            self.twitter['accesstoken'],
            self.twitter['accesstokensecret'],
        )



class Util:
    def id_generator(self, size: int, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def formatDate(self, time: str):
        millis = int(time)
        seconds = (millis / 1000) % 60
        seconds = int(seconds)
        minutes = (millis / (1000 * 60)) % 60
        minutes = int(minutes)
        hours = (millis / (1000 * 60 * 60)) % 24
        return "%dh %dmin" % (hours, minutes)


class TagConfig:
    config = configparser.ConfigParser()
    config.read("tag.ini")
    section = config['tags']

    def get_blocked(self) -> list:
        return list(self.config['blocked']['blocked'].split(","))

    def get_all_tags_with_paths(self) -> dict:
        return dict(self.config.items('tags'))

    def get_all_tags(self) -> list:
        return list(self.get_all_tags_with_paths().keys())

    def get_path_of_tag(self, tag) -> str:
        return self.section[tag]

    def get_tag(self, path) -> str:
        return str(open(path, encoding='utf-8').read())

    def add_tag_to_config(self, path, name):
        self.section[name] = path
        with open('tag.ini', 'w') as configfile:
            self.config.write(configfile)

    def get_min_role(self):
        return str(configparser.ConfigParser().read("settings.ini")['guild']['min_tag_role'])


class ModulesConfig:
    config = configparser.ConfigParser()
    config.read("settings.ini")
    section = config['modules']

    def is_enabled(self, name) -> bool:
        return self.section[name] == "true"

class TwitterLoginInfos:
    apikey = ""
    apisecret = ""
    accesstoken = ""
    accesstokensecret = ""
    def __init__(self, key, secret, token, tokensecret):
        self.apikey = key
        self.apisecret = secret
        self.accesstoken = token
        self.accesstokensecret = tokensecret
    def set_apikey(self, key):
        self.apikey = key
    def set_apiscrecet(self, key):
        self.apisecret = key
    def set_accesstoken(self, key):
        self.accesstoken = key
    def set_accesstokensecret(self, key):
        self.accesstokensecret = key
    def get_apikey(self):
        return self.apikey
    def get_apisecret(self):
        return self.apisecret
    def get_accesstoken(self):
        return self.accesstoken
    def get_accesstokensecret(self):
        return self.accesstokensecret

