import argparse
import asyncio
import config
import threading
from tool_manager import process_requests

async def listener():
    print("CHAD Tool Manager - Running\n")
    while True:
        process_requests()
        await asyncio.sleep(0.5)

async def main():
    ai_tasks = []
    ai_tasks.append(asyncio.create_task(listener()))
    await asyncio.gather(*ai_tasks)

if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description="CHAD Tool Manager")
    # parser.add_argument("tool_channel", type=str, help="tool_channel")
    # args = parser.parse_args()
    # config.USER_ID = args.user_id

    asyncio.run(main())