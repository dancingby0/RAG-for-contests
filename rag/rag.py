import asyncio
import websockets
import json
from rag import RAG_economic
from rag import RAG_sports
async def send_message():
    async with websockets.connect("ws://10.242.11.43:8765/rag") as websocket:
        # 接收问题
        query = await websocket.recv()
        print(f"收到问题: {query}")
        # 发送回答
        answer_economic = RAG_economic.main(query)
        print("over-e")
        answer_sports = RAG_sports.main(query)
        print("over-s")
        await websocket.send(json.dumps(answer_economic))
        print("over-ee")
        await websocket.send(json.dumps(answer_sports))
        print("over-ss")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(send_message())