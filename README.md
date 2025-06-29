# 智能多轮对话 Agent 项目报告

## 1. Agent 功能说明

### 1.1 背景说明
本项目基于 LangChain 框架，旨在构建一个能够与用户进行多轮自然语言交互的智能 Agent。通过整合知识库、本地函数和外部 API，Agent 可帮助用户完成任务查询、文档问答和工具调用。

### 1.2 功能列表
- 支持基于上下文的多轮对话
- 可从知识库中检索并回答文档相关问题
- 可调用搜索引擎获取实时信息（如天气）
- 可执行本地 Python 脚本完成数值计算

---

## 2. 系统实现细节

### 2.1 技术栈
- Python 3
- LangChain
- OpenAI GPT 模型（ChatOpenAI）
- FAISS（向量数据库）
- SerpAPI（外部搜索接口）

### 2.2 Agent 使用的 Tools

| 工具名称 | 类型 | 说明 |
|----------|------|------|
| DocumentQA | 知识库工具 | 基于本地 guide.txt 文档，实现文档问答 |
| Search | API 工具 | 使用 SerpAPI 查询实时信息（如天气、百科） |
| PythonREPLTool | 本地函数工具 | 可执行 Python 表达式，如数学计算 |

---

## 3. 运行与测试方法说明

### 3.1 环境配置
- Python >= 3.8
- 安装依赖：
```bash
pip install langchain openai faiss-cpu serpapi
```
- 添加文件 ./docs/guide.txt（用于知识库）
- 设置环境变量：
```python
os.environ["OPENAI_API_KEY"] = "your-openai-key"
os.environ["SERPAPI_API_KEY"] = "your-serpapi-key"
```

### 3.2 启动方式
```bash
python langchain_agent.py
```
输入文字与 Agent 对话，输入“退出”可结束程序。

---

## 4. 聊天记录示例

### 示例 1：天气查询
```
你：请问今天广州的天气怎么样？
Agent：广州今天的天气为多云，最高气温 31℃。
```

### 示例 2：知识库问答
```
你：实验的合作要求是什么？
Agent：实验要求每组必须由 2 名学生组成，不得单人完成。
```

### 示例 3：本地工具计算
```
你：请帮我算一下 9 的平方根
Agent：结果为 3.0
```

---

## 5. 合作与反思

### 5.1 分工说明
- 成员 A（GitHub: @userA）：完成 LangChain Agent 主体构建、知识库接入与文档处理模块；编写 README 第 1、2 部分。
- 成员 B（GitHub: @userB）：实现 API 查询模块与本地函数工具，完成测试用例与示例记录；编写 README 第 3、4、5 部分。

### 5.2 学习收获
- 掌握了 LangChain 核心模块 Memory、Tool、Agent 初始化流程
- 熟悉了多工具调用方式，能设计结构化对话系统
- 理解了如何接入外部 API 与构建向量知识库

### 5.3 遇到问题与解决方法
- 问题：知识库检索不准确  
  解决：改用较小 chunk_size，提高召回质量
- 问题：SerpAPI 有时查询失败  
  解决：加入异常处理并重试机制

---

感谢阅读本项目报告。
