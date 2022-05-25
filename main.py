from discord.ext import commands
import datetime
import psycopg2
import asyncio
import discord
import secreto
import random

TOKEN = secreto.TOKEN
DATABASE_URL = secreto.DATABASE_URL

bot = commands.Bot(command_prefix=',')
initial_extensions = ['comandos', 'ajuda', 'admin', 'cartas', 'beta', 'mensagens']

horario_local = datetime.timedelta(hours=-4)
fuso_horario = datetime.timezone(horario_local)

print(discord.__version__)


@bot.event
async def on_ready():
    agora = datetime.datetime.now(fuso_horario)
    print(f'Bot inicalizado em: {agora.strftime("%d/%m/%Y")}')
    print(f'Inicializado às: {agora.strftime("%H:%M")}')
    print(f'{bot.user.name} está pronto!')


@bot.event
async def on_member_join(member):
    print(f'Atualizando dados de: {member}')
    await update_data()


@bot.event
async def on_message(message: discord.Message):
    if message.author.id == bot.user.id:
        return

    conteudo = message.content.lower()
    resposta = None
    url = None
    cor = discord.Colour

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM resp_msg')
    tabela = cursor.fetchall()
    cursor.close()
    conn.close()

    linha_resp = []
    for linha in tabela:
        if conteudo == linha[1]:
            linha_resp = linha

    if linha_resp:
        resposta = random.choice(linha_resp[2]).format(message.author.name)

    elif conteudo.startswith('lolicon'):
        resposta = 'Você quis dizer _Emmanuel_'

    elif conteudo.startswith('tuturu'):
        url = 'https://www.myinstants.com/media/instants_images/1340305905201.png'
        cor = cor.blue()

    elif conteudo.startswith('fbi'):
        url = 'https://i.imgur.com/xAQw8pK.gif'
        cor = cor.red()

    elif conteudo.startswith('ayaya'):
        url = 'https://media1.tenor.com/images/baf2d324d696b8e0b08daa8cff5c8f12/tenor.gif'
        cor = cor.gold()

    elif conteudo.startswith('padoru'):
        url = 'https://thumbs.gfycat.com/CavernousLegitimateCobra-small.gif'
        cor = cor.red()

    elif conteudo.startswith('nep'):
        url = 'https://i.pinimg.com/originals/50/a0/cf/50a0cf8926f424e675213cf664f3cc85.png'
        cor = cor.purple()

    elif conteudo.startswith('abababa') or conteudo.startswith('awawawa'):
        url = 'https://media1.tenor.com/images/20c153e5797f8cb5fc66cfd2802311ae/tenor.gif'
        cor = cor.red()

    elif conteudo.startswith('stonks'):
        url = 'https://i.ytimg.com/vi/if-2M3K1tqk/maxresdefault.jpg'
        cor = cor.blue

    elif conteudo.startswith('not stonks'):
        url = 'https://i.imgflip.com/35a1ly.jpg'
        cor = cor.red()

    elif conteudo.startswith('confused stonks'):
        url = 'https://i.imgflip.com/3ddsdr.jpg'
        cor = cor.green()

    elif conteudo.startswith('nico nico ni'):
        url = 'https://media.giphy.com/media/ZLr299JYCUEHm/giphy.gif'
        cor = cor.blue()

    if resposta:
        await message.channel.send(resposta)
    elif url:
        embed = discord.Embed(colour=cor)
        embed.set_image(url=url)
        await message.channel.send(embed=embed)

    await bot.process_commands(message)


@bot.event
async def at_specific_time():
    await bot.wait_until_ready()
    while not bot.is_closed():
        channel = bot.get_channel(659261108489682944)
        agora = datetime.datetime.now(fuso_horario)
        now_h = agora.hour
        now_m = agora.minute

        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = conn.cursor()
        cursor.execute('SELECT valor FROM configs WHERE chave=\'auto_msg\'')
        valor = eval(cursor.fetchone()[0])
        cursor.execute('SELECT * FROM auto_msg')
        tabela = cursor.fetchall()
        cursor.close()
        conn.close()

        resposta = None
        if now_m == 0 and now_h == 0:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            cursor = conn.cursor()
            cursor.execute('UPDATE membros SET daily=%s', (True,))
            conn.commit()
            cursor.close()
            conn.close()

        if valor:
            for linha in tabela:
                data = agora.strftime('%H:%M')
                if data == linha[3]:
                    resposta = random.choice(linha[2])

        if resposta:
            await channel.send(resposta)

        await asyncio.sleep(60)


@bot.event
async def in_status():
    await bot.wait_until_ready()
    segundos = 60
    minutos = 1
    tempo = segundos * minutos
    while not bot.is_closed():
        await bot.change_presence(activity=discord.Activity(
            name='tudo e todos',
            type=discord.ActivityType.listening)
        )
        await asyncio.sleep(tempo)

        await bot.change_presence(activity=discord.Streaming(
            name='sinais de gostosura', url='https://www.twitch.tv/ninjabitroom')
        )
        await asyncio.sleep(tempo)

        await bot.change_presence(activity=discord.Activity(
            name=f'vírus em {len(bot.guilds)} servidores',
            type=discord.ActivityType.playing)
        )
        await asyncio.sleep(tempo)


@bot.event
async def update_data():
    await bot.wait_until_ready()
    while not bot.guilds:
        await asyncio.sleep(1.0)

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    guild = bot.get_guild(496078152867512330)

    for member in guild.members:
        cursor.execute(f'SELECT id FROM membros')
        tabela = cursor.fetchall()

        existe = member.id in map(lambda x: x[0], tabela)

        if not existe:
            cursor.execute('INSERT INTO membros (id, nome) VALUES'
                           '(%s, %s)', (member.id, member.name))

    conn.commit()
    conn.close()


a_d = bot.loop.create_task(update_data())
a_s_t = bot.loop.create_task(at_specific_time())
i_s = bot.loop.create_task(in_status())

for extension in initial_extensions:
    bot.load_extension(extension)

bot.run(TOKEN)
