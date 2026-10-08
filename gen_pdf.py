from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate

# 注册中文字体
pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
FONT_NAME = 'STSong-Light'

# 产品介绍文本（已分段）
text_content = """神舟战神是国产电脑品牌神舟（Hasee）旗下的游戏本子系列，隶属于新天下集团，2013 年正式推出，凭借 “低价高配” 的特点，在玩家圈被称为 “神船”，选购战神笔记本也被玩家戏称为 “上船”。

在战神诞生之前，高性能游戏本价格普遍高昂，普通学生与游戏玩家很难负担。神舟选择与蓝天电脑合作，采用成熟的公模方案打造战神系列，在保证硬件性能的前提下大幅压缩成本，一举打破高端游戏本高价垄断的局面，“神船大法保平安” 的说法也由此流传开来。

产品定位上，战神主打高性能游戏与生产力场景，覆盖从入门到中高端多个档位，拥有 S、Z、T、TX、G 等多条产品线。S 系列定位入门性价比款，适合预算有限的学生，主流搭载 RTX4050、RTX4060 显卡；Z、T 系列为中端主力，CPU 搭配酷睿 HX 系列，屏幕升级到 2.5K 高刷屏，兼顾游戏、视频剪辑、3D 建模；TX、G 系列属于高端旗舰，搭载桌面级处理器与满血高端独显，面向重度 3A 游戏、AI 计算等高强度需求。战神机型普遍预留双内存、双硬盘插槽，支持用户自行升级扩容，可灵活增加内存与固态硬盘，可玩性很高。

硬件配置方面，战神全系采用英特尔酷睿高性能移动处理器，搭配 NVIDIA RTX 系列独立显卡，支持独显直连，屏幕覆盖 144Hz、165Hz、180Hz 等高刷新率 IPS 屏，部分高配机型拥有高色域面板，接口齐全，包含 USB、HDMI、网口等，方便外接显示器、外设。散热采用多热管 + 双风扇方案，配合控制中心可调节风扇转速与性能模式，平衡性能与噪音。

战神最大优势就是同价位性能释放更强，硬件规格扎实，可扩展性强，非常适合预算有限、懂基础电脑知识，追求硬件性能的用户。但它的短板同样明显，为控制成本，机身做工质感一般，塑料外壳居多；早期机型品控波动较大，自带的系统优化一般，售后网点数量相比一线品牌更少，更适合有一定动手能力、愿意自行排查小问题的用户。

时至今日，神舟战神依然是国内游戏本市场极具代表性的高性价比产品线，推动了国产游戏本普及，成为很多游戏玩家的入门首选。"""

pdf_path = "C:/Users/36585/Desktop/shenzhou_zhan_shen.pdf"
doc = SimpleDocTemplate(pdf_path, pagesize=A4)
story = []
styles = getSampleStyleSheet()

# 标题样式
title_style = ParagraphStyle(
    "CustomTitle",
    parent=styles["Heading1"],
    fontName=FONT_NAME,
    fontSize=18,
    spaceAfter=20
)
# 正文样式
body_style = ParagraphStyle(
    "CustomBody",
    parent=styles["Normal"],
    fontName=FONT_NAME,
    fontSize=12,
    leading=18
)

# 循环添加段落
lines = text_content.split("\n")
for idx, para_text in enumerate(lines):
    para_text = para_text.strip()
    if not para_text:
        continue
    if idx == 0:
        p = Paragraph(para_text, title_style)
    else:
        p = Paragraph(para_text, body_style)
    story.append(p)
doc.title = "神舟战神 产品介绍"
doc.build(story)
print(f"✅ PDF生成成功：{pdf_path}")
