import streamlit as st  # type: ignore

# 设置 ZhipuAI API Key
st.sidebar.title("设置")

global api_key_option
api_key_option = st.sidebar.radio("选择 API 密钥选项：", ("输入自定义密钥", "使用默认密钥"))

# Streamlit 前端界面
st.title("🔎 基于本地知识库的问答系统")
st.markdown("本系统主要通过本地知识库检索答案，并结合 ChatGLM 生成清晰、准确的回答。")
st.write("---")  # 分隔线

# 初始化 session_state 用于存储问答历史
if "qa_history" not in st.session_state:
    st.session_state["qa_history"] = [{"role": "assistant", "content": "您好！请问有什么可以帮助您？"}]

# 显示对话历史
for msg in st.session_state["qa_history"]:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])

# 定义检索和回答函数
def retrieve_answer(question):
    from langchain_community.embeddings import HuggingFaceBgeEmbeddings  # type: ignore
    from langchain_community.vectorstores import FAISS  # type: ignore
    from zhipuai import ZhipuAI  # type: ignore

    # 获取 API 密钥
    if api_key_option == "输入自定义密钥":
        zhipu_api_key = st.sidebar.text_input("输入您的 ZhipuAI API 密钥", type="password", help="从 https://open.bigmodel.cn/usercenter/apikeys 获取密钥")
    else:
        zhipu_api_key = "your_key_in_there"  # 替换为默认密钥

    if not zhipu_api_key:
        st.warning("请输入您的 ZhipuAI API 密钥。")
        st.warning("您可以从 https://open.bigmodel.cn/usercenter/apikeys 获取密钥。")
        st.stop()
        return

    # 初始化 ZhipuAI 客户端
    client = ZhipuAI(api_key=zhipu_api_key)

    # 加载嵌入模型
    model_name = "BAAI/bge-large-zh-v1.5"  # 替换为中文模型
    model_kwargs = {"device": "cpu"}
    encode_kwargs = {"normalize_embeddings": True}
    bgeEmbeddings = HuggingFaceBgeEmbeddings(
        model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
    )

    # 加载本地向量数据库
    db_path = "weibo"  # 替换为本地向量数据库路径
    new_db = FAISS.load_local(db_path, bgeEmbeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(question)

    # 提取上下文内容
    context = "\n\n".join([doc.page_content for doc in docs]) if docs else "未找到相关文档内容。"

    # 调试信息
    # st.write("检索到的上下文：", context)

    # 调用 ZhipuAI 的 API 生成回答
    with st.spinner("正在检索答案..."):
        response = client.chat.completions.create(
            model="glm-4-long",
            messages=[
                {
                    "role": "user",
                    "content": (
                        "请根据本地知识库，回答以下问题，并始终用中文作答。\n\n"
                        "### 回答规则：\n"
                        "1. 优先使用本地微博评论知识库中的信息进行回答。\n"
                        "2. 如果本地微博评论知识库中的信息不足，请补充使用网络搜索结果。\n"
                        "3. 如果无法从本地微博评论知识库或网络搜索中找到相关信息，请回答：“此信息在本地微博评论知识库或网络搜索结果中均不可用。”\n\n"
                        "### 提供的本地微博评论知识库：\n"
                        f"\"\"\"\n{context}\n\"\"\"\n\n"
                        "### 问题：\n"
                        f"\"\"\"\n{question}\n\"\"\"\n\n"
                        "### 回答要求：\n"
                        "1. 请直接提供最终答案。\n"
                        "2. 明确指出答案的来源：“微博评论知识库”、“网络搜索”或“两者结合”。\n"
                        "3. 如果回答中包含对评论内容的分析或解释，请提供简要的说明。\n"
                        "4. 确保回答内容简洁明了，符合网络交流的表述习惯，避免冗长。\n\n"
                        "### 请开始回答："
                        "### 举例： \n"
                        "问题1： 用户对某明星新电影的评论态度如何？\n"
                        "回答1：多数用户持正面态度，认为电影剧情吸引人，演员表现力强。\n"
                        "问题2： 网友对某品牌手机最新款式的评价怎样？\n"
                        "回答2：评价褒贬不一，部分用户认为新款手机设计新颖，性能提升明显，但也有用户反映价格偏高，性价比不如预期。\n"
                    ),
                }
            ],
            stream=True,
        )
        answer = "".join(chunk.choices[0].delta.content for chunk in response)

    # 检查回答是否为空
    if not answer.strip():
        st.error("API 返回的回答为空，请检查模型或上下文内容是否正确。")
    return answer

# 处理用户输入和响应
if prompt := st.chat_input("请输入您的问题："):
    # 保存用户输入
    st.session_state["qa_history"].append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # 获取回答并显示进度条
    response = retrieve_answer(prompt)
    st.session_state["qa_history"].append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)

# 清除聊天记录按钮

if st.sidebar.button("清除聊天记录"):
    st.session_state.clear()
    st.session_state["qa_history"] = [{"role": "assistant", "content": "您好！请问有什么可以帮助您？"}]