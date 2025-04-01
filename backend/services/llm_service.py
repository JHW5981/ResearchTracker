from openai import AsyncOpenAI
from typing import List, Dict
from ..config import settings
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.client = AsyncOpenAI(
            base_url="https://api2.aigcbest.top/v1",
            api_key=settings.OPENAI_API_KEY)  
          
    async def filter_papers(self, papers: List[Dict], criteria: str) -> List[Dict]:
        """
        使用LLM筛选论文，翻译摘要，并分析论文解决的问题
        papers: 论文列表
        criteria: 筛选标准
        """
        filtered_papers = []
        
        for paper in papers:
            prompt = f"""请分析以下论文并完成三个任务：

1. 判断论文是否符合筛选标准
筛选标准：{criteria}

2. 如果论文相关，请完成以下分析：
   a. 将摘要翻译成中文
   b. 分析该论文主要解决了哪些问题（用要点列出）
   c. 创新点是什么（用要点列出）

论文信息：
标题：{paper['title']}
摘要：{paper['abstract']}

请按以下格式回复：
相关性：[是/否]

如果相关，请提供：
中文摘要：
[翻译内容]

解决的问题：
- [问题1]
- [问题2]
...

创新点：
- [创新点1]
- [创新点2]
...

如果不相关，直接回复"不相关"

注意：
- 请保持翻译的专业性和准确性
- 保留原文中的专业术语
- 确保分析简洁明了
- 重点突出论文的实际贡献
"""
            
            try:
                response = await self.client.chat.completions.create(
                    model=settings.MODEL_NAME,
                    messages=[
                        {"role": "system", "content": "你是一个专业的论文分析专家，擅长准确理解和提炼论文的核心内容。"},
                        {"role": "user", "content": prompt}
                    ]
                )
                
                result = response.choices[0].message.content
                logger.debug(f"LLM响应：{result}")
                
                # 解析LLM响应
                if "相关性：是" in result:
                    # 提取各部分内容
                    sections = result.split('\n\n')
                    
                    # 解析中文摘要
                    abstract_zh = ""
                    problems = []
                    innovations = []
                    
                    for section in sections:
                        if section.startswith("中文摘要："):
                            abstract_zh = section.replace("中文摘要：", "").strip()
                        elif section.startswith("解决的问题："):
                            problems = [p.strip("- ").strip() for p in section.split("\n")[1:] if p.strip()]
                        elif section.startswith("创新点："):
                            innovations = [i.strip("- ").strip() for i in section.split("\n")[1:] if i.strip()]
                    
                    # 创建新的论文对象，包含所有信息
                    paper_with_analysis = paper.copy()
                    paper_with_analysis.update({
                        "abstract_zh": abstract_zh,
                        "abstract_en": paper['abstract'],
                        "problems_solved": problems,
                        "innovations": innovations
                    })
                    filtered_papers.append(paper_with_analysis)
                    logger.info(f"论文《{paper['title']}》符合标准并已完成分析")
                else:
                    logger.debug(f"论文《{paper['title']}》不符合标准")
                    
            except Exception as e:
                logger.error(f"处理论文时出错: {str(e)}")
                continue
                
        return filtered_papers