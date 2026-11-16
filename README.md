# 115-backend

實作單元「[從模型 API 到執行迴圈：六週實作](https://gloomcheng.github.io/115-backend/agent-runtime/)」的個人作業與練習倉庫。

## 環境設定

1. 安裝相依套件：

```bash
pip install -r requirements.txt
```

2. 設定 `NVIDIA_API_KEY`（**請勿將 `.env` 或真實金鑰提交至 Git**）：

```bash
cp .env.example .env
# 編輯 .env 填入你的 NVIDIA_API_KEY
```

或直接在終端機匯出環境變數：

```bash
export NVIDIA_API_KEY=YOUR_NVIDIA_API_KEY
```

## Week 1：第一次模型呼叫

- 程式檔案：[`week1_single_call.py`](week1_single_call.py)
- 端點：`POST https://integrate.api.nvidia.com/v1/chat/completions`
- 模型：`minimaxai/minimax-m3.1-flash`

執行 Python 單次呼叫：

```bash
python3 week1_single_call.py
```

也可在命令列傳入自訂提問：

```bash
python3 week1_single_call.py "請用一句話說明什麼是 REST API"
```

使用 `curl -v` 觀察 HTTP Request / Response 欄位：

```bash
curl -v https://integrate.api.nvidia.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $NVIDIA_API_KEY" \
  -d '{
    "model": "minimaxai/minimax-m3.1-flash",
    "messages": [
      {"role": "user", "content": "用一句話說明什麼是 HTTP"}
    ],
    "max_tokens": 512,
    "temperature": 1,
    "top_p": 0.95
  }'
```
