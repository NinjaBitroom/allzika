from PIL import Image, ImageDraw, ImageFont
import asyncio
import discord
from discord.ext import commands
import requests
import random
import wikipedia
import psycopg2
import os
from secreto import DATABASE_URL

wikipedia.set_lang('pt')


class Comandos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def desafio(self, ctx: commands.Context):
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = conn.cursor()

        cursor.execute('SELECT contos FROM membros WHERE id=%s', (ctx.author.id,))
        contos = cursor.fetchone()[0]
        if contos < 1:
            await ctx.channel.send('Você não tem contos suficientes!')
            conn.close()
            return

        cursor.execute('UPDATE membros SET contos=%s WHERE id=%s', (contos-1, ctx.author.id))

        conn.commit()
        conn.close()

        message = ctx.message
        await message.channel.send('Pensei em um número!\n'
                                   'Chute um número de 1 a 10.')

        def is_correct(m):
            return m.author == message.author and m.content.isdigit()

        numero = random.randint(1, 10)

        try:
            tentativa = await self.bot.wait_for('message', check=is_correct, timeout=5.0)
        except asyncio.TimeoutError:
            return await message.channel.send(f'Seu tempo acabou! O número era: {numero}.')

        if int(tentativa.content) == numero:
            await message.channel.send('Você acertou!')

            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            cursor = conn.cursor()

            cursor.execute('SELECT contos FROM membros WHERE ID=%s', (ctx.author.id,))
            contos = cursor.fetchone()[0] + 10
            print(contos)
            cursor.execute('UPDATE membros SET contos=%s WHERE id=%s', (contos, ctx.author.id))

            conn.commit()
            conn.close()
            await message.channel.send('Você ganhou 10 contos!')
        else:
            await message.channel.send(f'Opa! O número era: {numero}.')

    @commands.command(aliases=['wikipedia'])
    async def wiki(self, ctx: commands.Context, *, pesquisa: str=None):
        async with ctx.typing():
            if pesquisa is None:
                embed = discord.Embed(title='Escreva o que deseja pesquisar!',
                                      description=f'Exemplo: `{self.bot.command_prefix}wiki jamal`',
                                      colour=discord.Colour.red())
                return await ctx.send(embed=embed)
            bot_message = await ctx.send(embed=discord.Embed(
                description=f'Procurando resultados para: "{pesquisa}"',
                colour=discord.Colour.blue()))

            resultados = wikipedia.search(pesquisa)
            total = len(resultados)
            if total == 0:
                await bot_message.edit(embed=discord.Embed(
                    description=f'Não achei nenhum resultado para "{pesquisa}", tente outro nome.',
                    colour=discord.Colour.orange()))
            else:
                if total > 3:
                    limite = 3
                else:
                    limite = total

                await bot_message.edit(embed=discord.Embed(
                    title=f'Foram achados {total} resultados para "{pesquisa}"\n',
                    description=f'Buscando {limite} resultado(s)...',
                    colour=discord.Colour.orange()))

                porcento = int(100/limite)
                embed = discord.Embed(title=f'Resultados para "{pesquisa}"', colour=discord.Colour.orange())
                for resultado in range(limite):
                    try:
                        wiki_page = wikipedia.WikipediaPage(resultados[resultado])
                        valor = wiki_page.summary
                        url = wiki_page.url
                    except wikipedia.exceptions.DisambiguationError as erro:
                        for pagina in range(len(erro.options)):
                            try:
                                wiki_page = wikipedia.WikipediaPage(erro.options[pagina])
                                valor = wiki_page.summary
                                url = wiki_page.url
                            except wikipedia.exceptions.DisambiguationError:
                                valor = 'Não foi possível exibir este resultado!'
                                url = 'Não foi possível exibir o link!'
                            else:
                                break
                    if len(valor) > 1024:
                        valor = valor[:1021] + '...'
                    embed.add_field(name=resultados[resultado], value=valor, inline=False)
                    embed.add_field(name=f'Saiba mais em:', value=url)
                    await bot_message.edit(embed=discord.Embed(
                        description=f'Carregando resultados: {porcento*(resultado+1)}%',
                        colour=discord.Colour.blurple()))
                await asyncio.sleep(1.0)
                await bot_message.edit(embed=embed)

    @commands.command(aliases=['bd', 'bolsad', 'bolsadelicia'])
    async def bolsa_delicia(self, ctx, *, membro: discord.Member = None):
        if membro is None:
            membro = ctx.author

        cartao = Image.open('./imagens/Cartao-do-Bolsa-Delícia.png')
        fonte = ImageFont.truetype('./fontes/microsoft-sans-serif.ttf', 12)
        escrever = ImageDraw.Draw(cartao)

        escrever.text(xy=(22, 125), text=membro.name, fill=(0, 0, 0), font=fonte)
        escrever.text(xy=(22, 140), text=str(membro.id), fill=(0, 0, 0), font=fonte)

        cartao.save('./imagens/bolsa-delicia.png')

        await ctx.send(file=discord.File('./imagens/bolsa-delicia.png'))

    @commands.command(aliases=['coins', 'conto', 'contos', 'moeda', 'moedas', 'dinheiro'])
    async def coin(self, ctx, membro: discord.Member = None):
        if membro is None:
            membro = ctx.author
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM membros')
        tabela = cursor.fetchall()
        cursor.close()
        conn.close()
        for linha in tabela:
            if membro.id == linha[0]:
                await ctx.send(f'{membro.name} possui {linha[3]} conto.')

    @commands.command(aliases=['rank'])
    async def ranking(self, ctx):
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM membros ORDER BY pegar DESC')
        tabela = cursor.fetchall()
        cursor.close()
        conn.close()

        membros = ''
        for linha in range(len(tabela)):
            if linha == 0:
                medalha = '🥇'
            elif linha == 1:
                medalha = '🥈'
            elif linha == 2:
                medalha = '🥉'
            else:
                medalha = ''
            pos = str(linha+1)+'.'
            if tabela[linha][2] > 0 or tabela[linha][0] == ctx.author.id:
                if tabela[linha][0] == ctx.author.id:
                    membros += f'**{pos} {medalha}{tabela[linha][1]} [{tabela[linha][2]}]**\n'
                else:
                    membros += f'{pos} {medalha}{tabela[linha][1]} [{tabela[linha][2]}]\n'
        bester = await self.bot.fetch_user(tabela[0][0])
        embed = discord.Embed(title=f'🏆{bester.name} foi o que mais pegou na madeira🏆',
                              description=membros,
                              colour=discord.Colour.gold())
        embed.set_thumbnail(url=bester.avatar_url)

        await ctx.send(embed=embed)

    @commands.command(aliases=['say', 'fale', 'falar', 'dizer'])
    async def diga(self, ctx: commands.Context, *, texto: str = None):
        if texto is None:
            return
        await ctx.message.delete()
        await ctx.send(texto)
    
    @commands.command(aliases=['superfala', 'ss', 'supers', 'ssay'])
    async def supersay(self, ctx: commands.Context, *, texto: str = None):
        if texto is None:
            return
        
        resposta = requests.get(ctx.author.avatar_url)
        endereco = ctx.author.name.replace(' ', '_') + '.png'

        with open(endereco, 'wb') as novo_arquivo:
            novo_arquivo.write(resposta.content)

        with open(endereco, 'rb') as avatar_img:
            webhook = await ctx.channel.create_webhook(name=ctx.author.display_name, avatar=avatar_img.read())

        await ctx.message.delete()
        await webhook.send(texto)
        await webhook.delete()

    @commands.command()
    async def eval(self, ctx: commands.Context, *, eq: str = None):
        if eq is None:
            cor = discord.Colour.red()
            embed = discord.Embed(title='Por favor, insira uma expressão!\nExemplo: `.eval 1+1`', colour=cor)
            return await ctx.send(embed=embed)

        try:
            resposta = str(eval(eq))
        except Exception as erro:
            cor = discord.Colour.red()
            resposta = str(erro)
        else:
            cor = discord.Colour.green()

        embed = discord.Embed(colour=cor)
        embed.add_field(name='Seu problema:', value=f'```python\n{eq}```', inline=False)
        embed.add_field(name='Resolução:', value=f'```python\n{resposta}```')
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Comandos(bot))
