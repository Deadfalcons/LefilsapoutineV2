from discord.ext import commands
import discord
import os
from sys import platform
import random
import time
from utils import id_convert
from numpy.random import choice

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
        answer_list = [["That's a very bad work...\nYou won 50$", 50],
                       ["That's a bad work...\nYou won 100$", 100],
                       ["That's a good work!\nYou won 200$", 200],
                       ["That's a very good work!\nYou won 300$", 300],
                       ["That's an excelent work!\nYou won 500$", 500]]
        answer = int(choice([x for x in range(5)], 1, p=[0.09, 0.2, 0.5, 0.2, 0.01]))
        self.modify_money(ctx.author.id, answer_list[answer][1])
        await ctx.send(answer_list[answer][0])

    @commands.command(name="steal", brief="Steal other people", aliases=["st"])
    async def steal(self, ctx, user_id):
        user = int(id_convert(user_id))
        if ctx.author.id == user:
            return await ctx.send("You can't steal yourself lmao")
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
        self.search_balance(ctx.author.id)
        bal = self.search_balance(user)
        answer_list = [["It's a trap!\nYou won ", int(bal * -0.1)],
                       ["You stole a little portion...\nYou won ", int(bal * 0.1)],
                       ["You stole a good portion!\nYou won ", int(bal * 0.2)],
                       ["You stole a very good portion!\nYou won ", int(bal * 0.3)],
                       ["You stole an ENORMOUS portion!\nYou won ", int(bal * 0.5)]]
        answer = int(choice([x for x in range(5)], 1, p=[0.09, 0.2, 0.5, 0.2, 0.01]))
        is_stole = self.modify_money(user, -answer_list[answer][1], gotozero=True)
        if is_stole:
            self.modify_money(ctx.author.id, answer_list[answer][1], gotozero=True)
        await ctx.send(f"{answer_list[answer][0]}{answer_list[answer][1]}$")

    @commands.command(name="baltop", brief="The rank of money")
    async def baltop(self, ctx):
        balances = {}
        with open(path + "balance.csv", "r") as file:
            for line in file:
                balances[line.split(",")[0]] = line.split(",")[1]
        balances_list = []
        while len(balances) > 0:
            max_k = random.choice(list(balances.keys()))
            max_ = int(balances[max_k])
            for k, v in balances.items():
                if int(v) > max_:
                    max_ = int(v)
                    max_k = k
            balances_list.append([int(max_k), int(balances[max_k][:-1])])
            del balances[max_k]
        balances_list = [balances_list[k: k+10] for k in range(0, len(balances_list), 10)] # Set for paginator in the future
        displayed_list = [f"{x + 1} {self.client.get_user(balances_list[0][x][0])} : {balances_list[0][x][1]}\n" for x in range(len(balances_list[0]))]
        e = discord.Embed(
            title="Baltop",
            description="".join(displayed_list)
        )
        e.set_footer(text="Made by </Deadfalcon>")
        await ctx.send(embed=e)


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
