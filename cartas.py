import discord
from discord.ext import commands
import psycopg2
import asyncio
import random
import typing
from secreto import DATABASE_URL
from cardtools.cardtools import Carta, JogadorBot, JogadorReal

cores = (discord.Colour.blue(), discord.Colour.red())


class Cartas(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def daily(self, ctx: commands.Context):
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = conn.cursor()
        cursor.execute('SELECT daily FROM membros WHERE id=%s', (ctx.author.id,))
        daily = cursor.fetchone()[0]

        if not daily:
            return await ctx.send('Você já pegou o seu daily hoje!')

        cursor.execute('UPDATE membros SET daily=%s WHERE id=%s', (False, ctx.author.id))
        cursor.execute('SELECT contos FROM membros WHERE id=%s', (ctx.author.id,))
        contos = cursor.fetchone()[0]

        sorte = random.randint(1, 187)
        if sorte <= 100:
            conto_diario = 2
        elif sorte <= 150:
            conto_diario = 5
        elif sorte <= 170:
            conto_diario = 10
        elif sorte <= 180:
            conto_diario = 20
        elif sorte <= 185:
            conto_diario = 50
        else:
            conto_diario = 100

        contos_totais = contos + conto_diario
        cursor.execute('UPDATE membros SET contos=%s WHERE id=%s', (contos_totais, ctx.author.id))
        conn.commit()
        cursor.close()
        conn.close()
        await ctx.send(f'Você recebeu {conto_diario} contos e ficou com {contos_totais}!')

    @commands.command()
    async def free(self, ctx: commands.Context):
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = conn.cursor()
        cursor.execute('SELECT free_box FROM membros WHERE id=%s', (ctx.author.id,))

        if not cursor.fetchone()[0]:
            cursor.close()
            conn.close()
            return await ctx.send('Você já pegou o seu Free Gacha!')

        cursor.execute('UPDATE membros SET free_box=%s WHERE id=%s', (False, ctx.author.id))
        cursor.execute('SELECT * FROM cartas WHERE raridade=%s', ("COMUM",))

        tabela = cursor.fetchall()
        cartas = []
        cartas.append(random.choice(tabela))
        cartas.append(random.choice(tabela))
        cartas.append(random.choice(tabela))

        for carta in cartas:
            await ctx.send(f'Parabéns {ctx.author.mention}! Você ganhou um **{carta[1]}**!\n'
                           f'Digite `{self.bot.command_prefix}info {carta[0]}` para mais informações.')
            cursor.execute('SELECT cartas, sala FROM membros WHERE id=%s', (ctx.author.id,))
            member_info = cursor.fetchone()
            if carta[0] in member_info[0]:
                await ctx.send('Mas espere! Parece que você já possui esta carta!\n'
                               'Colocando na sala de espera...')
                member_info[1].append(carta[0])
                cursor.execute('UPDATE membros SET sala=%s WHERE id=%s', (member_info[1], ctx.author.id))
            else:
                if carta[6] == 'ULTRA':
                    await ctx.send('Oh, cheetos! Você pegou uma carta ULTRA!\n'
                                   'Corram para as montanhas!')
                member_info[0].append(carta[0])
                cursor.execute('UPDATE membros SET cartas=%s WHERE id=%s', (member_info[0], ctx.author.id))
            conn.commit()

        cursor.close()
        conn.close()

    @commands.command(aliases=['mycards', 'mc'])
    async def my_cards(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.author
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = conn.cursor()
        cursor.execute('SELECT cartas FROM membros WHERE id=%s', (member.id,))
        cartas = cursor.fetchone()[0]
        cartas.sort()

        string = 'ID | NOME | ATQ | DEF | DES | VIT | RAR \n'
        for carta in cartas:
            cursor.execute('SELECT * FROM cartas WHERE id=%s', (carta,))
            info = cursor.fetchone()
            string += f'{info[0]} | {info[1]} | {info[2]} | {info[3]} | {info[4]} | {info[5]} | {info[6]} \n'

        cursor.close()
        conn.close()

        embed = discord.Embed(title=f'Cartas de {member.name}',
                              description=string,
                              colour=discord.Colour.gold())

        await ctx.send(embed=embed)

    @commands.command(aliases=['i', 'in', 'inf'])
    async def info(self, ctx, card_id: int = None):
        if card_id is None:
            return await ctx.send('Digite o ID da carta!')

        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM cartas')
        tabela = cursor.fetchall()
        cursor.close()
        conn.close()

        carta = []
        for linha in tabela:
            if card_id == linha[0]:
                carta = linha

        if not carta:
            return await ctx.send('Nenhuma cartas com esta id encontrada...')

        cor = discord.Colour.red()
        if carta[6] == 'ULTRA':
            cor = discord.Colour.gold()
        elif carta[6] == 'PLUS':
            cor = discord.Colour.green()

        embed = discord.Embed(title=f'{carta[1]}#{carta[0]}', colour=cor)
        embed.add_field(name='ATAQUE', value=carta[2])
        embed.add_field(name='DEFESA', value=carta[3])
        embed.add_field(name='DESTREZA', value=carta[4])
        embed.add_field(name='VITALIDADE', value=carta[5])
        embed.add_field(name='RARIDADE', value=carta[6])
        embed.set_image(url=carta[7])

        await ctx.send(embed=embed)

    @commands.command(aliases=['miniinfo', 'mininfo', 'minfo', 'minin', 'mi'])
    async def mini_info(self, ctx, card_id: int = None):
        if card_id is None:
            return await ctx.send('Digite o ID da carta!')

        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM cartas')
        tabela = cursor.fetchall()
        cursor.close()
        conn.close()

        carta = []
        for linha in tabela:
            if card_id == linha[0]:
                carta = linha

        if not carta:
            return await ctx.send('Nenhuma cartas com esta id encontrada...')

        cor = discord.Colour.red()
        if carta[6] == 'ULTRA':
            cor = discord.Colour.gold()
        elif carta[6] == 'PLUS':
            cor = discord.Colour.green()

        embed = discord.Embed(title=f'{carta[1]}#{carta[0]}', colour=cor)
        embed.add_field(name='ATQ', value=carta[2])
        embed.add_field(name='DEF', value=carta[3])
        embed.add_field(name='DES', value=carta[4])
        embed.add_field(name='VIT', value=carta[5])
        embed.add_field(name='RAR', value=carta[6])
        embed.set_thumbnail(url=carta[7])

        await ctx.send(embed=embed)

    @commands.command()
    async def gacha(self, ctx, gacha_id: int = None):
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM gacha ORDER BY id ASC')
        tabela_gacha = cursor.fetchall()
        cursor.close()
        conn.close()

        if gacha_id is None:
            gacha_info = ''
            for linha in tabela_gacha:
                gacha_info += f'{linha[0]}. {linha[1]} ({linha[2]} contos)\n'

            embed = discord.Embed(title='Escolha um gacha para ganhar cartas!',
                                  description='Ganhe cartas a partir dos seguintes gachas:\n' +
                                              gacha_info + f'Exemplo: `{self.bot.command_prefix}gacha 1`.',
                                  colour=discord.Colour.blurple())

            return await ctx.send(embed=embed)

        gacha_box = []
        for linha in tabela_gacha:
            if linha[0] == gacha_id:
                gacha_box = linha

        if not gacha_box:
            return await ctx.send(f'Este gacha não existe...\n'
                                  f'Digite `{self.bot.command_prefix}gacha` para ver os gachas disponíveis.')

        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = conn.cursor()
        cursor.execute('SELECT contos, cartas, sala FROM membros WHERE id=%s', (ctx.author.id,))

        member_info = cursor.fetchone()

        if member_info[0] < gacha_box[2]:
            conn.close()
            return await ctx.send('Você não possui contos o suficiente')

        cursor.execute('UPDATE membros SET contos=%s WHERE id=%s', (member_info[0] - gacha_box[2], ctx.author.id))
        conn.commit()

        pacote = [random.randint(1, 100) for i in range(3)]

        tipos = []
        for numero in pacote:
            if numero <= gacha_box[4][0]:
                tipos.append(gacha_box[3][0])
            elif numero <= gacha_box[4][1] + gacha_box[4][0]:
                tipos.append(gacha_box[3][1])
            else:
                tipos.append(gacha_box[3][2])

        cartas = []
        for tipo in tipos:
            cursor.execute('SELECT * FROM cartas WHERE raridade=%s', (tipo,))
            cartas.append(random.choice(cursor.fetchall()))

        for carta in cartas:
            await ctx.send(f'Parabéns {ctx.author.mention}! Você ganhou um **{carta[1]}**!\n'
                           f'Digite `{self.bot.command_prefix}info {carta[0]}` para mais informações.')
            cursor.execute('SELECT cartas, sala FROM membros WHERE id=%s', (ctx.author.id,))
            member_info = cursor.fetchone()
            if carta[0] in member_info[0]:
                await ctx.send('Mas espere! Parece que você já possui esta carta!\n'
                               'Colocando na sala de espera...')
                member_info[1].append(carta[0])
                cursor.execute('UPDATE membros SET sala=%s WHERE id=%s', (member_info[1], ctx.author.id))
            else:
                if carta[6] == 'ULTRA':
                    await ctx.send('Oh, cheetos! Você pegou uma carta ULTRA!\n'
                                   'Corram para as montanhas!')
                member_info[0].append(carta[0])
                cursor.execute('UPDATE membros SET cartas=%s WHERE id=%s', (member_info[0], ctx.author.id))
            conn.commit()

        cursor.close()
        conn.close()

    @commands.command()
    async def fight(self, ctx, card_id: int = None, desafiado: typing.Union[int, discord.Member] = None):
        await ctx.send('**ATENÇÃO:** Este comando está em manutenção e erros podem acontecer durante a execução do '
                       'comando!')

        if not card_id:
            embed = discord.Embed(title=f'Por favor, informe o id de sua carta!\n'
                                        f'Para ver as suas cartas digite `{self.bot.command_prefix}mc`')
            return await ctx.send(embed=embed)

        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = conn.cursor()
        cursor.execute('SELECT cartas FROM membros WHERE id=%s', (ctx.author.id,))

        cartas_desafiante = cursor.fetchone()[0]

        if card_id not in cartas_desafiante:
            embed = discord.Embed(title=f'Você não possui esta carta!\n'
                                        f'Para ver as suas cartas digite `{self.bot.command_prefix}mc`')
            conn.close()
            return await ctx.send(embed=embed)

        if isinstance(desafiado, int):
            cursor.execute('SELECT id FROM cartas')
            tabelinha = cursor.fetchall()
            numeros = []

            for linha in tabelinha:
                numeros.append(linha[0])

            if not desafiado in numeros:
                cursor.close()
                conn.close()
                return await ctx.send(f'Não encontramos a carta com o id {desafiado}...')
            num_carta_desafiado = desafiado

        elif isinstance(desafiado, discord.Member):
            cursor.execute('SELECT cartas FROM membros WHERE id=%s', (desafiado.id,))
            cartas_desafiado = cursor.fetchone()[0]
            if cartas_desafiado is None:
                cartas_desafiado = []

            def aceitar_desafio(resposta):
                if resposta.content.isdigit():
                    dados = int(resposta.content)
                else:
                    dados = resposta.content
                return resposta.author.id == desafiado.id and dados in cartas_desafiado

            await ctx.send(f'{desafiado.mention} foi desafiado por {ctx.author.mention}!')
            await ctx.send(f'Para aceitar o desafio digite o id de sua carta!')
            await ctx.send(f'Use `{self.bot.command_prefix}mc` para ver as suas cartas!')
            await ctx.send(f'Para recusar apenas ignore...')

            try:
                mensagem_resposta = await self.bot.wait_for('message', check=aceitar_desafio, timeout=10)
            except asyncio.TimeoutError:
                embed = discord.Embed(title=f'{desafiado.name} não aceitou o desafio...')
                conn.close()
                return await ctx.send(embed=embed)

            num_carta_desafiado = int(mensagem_resposta.content)
        else:
            num_carta_desafiado = random.randint(1, 41)

        if not isinstance(desafiado, discord.Member):
            desafiado = None

        num_carta_desafiante = card_id

        cursor.execute('SELECT * FROM cartas WHERE id=%s', (num_carta_desafiante,))
        dados_carta_desafiante = cursor.fetchone()
        cursor.execute('SELECT * FROM cartas WHERE id=%s', (num_carta_desafiado,))
        dados_cartas_desafiado = cursor.fetchone()

        carta_desafiante = Carta(dados_carta_desafiante)
        carta_desafiado = Carta(dados_cartas_desafiado)

        jogador1 = JogadorReal(ctx.author.id, ctx.author.name, carta_desafiante)

        if desafiado:
            jogador2 = JogadorReal(desafiado.id, desafiado.name, carta_desafiado)
        else:
            jogador2 = JogadorBot(0, 'BOT', carta_desafiado)

        perde = False
        atacante = jogador1
        defensor = jogador2
        contador = 0
        while not perde:
            if contador % 2 == 0:
                cor = cores[0]
            else:
                cor = cores[1]
            embed_luta = discord.Embed(title=f'{ctx.author.name} VS {desafiado.name if desafiado else "BOT"}',
                                       colour=cor)
            mensagem_luta = await ctx.send(embed=embed_luta)

            embed_luta.add_field(name=f'{atacante.carta.nome} ({atacante.nome})',
                                 value=f'**ATQ={atacante.carta.ataque}** | '
                                       f'DEF={atacante.carta.defesa} | '
                                       f'DES={atacante.carta.destreza} | '
                                       f'HP={atacante.carta.vida}',
                                 inline=False)
            await mensagem_luta.edit(embed=embed_luta)
            await asyncio.sleep(1)

            embed_luta.add_field(name=f'{defensor.carta.nome} ({defensor.nome})',
                                 value=f'ATQ={defensor.carta.ataque} | '
                                       f'**DEF={defensor.carta.defesa}** | '
                                       f'**DES={defensor.carta.destreza}** | '
                                       f'**HP={defensor.carta.vida}**',
                                 inline=False)
            await mensagem_luta.edit(embed=embed_luta)
            await asyncio.sleep(1)

            embed_luta.add_field(name=f'Jogador {atacante.nome} ataca!',
                                 value=f'**Jogador {defensor.nome} defende!**',
                                 inline=False)
            await mensagem_luta.edit(embed=embed_luta)
            await asyncio.sleep(1)

            if atacante.turno_atq > 0:
                embed_luta.add_field(name=f'O turno de ataque de {atacante.nome} será pulado...',
                                     value=f'{atacante.nome} não atacará...',
                                     inline=False)
                await mensagem_luta.edit(embed=embed_luta)
                await asyncio.sleep(1)
                contador += 1
                atacante.turno_atq -= 1
                if atacante is jogador1:
                    atacante = jogador2
                    defensor = jogador1
                else:
                    atacante = jogador1
                    defensor = jogador2
                continue

            if defensor.id != 0:
                embed_luta.add_field(name=f'Jogador {defensor.nome}! Escolha o que fazer...',
                                     value='🛡 Defender\n'
                                           '💨 Desviar',
                                     inline=False)
                await mensagem_luta.add_reaction('🛡')
                await mensagem_luta.add_reaction('💨')

            await mensagem_luta.edit(embed=embed_luta)
            escolha = await defensor.defender(self.bot, mensagem_luta)

            dado_atacante = random.randint(1, 6)
            dado_defensor = random.randint(1, 6)

            ataque = atacante.carta.ataque

            ataque = f'{ataque}'
            if int(ataque) >= 0:
                ataque = '+' + ataque

            if escolha == 1:
                defesa = defensor.carta.defesa
            else:
                defesa = defensor.carta.destreza

            defesa = f'{defesa}'
            if int(defesa) >= 0:
                defesa = '+' + defesa

            embed_luta.add_field(name=f'Rolando os dados...',
                                 value=f'{atacante.nome} tirou {dado_atacante} ({ataque})\n'
                                       f'{defensor.nome} tirou {dado_defensor} ({defesa})',
                                 inline=False)

            await mensagem_luta.edit(embed=embed_luta)
            await asyncio.sleep(1)

            if escolha == 1:
                nome = f'{defensor.nome} escolheu **Defender**!'
                defesa_total = defensor.carta.defesa + dado_defensor
                ataque_total = atacante.carta.ataque + dado_atacante

                if defesa_total >= ataque_total:
                    defensor.carta.vida -= 1
                    valor = f'**{atacante.nome} causou 1 de dano!**'
                else:
                    ataque_total -= defesa_total
                    defensor.carta.vida -= ataque_total
                    valor = f'**{atacante.nome} causou {ataque_total} de dano!**'
            else:
                nome = f'{defensor.nome} escolheu **Desviar**!'
                destreza_total = defensor.carta.destreza + dado_defensor
                ataque_total = atacante.carta.ataque + dado_atacante

                if destreza_total > ataque_total:
                    valor = f'**{atacante.nome} não causou dano!**'
                else:
                    defensor.carta.vida -= ataque_total
                    valor = f'**{atacante.nome} causou {ataque_total} de dano!**'

            embed_luta.add_field(name=nome, value=valor, inline=False)
            await mensagem_luta.edit(embed=embed_luta)
            await asyncio.sleep(1)

            if defensor.carta.vida <= 0:
                perde = True

            if atacante is jogador1:
                atacante = jogador2
                defensor = jogador1
            else:
                atacante = jogador1
                defensor = jogador2

            contador += 1

        embed_final = discord.Embed(title=f'{defensor.nome} venceu!',
                                    description='Parabéns!',
                                    colour=cor)
        embed_final.set_image(url=defensor.carta.imagem)
        await ctx.send(embed=embed_final)


def setup(bot):
    bot.add_cog(Cartas(bot))
