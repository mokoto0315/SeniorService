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
        school=[Choice(name="國立華僑高級中等學校(新北市)", value="010301"),
                Choice(name="私立淡江高中(新北市)", value="011301"),
                Choice(name="私立康橋高中(新北市)", value="011302"),
                Choice(name="私立金陵女中(新北市)", value="011306"),
                Choice(name="新北市裕德高級中等學校(新北市)", value="011307"),
                Choice(name="財團法人南山高中(新北市)", value="011309"),
                Choice(name="財團法人恆毅高中(新北市)", value="011310"),
                Choice(name="私立聖心女中(新北市)", value="011311"),
                Choice(name="私立崇義高中(新北市)", value="011312"),
                Choice(name="新北市福瑞斯特高中(新北市)", value="011314"),
                Choice(name="私立東海高中(新北市)", value="011315"),
                Choice(name="私立格致高中(新北市)", value="011316"),
                Choice(name="私立醒吾高中(新北市)", value="011317"),
                Choice(name="私立徐匯高中(新北市)", value="011318"),
                Choice(name="新北市崇光高中(新北市)", value="011322"),
                Choice(name="私立光仁高中(新北市)", value="011323"),
                Choice(name="私立竹林高中(新北市)", value="011324"),
                Choice(name="私立及人高中(新北市)", value="011325"),
                Choice(name="財團法人辭修高中(新北市)", value="011329"),
                Choice(name="新北市林口康橋國際高中(新北市)", value="011330"),
                Choice(name="私立時雨高中(新北市)", value="011399"),
                Choice(name="私立樹人家商(新北市)", value="011405"),
                Choice(name="私立復興商工(新北市)", value="011407"),
                Choice(name="私立南強工商(新北市)", value="011408"),
                Choice(name="私立穀保家商(新北市)", value="011413"),
                Choice(name="私立智光商工(新北市)", value="011420"),
                Choice(name="私立清傳高商(新北市)", value="011421"),
                Choice(name="私立能仁家商(新北市)", value="011426"),
                Choice(name="私立豫章工商(新北市)", value="011427"),
                Choice(name="私立莊敬工家(新北市)", value="011431"),
                Choice(name="私立中華商海(新北市)", value="011432"),
                Choice(name="市立泰山高中(新北市)", value="013303"),
                Choice(name="市立板橋高中(新北市)", value="013304"),
                Choice(name="市立新店高中(新北市)", value="013335"),
                Choice(name="市立中和高中(新北市)", value="013336"),
                Choice(name="市立新莊高中(新北市)", value="013337"),
                Choice(name="市立新北高中(新北市)", value="013338"),
                Choice(name="市立林口高中(新北市)", value="013339"),
                Choice(name="市立瑞芳高工(新北市)", value="013402"),
                Choice(name="市立三重商工(新北市)", value="013430"),
                Choice(name="市立新北高工(新北市)", value="013433"),
                Choice(name="市立淡水商工(新北市)", value="013434"),
                Choice(name="市立海山高中(新北市)", value="014302"),
                Choice(name="市立三重高中(新北市)", value="014311"),
                Choice(name="市立永平高中(新北市)", value="014315"),
                Choice(name="市立樹林高中(新北市)", value="014322"),
                Choice(name="市立明德高中(新北市)", value="014326"),
                Choice(name="市立秀峰高中(新北市)", value="014332"),
                Choice(name="市立金山高中(新北市)", value="014338"),
                Choice(name="市立安康高中(新北市)", value="014343"),
                Choice(name="市立雙溪高中(新北市)", value="014347"),
                Choice(name="市立石碇高中(新北市)", value="014348"),
                Choice(name="市立丹鳳高中(新北市)", value="014353"),
                Choice(name="市立清水高中(新北市)", value="014356"),
                Choice(name="市立三民高中(新北市)", value="014357"),
                Choice(name="市立錦和高中(新北市)", value="014362"),
                Choice(name="市立光復高中(新北市)", value="014363"),
                Choice(name="市立竹圍高中(新北市)", value="014364"),
                Choice(name="市立北大高級中學(新北市)", value="014381"),
                Choice(name="市立豐珠中學(新北市)", value="014399"),
                Choice(name="市立鶯歌工商(新北市)", value="014439"),
                Choice(name="市立樟樹國際實中(新北市)", value="014468"),
                Choice(name="國立蘭陽女中(宜蘭縣)", value="020301"),
                Choice(name="國立宜蘭高中(宜蘭縣)", value="020302"),
                Choice(name="國立羅東高中(宜蘭縣)", value="020308"),
                Choice(name="國立宜蘭高商(宜蘭縣)", value="020403"),
                Choice(name="國立羅東高商(宜蘭縣)", value="020404"),
                Choice(name="國立蘇澳海事(宜蘭縣)", value="020405"),
                Choice(name="國立羅東高工(宜蘭縣)", value="020407"),
                Choice(name="國立頭城家商(宜蘭縣)", value="020409"),
                Choice(name="私立慧燈高中(宜蘭縣)", value="021301"),
                Choice(name="私立中道高中(宜蘭縣)", value="021310"),
                Choice(name="縣立南澳高中(宜蘭縣)", value="024322"),
                Choice(name="縣立慈心華德福實中(宜蘭縣)", value="024325"),
                Choice(name="國立中央大學附屬中壢高中(桃園市)", value="030305"),
                Choice(name="國立北科大附屬桃園農工(桃園市)", value="030403"),
                Choice(name="桃園市懷恩高中(桃園市)", value="031301"),
                Choice(name="桃園市育達高中(桃園市)", value="031309"),
                Choice(name="私立六和高中(桃園市)", value="031310"),
                Choice(name="桃園市復旦高中(桃園市)", value="031311"),
                Choice(name="桃園市治平高中(桃園市)", value="031312"),
                Choice(name="桃園市振聲高中(桃園市)", value="031313"),
                Choice(name="私立光啟高中(桃園市)", value="031317"),
                Choice(name="桃園市啟英高中(桃園市)", value="031318"),
                Choice(name="桃園市清華高中(桃園市)", value="031319"),
                Choice(name="桃園市新興高中(桃園市)", value="031320"),
                Choice(name="私立至善高中(桃園市)", value="031323"),
                Choice(name="桃園市大興高中(桃園市)", value="031324"),
                Choice(name="私立大華高中(桃園市)", value="031326"),
                Choice(name="桃園市世紀綠能工商(桃園市)", value="031414"),
                Choice(name="私立方曙商工(桃園市)", value="031415"),
                Choice(name="私立永平工商(桃園市)", value="031421"),
                Choice(name="市立龍潭高中(桃園市)", value="033302"),
                Choice(name="市立桃園高中(桃園市)", value="033304"),
                Choice(name="市立武陵高中(桃園市)", value="033306"),
                Choice(name="市立楊梅高中(桃園市)", value="033316"),
                Choice(name="市立陽明高中(桃園市)", value="033325"),
                Choice(name="市立內壢高中(桃園市)", value="033327"),
                Choice(name="市立中壢高商(桃園市)", value="033407"),
                Choice(name="市立中壢家商(桃園市)", value="033408"),
                Choice(name="市立南崁高中(桃園市)", value="034306"),
                Choice(name="市立大溪高中(桃園市)", value="034312"),
                Choice(name="市立壽山高中(桃園市)", value="034314"),
                Choice(name="市立平鎮高中(桃園市)", value="034319"),
                Choice(name="市立觀音高中(桃園市)", value="034332"),
                Choice(name="市立新屋高級中等學校(桃園市)", value="034335"),
                Choice(name="市立永豐高中(桃園市)", value="034347"),
                Choice(name="市立羅浮高中(桃園市)", value="034348"),
                Choice(name="市立大園國際高中(桃園市)", value="034399"),
                Choice(name="國立竹東高中(新竹縣)", value="040302"),
                Choice(name="國立關西高中(新竹縣)", value="040304"),
                Choice(name="國立竹北高中(新竹縣)", value="040308"),
                Choice(name="私立義民高中(新竹縣)", value="041303"),
                Choice(name="私立忠信高中(新竹縣)", value="041305"),
                Choice(name="私立東泰高中(新竹縣)", value="041306"),
                Choice(name="私立仰德高中(新竹縣)", value="041307"),
                Choice(name="私立內思高工(新竹縣)", value="041401"),
                Choice(name="縣立六家高級中學(新竹縣)", value="044311"),
                Choice(name="縣立湖口高中(新竹縣)", value="044320"),
                Choice(name="國立苗栗高中(苗栗縣)", value="050303"),
                Choice(name="國立竹南高中(苗栗縣)", value="050310"),
                Choice(name="國立卓蘭高中(苗栗縣)", value="050314"),
                Choice(name="國立苑裡高中(苗栗縣)", value="050315"),
                Choice(name="國立大湖農工(苗栗縣)", value="050401"),
                Choice(name="國立苗栗農工(苗栗縣)", value="050404"),
                Choice(name="國立苗栗高商(苗栗縣)", value="050407"),
                Choice(name="私立君毅高中(苗栗縣)", value="051302"),
                Choice(name="私立建臺高中(苗栗縣)", value="051306"),
                Choice(name="私立全人實驗高中(苗栗縣)", value="051307"),
                Choice(name="私立中興商工(苗栗縣)", value="051408"),
                Choice(name="私立育民工家(苗栗縣)", value="051411"),
                Choice(name="私立賢德工商(苗栗縣)", value="051412"),
                Choice(name="私立龍德家商(苗栗縣)", value="051413"),
                Choice(name="縣立三義高中(苗栗縣)", value="054308"),
                Choice(name="縣立苑裡高中(苗栗縣)", value="054309"),
                Choice(name="縣立興華高中(苗栗縣)", value="054317"),
                Choice(name="縣立大同高中(苗栗縣)", value="054333"),
                Choice(name="國立興大附中(臺中市)", value="060322"),
                Choice(name="國立中科實驗高級中學(臺中市)", value="060323"),
                Choice(name="財團法人常春藤高中(臺中市)", value="061301"),
                Choice(name="私立明台高中(臺中市)", value="061306"),
                Choice(name="私立致用高中(臺中市)", value="061309"),
                Choice(name="臺中市大明高中(臺中市)", value="061310"),
                Choice(name="私立嘉陽高中(臺中市)", value="061311"),
                Choice(name="私立明道高中(臺中市)", value="061313"),
                Choice(name="私立僑泰高中(臺中市)", value="061314"),
                Choice(name="私立華盛頓高中(臺中市)", value="061315"),
                Choice(name="私立青年高中(臺中市)", value="061316"),
                Choice(name="私立弘文高中(臺中市)", value="061317"),
                Choice(name="私立立人高中(臺中市)", value="061318"),
                Choice(name="私立玉山高中(臺中市)", value="061319"),
                Choice(name="私立慈明高中(臺中市)", value="061321"),
                Choice(name="華德福大地實驗學校(臺中市)", value="061322"),
                Choice(name="市立大甲高中(臺中市)", value="063303"),
                Choice(name="市立清水高中(臺中市)", value="063305"),
                Choice(name="市立豐原高中(臺中市)", value="063312"),
                Choice(name="市立豐原高商(臺中市)", value="063401"),
                Choice(name="市立大甲高工(臺中市)", value="063402"),
                Choice(name="市立東勢高工(臺中市)", value="063404"),
                Choice(name="市立沙鹿高工(臺中市)", value="063407"),
                Choice(name="市立霧峰農工(臺中市)", value="063408"),
                Choice(name="市立后綜高中(臺中市)", value="064308"),
                Choice(name="市立大里高中(臺中市)", value="064324"),
                Choice(name="市立新社高中(臺中市)", value="064328"),
                Choice(name="市立長億高中(臺中市)", value="064336"),
                Choice(name="市立中港高中(臺中市)", value="064342"),
                Choice(name="市立龍津高中(臺中市)", value="064350"),
                Choice(name="市立神岡高工(臺中市)", value="064406"),
                Choice(name="國立彰化女中(彰化縣)", value="070301"),
                Choice(name="國立員林高中(彰化縣)", value="070304"),
                Choice(name="國立彰化高中(彰化縣)", value="070307"),
                Choice(name="國立鹿港高中(彰化縣)", value="070316"),
                Choice(name="國立溪湖高中(彰化縣)", value="070319"),
                Choice(name="國立彰師附工(彰化縣)", value="070401"),
                Choice(name="國立永靖高工(彰化縣)", value="070402"),
                Choice(name="國立二林工商(彰化縣)", value="070403"),
                Choice(name="國立秀水高工(彰化縣)", value="070405"),
                Choice(name="國立彰化高商(彰化縣)", value="070406"),
                Choice(name="國立員林農工(彰化縣)", value="070408"),
                Choice(name="國立員林崇實高工(彰化縣)", value="070409"),
                Choice(name="國立員林家商(彰化縣)", value="070410"),
                Choice(name="國立北斗家商(彰化縣)", value="070415"),
                Choice(name="私立精誠高中(彰化縣)", value="071311"),
                Choice(name="私立文興高中(彰化縣)", value="071317"),
                Choice(name="財團法人正德高中(彰化縣)", value="071318"),
                Choice(name="私立大慶商工(彰化縣)", value="071413"),
                Choice(name="私立達德商工(彰化縣)", value="071414"),
                Choice(name="縣立彰化藝術高中(彰化縣)", value="074308"),
                Choice(name="縣立二林高中(彰化縣)", value="074313"),
                Choice(name="縣立和美高中(彰化縣)", value="074323"),
                Choice(name="縣立田中高中(彰化縣)", value="074328"),
                Choice(name="縣立成功高中(彰化縣)", value="074339"),
                Choice(name="國立南投高中(南投縣)", value="080302"),
                Choice(name="國立中興高中(南投縣)", value="080305"),
                Choice(name="國立竹山高中(南投縣)", value="080307"),
                Choice(name="國立暨大附中(南投縣)", value="080308"),
                Choice(name="國立仁愛高農(南投縣)", value="080401"),
                Choice(name="國立埔里高工(南投縣)", value="080403"),
                Choice(name="國立南投高商(南投縣)", value="080404"),
                Choice(name="國立草屯商工(南投縣)", value="080406"),
                Choice(name="國立水里商工(南投縣)", value="080410"),
                Choice(name="私立五育高中(南投縣)", value="081311"),
                Choice(name="私立三育高中(南投縣)", value="081312"),
                Choice(name="私立弘明實驗高中(南投縣)", value="081313"),
                Choice(name="私立普台高中(南投縣)", value="081314"),
                Choice(name="南投縣同德高中(南投縣)", value="081409"),
                Choice(name="縣立旭光高中(南投縣)", value="084309"),
                Choice(name="國立斗六高中(雲林縣)", value="090305"),
                Choice(name="國立北港高中(雲林縣)", value="090306"),
                Choice(name="國立虎尾高中(雲林縣)", value="090315"),
                Choice(name="國立虎尾農工(雲林縣)", value="090401"),
                Choice(name="國立西螺農工(雲林縣)", value="090402"),
                Choice(name="國立斗六家商(雲林縣)", value="090403"),
                Choice(name="國立北港農工(雲林縣)", value="090404"),
                Choice(name="國立土庫商工(雲林縣)", value="090413"),
                Choice(name="私立永年高中(雲林縣)", value="091307"),
                Choice(name="私立正心高中(雲林縣)", value="091308"),
                Choice(name="私立文生高中(雲林縣)", value="091311"),
                Choice(name="私立巨人高中(雲林縣)", value="091312"),
                Choice(name="私立揚子高中(雲林縣)", value="091316"),
                Choice(name="財團法人義峰高中(雲林縣)", value="091318"),
                Choice(name="福智高中(雲林縣)", value="091319"),
                Choice(name="雲林縣維多利亞實驗高中(雲林縣)", value="091320"),
                Choice(name="私立大成商工(雲林縣)", value="091410"),
                Choice(name="私立大德工商(雲林縣)", value="091414"),
                Choice(name="縣立斗南高中(雲林縣)", value="094301"),
                Choice(name="縣立麥寮高中(雲林縣)", value="094307"),
                Choice(name="縣立古坑華德福實驗高級中學(雲林縣)", value="094308"),
                Choice(name="縣立蔦松藝術高中(雲林縣)", value="094326"),
                Choice(name="國立東石高中(嘉義縣)", value="100301"),
                Choice(name="國立新港藝術高中(嘉義縣)", value="100302"),
                Choice(name="國立民雄農工(嘉義縣)", value="100402"),
                Choice(name="私立同濟高中(嘉義縣)", value="101303"),
                Choice(name="私立協同高中(嘉義縣)", value="101304"),
                Choice(name="私立萬能工商(嘉義縣)", value="101406"),
                Choice(name="縣立竹崎高中(嘉義縣)", value="104319"),
                Choice(name="縣立永慶高中(嘉義縣)", value="104326"),
                Choice(name="國立新豐高中(臺南市)", value="110302"),
                Choice(name="國立臺南大學附中(臺南市)", value="110308"),
                Choice(name="國立北門高中(臺南市)", value="110311"),
                Choice(name="國立新營高中(臺南市)", value="110312"),
                Choice(name="國立後壁高中(臺南市)", value="110314"),
                Choice(name="國立善化高中(臺南市)", value="110315"),
                Choice(name="國立新化高中(臺南市)", value="110317"),
                Choice(name="國立南科國際實驗高中(臺南市)", value="110328"),
                Choice(name="國立新化高工(臺南市)", value="110401"),
                Choice(name="國立白河商工(臺南市)", value="110403"),
                Choice(name="國立北門農工(臺南市)", value="110404"),
                Choice(name="國立曾文家商(臺南市)", value="110405"),
                Choice(name="國立新營高工(臺南市)", value="110406"),
                Choice(name="國立玉井工商(臺南市)", value="110407"),
                Choice(name="國立成大附屬南工(臺南市)", value="110409"),
                Choice(name="國立曾文農工(臺南市)", value="110410"),
                Choice(name="私立南光高中(臺南市)", value="111313"),
                Choice(name="私立港明高中(臺南市)", value="111320"),
                Choice(name="臺南市興國高中(臺南市)", value="111321"),
                Choice(name="私立明達高中(臺南市)", value="111322"),
                Choice(name="私立黎明高中(臺南市)", value="111323"),
                Choice(name="私立新榮高中(臺南市)", value="111326"),
                Choice(name="私立陽明工商(臺南市)", value="111419"),
                Choice(name="私立育德工家(臺南市)", value="111427"),
                Choice(name="市立大灣高中(臺南市)", value="114306"),
                Choice(name="市立永仁高中(臺南市)", value="114307"),
                Choice(name="國立鳳山高中(高雄市)", value="120303"),
                Choice(name="國立岡山高中(高雄市)", value="120304"),
                Choice(name="國立旗美高中(高雄市)", value="120311"),
                Choice(name="國立鳳新高中(高雄市)", value="120319"),
                Choice(name="國立旗山農工(高雄市)", value="120401"),
                Choice(name="國立岡山農工(高雄市)", value="120402"),
                Choice(name="國立鳳山商工(高雄市)", value="120409"),
                Choice(name="光禾華德福實驗學校(高雄市)", value="121302"),
                Choice(name="財團法人新光高中(高雄市)", value="121306"),
                Choice(name="財團法人普門中學(高雄市)", value="121307"),
                Choice(name="私立正義高中(高雄市)", value="121318"),
                Choice(name="私立義大國際高中(高雄市)", value="121320"),
                Choice(name="私立中山工商(高雄市)", value="121405"),
                Choice(name="私立旗美商工(高雄市)", value="121410"),
                Choice(name="私立高英工商(高雄市)", value="121413"),
                Choice(name="私立華德工家(高雄市)", value="121415"),
                Choice(name="私立高苑工商(高雄市)", value="121417"),
                Choice(name="市立文山高中(高雄市)", value="124302"),
                Choice(name="市立林園高中(高雄市)", value="124311"),
                Choice(name="市立仁武高中(高雄市)", value="124313"),
                Choice(name="市立路竹高中(高雄市)", value="124322"),
                Choice(name="市立六龜高中(高雄市)", value="124333"),
                Choice(name="市立福誠高中(高雄市)", value="124340"),
                Choice(name="國立屏東女中(屏東縣)", value="130302"),
                Choice(name="國立屏東高中(屏東縣)", value="130305"),
                Choice(name="國立潮州高中(屏東縣)", value="130306"),
                Choice(name="國立屏北高中(屏東縣)", value="130322"),
                Choice(name="國立內埔農工(屏東縣)", value="130401"),
                Choice(name="國立屏東高工(屏東縣)", value="130403"),
                Choice(name="國立佳冬高農(屏東縣)", value="130404"),
                Choice(name="國立東港海事(屏東縣)", value="130410"),
                Choice(name="國立恆春工商(屏東縣)", value="130417"),
                Choice(name="屏東縣崇華高中(屏東縣)", value="131302"),
                Choice(name="財團法人屏榮高中(屏東縣)", value="131307"),
                Choice(name="私立陸興高中(屏東縣)", value="131308"),
                Choice(name="私立美和高中(屏東縣)", value="131311"),
                Choice(name="私立民生家商(屏東縣)", value="131409"),
                Choice(name="私立日新工商(屏東縣)", value="131418"),
                Choice(name="縣立大同高中(屏東縣)", value="134304"),
                Choice(name="縣立枋寮高中(屏東縣)", value="134321"),
                Choice(name="縣立東港高中(屏東縣)", value="134324"),
                Choice(name="縣立來義高中(屏東縣)", value="134334"),
                Choice(name="國立臺東大學附屬體育高中(臺東縣)", value="140301"),
                Choice(name="國立臺東女中(臺東縣)", value="140302"),
                Choice(name="國立臺東高中(臺東縣)", value="140303"),
                Choice(name="國立關山工商(臺東縣)", value="140404"),
                Choice(name="國立臺東高商(臺東縣)", value="140405"),
                Choice(name="國立成功商水(臺東縣)", value="140408"),
                Choice(name="臺東縣均一高中(臺東縣)", value="141301"),
                Choice(name="私立育仁高中(臺東縣)", value="141307"),
                Choice(name="私立公東高工(臺東縣)", value="141406"),
                Choice(name="縣立蘭嶼高中(臺東縣)", value="144322"),
                Choice(name="國立花蓮女中(花蓮縣)", value="150302"),
                Choice(name="國立花蓮高中(花蓮縣)", value="150303"),
                Choice(name="國立玉里高中(花蓮縣)", value="150309"),
                Choice(name="國立花蓮高農(花蓮縣)", value="150401"),
                Choice(name="國立花蓮高工(花蓮縣)", value="150404"),
                Choice(name="國立花蓮高商(花蓮縣)", value="150405"),
                Choice(name="國立光復商工(花蓮縣)", value="150411"),
                Choice(name="私立海星高中(花蓮縣)", value="151306"),
                Choice(name="私立四維高中(花蓮縣)", value="151307"),
                Choice(name="財團法人慈濟大學附中(花蓮縣)", value="151312"),
                Choice(name="花蓮縣上騰工商(花蓮縣)", value="151410"),
                Choice(name="花蓮縣立體育高中(花蓮縣)", value="154301"),
                Choice(name="縣立南平中學(花蓮縣)", value="154399"),
                Choice(name="國立馬公高中(澎湖縣)", value="160302"),
                Choice(name="國立澎湖海事水產(澎湖縣)", value="160401"),
                Choice(name="國立基隆女中(基隆市)", value="170301"),
                Choice(name="國立基隆高中(基隆市)", value="170302"),
                Choice(name="國立海洋大學附屬基隆海事(基隆市)", value="170403"),
                Choice(name="國立基隆商工(基隆市)", value="170404"),
                Choice(name="私立二信高中(基隆市)", value="171306"),
                Choice(name="輔大聖心高中(基隆市)", value="171308"),
                Choice(name="私立光隆家商(基隆市)", value="171405"),
                Choice(name="私立培德工家(基隆市)", value="171407"),
                Choice(name="市立中山高中(基隆市)", value="173304"),
                Choice(name="市立安樂高中(基隆市)", value="173306"),
                Choice(name="市立暖暖高中(基隆市)", value="173307"),
                Choice(name="市立八斗高中(基隆市)", value="173314"),
                Choice(name="國立竹科實驗高級中等學校(新竹市)", value="180301"),
                Choice(name="國立新竹女中(新竹市)", value="180302"),
                Choice(name="國立新竹高中(新竹市)", value="180309"),
                Choice(name="國立新竹高商(新竹市)", value="180403"),
                Choice(name="國立新竹高工(新竹市)", value="180404"),
                Choice(name="私立光復高中(新竹市)", value="181305"),
                Choice(name="私立曙光女中(新竹市)", value="181306"),
                Choice(name="私立磐石高中(新竹市)", value="181307"),
                Choice(name="私立世界高中(新竹市)", value="181308"),
                Choice(name="市立成德高中(新竹市)", value="183306"),
                Choice(name="市立香山高中(新竹市)", value="183307"),
                Choice(name="市立建功高中(新竹市)", value="183313"),
                Choice(name="國立興大附農(臺中市)", value="190406"),
                Choice(name="私立東大附中(臺中市)", value="191301"),
                Choice(name="私立葳格高中(臺中市)", value="191302"),
                Choice(name="私立新民高中(臺中市)", value="191305"),
                Choice(name="私立宜寧高中(臺中市)", value="191308"),
                Choice(name="私立明德高中(臺中市)", value="191309"),
                Choice(name="私立衛道高中(臺中市)", value="191311"),
                Choice(name="私立曉明女中(臺中市)", value="191313"),
                Choice(name="私立嶺東高中(臺中市)", value="191314"),
                Choice(name="私立磊川華德福實驗教育學校(臺中市)", value="191315"),
                Choice(name="財團法人光華高工(臺中市)", value="191412"),
                Choice(name="市立臺中女中(臺中市)", value="193301"),
                Choice(name="市立臺中一中(臺中市)", value="193302"),
                Choice(name="市立忠明高中(臺中市)", value="193303"),
                Choice(name="市立西苑高中(臺中市)", value="193313"),
                Choice(name="市立東山高中(臺中市)", value="193315"),
                Choice(name="市立惠文高中(臺中市)", value="193316"),
                Choice(name="市立臺中家商(臺中市)", value="193404"),
                Choice(name="市立臺中高工(臺中市)", value="193407"),
                Choice(name="市立臺中二中(臺中市)", value="194303"),
                Choice(name="市立文華高中(臺中市)", value="194315"),
                Choice(name="國立嘉義女中(嘉義市)", value="200302"),
                Choice(name="國立嘉義高中(嘉義市)", value="200303"),
                Choice(name="國立華南高商(嘉義市)", value="200401"),
                Choice(name="國立嘉義高工(嘉義市)", value="200405"),
                Choice(name="國立嘉義高商(嘉義市)", value="200406"),
                Choice(name="國立嘉義家職(嘉義市)", value="200407"),
                Choice(name="私立興華高中(嘉義市)", value="201304"),
                Choice(name="私立仁義高中(嘉義市)", value="201309"),
                Choice(name="私立嘉華高中(嘉義市)", value="201310"),
                Choice(name="私立輔仁高中(嘉義市)", value="201312"),
                Choice(name="私立宏仁高中(嘉義市)", value="201313"),
                Choice(name="私立立仁高中(嘉義市)", value="201314"),
                Choice(name="私立東吳工家(嘉義市)", value="201408"),
                Choice(name="國立臺南二中(臺南市)", value="210303"),
                Choice(name="國立臺南一中(臺南市)", value="210305"),
                Choice(name="國立臺南女中(臺南市)", value="210306"),
                Choice(name="國立家齊高中(臺南市)", value="210309"),
                Choice(name="國立臺南高商(臺南市)", value="210408"),
                Choice(name="國立臺南海事(臺南市)", value="210416"),
                Choice(name="私立長榮高中(臺南市)", value="211301"),
                Choice(name="私立長榮女中(臺南市)", value="211302"),
                Choice(name="財團法人聖功女中(臺南市)", value="211304"),
                Choice(name="臺南市光華高中(臺南市)", value="211310"),
                Choice(name="私立六信高中(臺南市)", value="211314"),
                Choice(name="私立瀛海高中(臺南市)", value="211315"),
                Choice(name="臺南市崑山高中(臺南市)", value="211317"),
                Choice(name="私立德光高中(臺南市)", value="211318"),
                Choice(name="財團法人慈濟高中(臺南市)", value="211320"),
                Choice(name="私立南英商工(臺南市)", value="211407"),
                Choice(name="私立亞洲餐旅(臺南市)", value="211412"),
                Choice(name="私立慈幼工商(臺南市)", value="211419"),
                Choice(name="市立南寧高中(臺南市)", value="213303"),
                Choice(name="市立土城高中(臺南市)", value="213316"),
                Choice(name="私立育達高中(臺北市)", value="311401"),
                Choice(name="市立西松高中(臺北市)", value="313301"),
                Choice(name="市立中崙高中(臺北市)", value="313302"),
                Choice(name="私立協和祐德高中(臺北市)", value="321399"),
                Choice(name="市立松山高中(臺北市)", value="323301"),
                Choice(name="市立永春高中(臺北市)", value="323302"),
                Choice(name="市立松山家商(臺北市)", value="323401"),
                Choice(name="市立松山工農(臺北市)", value="323402"),
                Choice(name="國立師大附中(臺北市)", value="330301"),
                Choice(name="私立延平中學(臺北市)", value="331301"),
                Choice(name="私立金甌女中(臺北市)", value="331302"),
                Choice(name="私立復興實驗高中(臺北市)", value="331304"),
                Choice(name="私立東方工商(臺北市)", value="331402"),
                Choice(name="私立喬治工商(臺北市)", value="331403"),
                Choice(name="私立開平餐飲(臺北市)", value="331404"),
                Choice(name="市立和平高中(臺北市)", value="333301"),
                Choice(name="市立芳和實中(臺北市)", value="333304"),
                Choice(name="市立大安高工(臺北市)", value="333401"),
                Choice(name="私立大同高中(臺北市)", value="341302"),
                Choice(name="私立稻江護家(臺北市)", value="341402"),
                Choice(name="市立中山女中(臺北市)", value="343301"),
                Choice(name="市立大同高中(臺北市)", value="343302"),
                Choice(name="市立大直高中(臺北市)", value="343303"),
                Choice(name="私立強恕中學(臺北市)", value="351301"),
                Choice(name="臺北市開南高中(臺北市)", value="351402"),
                Choice(name="市立建國中學(臺北市)", value="353301"),
                Choice(name="市立成功中學(臺北市)", value="353302"),
                Choice(name="市立北一女中(臺北市)", value="353303"),
                Choice(name="私立靜修高中(臺北市)", value="361301"),
                Choice(name="私立稻江高商(臺北市)", value="361401"),
                Choice(name="市立明倫高中(臺北市)", value="363301"),
                Choice(name="市立成淵高中(臺北市)", value="363302"),
                Choice(name="市立華江高中(臺北市)", value="373301"),
                Choice(name="市立大理高中(臺北市)", value="373302"),
                Choice(name="國立政大附中(臺北市)", value="380301"),
                Choice(name="私立東山高中(臺北市)", value="381301"),
                Choice(name="私立滬江高中(臺北市)", value="381302"),
                Choice(name="私立大誠高中(臺北市)", value="381303"),
                Choice(name="私立再興中學(臺北市)", value="381304"),
                Choice(name="私立景文高中(臺北市)", value="381305"),
                Choice(name="私立靜心高中(臺北市)", value="381306"),
                Choice(name="市立景美女中(臺北市)", value="383301"),
                Choice(name="市立萬芳高中(臺北市)", value="383302"),
                Choice(name="市立數位實驗高中(臺北市)", value="383303"),
                Choice(name="市立木柵高工(臺北市)", value="383401"),
                Choice(name="市立南港高中(臺北市)", value="393301"),
                Choice(name="市立育成高中(臺北市)", value="393302"),
                Choice(name="市立南港高工(臺北市)", value="393401"),
                Choice(name="私立文德女中(臺北市)", value="401301"),
                Choice(name="私立方濟中學(臺北市)", value="401302"),
                Choice(name="私立達人高中(臺北市)", value="401303"),
                Choice(name="市立內湖高中(臺北市)", value="403301"),
                Choice(name="市立麗山高中(臺北市)", value="403302"),
                Choice(name="市立南湖高中(臺北市)", value="403303"),
                Choice(name="市立內湖高工(臺北市)", value="403401"),
                Choice(name="私立泰北高中(臺北市)", value="411301"),
                Choice(name="私立衛理女中(臺北市)", value="411302"),
                Choice(name="私立華興中學(臺北市)", value="411303"),
                Choice(name="私立華岡藝校(臺北市)", value="411401"),
                Choice(name="市立陽明高中(臺北市)", value="413301"),
                Choice(name="市立百齡高中(臺北市)", value="413302"),
                Choice(name="市立士林高商(臺北市)", value="413401"),
                Choice(name="私立薇閣高中(臺北市)", value="421301"),
                Choice(name="臺北市幼華高中(臺北市)", value="421302"),
                Choice(name="私立奎山實驗高級中學(臺北市)", value="421303"),
                Choice(name="私立惇敍工商(臺北市)", value="421404"),
                Choice(name="市立復興高中(臺北市)", value="423301"),
                Choice(name="市立中正高中(臺北市)", value="423302"),
                Choice(name="天主教明誠高中(高雄市)", value="521301"),
                Choice(name="私立大榮高中(高雄市)", value="521303"),
                Choice(name="私立中華藝校(高雄市)", value="521401"),
                Choice(name="市立鼓山高中(高雄市)", value="523301"),
                Choice(name="市立左營高中(高雄市)", value="533301"),
                Choice(name="市立新莊高中(高雄市)", value="533302"),
                Choice(name="市立海青工商(高雄市)", value="533401"),
                Choice(name="市立三民家商(高雄市)", value="533402"),
                Choice(name="國立中山大學附屬國光高中(高雄市)", value="540301"),
                Choice(name="市立中山高中(高雄市)", value="543301"),
                Choice(name="市立楠梓高中(高雄市)", value="543302"),
                Choice(name="私立立志高中(高雄市)", value="551301"),
                Choice(name="南海月光實驗學校(高雄市)", value="551303"),
                Choice(name="私立樹德家商(高雄市)", value="551402"),
                Choice(name="市立高雄中學(高雄市)", value="553301"),
                Choice(name="市立三民高中(高雄市)", value="553302"),
                Choice(name="市立高雄高工(高雄市)", value="553401"),
                Choice(name="市立新興高中(高雄市)", value="563301"),
                Choice(name="市立高雄高商(高雄市)", value="563401"),
                Choice(name="市立高雄女中(高雄市)", value="573301"),
                Choice(name="國立高師大附中(高雄市)", value="580301"),
                Choice(name="私立復華高中(高雄市)", value="581301"),
                Choice(name="天主教道明中學(高雄市)", value="581302"),
                Choice(name="私立三信家商(高雄市)", value="581402"),
                Choice(name="市立中正高中(高雄市)", value="583301"),
                Choice(name="市立前鎮高中(高雄市)", value="593301"),
                Choice(name="市立瑞祥高中(高雄市)", value="593302"),
                Choice(name="市立中正高工(高雄市)", value="593401"),
                Choice(name="國立高餐大附屬餐旅中學(高雄市)", value="610405"),
                Choice(name="市立小港高中(高雄市)", value="613301"),
                Choice(name="國立金門高中(金門縣)", value="710301"),
                Choice(name="國立金門農工(金門縣)", value="710401"),
                Choice(name="國立馬祖高中(連江縣)", value="720301"),
                Choice(name="私立光華高商進修學校(新北市)", value="011C71"),
                Choice(name="私立南華高中進修學校(臺北市)", value="351B09"),
                Choice(name="私立志仁中學進修學校(臺北市)", value="361B09"),
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
    async def register(self, interaction: discord.Interaction, area: Choice[str], school: Choice[str], name: str,
                       student_id: str, grade: Choice[str], tag: Choice[str]):
        embed = discord.Embed(title="🏫 NASH 註冊資料", color=0xea8053, timestamp=datetime.utcnow())
        embed.add_field(name="填報人", value=interaction.user.mention, inline=False)
        embed.add_field(name="地區", value=area.name, inline=False)
        embed.add_field(name="學校", value=school.name, inline=False)
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
            channel = self.bot.get_channel(int(channel_id['register']))
            await channel.send(embed=embed)
        except BaseException as e:
            print(traceback.format_exception(e.__class__, e, e.__traceback__))


# 載入cog中
async def setup(bot: commands.Bot):
    await bot.add_cog(Service(bot))
