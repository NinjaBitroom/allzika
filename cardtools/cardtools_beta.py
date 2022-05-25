import discord
from discord.ext import commands
from .cardtools_base import *
import asyncio
import random


class JogadorReal(Jogador):
    async def defender(self, *args, **kwargs):
        return random.randint(0, 1)


class JogadorBot(Jogador):
    async def defender(self, *args, **kwargs):
        return random.randint(0, 1)


class Jogo:
    def __init__(self, jogadores: list, context: commands.Context):
        self.jogadores = jogadores
        self.ctx = context
        self.embed = discord.Embed(title=str(self.jogadores), colour=discord.Colour.purple())

    async def gameloop(self):
        await self.ctx.send(embed=self.embed)

        acaba = False
        while not acaba:
            for jogador in self.jogadores:
                for carta in jogador.cartas:
                    carta.atacar()
