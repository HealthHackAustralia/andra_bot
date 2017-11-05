#!/usr/bin/env python

import asyncio
import websockets

async def hello():
    async with websockets.connect('ws://ec2-54-197-14-241.compute-1.amazonaws.com:8765') as websocket:
        while(True):
            with open('camera_0.png', 'rb') as image:
                print(image.read())
                name = input("What's your name? ")
                await websocket.send(image.read())
                print("> {}".format(name))

                greeting = await websocket.recv()
                print("< {}".format(greeting))

asyncio.get_event_loop().run_until_complete(hello())
