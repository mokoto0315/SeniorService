import os, asyncio, discord
from typing import Optional
from discord.ext import commands
import json
from datetime import datetime as dt
from discord import app_commands
from discord.app_commands import Choice

with open("setting/setup.json","r", encoding='UTF-8') as f:
    setup = json.load(f)
with open("setting/role.json","r",encoding='UTF-8') as f:
    role = json.load(f)
with open("setting/channel.json","r",encoding='UTF-8') as f:
    cha = json.load(f)

admin = role.get("admin", [])
intents = discord.Intents.all()
bot = commands.Bot(command_prefix = ".", intents = intents)

## 啟動管理
@bot.event
async def on_ready():
    slash = await bot.tree.sync()
    # 狀態顯示系統(後端)
    state = (
        "∴°﹒:+:-*-*-*-*-*-*-*☆★☆*-*-*-*-*-*-*-:+:‧°∴" + "\n"
        "     當前狀態: 運行中..." + "\n"
        "     登錄系統端: " + str(bot.user) + "\n"
        "     系統端版本: " + setup['version'] + "\n"
        "     載入指令數: " +  str(len(slash)) + "\n"
        "     當前時間: " + dt.now().strftime("%Y/%m/%d %H:%M:%S") + "\n"
        "∴°﹒:+:-*-*-*-*-*-*-*☆★☆*-*-*-*-*-*-*-:+:‧°∴"
    )
    print(state)
    # 狀態顯示系統(前端)
    embed=discord.Embed(title="系統狀態",color=0xb8d8af)
    embed.add_field(name="當前狀態", value="🚥 運行中...", inline=False)
    embed.add_field(name="登錄系統端", value=str(bot.user), inline=True)
    embed.add_field(name="系統端版本", value=setup['version'], inline=True)
    embed.add_field(name="載入指令數", value=str(len(slash)), inline=True)
    embed.set_footer(text="當前時間 "+ dt.now().strftime("%Y/%m/%d %H:%M:%S"))
    for channel_id in cha['data']:
        channel = bot.get_channel(channel_id)
        await channel.send(embed=embed)

    # 這邊設定機器人的狀態
    # discord.Status.<狀態>，可以是online（上線）,offline（下線）,idle（閒置）,dnd（請勿打擾）,invisible（隱身）
    status_w = discord.Status.online

    # 這邊設定機器當前的狀態文字
    # type可以是playing（遊玩中）、streaming（直撥中）、listening（聆聽中）、watching（觀看中）、custom（自定義）
    activity_w = discord.Activity(type=discord.ActivityType.playing, name="系統開發中...")

    await bot.change_presence(status=status_w, activity=activity_w) 


## 模組管理

# 一開始bot開機需載入全部程式檔案
async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

@bot.tree.command(name="mods", description="管理模組")
@app_commands.describe(type="選擇類型", mod="模組名")
@app_commands.choices(
    type=[
        Choice(name="載入模組", value="load"),
        Choice(name="重載模組", value="reload"),
        Choice(name="卸載模組", value="unload"),
        Choice(name="查詢當前模組",value="list")
    ],
)
async def mods(interaction: discord.Interaction, type: Choice[str], mod: Optional[str]):
    # 確認使用者身分
    user = interaction.user
    action = ""
    if user.id not in admin:
        await interaction.response.send_message("你沒有權限使用此指令。")
        return
    type = type.value
    if type == "load":
        await bot.load_extension(f"cogs.{mod}")
        action = discord.utils.get(bot.emojis, name='emoji_13')
        action = f'{action} **載入模組**'
    elif type == "reload":
        await bot.reload_extension(f"cogs.{mod}")
        action = discord.utils.get(bot.emojis, name='emoji_14')
        action = f'{action} **重載模組**'
    elif type == "unload":
        await bot.unload_extension(f"cogs.{mod}")
        action = discord.utils.get(bot.emojis, name='emoji_15')
        action = f'{action} **卸載模組**'
    elif type == "list":
        loaded_cogs = ", ".join(f"**{cog.replace('cogs.', '')}**" for cog in bot.extensions.keys())
        embed=discord.Embed(title="⚙ NASH 資訊管理", color=0xea8053)
        embed.add_field(name="已載入的模組", value=loaded_cogs, inline=False)
        await interaction.response.send_message(embed=embed)
        return

    embed=discord.Embed(title="⚙ NASH 資訊管理", color=0xea8053)
    embed.add_field(name=action, value=mod, inline=False)
    await interaction.response.send_message(embed=embed)

async def main():
    await load_extensions()
    async with bot:
        await bot.start(setup['Token'])


# 確定執行此py檔才會執行
if __name__ == "__main__":
    asyncio.run(main())