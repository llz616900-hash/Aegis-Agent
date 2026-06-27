# Quick Start — 10 分钟运行 Aegis-Agent

> 最精简步骤，适合已有 Python / Git 经验的用户

---

## 前置条件（提前完成）

- [ ] Python 3.10+ 已安装，`python --version` 可用
- [ ] [Ollama](https://ollama.com) 已安装，`ollama --version` 可用
- [ ] 至少 8 GB 可用磁盘空间

---

## Step 1 — 克隆并安装

```bash
git clone https://github.com/your-username/Aegis-Agent.git
cd Aegis-Agent
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
```

---

## Step 2 — 下载 Ollama 模型

```bash
ollama pull qwen3:4b
```

然后编辑 `backend/config/config.py`，修改第 25–26 行：

```python
MODEL_PRO   = "qwen3:4b"
MODEL_INTIM = "qwen3:4b"
```

---

## Step 3 — 下载 Vosk 模型

1. 下载 [vosk-model-small-en-us-0.15](https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip)
2. 解压，重命名目录为 `vosk`
3. 放到项目：`models/vosk/`

---

## Step 4 — 准备语音样本

录制 10–20 秒的清晰语音（WAV 格式，22050 Hz，单声道），放入：

```
sample_voice/formal/01.wav     ← 正式语音
sample_voice/intimate/01.wav   ← 亲密语音（可与正式相同）
```

格式转换（如果是 m4a/mp3）：
```bash
ffmpeg -i input.m4a -ac 1 -ar 22050 sample_voice/formal/01.wav
```

---

## Step 5 — 启动后端

```bash
# Windows
scripts\start_backend.bat

# macOS / Linux
bash scripts/start_backend.sh
```

看到 `Application startup complete.` 即成功。

验证：
```bash
curl http://localhost:8000/status
```

---

## Step 6 — 第一次对话

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, who are you?"}'
```

---

## Step 7 — 运行 Flutter 客户端（可选）

```bash
cd frontend/flutter_app

# 修改 lib/main.dart 中的 IP（改为你的局域网 IP）

flutter pub get
flutter run          # 连接手机或模拟器运行
```

---

## 完整 API 文档

后端运行后访问：**http://localhost:8000/docs**

---

## 遇到问题？

查看 [USER_GUIDE.md](USER_GUIDE.md) 第 9 节"常见问题"。
