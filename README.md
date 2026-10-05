# 智能助手 Agent App

基于 **Function Calling + RAG + Streamlit** 的多工具智能助手。  
支持天气查询与产品知识库问答，并提供可视化网页界面。

## 项目简介

本项目实现了一个简单的 AI Agent，能够根据用户问题自动选择工具：

- 问天气 → 调用天气 API
- 问产品 → 检索本地知识库（RAG）
- 其他问题 → 直接由大模型回答

同时提供 Streamlit 网页界面，支持多轮对话与历史记录展示。

### 主要功能

- 多工具自动调用（Function Calling）
- 产品知识库向量检索（ChromaDB + Embedding）
- 天气查询（第三方 API）
- Streamlit 可视化对话界面
- 对话历史记录
- 按类型区分回答样式（天气 / 产品 / 其他）

## 技术栈

- **大模型**：通义千问（Qwen）
- **Agent**：OpenAI 兼容 Function Calling
- **向量数据库**：ChromaDB
- **前端界面**：Streamlit
- **其他**：python-dotenv、requests

## 项目结构

```text
agent_app/
├── agent.py            # Agent 核心逻辑（工具调用 + RAG）
├── app.py              # Streamlit 网页入口
├── requirements.txt    # 依赖列表
├── .env.example        # 环境变量示例
├── .gitignore
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

建议的 `requirements.txt`：

```text
streamlit
chromadb
openai
python-dotenv
requests
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

### 4. 启动网页应用

```bash
streamlit run app.py
```

浏览器访问：http://localhost:8501

## 使用示例

| 问题 | 预期行为 |
|------|----------|
| 鄂州今天天气怎么样？ | 调用天气工具，返回天气信息 |
| 投影仪多重？ | 检索知识库，返回产品参数 |
| 电池能用多久？ | 检索知识库，返回续航信息 |
| 你是谁？ | 直接回答，不调用工具 |

## 核心流程

1. 用户在网页输入问题
2. Agent 判断是否需要调用工具
3. 如需查天气 → 调用天气 API  
   如需查产品 → Embedding + Chroma 检索
4. 将工具结果返回给大模型
5. 生成自然语言回答并在页面展示

## 注意事项

- `.env` 不要上传到 GitHub
- `chroma_db` 为本地向量库，首次运行会自动创建
- 需要有效的通义千问 API Key 和天气 API Code
- 首次启动会进行知识库向量化，可能需要一点时间

## 后续可优化方向

- 支持上传 PDF / Word 作为知识库
- 增加更多工具（如搜索、计算）
- 优化多轮对话上下文管理
- 部署到云服务器或 Streamlit Cloud
- 增加用户登录与权限控制

## 作者

个人 AI 应用学习项目，用于练习 Agent、RAG 与工程化落地。
```