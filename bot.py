import discord
from discord.ext import commands

import os
from asyncio.windows_events import NULL
from dotenv import load_dotenv

from typing import Union
import sqlite3

client = discord.Client(intents=discord.Intents.default())


bot = commands.Bot(
    command_prefix='',
    intents=discord.Intents.all()
)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command(name="1234")
async def _1234(ctx):
    await ctx.send("5678")

#설명서
@bot.command(name='!명령어')
async def howTodo(ctx):
    embed = discord.Embed(title = '짭니쿠다 설명서', color=0xFFE08C)
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/659428348883107870/873425790744805406/img.png')
    embed.add_field(name='!이모지추가 이모지이름 [원하는 이모지]', value='원하는 이모지를 원하는 명령어로 등록할 수 있어요.', inline=False)
    embed.add_field(name='!사진추가 이모지이름 (같이 사진파일 업로드)', value='원하는 사진도 원하는 명령어로 등록할 수 있어요.', inline=False)
    embed.add_field(name='!이모지목록 [검색어]', value='이모지 목록을 볼 수 있어요.(전체 목록은 검색어에 전체를 넣어주세요)', inline=False)
    embed.add_field(name='!이모지정보 이모지이름', value='등록된 이모지의 정보를 볼 수 있어요.', inline=False)
    embed.add_field(name='~ 이모지이름', value='등록한 이모지를 불러오세요.', inline=False)
    embed.set_footer(text='AngryBired', icon_url='https://cdn.discordapp.com/attachments/659428348883107870/873425519490773052/icon_10.png')
    msg = await ctx.send(embed=embed)



#이모지추가
@bot.command(name='!이모지추가')
async def add_emoji(ctx, arg, emoji: Union[discord.Emoji, discord.PartialEmoji]):
    if not emoji:
        return #await ctx.invoke(self.bot.get_command("help"), entity="emoji")

    try:
        print(emoji.url)
        conn = sqlite3.connect("d:/Code/Discord/Minikuda2/data/emoji_H.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO TABLE1(Emoji_name, link, user) VALUES(?,?,?)", (arg, str(emoji.url), str(ctx.message.author)))
        conn.commit()
        conn.close()
        await ctx.send(f"이모지 목록에 ~{arg} 이모지가 추가되었습니다.")

    except discord.NotFound :
        return await ctx.send("오류!")
        
    except sqlite3.IntegrityError :
        return await ctx.send("같은 이름의 이모지를 추가할 수 없습니다.")

@bot.command(name='!사진추가')
async def add_picture(ctx, arg):
    if ctx.message.attachments == NULL:
        return await ctx.send("사진 파일을 같이 올려주세요.")
    
    try:
        pic = ctx.message.attachments
        print(pic[0].url)
        conn = sqlite3.connect("d:/Code/Discord/Minikuda2/data/emoji_H.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO TABLE1(Emoji_name, link, user) VALUES(?,?,?)", (arg, str(pic[0].url), str(ctx.message.author)))
        conn.commit()
        conn.close()
        await ctx.send(f"이모지 목록에 ~{arg} 이모지가 추가되었습니다.")

    except discord.NotFound :
        return await ctx.send("오류!")
        
    except sqlite3.IntegrityError :
        return await ctx.send("같은 이름의 이모지를 추가할 수 없습니다.")


@bot.command(name='!이모지목록')
async def arrays(ctx, arg):
    conn = sqlite3.connect("d:/Code/Discord/Minikuda2/data/emoji_H.db")
    cursor = conn.cursor()

    if arg == '전체':
        search = ''
    else :
        search = arg

    cursor.execute('SELECT Emoji_name FROM table1 WHERE Emoji_name LIKE ?', ('%' + search + '%', ))
    results = cursor.fetchall()
    if len(results) == 0 :
        await ctx.send('아무 이모지도 검색되지 않았습니다.')
        return

    embed = discord.Embed(title='이모지 목록', description=str(', '.join(map(lambda x: x[0], results))) )
    msg = await ctx.send(embed=embed)
    conn.close()

@bot.command(name='!이모지정보')
async def emojiInfo(ctx, *, arg):
    conn = sqlite3.connect("d:/Code/Discord/Minikuda2/data/emoji_H.db")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM table1 WHERE Emoji_name=?', (arg,))

    temp = []
    temp = cursor.fetchall()
    #print(temp)
    if len(temp) == 0:
        msg = await ctx.send('이모지가 존재하지 않습니다.')
        return

    cursor.execute('SELECT link FROM table1 WHERE Emoji_name=?', (arg,))
    #print(cursor.fetchone())
    #msg = await ctx.send(str(cursor.fetchone()[0]))
    embed = discord.Embed(title='~'+arg)
    embed.set_image(url=str(cursor.fetchone()[0]))

    cursor.execute('SELECT user FROM table1 WHERE Emoji_name=?', (arg,))
    embed.set_footer(text='Added By '+str(cursor.fetchone()[0]))
    msg = await ctx.send(embed=embed)
    conn.close()

@bot.command(name='~')
async def emojiloader(ctx, *,arg):
    conn = sqlite3.connect("d:/Code/Discord/Minikuda2/data/emoji_H.db")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM table1 WHERE Emoji_name=?', (arg,))

    temp = []
    temp = cursor.fetchall()

    #print(temp)
    if len(temp) == 0:
        msg = await ctx.send('이모지가 존재하지 않습니다.')
        return

    cursor.execute('SELECT link FROM table1 WHERE Emoji_name=?', (arg,))
            
    #print(cursor.fetchone())
    #msg = await message.channel.send(str(cursor.fetchone()[0]))

    embed = discord.Embed()
    embed.set_image(url=str(cursor.fetchone()[0]))
    embed.set_author(name=str(ctx.message.author), icon_url=ctx.message.author.avatar)
    await ctx.message.delete()
    msg = await ctx.send(embed=embed)
    conn.close()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot.run(TOKEN)