# Aegis-Agent 本地离线AI助手

### 开发工具说明（中文）
本项目使用Claude Code作为开发辅助工具，仅用于生成基础代码框架、优化语音算法流程、规范代码格式与辅助文档撰写；
项目整体架构设计、业务逻辑梳理、全模块调试、前后端联调与功能迭代均由本人独立完成。

## 项目简介
一款具备长期记忆、语音交互、离线本地大模型推理的轻量化AI客户端，采用Python后端+Flutter跨平台前端架构，完整实现本地大模型部署、对话记忆持久化、语音转文字/语音合成全链路。
> 个人独立开发，用于学习本地LLM工程化、多端交互、语音AI流水线。

## 核心功能
1. 离线本地大模型推理，无需联网调用API
2. 对话长期记忆存储，支持上下文检索历史会话
3. 实时语音交互：ASR语音输入 + TTS语音播报回复
4. 前后端分离架构：Python后端推理服务 + Flutter可视化客户端
5. 配套测试脚本、开发依赖、文档与示例数据

## 技术栈
- 后端：Python、FastAPI / Uvicorn、Ollama 本地模型推理、ChromaDB 、Vosk（ASR）、XTTS(TTS)
- 前端：Flutter、Dart、Desktop UI
- 语音模块：ASR语音识别、TTS语音合成
- 工程化能力：前后端分离架构设计RESTful、API通信、本地模型部署与调度、模块化语音流水线
- 环境管理：requirements.txt 标准化依赖

## 快速部署教程
### 1. 环境安装
```bash
# 克隆仓库
git clone https://github.com/llz616900-hash/Aegis-Agent.git
cd Aegis-Agent
# 安装依赖
pip install -r requirements.txt
