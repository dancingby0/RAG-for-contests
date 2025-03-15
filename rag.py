import asyncio
import websockets
import json

async def send_message():
    async with websockets.connect("ws://10.242.11.43:8765/rag") as websocket:
        # 接收问题
        question = await websocket.recv()
        print(f"收到问题: {question}")
        await asyncio.sleep(10)#模拟大模型生成答案等待的时间。
        # 发送回答
        answer1 = {"percentage": 0.9, "answer": "Michael Jordan"}
        answer2 = {"percentage": 1, "answer": "Stephen Curry"}
        answer3 = {"percentage": 0.1, "answer": "Lebron James"}
        await websocket.send(json.dumps(answer1))
        await websocket.send(json.dumps(answer2))
        await websocket.send(json.dumps(answer3))

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(send_message())