import asyncio
import json

import websockets

# 存储前端和大模型的连接
frontend_connection = None
rag_connection = None

async def handle_connection(websocket, path):
    global frontend_connection, rag_connection

    # 区分前端和大模型的连接
    if path == "/frontend":
        frontend_connection = websocket
        print("前端已连接")
    elif path == "/rag":
        rag_connection = websocket
        print("大模型已连接")

    try:
        # 接收前端的问题
        if websocket == frontend_connection:
            question = None
            async for message in websocket:
                print(f"收到前端的问题: {message}")
                question = message
                if frontend_connection and question:
                    await frontend_connection.send("at_server")
                # 将问题发送给大模型
                if rag_connection:
                    await rag_connection.send(question)
                    if frontend_connection:
                        await frontend_connection.send("at_rag")
                    print("问题已发送给大模型")

        # 接收大模型的回答
        elif websocket == rag_connection:
            answers = []
            async for message in websocket:
                print(f"收到大模型的回答: {message}")
                answers.append(message)

                # 如果收到 2 个回答，停止接收
                if len(answers) >= 2:
                    break
            if frontend_connection and answers:
                await frontend_connection.send("at_server")
            # 选择最佳答案
            best_answer = None
            best_percentage = 0
            for answer in answers:
                answer = json.loads(answer)
                percentage = answer["percentage"]
                if percentage > best_percentage:
                    best_percentage = percentage
                    best_answer = answer["answer"]

            # 将最佳答案发送给前端
            if frontend_connection and best_answer:
                await frontend_connection.send("at_frontend")
                await asyncio.sleep(2)
                await frontend_connection.send(best_answer)
                print("最佳答案已发送给前端")

    except websockets.ConnectionClosed:
        print("客户端断开连接")
    finally:
        # 移除断开连接的客户端
        if websocket == frontend_connection:
            frontend_connection = None
            print("前端已断开连接")
        elif websocket == rag_connection:
            rag_connection = None
            print("大模型已断开连接")

async def start_server():
    async with websockets.serve(handle_connection, "10.242.11.43", 8765):
        print("WebSocket 服务器已启动，监听 ws://10.242.11.43:8765")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(start_server())