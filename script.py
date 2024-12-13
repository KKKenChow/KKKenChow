import requests
from googletrans import Translator
import re

# 获取历史上的今天数据
def fetch_today_in_history():
    url = "http://history.muffinlabs.com/date"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        events = data["data"]["Events"]
        # 倒序排列一下事件（看离现在最近的30条）
        events_reversed = events[::-1]
        
        today_history = [
            f"- {event['year']}: {event['text']}" for event in events_reversed[:30]
        ]
        return "\n".join(today_history)
    else:
        return "Failed to fetch data."

# 翻译英文内容为中文，并修复格式
def translate_to_chinese(text):
    translator = Translator()
    translation = translator.translate(text, src='en', dest='zh-CN')
    translated_text = translation.text
    
    # 强制每个历史事件后添加换行符，去除多余的空格和换行
    events = translated_text.split('\n')
    formatted_events = [event.strip() for event in events if event.strip()]
    
    # 使用统一格式“- ”开头，确保每一条事件的格式一致
    formatted_translated_text = "\n".join([f"- {event}" for event in formatted_events])
    
    # 清理掉多余的空格，确保数字前没有多余空格
    formatted_translated_text = re.sub(r"\s*-", "-", formatted_translated_text)
    
    # 清理翻译中的不必要缩进，确保每行的开始是统一的格式
    formatted_translated_text = re.sub(r"^\s*", "", formatted_translated_text, flags=re.MULTILINE)

    # 确保每条历史事件后面都有换行符
    formatted_translated_text = "\n".join([f"- {event}" for event in formatted_events])
    
    return formatted_translated_text

# 更新README.md文件，添加英文和中文内容
def update_readme(english_content, chinese_content):
    with open("README.md", "w", encoding="utf-8") as file:
        file.write(f"# History of Today \n\n{english_content}\n\n*Data from muffinlabs* \n\n")
        file.write(f"# 历史上的今天 \n\n{chinese_content}\n\n*由googletrans翻译*")

if __name__ == "__main__":
    # 获取并保存英文内容
    history_content = fetch_today_in_history()
    
    # 翻译成中文
    translated_content = translate_to_chinese(history_content)
    
    # 更新 README.md 文件
    update_readme(history_content, translated_content)
