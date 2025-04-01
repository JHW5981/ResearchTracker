import asyncio
import sys
import os
import logging
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = str(Path(__file__).parent.parent.parent)
sys.path.append(project_root)

from backend.services.llm_service import LLMService
from backend.scraper.crawler import PaperCrawler

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

async def test_fetch():
    crawler = PaperCrawler()
    url = "https://papers.cool/venue/NeurIPS.2024?group=Oral"
    
    try:
        logger.info(f"开始测试爬取: {url}")
        
        # 获取多页论文
        papers = await crawler.fetch_all_papers(
            base_url=url,
            start=0,
            max_papers=100  # 设置想要获取的论文数量
        )
        
        logger.info(f"总共获取到 {len(papers)} 篇论文")
        
        # 打印前几篇论文的信息
        for i, paper in enumerate(papers[:5], 1):
            print(f"\n论文 {i}:")
            print(f"标题: {paper['title']}")
            print(f"摘要: {paper['abstract'][:200]}...")
            print("-" * 80)
            
    except Exception as e:
        logger.error(f"测试过程中出错: {str(e)}")
        raise

async def test_llm_filter():
    crawler = PaperCrawler()
    llm_service = LLMService()
    
    try:
        # 获取论文
        url = "https://papers.cool/venue/NeurIPS.2024?group=Oral"
        papers = await crawler.fetch_all_papers(url, max_papers=5)  # 先测试少量论文
        logger.info(f"获取到 {len(papers)} 篇论文")
        
        # 测试 LLM 筛选和分析
        criteria = "与强化学习相关的论文"
        filtered_papers = await llm_service.filter_papers(papers, criteria)
        logger.info(f"筛选后剩余 {len(filtered_papers)} 篇论文")
        
        # 打印筛选和分析结果
        for i, paper in enumerate(filtered_papers, 1):
            print(f"\n论文 {i}:")
            print(f"标题: {paper['title']}")
            print(f"\n英文摘要:\n{paper['abstract_en']}")
            print(f"\n中文摘要:\n{paper['abstract_zh']}")
            print("\n解决的问题:")
            for problem in paper['problems_solved']:
                print(f"- {problem}")
            print("\n创新点:")
            for innovation in paper['innovations']:
                print(f"- {innovation}")
            print("-" * 80)
            
    except Exception as e:
        logger.error(f"测试过程中出错: {str(e)}")
        raise

if __name__ == "__main__":
    # asyncio.run(test_fetch())
    asyncio.run(test_llm_filter())