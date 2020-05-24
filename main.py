import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import youtube_dl
import re
import json
import os.path

FILENAME = 'data.json'



MAX_WORDS = 100

client = commands.Bot(command_prefix='.')
client.remove_command('help')

def load_words(filename):
    if not os.path.isfile(filename):
        return {}

    with open(filename, encoding='utf-8') as json_file:
        data = json.load(json_file)
    
    return data

def save_words(data, filename):
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False)

    return True



data = load_words(FILENAME)

@client.event
async def on_message(message):
    args = message.content.split()

    # 봇이 채팅 치면 skip
    if message.author == client.user:
        return

    prefix = args[0]

    if prefix != "무군아":
        return

    command = args[1] if len(args) > 1 else []
    parameters = args[2:] if len(args) > 2 else []

    if not command:
        e = discord.Embed(title="왜 부르냐 인간", colour=0x8AF7FF)
        await client.send_message(message.channel, embed=e)

    elif command == "개발자":
        em = discord.Embed(title="개발자는 무군MG#9978 입니다!", colour=0xDEADBF)
        em.add_field(name="공동 개발자를 구합니다!", value="무군MG#9978로 문의주세요")
        await client.send_message(message.channel, embed=em)
        return
    
    elif command == "업뎃":
        em = discord.Embed(title="무군봇 1.5 업데이트", colour=0xDEADBF)
        em.set_author(name="무군봇 패치 내역", icon_url="https://cdn.discordapp.com/attachments/712645622607380482/713327725288357889/KakaoTalk_20200319_154506750.jpg")
        em.add_field(name="무군봇 항시 운영", value="무군봇이 앞으로는 24시간 운영됩니다! 불쌍한 녀석...")
        em.add_field(name="무군봇 호스팅", value="무군봇이 무군의 컴퓨터가 아닌 Github에게 맡겨졌습니다")
        em.add_field(name="무군봇이 단어를 기억못하는 오류 수정", value="무군봇에게 가르친 단어를 무군봇이 기억 못하는 오류를 수정했습니다")
        await client.send_message(message.channel, embed=em)

    elif command == "안녕?":
        em = discord.Embed(title="안녕하세요?", colour=0xDEADBF)
        em.add_field(name="공동 개발자를 구합니다!", value="무군MG#9978로 문의주세요")
        await client.send_message(message.channel, embed=em)
        return

    elif command == "초대":
        em = discord.Embed(title="여기를 클릭해 주세요", url="https://discord.com/oauth2/authorize?client_id=712558279469039637&permissions=3468352&scope=bot", colour=0xDEADBF)
        await client.send_message(message.channel, embed=em)
        return

    elif command == "도움":
        aem = discord.Embed(title="도움말",description="명령어 목록", colour=0x8AF7FF)
        aem.set_author(name="무군봇 도움말", icon_url="https://cdn.discordapp.com/attachments/712645622607380482/713327725288357889/KakaoTalk_20200319_154506750.jpg")
        aem.set_thumbnail(url="https://cdn.discordapp.com/attachments/712645622607380482/713327725288357889/KakaoTalk_20200319_154506750.jpg")
        aem.add_field(name="무군아 안녕?",value="무군봇에게 인사합니다", inline=False)
        aem.add_field(name="무군아 배워 <단어> <내용>",value="무군봇을 가르칩니다\n이미 알고있는 내용은 새로 배운 내용으로대채됩니다", inline=False)
        aem.add_field(name="무군아 잊어 <단어>",value="무군봇에게 가르친 단어를 잊게 합니다",inline=False)
        aem.add_field(name="무군아 <단어>",value="무군봇에게 가르친 단어를 물어봅니다",inline=False)
        aem.add_field(name="무군아 초대",value="무군봇 초대링크를 받습니다",inline=False)
        aem.add_field(name="무군아 개발자",value="무군봇 개발자를 알아냅니다",inline=False)
        aem.add_field(name="무군아 업뎃",value="무군봇 업데이트 내역을 봅니다",inline=False)
        await client.send_message(message.channel, embed=aem)
        return

    elif command == "배워":
        if len(data) >= MAX_WORDS:
            one = discord.Embed(title="흐에...너무 많이 알고 있어요...못외우겠어요 죄송해요...", colour=0x8AF7FF)
            await client.send_message(message.channel, embed=one)
            return

        if len(parameters) < 2:
            one = discord.Embed(title="뭘 배우라는거냐 인간 똑바로 말해라", colour=0x8AF7FF)
            await client.send_message(message.channel, embed=one)
            return

        word, text = parameters[0], ' '.join(parameters[1:])

        if word in data:
            one = discord.Embed(title="이미 {}(이)라고 배웠지만 바꿔주겠다 인간".format(data[word]), colour=0x8AF7FF)
            await client.send_message(message.channel, embed=one)
        else:
            one = discord.Embed(title="알겠다 인간 기억하도록 노력해보지", colour=0x8AF7FF)
            await client.send_message(message.channel, embed=one)
        
        data[word] = text
        
        
        
        save_words(data, FILENAME)
        return

    elif command == "잊어":

        if not parameters:
            dus = discord.Embed(title="뭘 잊어야할지 말해라 인간", colour=0x8AF7FF)
            await client.send_message(message.channel, embed=dus)
            return

        word = parameters[0]

        if word not in data:
            f = discord.Embed(title="원래부터 그런 단어는 몰랐다 인간", colour=0x8AF7FF)
            await client.send_message(message.channel, embed=f)
            return

        del data[word]
        s = discord.Embed(title="{}을(를) 잊어버렸다 인간...외우라고 했다가 잊으라니 너무하군" .format(word), colour=0x8AF7FF)
        await client.send_message(message.channel, embed=s)

        save_words(data, FILENAME)
        return



    else:
        word = command

        if word not in data:
            a = discord.Embed(title="뭐라는거냐 인간 내가 아는걸 말해라", colour=0x8AF7FF)
            await client.send_message(message.channel, embed=a)
            return
        
        else:
            aaem = discord.Embed(title=data[word], colour=0x8AF7FF)
            await client.send_message(message.channel, embed=aaem)
            return




@client.event
async def on_ready():
    print("다음으로 로그인합니다 : ")
    print(client.user.name)
    print(client.user.id)
    print("==========")
    await client.change_presence(game=discord.Game(name="도움말은 '무군아 도움'을 입력해!", type=1))


access_token = os.environ["BOT_TOKEN"]
client.run(access_token)
