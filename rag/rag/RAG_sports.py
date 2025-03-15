import torch
import websocket
from sentence_transformers import SentenceTransformer, util
import requests
import pickle
import os
from tqdm import tqdm
import asyncio
import websockets
import json

# 模型和向量的缓存路径
CACHE_DIR = r"D:\DUT\freshterm\science_creation\信息安全竞赛\web\rag\cache"
MODEL_CACHE = os.path.join(CACHE_DIR, "model.pkl")
EMBEDDINGS_CACHE = os.path.join(CACHE_DIR, "embeddings.pkl")

# 创建缓存目录
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

# 初始化向量数据库（使用缓存机制）
documents = []
document_embeddings = None

# 延迟加载模型
embedding_model = None

def get_embedding_model():
    global embedding_model
    if embedding_model is None:
        # 尝试从缓存加载模型
        if os.path.exists(MODEL_CACHE):
            try:
                with open(MODEL_CACHE, 'rb') as f:
                    embedding_model = pickle.load(f)
                print("已从缓存加载模型")
            except:
                embedding_model = SentenceTransformer("paraphrase-MiniLM-L6-v2")
                # 保存模型到缓存
                with open(MODEL_CACHE, 'wb') as f:
                    pickle.dump(embedding_model, f)
        else:
            embedding_model = SentenceTransformer("paraphrase-MiniLM-L6-v2")
            # 保存模型到缓存
            with open(MODEL_CACHE, 'wb') as f:
                pickle.dump(embedding_model, f)
    return embedding_model

# 添加文档到向量数据库
def add_documents(docs):
    """将文档添加到向量数据库中"""
    global documents, document_embeddings
    documents.extend(docs)
    
    print("正在处理文档...")
    with tqdm(total=2, desc="知识库初始化") as pbar:
        # 如果缓存存在且文档数量匹配，直接加载缓存的嵌入向量
        if os.path.exists(EMBEDDINGS_CACHE):
            try:
                with open(EMBEDDINGS_CACHE, 'rb') as f:
                    cached_data = pickle.load(f)
                    if len(cached_data['documents']) == len(documents):
                        documents = cached_data['documents']
                        document_embeddings = cached_data['embeddings']
                        pbar.update(2)
                        print("已从缓存加载文档向量")
                        return
            except:
                pass
        
        pbar.update(1)
        # 计算文档的嵌入向量，使用批处理和并行
        model = get_embedding_model()
        document_embeddings = model.encode(
            documents, 
            convert_to_tensor=True,
            show_progress_bar=True,
            batch_size=32,  # 增加批处理大小
            device='cuda' if torch.cuda.is_available() else 'cpu'  # 使用GPU如果可用
        )
        
        # 保存到缓存
        cache_data = {
            'documents': documents,
            'embeddings': document_embeddings
        }
        with open(EMBEDDINGS_CACHE, 'wb') as f:
            pickle.dump(cache_data, f)
        
        pbar.update(1)
    
    print(f"已添加 {len(docs)} 个文档到知识库")

# 从向量数据库中检索相关文档
def retrieve_from_vectordb(query, top_k=1):
    """从向量数据库中检索与问题相关的文档片段"""
    try:
        if not documents or document_embeddings is None:
            return ["知识库为空，请先添加文档"]

        model = get_embedding_model()
        query_embedding = model.encode(query, convert_to_tensor=True)

        # 计算相似度并获取最相关的文档
        scores = util.cos_sim(query_embedding, document_embeddings)
        top_indices = torch.topk(scores, k=min(top_k, len(documents))).indices[0]

        return [documents[idx] for idx in top_indices]
    except Exception as e:
        print(f"检索文档时出错: {e}")
        return ["检索过程中出现错误"]


# 使用本地部署的模型进行文本生成
def generate(query, retrieved_docs):
    """使用 DeepSeek API 结合检索的文档进行文本生成"""
    messages = [
        {
            "role": "system",
            "content": "你是一个知识丰富的 AI 助手。请针对用户的问题提供3个不同的答案，每个答案用[答案X]（X为1-3的数字）标记。",
        },
        {"role": "user", "content": f"以下是相关知识库内容：\n{retrieved_docs[0]}"},
        {
            "role": "user",
            "content": f"问题：{query}\n\n请提供3个不同的答案。",
        },
    ]

    headers = {
        "Authorization": "Bearer sk-249d0e7720a24e1e832c93694c15747e",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    payload = {
        "model": "deepseek-chat",
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 800,
        "stream": False
    }

    try:
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            json=payload,
            headers=headers,
            timeout=30
        )
        if response.status_code != 200:
            print(f"API 响应错误，状态码：{response.status_code}")
            print(f"错误详情：{response.text}")
            return "API 调用失败，请检查配置和网络连接。"
            
        result = response.json()
        answers = result["choices"][0]["message"]["content"]
        
        # 分割三个答案
        answer_list = []
        for i in range(1, 4):
            start = answers.find(f"[答案{i}]")
            if start != -1:
                if i < 3:
                    end = answers.find(f"[答案{i+1}]")
                    if end == -1:
                        end = len(answers)
                else:
                    end = len(answers)
                answer = answers[start+5:end].strip()
                answer_list.append(answer)
        
        # 计算每个答案与知识库的相似度
        model = get_embedding_model()
        knowledge_embedding = model.encode(retrieved_docs[0], convert_to_tensor=True)
        
        max_confidence = 0
        best_answer = ""
        
        for answer in answer_list:
            answer_embedding = model.encode(answer, convert_to_tensor=True)
            confidence = float(util.cos_sim(answer_embedding, knowledge_embedding)[0][0])
            if confidence > max_confidence:
                max_confidence = confidence
                best_answer = answer
        ans = {"answer":best_answer,"percentage":max_confidence}
        return ans
        #return f"{best_answer}\n\n置信度：{max_confidence:.2f}"
        
    except Exception as e:
        print(f"调用 DeepSeek API 时出错: {e}")
        if 'response' in locals():
            print(f"错误详情: {response.text}")
        return "未能生成答案，请检查网络连接和 API 密钥是否正确。"
def main(query:str):
    # 从文件读取知识库内容
    sample_docs = []
    knowledge_files = [
        r"D:\DUT\freshterm\science_creation\信息安全竞赛\web\rag\rag\baidu_knowledge.txt",
    ]

    # print("开始加载知识库文件...")
    # 使用更大的批量处理大小
    batch_size = 100  # 增加批处理大小

    with tqdm(total=len(knowledge_files), desc="文件加载") as pbar:
        for file_path in knowledge_files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read().strip()  # 一次性读取并处理
                    # 直接分割并过滤
                    docs = [
                        line.strip()
                        for line in content.split("\n")
                        if line.strip() and not line.startswith("#")
                    ]
                    sample_docs.extend(docs)
                    pbar.update(1)
                    print(f"成功加载知识库文件：{file_path}")
            except Exception as e:
                print(f"读取知识库文件时出错 {file_path}: {e}")
                continue

    if not sample_docs:
        print("没有成功加载任何知识库文件")
        exit(1)

    add_documents(sample_docs)
    k = 0
    # 添加交互式问答循环
    # print("\n知识库加载完成！请输入您的问题（输入 'q' 退出）：")
    while k == 0:
        # async with websockets.connect("ws://10.242.11.43:8765/rag") as websocket:
        #     # 接收问题
        #     query = websocket.recv()
        # query = input("\n请输入问题: ").strip()
        if query.lower() in ["q", "quit"]:
            print("感谢使用，再见！")
            break

        if not query:
            print("问题不能为空，请重新输入！")
            continue  # 删除多余的 break

        # 检索相关文档
        retrieved_docs = retrieve_from_vectordb(query)
        print("\n检索到的相关文档标题：")
        # 假设每个文档的第一行是标题，只显示前30个字符
        doc_title = (
            retrieved_docs[0].split("\n")[0][:30] + "..."
            if len(retrieved_docs[0]) > 30
            else retrieved_docs[0]
        )
        # print(doc_title)
        # print("\n正在生成回答...\n")

        # 生成答案
        answer = generate(query, retrieved_docs)
        k+=1
        # print("回答：")
        # if "置信度：" not in answer:
        #     print(answer)
        #     # 根据检索文档的相关性计算默认置信度
        #     scores = util.cos_sim(
        #         embedding_model.encode(query, convert_to_tensor=True),
        #         embedding_model.encode(retrieved_docs[0], convert_to_tensor=True),
        #     )
        #     default_confidence = float(scores[0][0])
        #     print(f"\n置信度：{default_confidence:.2f}")
        # else:
        #     print(answer)

            # websocket.send(json.dumps(answer))
    return answer

# 主流程
if __name__ == "__main__":
    main("世界上最伟大的运动员？")
    # # 从文件读取知识库内容
    # sample_docs = []
    # knowledge_files = [
    #     r"D:\DUT\freshterm\science_creation\信息安全竞赛\web\rag\rag\baidu_knowledge.txt",
    # ]
    #
    # print("开始加载知识库文件...")
    # # 使用更大的批量处理大小
    # batch_size = 100  # 增加批处理大小
    #
    # with tqdm(total=len(knowledge_files), desc="文件加载") as pbar:
    #     for file_path in knowledge_files:
    #         try:
    #             with open(file_path, "r", encoding="utf-8") as f:
    #                 content = f.read().strip()  # 一次性读取并处理
    #                 # 直接分割并过滤
    #                 docs = [
    #                     line.strip()
    #                     for line in content.split("\n")
    #                     if line.strip() and not line.startswith("#")
    #                 ]
    #                 sample_docs.extend(docs)
    #                 pbar.update(1)
    #                 print(f"成功加载知识库文件：{file_path}")
    #         except Exception as e:
    #             print(f"读取知识库文件时出错 {file_path}: {e}")
    #             continue
    #
    # if not sample_docs:
    #     print("没有成功加载任何知识库文件")
    #     exit(1)
    #
    # add_documents(sample_docs)
    #
    # # 添加交互式问答循环
    # print("\n知识库加载完成！请输入您的问题（输入 'q' 退出）：")
    # while True:
    #     # async with websockets.connect("ws://10.242.11.43:8765/rag") as websocket:
    #     #     # 接收问题
    #     #     query = websocket.recv()
    #     query = input("\n请输入问题: ").strip()
    #     if query.lower() in ["q", "quit"]:
    #         print("感谢使用，再见！")
    #         break
    #
    #     if not query:
    #         print("问题不能为空，请重新输入！")
    #         continue  # 删除多余的 break
    #         break
    #
    #     # 检索相关文档
    #     retrieved_docs = retrieve_from_vectordb(query)
    #     print("\n检索到的相关文档标题：")
    #     # 假设每个文档的第一行是标题，只显示前30个字符
    #     doc_title = (
    #         retrieved_docs[0].split("\n")[0][:30] + "..."
    #         if len(retrieved_docs[0]) > 30
    #         else retrieved_docs[0]
    #     )
    #     print(doc_title)
    #     print("\n正在生成回答...\n")
    #
    #     # 生成答案
    #     answer = generate(query, retrieved_docs)
    #     print("回答：")
    #     if "置信度：" not in answer:
    #         print(answer)
    #         # 根据检索文档的相关性计算默认置信度
    #         scores = util.cos_sim(
    #             embedding_model.encode(query, convert_to_tensor=True),
    #             embedding_model.encode(retrieved_docs[0], convert_to_tensor=True),
    #         )
    #         default_confidence = float(scores[0][0])
    #         print(f"\n置信度：{default_confidence:.2f}")
    #     else:
    #         print(answer)
    #         #websocket.send(json.dumps(answer))
