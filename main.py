from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List
import random

app = FastAPI()

# 存储与客户端的 WebSocket 连接
clients: List[WebSocket] = []

# 模拟大模型处理函数
def large_model_process(content: str, client_id: int) -> str:
    # 假设大模型处理的内容会改变输入内容（这里只是一个简单的模拟）
    return f"Model {client_id} processed: {content}"

# WebSocket 路由：前端连接时接收内容并分发给两个客户端
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        # 接收前端的内容
        content = await websocket.receive_text()
        
        # 将内容处理后发送给两个客户端
        responses = []
        if len(clients) >= 2:
            # 随机选择两个客户端并处理内容
            for client_id, client in enumerate(clients[:2]):
                # 将内容发送给客户端
                await client.send_text(content)
                # 等待客户端返回结果
                response = await client.receive_text()
                # 保存客户端返回的处理结果
                responses.append(f"Client {client_id + 1}: {response}")
        
        # 从客户端返回的响应中随机选择一个
        if responses:
            final_response = random.choice(responses)
            # 将最终结果返回给前端
            await websocket.send_text(final_response)
        
    except WebSocketDisconnect:
        clients.remove(websocket)
        print("Client disconnected")

# WebSocket 路由：客户端连接时加入到客户端列表
@app.websocket("/client/ws")
async def client_websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            # 客户端处理前端发送的内容并返回
            content = await websocket.receive_text()
            # 模拟大模型处理
            processed_content = large_model_process(content, len(clients))
            # 将处理后的内容返回给服务端
            await websocket.send_text(processed_content)
    except WebSocketDisconnect:
        clients.remove(websocket)
        print("Client disconnected")
