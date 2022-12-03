import aiofiles
import disnake
import datetime
from disnake.ext import commands


class Ticket(commands.Cog):

    def __init__(self, bot: commands.Bot, *args, **kwargs):
        self.ticket_count = 0
        self.file_counter = "__save__/counter_save.txt"
        super().__init__(*args, **kwargs)
        try:
            with open(self.file_counter, 'r') as f:
                self.data = int(f.readlines()[0]),
                self.ticket_count = self.data[0]
        except IndexError:
            self.ticket_count = self.ticket_count

        self.ticket_dir = "ticket.txt"
        self.saved_counter = None
        self.new_thread = None
        self.count = 0
        self.ticket = None
        self._ticket_id: int = 0
        self.bot = bot

    def check_ticket_channel(self, inter: disnake.ApplicationCommandInteraction):

        channel = [inter.guild.channels[i].name for i in range(len(inter.guild.channels))]
        # we check if the server has a ticket channel
        if 'Ticket' in channel or 'ticket' in channel:
            indexed = channel.index("ticket")
            self._ticket_id = inter.guild.channels[indexed].id
            self.ticket = inter.guild.channels[indexed]
            return True
        else:
            return False

    @commands.slash_command()
    async def ticket(self,
                     inter: disnake.ApplicationCommandInteraction):
        if self.check_ticket_channel(inter):
            await inter.response.defer()
            embed = disnake.Embed(title="Support",
                                  timestamp=datetime.datetime.now(),
                                  colour=0x452F8B,
                                  description="**Ticket** if there are problems in the server then please create a "
                                              "ticket "
                                              " so that the owner/admin know about it, e.g. spam messages,"
                                              "letters etc... if you want to have the chat in txt format,\n then "
                                              "before you close the ticket,\n give the command: '!end' and then we "
                                              "saved everything in the thread.")

            await inter.send("ticket channel is crated")
            await self.bot.get_channel(self._ticket_id).send(embed=embed,
                                                             components=[disnake.ui.Button(label="Create",
                                                                                           style=disnake.ButtonStyle.blurple,
                                                                                           custom_id="create")], )
        else:
            await inter.send(
                "Need You Ticket channel should i create?",
                components=[
                    disnake.ui.Button(label="Yes", style=disnake.ButtonStyle.success, custom_id="yes"),
                    disnake.ui.Button(label="No", style=disnake.ButtonStyle.danger, custom_id="no"),
                ],
                delete_after=50)

    @commands.Cog.listener("on_button_click")
    async def create_ticket(self,
                            inter: disnake.ApplicationCommandInteraction):

        self.ticket_count += 1
        async with aiofiles.open(self.file_counter, 'r+') as f:
            await f.write(f"{str(self.ticket_count)}\n")

        if inter.component.custom_id not in ["yes", "no", "create", "locked", "script", "delete"]:
            # We filter out any other button presses except
            # the components we wish to process.
            return

        if 'yes' in inter.component.custom_id:
            # create Ticket channel
            await inter.guild.create_text_channel(name='Ticket', reason='Ticket', nsfw=False)
            await inter.send("Ticket is created!!", delete_after=50)
        # if the button ass created:
        elif 'create' in inter.component.custom_id:
            await inter.send(f"Ticket created **ticket-{self.ticket_count}**", ephemeral=True,
                             delete_after=50)  # Added ephemeral

            if self.check_ticket_channel(inter):
                self.new_thread = await self.ticket.create_thread(name=f"ticket-{self.ticket_count}",
                                                                  invitable=False,
                                                                  type=disnake.ChannelType.private_thread)  # define
                # the properties of the thread
                await self.new_thread.add_user(user=inter.guild.owner)  # add the owner to thread
                await inter.guild.owner.send("Ticket-Channel is Created", delete_after=50)  # This is a DM

                embed = disnake.Embed(title="Welcome To Ticket-Channel",
                                      description="Support will be with you Shorty.\nTo close this ticket react with🔒",
                                      timestamp=datetime.datetime.now(),
                                      colour=0xEDCE02)
                lock_button = disnake.ui.Button(label="🔒",
                                                style=disnake.ButtonStyle.blurple,
                                                custom_id="locked")
                await self.new_thread.send(embed=embed, components=[lock_button])
            # endif
        elif "locked" in inter.component.custom_id:
            ticket_script = disnake.ui.Button(
                label="📝",
                style=disnake.ButtonStyle.primary,
                custom_id="script"
            )

            delete_script = disnake.ui.Button(
                label="❌",
                style=disnake.ButtonStyle.gray,
                custom_id="delete"
            )

            embed = disnake.Embed(description=f"Ticket closed by {inter.author.name}", colour=0xFFD444,
                                  timestamp=datetime.datetime.now())

            await inter.send(embed=embed, components=[ticket_script, delete_script])

        elif "script" in inter.component.custom_id:
            # send the chat in txt format
            await inter.send(file=disnake.File(self.ticket_dir))

        elif "delete" in inter.component.custom_id:
            # delete all script and channel
            await self.new_thread.delete()

        else:
            await inter.send("Than create ticket channel to use this command", delete_after=50)


def setup(bot: commands.bot):
    bot.add_cog(Ticket(bot))
