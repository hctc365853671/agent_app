下面是更新后的完整 README，可直接覆盖使用：

```markdown
# 智能助手 Agent App

基于 **Function Calling + RAG + Streamlit** 的多工具智能助手。  
支持天气查询、PDF 产品知识库问答，并提供可视化网页界面。

## 项目简介

本项目实现了一个简单的 AI Agent，能够根据用户问题自动选择工具：

- 问天气 → 调用天气 API
- 问产品 → 从 PDF 知识库检索（RAG）
- 其他问题 → 直接由大模型回答

知识库不再写死在代码中，而是从 `docs/` 目录下的 PDF 文档自动加载、切分并向量化。

### 主要功能

- 多工具自动调用（Function Calling）
- **PDF 知识库加载与向量检索**（ChromaDB + Embedding）
- 天气查询（第三方 API）
- Streamlit 可视化对话界面
- 对话历史记录
- 按类型区分回答样式（天气 / 产品 / 其他）
- 支持 Docker 运行

## 技术栈

- **大模型**：通义千问（Qwen）
- **Agent**：OpenAI 兼容 Function Calling
- **向量数据库**：ChromaDB
- **PDF 解析**：pypdf
- **前端界面**：Streamlit
- **其他**：python-dotenv、requests
- **容器化**：Docker

## 项目结构

```text
agent_app/
├── docs/
│   └── produce.pdf     # 产品说明 PDF（知识库来源）
├── agent.py            # Agent 核心逻辑（工具调用 + RAG）
├── app.py              # Streamlit 网页入口
├── pdf_loader.py       # PDF 文本提取
├── gen_pdf.py          # 生成测试用 PDF（可选）
├── requirements.txt    # 依赖列表
├── .env.example        # 环境变量示例
├── .gitignore
├── Dockerfile          # 容器构建文件（如有）
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

### 4. 准备知识库 PDF

将产品说明 PDF 放到：

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

## 使用示例

| 问题 | 预期行为 |
|------|----------|
| 鄂州今天天气怎么样？ | 调用天气工具，返回天气信息 |
| 续航多久？ / 有哪些摄像头？ | 检索 PDF 知识库，返回产品参数 |
| 你是谁？ | 直接回答，不调用工具 |

## 核心流程

1. 启动时读取 `docs/produce.pdf`，提取文本并切分
2. 文本向量化后写入 ChromaDB（已有数据则跳过）
3. 用户提问后，Agent 判断是否调用工具
4. 问天气 → 调用天气 API  
   问产品 → Embedding 检索知识库
5. 将工具结果返回大模型，生成最终回答
6. 在 Streamlit 页面展示，并记录对话历史

## 注意事项

- `.env` 不要上传到 GitHub
- `chroma_db` 为本地向量库，更换 PDF 后如需重建，可删除该目录再启动
- 首次启动会进行向量化，可能需要一些时间
- 请使用可选中文字的 PDF（扫描件图片 PDF 需要 OCR，当前版本不支持）
- 需要有效的通义千问 API Key 和天气 API Code

## 后续可优化方向

- Streamlit 支持上传 PDF，动态更新知识库
- 支持 Word / Markdown 等多种文档
- 增加更多业务工具（订单、库存等）
- 优化多轮对话与检索效果
- 部署到云服务器或 Streamlit Cloud

## 作者

个人 AI 应用学习项目，用于练习 Agent、RAG、PDF 知识库与工程化落地。
```