import asyncio
import websockets

async def send_message():
    async with websockets.connect("ws://10.242.11.43:8765/frontend") as websocket:
        # 发送问题
        question = "who is the goat of the NBA history?"
        await websocket.send(question)
        print(f"已发送问题: {question}")
        statement = "none"
        while statement != "at_frontend":
            statement = await websocket.recv()
            print("进程进展：{}".format(statement))
        # 接收最佳答案
        best_answer = await websocket.recv()
        print(f"最佳答案: {best_answer}")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(send_message())