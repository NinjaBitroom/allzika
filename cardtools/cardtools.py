from .cardtools_base import *
import asyncio
import random


class JogadorReal(Jogador):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def defender(self, bot, msg, *args, **kwargs):
        def escolher(react_defesa, user_sefesa):
            usuario_igual = user_sefesa.id == self.id
            mesma_mensagem = react_defesa.message.id == msg.id
            true_react = react_defesa.emoji == '🛡' or react_defesa.emoji == '💨'
            return usuario_igual and mesma_mensagem and true_react

        try:
            escolha = await bot.wait_for('reaction_add', check=escolher, timeout=60)
        except asyncio.TimeoutError:
            escolha = random.randint(0, 1)
        else:
            if escolha[0].emoji == '🛡':
                escolha = 1
            else:
                escolha = 0
        return escolha


class JogadorBot(Jogador):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def defender(self, *args, **kwargs):
        return random.randint(0, 1)
