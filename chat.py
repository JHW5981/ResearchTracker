import warnings
import requests
import os

# retrieve the API key from the environment variables
api_key = os.environ.get('OPENAI_API_KEY')

# Chat with GPT in conversations
class Chat:
    def __init__(self, system_prompt) -> None:
        self.conversation_list = [{'role':'system', 'content': system_prompt}]
    
    def ask(self, prompt):
        self.conversation_list.append({'role':'user', 'content':prompt})
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            response = requests.post(
                url='https://openai.acemap.cn/v1/chat/completions',
                headers={'Authorization': f'{api_key}'},
                json={
                    'model': 'gpt-3.5-turbo',
                    'messages': self.conversation_list
                },
                verify=False
            )
        answer = response.json()['choices'][0]['message']['content']
        self.conversation_list.append({'role':'assistant', 'content':answer})
        return self.conversation_list

def main():
    chat = Chat('你是一个帮助我分析文章摘要的助手，替我选出来我需要的文章')
    conversation_list = chat.ask("我需要一篇关于OCR（Optical Character Reconstruction）的文章，下面帮我判断一下我给你的这篇文章摘要是不是关于OCR的： Language models (LMs) have become pivotal in the realm of technological advancements. While their capabilities are vast and transformative, they often include societal biases encoded in the human-produced datasets used for their training. This research delves into the inherent biases present in masked language models (MLMs), with a specific focus on gender biases. This study evaluated six prominent models: BERT, RoBERTa, DistilBERT, BERT-multilingual, XLM-RoBERTa, and DistilBERT-multilingual. The methodology employed a novel dataset, bifurcated into two subsets: one containing prompts that encouraged models to generate subject pronouns in English, and the other requiring models to return the probabilities of verbs, adverbs, and adjectives linked to the prompts' gender pronouns. The analysis reveals stereotypical gender alignment of all models, with multilingual variants showing comparatively reduced biases. ")
    for conversation in conversation_list:
        print(f"{conversation['role']}: {conversation['content']}")

if __name__ == '__main__':
    main()