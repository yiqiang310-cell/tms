# 手写 ReAct Agent

> 从零实现的 ReAct (Reasoning + Acting) Agent，不依赖 LangChain 等框架，只用原生 Python + 阿里云千问 API。

## 🎯 项目背景

在学习 Agent 开发时发现，大多数课程只教如何调用 LangChain API，而不解释 Agent 的底层原理。于是决定手写一个 ReAct 循环，真正理解：

- Agent 如何思考和决策
- 工具如何被调用和执行
- 模型输出如何被解析和处理

## 🧠 核心原理

ReAct 模式的核心循环：
用户提问 → 模型思考 → 调用工具 → 观察结果 → 继续思考/给出答案

### 环境要求

- Python 3.8+
- 阿里云百炼 API Key（千问模型）

### 安装

```bash
git clone https://github.com/yiqiang310-cell/tms.git
cd tms

配置 API Key
bash
# Linux/Mac
export DASHSCOPE_API_KEY="你的 API Key"

# Windows
set DASHSCOPE_API_KEY="你的 API Key"

运行
bash
python react_agent.py

使用示例
text
你要查询的关系（输入 q 退出）：弟

--- Step 1 ---
模型输出: Action: query_relation[弟]
工具返回: 小林，16岁

--- Step 2 ---
模型输出: Final: 弟弟是今年16岁的小林
最终答案: 弟弟是今年16岁的小林
📁 项目结构
text
tms/
├── react_agent.py   # 主程序：ReAct 循环实现
├── .env.example     # 环境变量示例（不包含真实 Key）
├── .gitignore       # Git 忽略文件配置
└── README.md        # 项目说明
