# 115-backend

Agent Runtime 課程實作練習（[教材連結](https://gloomcheng.github.io/115-backend/agent-runtime/)）。

## 環境設定

```bash
pip install -r requirements.txt
cp .env.example .env  # 填入 NVIDIA_API_KEY（.env 已忽略，不會提交）
```

或直接在終端機設定環境變數：

```bash
export NVIDIA_API_KEY=your_api_key
```

## Week 1：`week1_single_call.py`

```bash
# 預設提問
python3 week1_single_call.py

# 自訂提問 / 指定模型
python3 week1_single_call.py "用一句話說明什麼是 HTTP"
python3 week1_single_call.py --model minimaxai/minimax-m3.1-flash "什麼是 REST API"
```
