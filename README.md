# 基于本地知识库的智能问答系统 / Local Knowledge Base Q&A System

> Author: Junjie Chen (cliffcedar0@gmail.com)

这是一个基于 Streamlit 构建的智能问答系统，集成了本地知识库检索和智谱AI的 ChatGLM 模型，能够根据本地知识库内容提供智能问答服务。

This is an intelligent Q&A system built with Streamlit, integrating local knowledge base retrieval and ZhipuAI's ChatGLM model, capable of providing intelligent Q&A services based on local knowledge base content.

## 功能特点 / Features

- 🎯 基于本地知识库的智能问答 / Intelligent Q&A based on local knowledge base
- 🔍 使用 FAISS 向量数据库进行高效检索 / Efficient retrieval using FAISS vector database
- 🤖 集成智谱AI的 ChatGLM 模型 / Integrated with ZhipuAI's ChatGLM model
- 💬 简洁直观的聊天界面 / Simple and intuitive chat interface
- 🔄 支持对话历史记录 / Support for conversation history
- 🔑 灵活的 API 密钥配置 / Flexible API key configuration

## 技术栈 / Tech Stack

- Streamlit: 用于构建 Web 界面 / For building web interface
- LangChain: 用于向量数据库和嵌入模型 / For vector database and embedding models
- FAISS: 用于向量相似度搜索 / For vector similarity search
- HuggingFace BGE Embeddings: 用于文本向量化 / For text vectorization
- 智谱AI API: 用于生成回答 / ZhipuAI API: For generating answers

## 安装与配置 / Installation & Configuration

1. 克隆项目到本地 / Clone the project:
```bash
git clone [项目地址]
cd [项目目录]
```

2. 安装依赖 / Install dependencies:
```bash
pip install -r requirements.txt
```

3. 配置 API 密钥 / Configure API key:
   - 访问 [智谱AI开放平台](https://open.bigmodel.cn/usercenter/apikeys) 获取 API 密钥 / Visit [ZhipuAI Open Platform](https://open.bigmodel.cn/usercenter/apikeys) to get API key
   - 在应用界面选择 API 密钥选项 / Choose API key option in the application interface:
     - 使用默认密钥 / Use default key
     - 或输入自定义密钥 / Or input custom key

## 使用方法 / Usage

1. 运行应用 / Run the application:
```bash
streamlit run app.py
```

2. 在浏览器中访问应用界面 / Access the application interface in your browser

3. 在输入框中输入问题，系统将 / Enter your question in the input box, the system will:
   - 从本地知识库检索相关信息 / Retrieve relevant information from local knowledge base
   - 结合检索结果生成回答 / Generate answers based on retrieval results
   - 显示回答来源（微博评论知识库/网络搜索/两者结合） / Show answer sources (Weibo comment knowledge base/Web search/Both)

## 项目结构 / Project Structure

```
.
├── app.py              # 主应用文件 / Main application file
├── requirements.txt    # 项目依赖 / Project dependencies
└── weibo/             # 本地知识库目录 / Local knowledge base directory
```

## 注意事项 / Notes

- 确保本地知识库（weibo 目录）已正确配置 / Ensure the local knowledge base (weibo directory) is properly configured
- API 密钥需要正确设置才能使用 / API key needs to be correctly set to use
- 建议使用支持中文的模型进行向量化 / It is recommended to use Chinese-supported models for vectorization

## 贡献指南 / Contributing

欢迎提交 Issue 和 Pull Request 来帮助改进项目。
Feel free to submit issues and pull requests to help improve the project.

## 许可证 / License

[添加许可证信息] / [Add license information]

## 联系方式 / Contact

- Author: Junjie Chen
- Email: cliffcedar0@gmail.com 