下面是一份完整、可直接覆盖使用的 `README.md`：

```markdown
# 智能助手 Agent App

基于 **Function Calling + RAG + Streamlit** 的多工具智能助手。  
支持天气查询、PDF 产品知识库问答、网页上传 PDF 扩展知识库，并提供可视化对话界面。

## 项目简介

本项目实现了一个可演示的 AI Agent 应用，能够根据用户问题自动选择工具：

- 问天气 → 调用天气 API
- 问产品 → 从 PDF 知识库检索（RAG）
- 其他问题 → 由大模型直接回答

知识库支持：
1. 启动时加载默认 PDF（`docs/produce.pdf`）
2. 在网页中上传新的 PDF，动态追加到向量库

适用于学习与展示：**Agent 工具调用、RAG、文档解析、前端交互、基础工程化**。

### 主要功能

- 多工具自动调用（Function Calling）
- PDF 知识库加载与向量检索（ChromaDB + Embedding）
- 网页上传 PDF，动态扩展知识库
- 天气查询（第三方 API）
- Streamlit 可视化对话界面
- 对话历史记录
- 按类型区分回答样式（天气 / 产品 / 其他）
- 产品回答可展示参考资料片段
- 支持 Docker 运行

## 技术栈

- **大模型**：通义千问（Qwen）
- **Agent**：OpenAI 兼容 Function Calling
- **向量数据库**：ChromaDB
- **PDF 解析**：pypdf
- **前端界面**：Streamlit
- **其他**：python-dotenv、requests
- **容器化**：Docker（可选）

## 项目结构

```text
agent_app/
├── docs/
│   ├── produce.pdf         # 默认产品说明 PDF
│   └── uploads/            # 用户上传的 PDF（本地生成，不提交）
├── agent.py                # Agent 核心逻辑（工具调用 + RAG）
├── app.py                  # Streamlit 网页入口
├── pdf_loader.py           # PDF 文本提取
├── gen_pdf.py              # 生成测试用 PDF（可选）
├── requirements.txt        # 依赖列表
├── .env.example            # 环境变量示例
├── .gitignore
├── Dockerfile              # 容器构建文件（如有）
└── README.md
```

## 安装与运行

### 1. 克隆项目

```bash
git clone https://github.com/hctc365853671/agent_app.git
cd agent_app
```

### 2. 创建虚拟环境并安装依赖

```bash
python -m venv venv

# Windows Git Bash
source venv/Scripts/activate

# Windows CMD
# venv\Scripts\activate

pip install -r requirements.txt
```

`requirements.txt` 建议包含：

```text
streamlit
chromadb
openai
python-dotenv
requests
pypdf
```

### 3. 配置环境变量

```bash
cp .env.example .env
```

编辑 `.env`：

```env
QWEN_KEY=你的通义千问API_Key
WEATHER_API_CODE=你的天气API_Code
```

### 4. 准备默认知识库 PDF

确保存在：

```text
docs/produce.pdf
```

如需重新生成测试 PDF，可运行：

```bash
python gen_pdf.py
```

### 5. 启动网页应用

```bash
streamlit run app.py
```

浏览器访问：http://localhost:8501

### 6. 使用 Docker 运行（可选）

```bash
docker build -t agent-app .
docker run --rm -p 8501:8501 -v ${PWD}/.env:/app/.env agent-app
```

然后访问：http://localhost:8501

## 使用说明

### 对话提问

| 问题示例 | 预期行为 |
|----------|----------|
| 鄂州今天天气怎么样？ | 调用天气工具，返回天气信息 |
| 续航多久？/ 有哪些摄像头？ | 检索 PDF 知识库，返回产品相关回答 |
| 你是谁？ | 直接回答，不调用工具 |

### 上传 PDF 扩展知识库

1. 在页面左侧选择 PDF 文件
2. 点击「入库知识库」
3. 等待解析与向量化完成
4. 使用新文档中的内容进行提问

上传文件会保存到 `docs/uploads/`，并追加写入 Chroma 向量库。

## 核心流程

1. 启动时读取默认 PDF，切分文本并写入 ChromaDB（已有数据则跳过）
2. 用户提问后，Agent 判断是否调用工具
3. 问天气 → 调用天气 API  
   问产品 → Embedding 检索知识库
4. 将工具结果返回大模型，生成最终回答
5. 在 Streamlit 页面展示回答与对话历史
6. 用户上传新 PDF 时：保存文件 → 解析 → 向量化 → 追加入库

## 注意事项

- `.env` 不要上传到 GitHub
- `chroma_db` 为本地向量库；更换默认 PDF 后如需重建，可删除该目录再启动
- `docs/uploads/` 为用户上传目录，建议加入 `.gitignore`
- 首次启动会进行向量化，可能需要一些时间
- 请使用可选中文字的 PDF（扫描件图片型 PDF 需要 OCR，当前版本不支持）
- 需要有效的通义千问 API Key 和天气 API Code

## 后续可优化方向

- 检索效果评测（准确率 / 召回）
- 更细的文档切分与元数据管理
- 支持 Word / Markdown 等多种格式
- 增加业务工具（订单查询、FAQ 等）
- 简单鉴权与接口限流
- 部署到云服务器或 Streamlit Cloud

## 作者

个人 AI 应用学习项目，用于练习 Agent、RAG、PDF 知识库与工程化落地。
```