import streamlit as st
from agent import TwoTools
import re,os
import pdf_loader



# 初始化 放在最顶部
if "rag_bot" not in st.session_state:
    st.session_state.rag_bot = TwoTools()
    print("rag_bot 已加载")
rag_bot = st.session_state.rag_bot

if "history_session" not in st.session_state:
    st.session_state.history_session = []

if "is_disabled" not in st.session_state:
    st.session_state.is_disabled = False
if "up_file_names" not in st.session_state:
    st.session_state.up_file_names = []
# 临时存放上传的PDF文件对象
if "temp_pdf_file" not in st.session_state:
    st.session_state.temp_pdf_file = None

col_up,col_chat, col_history = st.columns([3,3,3])

# ========== 左侧上传PDF区域 ==========
with col_up:
    try:
        #上传pdf文档补充知识库
        with st.form("upload_pdf_form", clear_on_submit=True):
            upload_button_pdf = st.file_uploader(
                "上传PDF文件，补充知识库",
                type=["pdf"],
                max_upload_size=10,
                disabled=st.session_state.is_disabled
            )
            submit_button = st.form_submit_button(
                "入库知识库",
                disabled=st.session_state.is_disabled
            )
            if submit_button:
                if not upload_button_pdf:
                    st.warning("请先选择PDF文件！")
                else:
                    # 暂存文件，标记处理中，立刻rerun锁定UI 
                    if upload_button_pdf.name in st.session_state.up_file_names :
                        st.session_state.is_disabled=False
                        st.session_state.temp_pdf_file=None
                        st.warning("文件名或则内容重复")
                    else:
                        st.session_state.temp_pdf_file = upload_button_pdf
                        st.session_state.is_disabled=True
                        st.rerun()

        # ======== 表单外部执行入库逻辑 ========
        if st.session_state.is_disabled and st.session_state.temp_pdf_file is not None:
            with st.spinner("正在解析PDF并入库..."):
                os.makedirs("docs/uploads",exist_ok=True)
                save_path = os.path.join("docs/uploads", st.session_state.temp_pdf_file.name)
                with open(save_path,"wb") as file:
                    file.write(st.session_state.temp_pdf_file.getvalue())
                
                pdf_content = pdf_loader.load_pdf(save_path)
                rag_bot.collectionAdd(pdf_content)
                st.session_state.up_file_names.append(st.session_state.temp_pdf_file.name)
            # 清理临时文件，解锁
            st.session_state.temp_pdf_file = None
            st.session_state.is_disabled=False
            st.rerun()
       

        if bool(st.session_state.up_file_names):
            st.write("现有库存有:\n"+"\n".join(st.session_state.up_file_names))
        else:
            st.write("尚未上传知识库")

    except Exception as e:
        st.error(f"PDF入库失败: {str(e)}")
        # 异常兜底解锁
        st.session_state.is_disabled=False
        st.session_state.temp_pdf_file = None
        st.rerun()

# ========== 侧边栏 ==========
with st.sidebar:
    st.title("智能助手使用说明")
    st.markdown("# 📖 使用说明")
    st.divider()
    st.markdown("""
    - 🌤️ **天气查询**
      提问包含城市+天气，会返回天气卡片
      > 示例：鄂州今天天气怎么样？
    - 📦 **产品咨询**
      提问产品相关，返回产品介绍卡片
      > 示例：投影仪参数、投影仪怎么选
    - ✅ 操作
      1. 在输入框输入问题
      2. 点击【发送】获取回答
      3. 点击【清空对话】清空回答内容
    """)
    st.divider()
    st.markdown("💡 提示：一次只提一个问题，识别更准确")

# ========== 聊天区域 ==========
try:
    with col_chat:
        st.title("智能助手")
        clear_button = st.button("清空对话")
        # ========== 表单区域 start ==========
        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_area("请输入您的问题或需求", height=100)
            send_button = st.form_submit_button("发送")
        # ========== 表单区域 end ==========
        if send_button:
            if not user_input.strip():
                st.warning("请输入内容后再发送")
            else:
                st_waiting=st.text("正在处理您的请求，请稍等...")
                responseJson = rag_bot.get_response(user_input)
                ai_answer = responseJson.get('data')
                pattern = r"【category:(weather|product|other)】"
                ture_ai_answer = re.sub(pattern, "", ai_answer).strip()
                st.session_state.history_session.append({"user_input": user_input, "ai_answer": ture_ai_answer})
                st_waiting.empty()
                # AI回答框
                if "【category:weather】" in ai_answer:
                    st.info(ture_ai_answer, icon="🌤️")
                elif "【category:product】" in ai_answer:
                    st.success(ture_ai_answer, icon="📦")
                    ai_reference=responseJson.get("reference")
                    if ai_reference:
                        st.success("参考资料为:"+ai_reference)
                else:
                    st.warning(ai_answer, icon="⚠️")
        # 清空对话按钮逻辑
        if clear_button:
            rag_bot.messages = [{
                "role": "system",
                "content": """你是一个专业的产品助手。
                如果用户问天气请调用天气查询工具getWeather，如果客户要查产品知识库请调用getCorrelation工具。
                回答结束，在输出的末尾单独一行输出标签：
                如果是天气相关回答，输出【category:weather】
                如果是产品相关回答，输出【category:product】
                无关问题输出【category:other】
                严格根据参考资料回答，不要编造。如果资料不足，请回答：根据现有资料无法回答。"""
            }]
            st.session_state.history_session = []
            st.rerun()

    with col_history:
        st.title("对话历史")
        st.divider()
        if st.session_state.history_session:
            for msg in st.session_state.history_session:
                st.markdown(f"**用户问题:** {msg['user_input']}")
                st.divider()
                st.markdown(f"**AI回答:** {msg['ai_answer']}")
                st.divider()
        else:
            st.info("暂无对话历史")
except Exception as e:
    st.error(f"发生错误: {str(e)}")
