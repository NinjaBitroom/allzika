import discord
from discord.ext import commands
import psycopg2
from secreto import DATABASE_URL
from cardtools import cardtools_beta as ct
import random


class Beta(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def battle(self, ctx: commands.Context, card_id: int = None, desafiado: discord.Member = None):
        if ctx.guild.id != 666001885609721926:
            return await ctx.send('Comando indisponível no momento...')

        if card_id is None:
            return await ctx.send(f'Por favor! Digite o id de sua carta!\n'
                                  f'Para ver as suas cartas, digite `{self.bot.command_prefix}mc`!')

        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = conn.cursor()
        cursor.execute('SELECT cartas FROM membros WHERE id=%s', (ctx.author.id,))
        cards = cursor.fetchone()[0]
        cursor.close()
        conn.close()

        if card_id not in cards:
            return await ctx.send(f'Você não possui esta carta!\n'
                                  f'Para ver as suas cartas digite `{self.bot.command_prefix}mc`!')

        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM cartas WHERE id=%s', (card_id,))
        carta_desafiante = ct.Carta(cursor.fetchone())
        cursor.close()
        conn.close()

        if not desafiado:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM cartas')
            carta_desafiado = ct.Carta(random.choice(cursor.fetchall()))
            cursor.close()
            conn.close()
            desafiado = ct.JogadorBot(0, 'BOT', carta_desafiado)

        desafiante = ct.JogadorReal(ctx.author.id, ctx.author.name, carta_desafiante)
        jogo = ct.Jogo([desafiante, desafiado], ctx)
        await jogo.gameloop()


def setup(bot):
    bot.add_cog(Beta(bot))
