import streamlit as st
from RAG本地 import add_documents, retrieve_from_vectordb, generate

# 设置页面标题
st.set_page_config(page_title="RAG 问答系统", layout="wide")
st.title("RAG 问答系统")

# 初始化会话状态
if 'knowledge_initialized' not in st.session_state:
    st.session_state.knowledge_initialized = False
if 'knowledge_cache' not in st.session_state:
    st.session_state.knowledge_cache = {}

# 初始化知识库
# 在初始化知识库函数中添加进度条
def init_knowledge_base():
    sample_docs = []
    knowledge_files = [
        "d:/pathonpro/pythonProject6/RAG本地运行/example.txt",
        "d:/pathonpro/pythonProject6/RAG本地运行/baidu_knowledge.txt",
    ]

    progress_bar = st.progress(0)
    total_files = len(knowledge_files)

    for idx, file_path in enumerate(knowledge_files):
        try:
            # 更新进度条
            progress = (idx + 1) / total_files
            progress_bar.progress(progress)

            # 原有的文件处理逻辑
            if file_path in st.session_state.knowledge_cache:
                sample_docs.extend(st.session_state.knowledge_cache[file_path])
                st.success(f"从缓存加载知识库文件：{file_path}")
                continue

            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                docs = [
                    line.strip()
                    for line in content.split("\n")
                    if line.strip() and not line.startswith("#")
                ]
                # 保存到缓存
                st.session_state.knowledge_cache[file_path] = docs
                sample_docs.extend(docs)
                st.success(f"成功加载知识库文件：{file_path}")
        except Exception as e:
            st.error(f"读取知识库文件时出错 {file_path}: {e}")
            continue

    if not sample_docs:
        st.error("没有成功加载任何知识库文件")
        return False

    add_documents(sample_docs)
    st.session_state.knowledge_initialized = True
    return True

# 在侧边栏添加初始化按钮
with st.sidebar:
    st.header("知识库管理")
    if st.button("初始化知识库") or st.session_state.knowledge_initialized:
        if not st.session_state.knowledge_initialized:
            init_knowledge_base()

    # 添加文件上传功能
    uploaded_file = st.file_uploader("上传新的知识文件（TXT格式）", type=["txt"])
    if uploaded_file is not None:
        content = uploaded_file.getvalue().decode("utf-8")
        new_docs = [
            line.strip()
            for line in content.split("\n")
            if line.strip() and not line.startswith("#")
        ]
        try:
            add_documents(new_docs)
            st.success("成功添加新知识！")
        except Exception as e:
            st.error(f"添加知识时出错: {e}")

# 主界面
# 创建输入框
query = st.text_area("请输入您的问题：", height=100)

# 创建提交按钮
# 添加缓存装饰器
@st.cache_data(ttl=3600)  # 缓存1小时
def cached_retrieve(query):
    return retrieve_from_vectordb(query)

@st.cache_data(ttl=3600)
def cached_generate(query, docs):
    return generate(query, docs)

# 主界面部分
if st.button("提交问题"):
    if not st.session_state.knowledge_initialized:
        st.warning("请先初始化知识库！")
    elif query:
        with st.spinner("正在思考中..."):
            # 使用缓存版本的函数
            retrieved_docs = cached_retrieve(query)
            
            if retrieved_docs and retrieved_docs[0] != "知识库为空，请先添加文档":
                doc_title = (
                    retrieved_docs[0].split("\n")[0][:30] + "..."
                    if len(retrieved_docs[0]) > 30
                    else retrieved_docs[0]
                )

                # 使用缓存版本的生成函数
                answer = cached_generate(query, retrieved_docs)

                # 显示结果
                st.subheader("参考文档：")
                st.info(doc_title)

                st.subheader("回答：")
                if "置信度：" not in answer:
                    st.write(answer)
                    st.success(f"置信度：0.50")
                else:
                    answer_parts = answer.rsplit("置信度：", 1)
                    st.write(answer_parts[0])
                    st.success(f"置信度：{answer_parts[1]}")
            else:
                st.error("知识库为空或检索失败，请确保已正确初始化知识库")
    else:
        st.warning("请输入问题！")

    progress_bar.empty()  # 完成后清除进度条
