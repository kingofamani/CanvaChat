import asyncio
import json
import websockets
import logging
import socket
from datetime import datetime

# 設置日誌
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("chat_server")

# 全局變數
CLIENTS = {}  # 存儲連接的客戶端 {websocket: username}
USERS = {}    # 存儲用戶名和對應的連接 {username: websocket}

def get_local_ip():
    """獲取本機的區域網IP地址"""
    try:
        # 創建一個臨時連接來獲取本機在區域網中的IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 不需要真正連接到這個地址，只是用來確定使用哪個網絡接口
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        # 如果上述方法失敗，嘗試獲取所有網絡接口
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            return local_ip
        except Exception:
            return "127.0.0.1"  # 如果都失敗，返回本地回環地址

async def register(websocket, username):
    """註冊新客戶端"""
    # 檢查用戶名是否已存在
    if username in USERS:
        # 如果用戶名已存在，生成一個新的用戶名
        base_username = username
        counter = 1
        while username in USERS:
            username = f"{base_username}_{counter}"
            counter += 1
        
        # 通知客戶端用戶名已被修改
        await websocket.send(json.dumps({
            "type": "system",
            "content": f"用戶名 '{base_username}' 已被使用，您的用戶名已更改為 '{username}'"
        }))
    
    # 註冊客戶端
    CLIENTS[websocket] = username
    USERS[username] = websocket
    
    # 通知所有客戶端有新用戶加入
    if len(CLIENTS) > 1:  # 如果不只有一個用戶
        message = {
            "type": "user_joined",
            "username": username,
            "users": list(USERS.keys())
        }
        await broadcast(json.dumps(message))
    
    # 向新客戶端發送當前在線用戶列表
    await websocket.send(json.dumps({
        "type": "user_list",
        "users": list(USERS.keys())
    }))
    
    logger.info(f"用戶 '{username}' 已連接. 當前在線用戶: {len(CLIENTS)}")

async def unregister(websocket):
    """註銷客戶端"""
    if websocket in CLIENTS:
        username = CLIENTS[websocket]
        del CLIENTS[websocket]
        del USERS[username]
        
        # 通知所有客戶端有用戶離開
        message = {
            "type": "user_left",
            "username": username,
            "users": list(USERS.keys())
        }
        await broadcast(json.dumps(message))
        
        logger.info(f"用戶 '{username}' 已斷開連接. 當前在線用戶: {len(CLIENTS)}")

async def broadcast(message):
    """向所有連接的客戶端廣播消息"""
    if CLIENTS:  # 確保有客戶端連接
        await asyncio.gather(
            *[client.send(message) for client in CLIENTS]
        )

async def handle_message(websocket, message_data):
    """處理客戶端發送的消息"""
    try:
        data = json.loads(message_data)
        message_type = data.get("type")
        username = CLIENTS.get(websocket, "未知用戶")
        
        if message_type == "join":
            # 處理加入消息
            new_username = data.get("username", "訪客")
            await register(websocket, new_username)
        
        elif message_type == "message":
            # 處理聊天消息
            content = data.get("content", "")
            if content:
                # 添加時間戳
                timestamp = datetime.now().strftime("%H:%M:%S")
                
                # 創建消息對象
                message = {
                    "type": "message",
                    "username": username,
                    "content": content,
                    "timestamp": timestamp
                }
                
                # 廣播消息
                await broadcast(json.dumps(message))
                logger.info(f"消息來自 '{username}': {content}")
    
    except json.JSONDecodeError:
        logger.error(f"無效的 JSON 格式: {message_data}")
        await websocket.send(json.dumps({
            "type": "system",
            "content": "錯誤: 無效的消息格式"
        }))
    
    except Exception as e:
        logger.error(f"處理消息時出錯: {str(e)}")
        await websocket.send(json.dumps({
            "type": "system",
            "content": f"錯誤: {str(e)}"
        }))

async def chat_server(websocket):
    """處理 WebSocket 連接"""
    try:
        # 發送歡迎消息
        await websocket.send(json.dumps({
            "type": "system",
            "content": "歡迎來到聊天室！請輸入您的用戶名。"
        }))
        
        # 處理消息
        async for message in websocket:
            await handle_message(websocket, message)
    
    except websockets.exceptions.ConnectionClosed as e:
        logger.info(f"連接已關閉: {e.code if hasattr(e, 'code') else 'unknown'} {e.reason if hasattr(e, 'reason') else ''}")
    except Exception as e:
        logger.error(f"處理連接時出錯: {str(e)}")
    
    finally:
        # 確保客戶端被註銷
        await unregister(websocket)

async def main():
    """啟動 WebSocket 伺服器"""
    # 獲取本地IP地址
    local_ip = get_local_ip()
    host = local_ip  # 使用本地IP地址
    port = 8765
    
    # 同時監聽本地回環地址和區域網IP
    logger.info(f"啟動聊天伺服器於 {host}:{port}")
    logger.info(f"您可以使用以下地址連接到伺服器:")
    logger.info(f"本機連接: ws://localhost:{port}")
    logger.info(f"區域網連接: ws://{host}:{port}")
    
    # 啟動伺服器
    async with websockets.serve(chat_server, host, port):
        await asyncio.Future()  # 運行直到被取消

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("伺服器已停止")