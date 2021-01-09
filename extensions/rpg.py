from discord.ext import commands
import discord
import os
from sys import platform
import random
import time
from utils import id_convert

if platform == "win32":
    path = "extensions/rpg/"
else:
    path = "/home/pi/LefilsapoutineV2/extensions/rpg/"


class rpg(commands.Cog):
    def __init__(self, client):
        self.client = client

    def search_balance(self, user_id: int) -> int:
        with open(path + "balance.csv", "r") as file:
            for line in file:
                if line.split(",")[0] == str(user_id):
                    balance = int(line.split(",")[1])
                    break
            else:
                with open(path + "balance.csv", "a") as file_write:
                    balance = 1000
                    file_write.write(f"{user_id},{balance}\n")
        return balance

    def modify_money(self, user_id: int, amount: int, gotozero=False):
        list_lines = []
        balance = 1000
        with open(path + "balance.csv", "r") as file:
            for line in file:
                if str(user_id) not in line:
                    list_lines.append(line)
                else:
                    balance = int(line.split(",")[1])
        if balance + amount < 0:
            if gotozero:
                balance = amount
            else:
                return False
        list_lines.append(f"{user_id},{balance + amount}\n")
        with open(path + "balance.csv", "w") as file:
            file.write("".join(list_lines))
        return True

    @commands.command(name="balance", brief="Shows your amount of money", aliases=["bal"])
    async def balance(self, ctx, user_given=None):
        if user_given is None:
            user = ctx.author.id
        else:
            user = id_convert(user_given)
        e = discord.Embed(
            title=f"Balance of {self.client.get_user(int(user)).display_name}",
            description=f"{self.search_balance(int(user))}$"
        )
        e.set_footer(text="Made by </Deadfalcon>")
        await ctx.send(embed=e)

    @commands.command(name="work", brief="Work to gain some money", aliases=["w"])
    async def work(self, ctx):
        list_lines = []
        with open(path + "work_cooldown.csv", "r") as file:
            for line in file:
                if line.split(",")[0] == str(ctx.author.id):
                    if int(line.split(",")[1]) > int(time.time()) - 3600:
                        return await ctx.send("Wowowo cool man, you already worked this hour")
                else:
                    list_lines.append(line)
        list_lines.append(f"{ctx.author.id},{int(time.time())}\n")
        with open(path + "work_cooldown.csv", "w") as file:
            file.write("".join(list_lines))
        number = random.randint(0, 12)
        if number == 0:
            self.modify_money(ctx.author.id, 50)
            answer = "That's a very bad work...\nYou win 50$"
        elif 0 < number < 4:
            self.modify_money(ctx.author.id, 100)
            answer = "That's a bad work...\nYou win 100$"
        elif 3 < number < 9:
            self.modify_money(ctx.author.id, 200)
            answer = "That's a good work!\nYou win 200$"
        elif 8 < number < 12:
            self.modify_money(ctx.author.id, 300)
            answer = "That's a very good work!\nYou win 300$"
        elif number == 12:
            self.modify_money(ctx.author.id, 500)
            answer = "That's an excelent work!\nYou win 500$"
        await ctx.send(answer)

    @commands.command(name="steal", brief="Steal other people", aliases=["st"])
    async def steal(self, ctx, user_id):
        user = int(id_convert(user_id))
        list_lines = []
        stole_c = 0
        steal_c = 0
        with open(path + "steal_cooldown.csv", "r") as file:
            for line in file:
                try :
                    if line.split(",")[0] == str(ctx.author.id):
                        if int(line.split(",")[1]) > int(time.time()) - 600:
                            return await ctx.send("Wowowo cool man, you already stole someone in the past 5 minutes")
                        stole_c = line.split(",")[2]
                    elif line.split(",")[0] == str(user):
                        if int(line.split(",")[2]) > int(time.time()) - 120:
                            return await ctx.send("Wowowo cool man, this guys was stole in the past 2 minutes")
                        steal_c = line.split(",")[1]
                    else:
                        list_lines.append(line)
                except:
                    pass
        list_lines.append(f"{ctx.author.id},{int(time.time())},{stole_c}\n")
        list_lines.append(f"{user},{steal_c},{int(time.time())}\n")
        with open(path + "steal_cooldown.csv", "w") as file:
            file.write("".join(list_lines))
        number = random.randint(0, 12)
        self.search_balance(ctx.author.id)
        bal = self.search_balance(user)
        if number == 0:
            portion = -0.1
            answer = f"It's a trap!\nYou lost {int(-bal * portion)}$"
        elif 0 < number < 4:
            portion = 0.1
            answer = f"You stole a little portion...\nYou won {int(bal * portion)}$"
        elif 3 < number < 9:
            portion = 0.2
            answer = f"You stole a good portion!\nYou won {int(bal * portion)}$"
        elif 8 < number < 12:
            portion = 0.3
            answer = f"You stole a very good portion!\nYou won {int(bal * portion)}$"
        elif number == 12:
            portion = 0.5
            answer = f"You stole an ENORMOUS portion!\nYou won {int(bal * portion)}$"
        is_stole = self.modify_money(user, int(-bal * portion), gotozero=True)
        if is_stole:
            self.modify_money(ctx.author.id, int(bal * portion), gotozero=True)
        await ctx.send(answer)


def setup(client):
    if not os.path.isdir(path):
        os.mkdir(path)
    if not os.path.isfile(path + "balance.csv"):
        with open(path + "balance.csv", "w"):
            pass
    if not os.path.isfile(path + "work_cooldown.csv"):
        with open(path + "work_cooldown.csv", "w"):
            pass
    if not os.path.isfile(path + "steal_cooldown.csv"):
        with open(path + "steal_cooldown.csv", "w"):
            pass
    client.add_cog(rpg(client))
