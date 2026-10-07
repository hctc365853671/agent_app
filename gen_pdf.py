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
text_content = """DJI Mavic 4 Pro 产品介绍
大疆创新作为全球无人机行业的领军品牌，持续推动航拍技术走向更高水准。DJI Mavic 4 Pro 是大疆推出的消费级旗舰航拍无人机，兼顾便携机身、多摄影像系统、强大飞行性能与智能安全能力，面向风光摄影师、短视频创作者、航拍爱好者等群体，为空中影像创作提供专业可靠的解决方案。

在影像配置上，Mavic 4 Pro 搭载三摄系统，包含一枚 4/3 英寸哈苏主摄、1/1.3 英寸中长焦相机以及 1/1.5 英寸长焦相机。哈苏主摄拥有一亿像素拍摄能力，支持 6K/60fps HDR 视频录制，色彩还原真实细腻，动态范围出色，无论是日出日落的大光比风光，还是城市建筑细节，都能保留丰富层次。两枚长焦镜头拓展拍摄空间，远距离拍摄山体、高塔、野生动物时，无需靠近主体，即可捕捉清晰画面。全系镜头支持双原生 ISO 融合技术，暗光环境下噪点控制优秀，夜晚城市航拍也能获得干净通透的素材。云台支持 360° 旋转，打破传统云台拍摄角度限制，环绕运镜、仰拍、俯拍等镜头语言都可以轻松实现，大幅拓宽创作者的运镜思路。

飞行性能方面，Mavic 4 Pro 最长飞行时间可达 51 分钟，长续航可以支持大范围风光拍摄、长距离跟拍，减少频繁更换电池带来的中断。机身配备 O4 + 图传系统，最远图传距离可达 30 公里，支持 10-bit HDR 高清实时画面回传，远距离飞行时画面依然流畅稳定，延迟低，方便创作者实时构图。同时搭载 0.1Lux 夜景级全向主动避障系统，机身六个方向都配备感知传感器，白天、弱光环境都可以识别树木、电线、建筑等障碍物，飞行途中自动规避风险。即使在城市复杂环境、峡谷树林等场景，也能显著降低炸机风险，新手和专业用户都能获得更高的飞行安全保障。

智能拍摄功能是这款产品的一大亮点。内置多种智能运镜模式，包括环绕、渐远、锁定、跟随等，用户只需要设定目标主体，无人机自动完成流畅的电影级镜头。全向智能跟随算法经过优化，可以识别行人、骑行者、车辆等目标，主体移动时持续锁定，非常适合户外 vlog、运动记录。同时支持焦点跟随、智能航点飞行，预先规划航线，无人机按照预设路线自动飞行拍摄，适合固定场景的重复性航拍作业。搭配 DJI RC 2 带屏遥控器，内置高亮屏幕，强光下也能看清画面，无需额外连接手机，开机即可飞行，提升外出拍摄效率。

机身设计延续 Mavic 系列可折叠结构，机臂快速折叠收纳，体积紧凑，方便放入背包携带，适合旅行、户外采风。在可靠性方面，支持 DJI Care 随心换服务，意外损坏可以享受低价置换，同时新增安全奖励与操作者意外险，进一步降低使用顾虑。

产品应用场景十分广泛。风光摄影爱好者可以奔赴山川湖泊，记录宏大自然景观；短视频创作者利用长焦与智能跟拍，产出高质量空中镜头；工程、文旅从业者也可以使用它完成场地勘测、景区全景拍摄。

总体而言，DJI Mavic 4 Pro 将专业影像能力、长续航、可靠避障与便携设计融为一体，降低了高质量航拍的创作门槛。它不只是一台航拍工具，更是普通人探索空中视角、记录世界的创作载体，代表着消费级航拍设备的高水平发展方向。"""

pdf_path = "docs/produce.pdf"
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
doc.title = "DJI Mavic 4 Pro 产品介绍"
doc.build(story)
print(f"✅ PDF生成成功：{pdf_path}")
