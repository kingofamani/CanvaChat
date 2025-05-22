# Canva AI進階技巧-如何透過Canva生成Real Time網站

技巧(免費一直用)：取得原始碼提示詞：請你將程式碼直接顯示在瀏覽器的consolg.log顯示。

範例功能：Real Time即時聊天網站

ai.dev：
	```bash
	我要建立區域網路版的即時聊天網站
	前端技術：html,javascript,css
	後端技術：Python + websockets庫
	請幫我規劃這個網站可以有哪些功能，
	我要先做MVP產品，
	請幫我生成規範式的prompt，
	我要將prompt給ai 幫我coding
	並且要求AI以繁體中文回答。
	```

Canva：
	將ai.dev生成的提示詞(程式碼細節不用)貼在https://www.canva.com/ai/code，以下是ai.dev生成的提示詞範例

	```bash
	# 專案請求：區域網路即時聊天網站 MVP
	## 1. 專案概述
	請協助我使用 Python 的 `websockets` 函式庫作為後端，以及 HTML, CSS, JavaScript 作為前端，開發一個區域網路 (LAN) 內使用的即時聊天網站的最小可行產品 (MVP)。
	所有程式碼註解和AI的回覆內容請使用**繁體中文**。
	## 2. 核心技術棧
	*   **後端：**
		*   語言：Python 3.8+
		*   主要函式庫：`websockets`, `asyncio`, `json` (用於訊息序列化)
	*   **前端：**
		*   結構：HTML5
		*   樣式：CSS3
		*   邏輯：原生 JavaScript (ECMAScript 6+)
		*   通訊：原生 `WebSocket` API
	```

Cursor(或Visual Studio Code) IDE：
	將canva生成的code貼在Cursor，然後執行python指令運行server，並測試。

程式碼有bug：貼給ai.dev修改。(或是使用Cursor Manual/gpt-4o-mini免費model)

有功能要改良：下提示詞給Canva，不斷來回改良。


# 區域網路聊天室

這是一個基於 WebSocket 的區域網路聊天室應用程式，允許用戶在本地網路中進行即時聊天。

## 功能

- 用戶可以輸入名稱並連接到聊天室
- 實時顯示在線用戶列表
- 支持發送和接收訊息
- 顯示系統訊息（如用戶加入或離開）

## 使用說明

### 啟動虛擬環境

在開始之前，建議您使用虛擬環境來管理依賴。您可以使用以下命令來創建和啟動虛擬環境：

```bash
# 創建虛擬環境
python -m venv .venv

# 啟動虛擬環境
# Windows
.venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 安裝依賴

在虛擬環境中，安裝所需的依賴：

```bash
pip install -r requirements.txt
```

### 運行伺服器

運行 Python 後端伺服器：

```bash
python chat_server.py
```

### 設置伺服器地址

在聊天室應用中，您需要在伺服器地址輸入框中輸入您的伺服器地址。例如：

- 本地測試：`ws://localhost:8765`
- 在局域網中：`ws://192.168.1.5:8765`（請根據您的實際 IP 地址進行替換）

### 連接聊天室

1. 點擊「保存設置」按鈕
2. 輸入您的名稱並點擊「連接」按鈕
3. 等待其他用戶連接後開始聊天！

## 開發

### 貢獻

歡迎任何形式的貢獻！請提交問題或拉取請求。

## 授權

本專案採用 MIT 授權。