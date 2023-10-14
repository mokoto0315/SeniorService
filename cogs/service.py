import json
import traceback
from datetime import datetime
from typing import Optional, List

import discord
from discord import app_commands, File
from discord.app_commands import Choice
from discord.ext import commands

# 導入core資料夾中的自寫模組
from core.classes import Cog_Extension

with open("setting/channel.json", "r", encoding='UTF-8') as f:
    channel_id = json.load(f)
with open("setting/role.json", "r", encoding='UTF-8') as f:
    role_id = json.load(f)

admin = role_id.get("admin", [])

with open("setting/school.json", "r", encoding='UTF-8') as f:
    school_list: dict = json.load(f)


def reload_school_json():
    with open("setting/school.json", "r", encoding='UTF-8') as school_file:
        global school_list
        school_list = json.load(school_file)


# 繼承Cog_Extension的self.bot物件
class Service(Cog_Extension):
    @app_commands.command(name="reload_school")
    async def reload_school(self, interaction: discord.Interaction):
        await interaction.response.defer()
        reload_school_json()
        for school_data in school_list.values():
            if school_data["role_id"] != 0:
                school_role_id: int = school_data["role_id"]
                if school_data["nickname"] != "" and interaction.guild.get_role(school_role_id).name != \
                        school_data["nickname"]:
                    await interaction.guild.get_role(school_role_id).edit(name=school_data["nickname"])
            else:
                for role in interaction.guild.roles:
                    if school_data["name"] == role.name or school_data["nickname"] == role.name:
                        school_role_id: int = role.id
                        school_data["role_id"] = school_role_id
        with open("setting/school.json", "w", encoding='UTF-8') as school_file:
            school_file.write(json.dumps(school_list, indent=4, ensure_ascii=False))
        await interaction.followup.send("reloaded!", file=File("./setting/school.json"))

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        # interaction.data 是一個包含交互資訊的字典
        # 有些交互不包含 custom_id，需要判斷式處理來防止出錯
        del_btn = discord.ui.Button(
            label="✔ 完成註冊",
            style=discord.ButtonStyle.green,
            custom_id="delete"
        )
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
                phone_video_btn = discord.ui.Button(label="查看手機板註冊教學", custom_id="phone_video_btn")
                pc_video_btn = discord.ui.Button(label="查看電腦板註冊教學", custom_id="pc_video_btn")
                view = discord.ui.View()
                view.add_item(del_btn)
                view.add_item(phone_video_btn)
                view.add_item(pc_video_btn)
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
            if interaction.data["custom_id"] == "phone_video_btn":
                await interaction.response.send_message(file=File("./assets/phone.mp4"))
            if interaction.data["custom_id"] == "pc_video_btn":
                await interaction.response.send_message(file=File("./assets/pc.mp4"))

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

    @app_commands.command(name="school_nickname", description="設定學校短稱")
    async def school_nickname(self, interaction: discord.Interaction, school: str,
                              nickname: str,
                              ):
        if interaction.user.id not in admin:
            await interaction.response.send_message("你沒有權限使用此指令。")
            return
        await interaction.response.defer()
        school_list[school]["nickname"] = nickname
        with open("setting/school.json", "w", encoding='UTF-8') as school_file:
            school_file.write(json.dumps(school_list, indent=4, ensure_ascii=False))
        await interaction.followup.send(f"{school_list[school]['name']} 的短稱被設為 {school_list[school]['nickname']}")

    @app_commands.command(name="register", description="開始註冊")
    @app_commands.describe(school="輸入學校名稱，直至出現選項並選擇，如無學校選項，請嘗試改變輸入詞",
                           name="請輸入名字(真名匿名皆可)",
                           student_id="請輸入學號(末三碼請以***替換)", grade="選擇年級", tag="是否接受通知")
    @app_commands.choices(
        grade=[
            Choice(name="高一", value="grade_1"),
            Choice(name="高二", value="grade_2"),
            Choice(name="高三", value="grade_3"),
            Choice(name="畢業", value="graduated"),
        ],
        tag=[
            Choice(name="是", value="allow"),
            Choice(name="否", value="non_allow"),
        ]
    )
    async def register(self, interaction: discord.Interaction, school: str,
                       name: str,
                       student_id: str, grade: Choice[str], tag: Choice[str]):
        await self._register_member(interaction, interaction.user, school, name, student_id, grade, tag)

    @app_commands.command(name="register_member", description="註冊別人")
    @app_commands.describe(school="輸入學校名稱，直至出現選項並選擇，如無學校選項，請嘗試改變輸入詞",
                           name="請輸入名字(真名匿名皆可)",
                           student_id="請輸入學號(末三碼請以***替換)", grade="選擇年級", tag="是否接受通知")
    @app_commands.choices(
        grade=[
            Choice(name="高一", value="grade_1"),
            Choice(name="高二", value="grade_2"),
            Choice(name="高三", value="grade_3"),
            Choice(name="畢業", value="graduated"),
        ],
        tag=[
            Choice(name="是", value="allow"),
            Choice(name="否", value="non_allow"),
        ]
    )
    async def register_member(self, interaction: discord.Interaction, member: discord.Member, school: str,
                              name: str,
                              student_id: str, grade: Choice[str], tag: Choice[str]):
        if interaction.user.id not in admin:
            await interaction.response.send_message("你沒有權限使用此指令。")
            return
        await self._register_member(interaction, member, school, name, student_id, grade, tag)

    async def _register_member(self, interaction: discord.Interaction, member: discord.Member, school: str,
                               name: str,
                               student_id: str, grade: Choice[str], tag: Choice[str]):
        await interaction.response.defer()
        if school in school_list.keys():
            school_role_id = 0
            if school_list[school]["role_id"] != 0:
                school_role_id: int = school_list[school]["role_id"]
                if school_list[school]["nickname"] != "" and interaction.guild.get_role(school_role_id).name != \
                        school_list[school]["nickname"]:
                    await interaction.guild.get_role(school_role_id).edit(name=school_list[school]["nickname"])
            else:
                for role in interaction.guild.roles:
                    if school_list[school]["name"] == role.name or school_list[school]["nickname"] == role.name:
                        school_role_id: int = role.id
                        break
                if school_role_id == 0:
                    new_school_role = await interaction.guild.create_role(
                        name=school_list[school]["nickname"] if school_list[school]["nickname"] != "" else
                        school_list[school][
                            "name"])
                    await interaction.guild.edit_role_positions({new_school_role: 16})
                    school_role_id = new_school_role.id
                school_list[school]["role_id"] = school_role_id
                with open("setting/school.json", "w", encoding='UTF-8') as school_file:
                    school_file.write(json.dumps(school_list, indent=4, ensure_ascii=False))
            await member.add_roles(interaction.guild.get_role(role_id["school_prefix"]),
                                   interaction.guild.get_role(school_role_id))
        else:
            await member.add_roles(interaction.guild.get_role(role_id["school_prefix"]))
            await interaction.followup.send(
                "您所輸入的學校不在名單上，請確認您是否選擇了提供的選項，如果沒有出現選項則請更換不同詞彙再嘗試，若仍無請通知註冊人員協助。")
        await member.add_roles(interaction.guild.get_role(role_id["grade"]["prefix"]),
                               interaction.guild.get_role(role_id["grade"][grade.value]))
        await member.add_roles(interaction.guild.get_role(role_id["tag"]["prefix"]),
                               interaction.guild.get_role(role_id["tag"][tag.value]))
        embed = discord.Embed(title="🏫 NASH 註冊資料", color=0xea8053, timestamp=datetime.utcnow())
        embed.add_field(name="填報人", value=member.mention, inline=False)
        embed.add_field(name="學校", value=school_list[school][
            "name"] if school in school_list.keys() else "無學校，請重新註冊或請註冊人員協助", inline=False)
        embed.add_field(name="姓名", value=name, inline=False)
        embed.add_field(name="ID", value=student_id, inline=False)
        embed.add_field(name="年級", value=grade.name, inline=True)
        embed.add_field(name="是否接受提及", value=tag.name, inline=True)
        embed.add_field(name="請確認是否填寫正確", value="請稍後註冊人員接手", inline=False)
        embed.set_footer(text=interaction.guild.name)
        await interaction.followup.send(embed=embed)

    @app_commands.command(name="edit_register", description="修改註冊資料")
    @app_commands.describe(mid="註冊ID", school="修改學校", name="修改名字", student_id="修改學號", grade="修改年級",
                           tag="修改通知")
    @app_commands.choices(
        grade=[
            Choice(name="高一", value="grade_1"),
            Choice(name="高二", value="grade_2"),
            Choice(name="高三", value="grade_3"),
            Choice(name="畢業", value="graduated"),
        ],
        tag=[
            Choice(name="是", value="allow"),
            Choice(name="否", value="non_allow"),
        ]
    )
    async def edit_register(self, interaction: discord.Interaction, mid: str,
                            school: Optional[str], name: Optional[str], student_id: Optional[str],
                            grade: Optional[Choice[str]],
                            tag: Optional[Choice[str]]):
        await interaction.response.defer(ephemeral=True)
        try:
            # 取得要編輯的訊息
            channel = interaction.client.get_channel(interaction.channel_id)
            message = await channel.fetch_message(int(mid))
            # 更新訊息
            # 取得要編輯的嵌入
            new_embed = message.embeds[message.embeds.index(message.embeds[0])]
            member = interaction.guild.get_member(int(new_embed.fields[0].value[2:-1]))
            if school is not None:
                if school in school_list.keys():
                    school_role_id = 0
                    if school_list[school]["role_id"] != 0:
                        school_role_id: int = school_list[school]["role_id"]
                        if school_list[school]["nickname"] != "" and interaction.guild.get_role(school_role_id).name != \
                                school_list[school]["nickname"]:
                            await interaction.guild.get_role(school_role_id).edit(name=school_list[school]["nickname"])
                    else:
                        for role in interaction.guild.roles:
                            if school_list[school]["name"] == role.name or school_list[school]["nickname"] == role.name:
                                school_role_id: int = role.id
                                break
                        if school_role_id == 0:
                            new_school_role = await interaction.guild.create_role(
                                name=school_list[school]["nickname"] if school_list[school]["nickname"] != "" else
                                school_list[school][
                                    "name"])
                            await interaction.guild.edit_role_positions({new_school_role: 16})
                            school_role_id = new_school_role.id
                        school_list[school]["role_id"] = school_role_id
                        with open("setting/school.json", "w", encoding='UTF-8') as school_file:
                            school_file.write(json.dumps(school_list, indent=4, ensure_ascii=False))
                    await member.add_roles(interaction.guild.get_role(role_id["school_prefix"]),
                                           interaction.guild.get_role(school_role_id))
                else:
                    await member.add_roles(interaction.guild.get_role(role_id["school_prefix"]))
                    await interaction.followup.send(
                        "您所輸入的學校不在名單上，請確認您是否選擇了提供的選項，如果沒有出現選項則請更換不同詞彙再嘗試，若仍無請通知註冊人員協助。")
            if name is None:
                name = new_embed.fields[2].value
            if student_id is None:
                student_id = new_embed.fields[3].value
            if grade is not None:
                await member.add_roles(interaction.guild.get_role(role_id["grade"]["prefix"]),
                                       interaction.guild.get_role(role_id["grade"][grade.value]))
            if tag is not None:
                await member.add_roles(interaction.guild.get_role(role_id["tag"]["prefix"]),
                                       interaction.guild.get_role(role_id["tag"][tag.value]))

            embed = discord.Embed(title="🏫 NASH 註冊資料", color=0xea8053, timestamp=datetime.utcnow())
            embed.add_field(name="填報人", value=member.mention, inline=False)
            embed.add_field(name="學校", value=new_embed.fields[1].value if school is None else (
                school_list[school]["name"] if school in school_list.keys() else "無學校，請重新註冊或請註冊人員協助"),
                            inline=False)
            embed.add_field(name="姓名", value=name, inline=False)
            embed.add_field(name="ID", value=student_id, inline=False)
            embed.add_field(name="年級", value=new_embed.fields[4].value if grade is None else grade.name, inline=True)
            embed.add_field(name="是否接受提及", value=new_embed.fields[5].value if tag is None else tag.name,
                            inline=True)
            embed.add_field(name="資料已送出", value="請等候註冊人員給予身分", inline=False)
            await message.edit(embed=embed)
            await interaction.followup.send("已更新完成")
            channel = self.bot.get_channel(int(channel_id['register']))
            await channel.send(embed=embed)
        except BaseException as e:
            print(traceback.format_exception(e.__class__, e, e.__traceback__))

    @register.autocomplete('school')
    @register_member.autocomplete('school')
    @school_nickname.autocomplete('school')
    @edit_register.autocomplete('school')
    async def school_autocomplete(self, interaction: discord.Interaction, current: str) -> List[Choice[str]]:
        schools = [
            Choice(name=data["name"] if data["nickname"] == "" else f"[{data['nickname']}]{data['name']}", value=code)
            for
            code, data in
            school_list.items()]
        suggestion = []
        for school in schools:
            if current in school.name:
                suggestion.append(school)
        return suggestion if len(suggestion) <= 25 else suggestion[0:24]


# 載入cog中
async def setup(bot: commands.Bot):
    await bot.add_cog(Service(bot))
