# Aegis-Agent 用户使用手册

> 面向零基础用户的完整部署指南

---

## 1. 项目介绍

**Aegis-Agent** 是一个完全运行在本地的 AI 陪伴系统。

它的核心特点：

- **完全离线** — 所有数据、对话、语音全部存储在本地，不联网，不上传
- **双人格引擎** — 支持正式（Professional）和亲密（Intimate）两种对话风格，可手动切换或按场景自动切换
- **长期记忆** — 使用向量数据库记住历史对话，每次聊天都能"记得"你说过的话
- **语音克隆** — 使用你自己录制的声音样本，生成专属 AI 语音（XTTS-v2）
- **离线语音识别** — 说话直接转文字，不需要网络（Vosk）
- **跨平台客户端** — Flutter App 支持 Android 和 iOS

---

## 2. 系统要求

### 推荐配置（流畅运行）

| 组件 | 推荐规格 |
|---|---|
| CPU | Intel i5 12代 / AMD Ryzen 5 5600 或更高 |
| 内存 | 16 GB RAM |
| 显卡 | NVIDIA RTX 3060 / 4060（8 GB VRAM） |
| 存储 | 20 GB 可用空间（SSD 推荐） |
| 系统 | Windows 10/11 64位 |

### 最低配置（可运行，速度较慢）

| 组件 | 最低规格 |
|---|---|
| CPU | Intel i5 8代 / AMD Ryzen 5 3600 |
| 内存 | 8 GB RAM |
| 显卡 | NVIDIA RTX 3050（**4 GB VRAM**） |
| 存储 | 15 GB 可用空间 |
| 系统 | Windows 10 64位 |

### RTX 3050 4GB 实测说明

本项目最初在 RTX 3050 4GB 显卡上开发，针对 4GB 显存做了优化：

- XTTS-v2 语音合成：限制单次文本长度 ≤ 150 字符，防止显存溢出
- LLM 推理通过 Ollama 管理，使用量化模型（4-bit）
- 建议同时只运行一个 GPU 任务（语音合成 或 LLM，不要同时高负载）

> **纯 CPU 模式：** 无独立显卡也可运行，但语音合成速度会明显变慢（每句话需要 10–30 秒）。

---

## 3. 环境安装

### 3.1 安装 Python

1. 打开 https://www.python.org/downloads/
2. 下载 **Python 3.10.x**（推荐 3.10，兼容性最佳）
3. 安装时 **必须勾选** `Add Python to PATH`
4. 验证安装：

```cmd
python --version
# 输出示例：Python 3.10.11
```

### 3.2 安装 Git

1. 打开 https://git-scm.com/download/win
2. 下载并安装（全部默认选项即可）
3. 验证：

```cmd
git --version
# 输出示例：git version 2.44.0
```

### 3.3 安装 Ollama

1. 打开 https://ollama.com
2. 点击 **Download** → 下载 Windows 版安装包
3. 运行安装程序
4. 安装完成后，Ollama 会在后台自动启动
5. 验证：

```cmd
ollama --version
```

### 3.4 克隆项目

```cmd
git clone https://github.com/your-username/Aegis-Agent.git
cd Aegis-Agent
```

### 3.5 创建 Python 虚拟环境

```cmd
python -m venv venv
venv\Scripts\activate
```

激活成功后，命令行前面会出现 `(venv)`。

### 3.6 安装依赖

```cmd
pip install -r requirements.txt
```

> 首次安装时间较长（约 10–30 分钟），需要下载 PyTorch 等大型依赖。
> 
> 如果有 NVIDIA 显卡，安装完成后执行以下命令验证 GPU 可用：
> ```cmd
> python -c "import torch; print(torch.cuda.is_available())"
> # 输出 True 表示 GPU 可用
> ```

---

## 4. 模型下载

### 4.1 下载 Ollama 模型

```cmd
# 推荐：轻量快速（4B，约 3.5GB）
ollama pull qwen3:4b

# 拉取完成后验证
ollama list
```

创建专属人格模型（可选）：

```cmd
ollama create aegis-agent -f docs/Modelfile.example
```

然后修改 `backend/config/config.py`：

```python
MODEL_PRO   = "aegis-agent:latest"
MODEL_INTIM = "aegis-agent:latest"
```

### 4.2 下载 Vosk 语音识别模型

1. 打开 https://alphacephei.com/vosk/models
2. 下载 `vosk-model-small-en-us-0.15`（英文，40MB，速度快）
3. 解压缩，确保目录结构如下：

```
models/
└── vosk/
    ├── am/
    ├── conf/
    ├── graph/
    └── ivector/
```

### 4.3 XTTS-v2 语音合成模型

**首次运行时自动下载**（约 1.8 GB），无需手动操作。

如果想提前下载：

```cmd
python -c "from TTS.api import TTS; TTS('tts_models/multilingual/multi-dataset/xtts_v2')"
```

---

## 5. 启动后端

确保已激活虚拟环境（命令行前有 `(venv)`）：

```cmd
# Windows
scripts\start_backend.bat

# 或者直接运行
uvicorn backend.app:app --host 0.0.0.0 --port 8000 --reload
```

启动成功后会看到：

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

打开浏览器访问：

- **API 文档（Swagger）：** http://localhost:8000/docs
- **健康检查：** http://localhost:8000/status

---

## 6. 启动 Flutter 客户端

### 准备工作

1. 安装 Flutter SDK：https://docs.flutter.dev/get-started/install
2. 安装 Android Studio（用于 Android 模拟器/编译）

### 修改后端地址

编辑 `frontend/flutter_app/lib/main.dart`，找到：

```dart
Uri.parse("http://192.168.1.101:8000/chat")
```

替换为你的后端 IP 地址（本机测试用 `127.0.0.1`，手机连接用局域网 IP）：

```dart
Uri.parse("http://192.168.1.xxx:8000/chat")
```

查询本机局域网 IP：

```cmd
ipconfig
# 查看 IPv4 地址，通常是 192.168.x.x
```

### 运行（开发模式）

```cmd
cd frontend/flutter_app
flutter pub get
flutter run
```

### 打包 Android APK

```cmd
cd frontend/flutter_app
flutter build apk --release
```

APK 文件路径：`frontend/flutter_app/build/app/outputs/flutter-apk/app-release.apk`

---

## 7. 首次运行配置

### 修改 config.py

打开 `backend/config/config.py`，按需修改以下内容：

```python
# Ollama 地址（默认本机，不需要改）
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

# 使用的模型名称（改为你实际下载的模型）
MODEL_PRO   = "aegis-agent:latest"   # 或 "qwen3:4b"
MODEL_INTIM = "aegis-agent:latest"

# 正式语音样本文件（指向 sample_voice/formal/ 下的文件）
VOICE_FORMAL_WAV   = VOICE_FORMAL_DIR / "01.wav"

# 亲密语音样本文件
VOICE_INTIMATE_WAV = VOICE_INTIMATE_DIR / "15.wav"
```

---

## 8. 创建自己的语音克隆

### 为什么需要录音？

XTTS-v2 是一个**零样本语音克隆**模型。它通过分析你提供的 WAV 样本，学习说话者的音色、语调、语速，然后用这个"声音特征"合成任意文字的语音。

### 录音要求

| 项目 | 要求 |
|---|---|
| 时长 | **10–20 秒**（最少 6 秒） |
| 格式 | WAV，单声道，22050 Hz |
| 内容 | 自然朗读，避免长时间停顿 |
| 环境 | 安静房间，无回声，无背景音乐 |

### 步骤

1. 打开 Windows **录音机** App（或 Audacity）
2. 录制 10–20 秒的自然朗读
3. 保存为 `.m4a` 或 `.wav`
4. 如需格式转换，使用 ffmpeg：

```cmd
ffmpeg -i your_voice.m4a -ac 1 -ar 22050 sample_voice/formal/01.wav
```

5. 将文件放到对应目录：
   - 正式风格：`sample_voice/formal/01.wav`
   - 亲密风格：`sample_voice/intimate/01.wav`

6. 重启后端，测试语音：

```bash
# 通过 API 测试 TTS
curl -X POST http://localhost:8000/tts \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello, this is a test.", "persona": "aegis_pro"}'
```

---

## 9. 常见问题

### Ollama 超时 / 无响应

**现象：** `/chat` 接口返回 `Error: ...timeout`

**解决：**
1. 检查 Ollama 是否在运行：打开任务管理器，查找 `ollama.exe`
2. 重启 Ollama：
   ```cmd
   # 关闭后重新运行
   ollama serve
   ```
3. 确认模型已下载：`ollama list`
4. 检查 `config.py` 中的 `MODEL_PRO` 名称是否与 `ollama list` 输出一致

---

### XTTS 加载失败 / 显存不足

**现象：** `CUDA out of memory` 或 `RuntimeError: CUDA error`

**解决：**
1. 关闭其他占用显存的程序（游戏、其他 AI 软件）
2. 检查文本长度是否超过 150 字符（`voice_clone.py` 中已有截断保护）
3. 强制使用 CPU：

```python
# 在 backend/speech/voice_clone.py 中修改
tts = TTS(
    model_name="tts_models/multilingual/multi-dataset/xtts_v2",
    gpu=False   # 改为 False
)
```

---

### Vosk 找不到模型

**现象：** `Exception: Failed to create a model...`

**解决：**
1. 确认 `models/vosk/` 目录存在且包含 `am/`, `conf/`, `graph/` 等子目录
2. 检查 `config.py` 中的路径：

```python
VOSK_MODEL_PATH = MODELS_DIR / "vosk"
```

3. 在 Python 中手动验证路径：

```python
from backend.config.config import VOSK_MODEL_PATH
print(VOSK_MODEL_PATH.exists())  # 应输出 True
```

---

### ChromaDB 错误

**现象：** `RuntimeError: Chroma...` 或数据库锁定

**解决：**
1. 确保没有两个后端实例同时运行
2. 删除数据库重新开始：

```cmd
# WARNING: 这会清除所有记忆
rmdir /s /q data\chroma_db
```

3. 重启后端，ChromaDB 会自动重新创建

---

### 端口占用

**现象：** `ERROR: [Errno 10048] Only one usage of each socket address...`

**解决：**

```cmd
# 查找占用 8000 端口的进程
netstat -ano | findstr :8000

# 结束该进程（将 <PID> 替换为实际数字）
taskkill /PID <PID> /F
```

或者换一个端口启动：

```cmd
uvicorn backend.app:app --host 0.0.0.0 --port 8001
```

---

## 10. 项目结构说明

```
Aegis-Agent/
│
├── backend/                  ← Python 后端（FastAPI）
│   ├── app.py               ← 服务主入口，所有 API 路由
│   ├── api/                 ← 路由模块（可扩展）
│   ├── agent/               ← 人格管理、场景控制、主动消息
│   │   ├── persona_manager.py  ← 切换 pro/intim 人格，锁定功能
│   │   ├── scene_manager.py    ← 管理当前场景状态
│   │   ├── scene_auto.py       ← 场景→人格自动同步逻辑
│   │   ├── proactive_manager.py← 主动消息队列
│   │   └── proactive_worker.py ← 后台定时推送线程
│   ├── config/              ← 配置管理
│   │   └── config.py        ← 所有路径、模型名称的统一配置
│   ├── core/                ← 数据模型（Pydantic schemas）
│   ├── llm/                 ← LLM 调用层
│   │   └── ollama_client.py ← Ollama HTTP 接口封装
│   ├── memory/              ← 向量记忆系统
│   │   ├── memory.py        ← ChromaDB 增删查清操作
│   │   └── memory_loader.py ← 从文件导入历史记忆
│   └── speech/              ← 语音模块
│       ├── speech.py        ← Vosk 语音识别（STT）
│       ├── voice_clone.py   ← XTTS-v2 语音合成（TTS）
│       └── convert_audio.py ← M4A→WAV 格式转换工具
│
├── frontend/
│   └── flutter_app/         ← Flutter 跨平台客户端（Android/iOS）
│       └── lib/main.dart    ← 主界面（聊天 UI）
│
├── sample_voice/            ← 你的语音克隆样本（不上传 git）
│   ├── formal/              ← 正式人格语音样本
│   └── intimate/            ← 亲密人格语音样本
│
├── models/                  ← AI 模型文件（不上传 git，手动下载）
│   ├── vosk/                ← Vosk ASR 模型
│   ├── xtts/                ← XTTS-v2 缓存（自动下载）
│   └── ollama/              ← Ollama 模型（由 Ollama 管理）
│
├── data/                    ← 运行时数据（不上传 git）
│   ├── chroma_db/           ← ChromaDB 向量数据库
│   └── generated_audio/     ← TTS 生成的音频文件
│
├── docs/                    ← 文档
├── scripts/                 ← 启动脚本
├── sample_data/             ← 用于导入的记忆文件示例
│
├── README.md                ← GitHub 首页介绍
├── requirements.txt         ← Python 依赖
└── .gitignore               ← Git 忽略规则
```
