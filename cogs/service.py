import json
import traceback
from datetime import datetime
from typing import Optional

import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands

# 導入core資料夾中的自寫模組
from core.classes import Cog_Extension

with open("setting/channel.json", "r", encoding='UTF-8') as f:
    channel_id = json.load(f)
with open("setting/role.json", "r", encoding='UTF-8') as f:
    admin_id = json.load(f)
admin = admin_id.get("admin", [])


# 繼承Cog_Extension的self.bot物件
class Service(Cog_Extension):

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        # interaction.data 是一個包含交互資訊的字典
        # 有些交互不包含 custom_id，需要判斷式處理來防止出錯
        del_btn = discord.ui.Button(
            label="✔ 完成註冊",
            style=discord.ButtonStyle.green,
            custom_id="delete"
        )
        try:
            if "custom_id" in interaction.data:
                if interaction.data["custom_id"] == "register":
                    category = discord.utils.get(interaction.guild.categories, id=1155424378553651250)
                    permissions = {
                        interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                        interaction.user: discord.PermissionOverwrite(read_messages=True)
                    }
                    cha = await interaction.guild.create_text_channel(name="註冊代碼 " + interaction.user.name,
                                                                      category=category, overwrites=permissions)
                    await interaction.response.send_message(cha.mention + " 已創建", ephemeral=True)
                    view = discord.ui.View()
                    view.add_item(del_btn)
                    embed = discord.Embed(title="🏫 NASH 新生註冊", color=0xea8053, timestamp=datetime.utcnow())
                    embed.add_field(name="請輸入 **/register** 填寫資料開始註冊",
                                    value="需求資料\n```學校:\n姓名:\n學號:\n年級:\n是否願意接受通知:```", inline=False)
                    embed.set_footer(text=cha.guild.name)
                    await cha.send(embed=embed, view=view)
                if interaction.data["custom_id"] == "delete":
                    try:
                        if interaction.user.id in admin:
                            await interaction.channel.delete()
                        else:
                            await interaction.response.send_message("此為管理員專用", ephemeral=True)
                    except Exception as e:
                        print(e)

        except Exception as e:
            print(e)

    @commands.Cog.listener()
    async def on_ready(self):
        # 宣告 View
        try:
            view = discord.ui.View()
            # 使用 class 方式宣告 Button 並設置 custom_id
            register = discord.ui.Button(
                label="✉ 開始註冊",
                style=discord.ButtonStyle.blurple,
                custom_id="register"
            )
            # 將 Button 添加到 View 中
            view.add_item(register)
            channel = self.bot.get_channel(int(channel_id['Register']))
            await channel.purge(check=lambda msg: msg.author == self.bot.user)
            embed = discord.Embed(title="🏫 NASH 新生註冊", color=0xea8053, timestamp=datetime.utcnow())
            embed.add_field(name="按下下方按鈕開始註冊", value="", inline=False)
            embed.set_footer(text=channel.guild.name)
            await channel.send(embed=embed, view=view)
        except Exception as e:
            print(e)

    @app_commands.command(name="register", description="開始註冊")
    @app_commands.describe(area="選擇學校地區", school="輸入學校", name="請輸入名字(真名匿名皆可)",
                           student_id="請輸入學號(末三碼請以***替換)", grade="選擇年級", tag="是否接受通知")
    @app_commands.choices(
        area=[
            Choice(name="✪ 北部", value="✪ 北部"),
            Choice(name="♞ 中部", value="♞ 中部"),
            Choice(name="⚘ 南部", value="⚘ 南部"),
            Choice(name="♨ 東部", value="♨ 東部"),
            Choice(name="⛴︎ 離島", value="⛴︎ 離島"),
        ],
        grade=[
            Choice(name="高一", value="高一"),
            Choice(name="高二", value="高二"),
            Choice(name="高三", value="高三"),
            Choice(name="畢業", value="畢業"),
        ],
        tag=[
            Choice(name="是", value="是"),
            Choice(name="否", value="否"),
        ]
    )
    async def register(self, interaction: discord.Interaction, area: Choice[str], school: str, name: str,
                       student_id: str, grade: Choice[str], tag: Choice[str]):
        embed = discord.Embed(title="🏫 NASH 註冊資料", color=0xea8053, timestamp=datetime.utcnow())
        embed.add_field(name="填報人", value=interaction.user.mention, inline=False)
        embed.add_field(name="地區", value=area.name, inline=False)
        embed.add_field(name="學校", value=school, inline=False)
        embed.add_field(name="姓名", value=name, inline=False)
        embed.add_field(name="ID", value=student_id, inline=False)
        embed.add_field(name="年級", value=grade.name, inline=True)
        embed.add_field(name="是否接受提及", value=tag.name, inline=True)
        embed.add_field(name="請確認是否填寫正確", value="請稍後註冊人員接手", inline=False)
        embed.set_footer(text=interaction.guild.name)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="edit_register", description="修改註冊資料")
    @app_commands.describe(mid="註冊ID", school="修改學校", name="修改名字", student_id="修改學號", grade="修改年級",
                           tag="修改通知")
    async def edit_register(self, interaction: discord.Interaction, mid: int, area: Optional[str],
                            school: Optional[str], name: Optional[str], student_id: Optional[str], grade: Optional[str],
                            tag: Optional[str]):
        try:
            # 取得要編輯的訊息
            channel = interaction.client.get_channel(interaction.channel_id)
            message = await channel.fetch_message(mid)
            # 更新訊息
            # 取得要編輯的嵌入
            new_embed = message.embeds[message.embeds.index(message.embeds[0])]

            user = new_embed.fields[0].value
            if area is None:
                area = new_embed.fields[1].value
            if school is None:
                school = new_embed.fields[2].value
            if name is None:
                name = new_embed.fields[3].value
            if student_id is None:
                student_id = new_embed.fields[4].value
            if grade is None:
                grade = new_embed.fields[5].value
            if tag is None:
                tag = new_embed.fields[6].value

            embed = discord.Embed(title="🏫 NASH 註冊資料", color=0xea8053, timestamp=datetime.utcnow())
            embed.add_field(name="填報人", value=user, inline=False)
            embed.add_field(name="地區", value=area, inline=False)
            embed.add_field(name="學校", value=school, inline=False)
            embed.add_field(name="姓名", value=name, inline=False)
            embed.add_field(name="ID", value=student_id, inline=False)
            embed.add_field(name="年級", value=grade, inline=True)
            embed.add_field(name="是否接受提及", value=tag, inline=True)
            embed.add_field(name="資料已送出", value="請等候註冊人員給予身分", inline=False)
            await message.edit(embed=embed)
            await interaction.response.send_message("已更新完成", ephemeral=True)
            await message.edit(embed=embed)
        except BaseException as e:
            print(traceback.format_exception(e.__class__, e, e.__traceback__))


# 載入cog中
async def setup(bot: commands.Bot):
    await bot.add_cog(Service(bot))
