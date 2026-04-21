import json
import urllib.request
import re
import os
from dotenv import load_dotenv

# ==================== 工具定义 ====================
def query_relation(relation):
    """根据关系查询人员信息"""
    relation_db = {
        "弟": "小林，16岁",
        "姐": "小陈，30岁",
        "哥": "小毅，26岁",
        "妹": "小美，14岁",
        "爸": "老张，50岁",
        "妈": "李华，48岁"
    }
    return relation_db.get(relation, f"没有找到'{relation}'的信息")


# 可用工具列表（给模型参考）
tools_description = """
你可以使用以下工具：
- query_relation[关系]：查询某个关系的人的信息，例如 query_relation[弟]

使用格式：
如果需要使用工具，请输出：
Action: query_relation[关系]

如果已经有足够信息回答用户，请输出：
Final: 你的回答
"""

# ==================== 千问 API ====================
load_dotenv()
API_KEY = os.getenv("DASHSCOPE_API_KEY")


def chat(messages):
    data = {
        "model": "qwen-turbo",
        "messages": messages
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    req = urllib.request.Request(
        "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
        data=json.dumps(data).encode("utf-8"),
        headers=headers,
        method="POST"
    )
    with urllib.request.urlopen(req) as f:
        res = json.load(f)
    return res["choices"][0]["message"]["content"]


# ==================== ReAct 循环 ====================
def react_loop(user_question, max_steps=5):
    messages = [
        {"role": "system", "content": f"""你是一个关系信息查询助手，可以使用工具查询关系对应的信息。

{tools_description}

规则：
1. 每次只能输出一个 Action 或 Final
2. 不要在一次回复中同时输出 Action 和 Final
3. 查询到信息后，用 Final 回答用户
4. 如果用户问的关系不在数据库里，如实告知

现在开始！"""},
        {"role": "user", "content": user_question}
    ]

    step = 0
    while step < max_steps:
        step += 1
        print(f"\n--- Step {step} ---")

        # 调用模型
        response = chat(messages)
        print(f"模型输出: {response}")

        # 解析 Action
        action_match = re.search(r"Action:\s*(\w+)\[(.*?)\]", response)
        if action_match:
            action_name = action_match.group(1)
            action_param = action_match.group(2)

            # 执行工具
            if action_name == "query_relation":
                observation = query_relation(action_param)
                print(f"工具返回: {observation}")

                # 将模型的 Action 和工具结果加入对话
                messages.append({"role": "assistant", "content": response})
                messages.append({"role": "user", "content": f"Observation: {observation}"})
                continue  # 继续循环，让模型根据 Observation 回答

        # 解析 Final
        final_match = re.search(r"Final:\s*(.+)", response, re.DOTALL)
        if final_match:
            answer = final_match.group(1).strip()
            print(f"\n最终答案: {answer}")
            return answer

        # 如果既不是 Action 也不是 Final，让模型重新输出
        messages.append({"role": "assistant", "content": response})
        messages.append({"role": "user", "content": "请按正确格式输出：要么 Action: 工具名[参数]，要么 Final: 你的答案"})

    print("超过最大步数，未得到答案")
    return None


# ==================== 运行 ====================
if __name__ == "__main__":
    while True:
        question = input("\n你要查询的关系（输入 q 退出）：")
        if question.lower() == 'q':
            break
        react_loop(question)