import asyncio, pyvts

plugin_info = {
    "plugin_name": "AIVtuber",
    "developer": "AIVtuber",
    "authentication_token_path": "./token.txt"
}
vts_api_info={
    "version" : "1.0",
    "name" : "VTubeStudioPublicAPI",
    "port": 8001
}

async def connect_auth(myvts):
    ''' functions to get authenticated '''
    await myvts.connect()
    await myvts.request_authenticate_token()
    await myvts.request_authenticate()
    await myvts.close()

async def trigger(myvts):
    ''' function to trigger hotkey '''
    myvts = pyvts.vts(plugin_info=plugin_info,vts_api_info=vts_api_info)
    await myvts.connect()
    await myvts.request_authenticate()
    response_data = await myvts.request(myvts.vts_request.requestHotKeyList())
    print(response_data)
    hotkey_list = []
    for hotkey in response_data["data"]["availableHotkeys"]:
        hotkey_list.append(hotkey["name"])
    send_hotkey_request = myvts.vts_request.requestTriggerHotKey(hotkey_list[6])
    await myvts.request(send_hotkey_request)  # send request to play 'My Animation 1'
    await myvts.close()


if __name__ == "__main__":
    asyncio.run(main())