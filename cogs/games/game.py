import asyncio
from random import random

import disnake
from disnake import Message
from disnake.ext import commands
from typing import Union, Callable
from cogs.games.char import *
import datetime


class MiniGame(commands.Cog, Player):
    """This will be for a ping command."""

    def __init__(self, bot) -> None:
        self.bot = bot

    @staticmethod
    def check(author_id: Union[str, int]) -> Callable[[Message], bool]:
        def inner_check(msg: disnake.Message) -> bool:
            return msg.author.id == author_id

        return inner_check

    @commands.slash_command()
    async def minigame(self, inter: disnake.ApplicationCommandInteraction) -> None:
        """This will be help you find games."""
        await inter.response.send_message("**Do you want to play? (y)/(n)**", delete_after=50)
        try:
            message = await self.bot.wait_for(
                "message", timeout=10.0, check=self.check(inter.author.id)
            )
            test = message.content

            if 'y' in test or 'yes' in test:
                embed = disnake.Embed(title="info",
                                      description="you can only use the functions with the ! call",
                                      colour=0xff0000)
                await inter.send("**OKAY LETS GO**", delete_after=50)
                await asyncio.sleep(1)
                await inter.send(embed=embed, delete_after=50)
                await asyncio.sleep(1)
                await inter.send(
                    "```these are our games you can play: "
                    "\n!quiz_game\n!coins\n!guess_number\n!tic_tac_toe\n!landmine\ntwenty```",
                    delete_after=50)

            if 'y' not in test or 'yes' not in test:
                pass

        except TimeoutError:
            await (await inter.original_message()).edit(content="timeout")

    @commands.command()
    async def coins(self, inter: disnake.ApplicationCommandInteraction, p=p):
        """This Show you your coins."""
        embed = disnake.Embed(title="**coins**",
                              description=f"*you have {p.coins} coins*",
                              colour=0xF0C43F,
                              timestamp=datetime.datetime.now(), )
        embed.set_image(url="https://i.gifer.com/origin/71/719ea2f44c791fc07e0e811940a0232b_w200.gif")
        await inter.send(embed=embed, delete_after=50)

    @commands.command()
    async def quiz_game(self, inter: disnake.ApplicationCommandInteraction, p=p):
        await inter.send("**QUIZ GAME:**", delete_after=50)
        await asyncio.sleep(1)
        await inter.send(f"**hallo {inter.author.name},I am the wizard of Shallow Swallow welcome\U0001F44B **",
                         delete_after=50)
        await asyncio.sleep(1)

        await inter.send(f"`wizard: do you like a play a quiz game?? (yes(y)/(n)no)`", delete_after=50)
        await asyncio.sleep(1)
        try:
            message = await self.bot.wait_for(
                "message", timeout=60.0, check=self.check(inter.author.id)
            )
            quiz = message.content
            if quiz == 'yes' or quiz == 'y':

                await inter.send('**wizard: you have to answer questions correctly, for one question you get 200 '
                                 'coins**',
                                 delete_after=50)

                await asyncio.sleep(1)
                await inter.send('**wizard: ok the first question is: **', delete_after=50)
                await asyncio.sleep(1)

                await inter.send(f'`wizard: when was the first computer built?`', delete_after=50)

                await asyncio.sleep(1)

                question1 = await self.bot.wait_for(
                    "message", timeout=60.0, check=self.check(inter.author.id)
                )

                question1 = question1.content

                if question1 == '1941' or '1941' in question1:
                    await inter.send('`wizard: YAY! That is right, YOU WON 200 coins`', delete_after=50)
                    p.coins += 200
                if question1 != '1941' or '1941' not in question1:
                    await inter.send("`wizard: anyway you still have 4 questions `", delete_after=50)

                await inter.send(f"`wizard: who is the founder of tesla?`", delete_after=50)

                await asyncio.sleep(1)

                question2 = await self.bot.wait_for(
                    "message", timeout=60.0, check=self.check(inter.author.id)
                )

                question2 = question2.content

                if 'elon musk' in question2:
                    p.coins += 200
                    await inter.send('`wizard: YAY! That is right, YOU WON 200 coins`', delete_after=50)

                if 'elon musk' not in question2:
                    await inter.send("`wizard: anyway you still have 3 questions `", delete_after=50)

                await asyncio.sleep(1)

                await inter.send(f"`wizard: what is the fastest car?`", delete_after=50)

                await asyncio.sleep(1)

                question3 = await self.bot.wait_for(
                    "message", timeout=60.0, check=self.check(inter.author.id)
                )
                question3 = question3.content
                if 'bugatti' in question3:
                    p.coins += 200
                    await inter.send('`wizard: YAY! That is right, YOU WON 200 coins`', delete_after=50)

                if 'bugatti' not in question3:
                    await inter.send("`wizard: anyway you still have 2 questions`", delete_after=50)

                await asyncio.sleep(1)
                await inter.send(f"`wizard: who invented the cell phone? `", delete_after=50)
                await asyncio.sleep(1)
                question4 = await self.bot.wait_for(
                    "message", timeout=60.0, check=self.check(inter.author.id)
                )
                question4 = question4.content
                if 'martin cooper' in question4:
                    p.coins += 200
                    await inter.send('`wizard: YAY! That is right, YOU WON 200 coins`', delete_after=50)

                if 'martin cooper' not in question4:
                    await inter.send("`wizard: anyway you still have 1 questions`", delete_after=50)

                await asyncio.sleep(1)
                await inter.send(f"`wizard: which person has the highest iq?`", delete_after=50)
                await asyncio.sleep(1)
                question5 = await self.bot.wait_for(
                    "message", timeout=60.0, check=self.check(inter.author.id)
                )
                question5 = question5.content
                if 'terence tao' in question5:
                    p.coins += 200
                    await inter.send('`wizard: YAY! That is right, YOU WON 200 coins`', delete_after=50)

                if 'terence tao' not in question5:
                    await inter.send("`wizard: anyway you still have 0 questions`", delete_after=50)

            if quiz != 'yes' or quiz != 'y':
                await inter.send(f"`wizard: okay see you {inter.author.name}\U0001F44B`", delete_after=50)

        except TimeoutError:
            await (await inter.original_message()).edit(content="timeout")

    @commands.command()
    async def guess_number(self, inter: disnake.ApplicationCommandInteraction, p=p):
        chance = random.randint(4, 10)
        num_guess = random.randint(0, 100)
        while chance != 0:
            await inter.send(f"**choose a number 0 out of 100 and you have {chance} chance**", delete_after=50)
            message = await self.bot.wait_for(
                "message", timeout=100.0, check=self.check(inter.author.id)
            )
            msg = int(message.content)
            if msg == num_guess:
                await inter.send("**YAY!!! YOU GUESS THE NUMBER**", delete_after=50)
                p.coins += 25
                break
            if msg > num_guess:
                await inter.send("**The number is smaller**", delete_after=50)
                chance -= 1
            if msg < num_guess:
                await inter.send("**The number is bigger**", delete_after=50)
                chance -= 1
            if chance == 0:
                await inter.send("**Your lose**")
                p.coins += 10
                await inter.send(f"*The number was {num_guess}*", delete_after=50)
                break


def setup(bot: commands.bot):
    bot.add_cog(MiniGame(bot))