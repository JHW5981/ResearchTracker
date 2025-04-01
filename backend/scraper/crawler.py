# import aiohttp
# from typing import List, Dict
# from bs4 import BeautifulSoup
# import logging

# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)

# class PaperCrawler:
#     def __init__(self):
#         self.headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Firefox/89.0',
#             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#             'Accept-Language': 'en-US,en;q=0.5',
#         }
    
#     async def fetch_page(self, url: str) -> str:
#         logger.debug(f"开始获取页面: {url}")
#         async with aiohttp.ClientSession(headers=self.headers) as session:
#             async with session.get(url) as response:
#                 html = await response.text()
#                 logger.debug(f"页面获取成功，长度: {len(html)}")
#                 return html
    
#     async def parse_papers(self, html: str) -> List[Dict]:
#         logger.debug("开始解析论文")
#         papers = []
#         soup = BeautifulSoup(html, 'html.parser')
        
#         # 根据实际网页结构调整选择器
#         paper_elements = soup.find_all('div', class_='panel paper')  # 需要根据实际网页调整
        
#         for element in paper_elements:
#             try:
#                 paper = {
#                     "title": element.find('h2').text.strip().split('\n')[1] if element.find('h2') else "",
#                     "abstract": element.find('p', class_='summary notranslate').text.strip() if element.find('p', class_='summary notranslate') else "",
#                 }
#                 papers.append(paper)
#             except Exception as e:
#                 logger.error(f"解析论文时出错: {str(e)}")
#                 continue
        
#         logger.debug(f"解析完成，找到 {len(papers)} 篇论文")
#         return papers

#     async def fetch_with_pagination(self, base_url: str, max_pages: int = 5) -> List[Dict]:
#         """获取多页内容"""
#         all_papers = []
        
#         for page in range(1, max_pages + 1):
#             try:
#                 # 构造分页URL（需要根据实际网站调整）
#                 page_url = f"{base_url}?page={page}"
#                 html = await self.fetch_page(page_url)
#                 papers = await self.parse_papers(html)
                
#                 if not papers:
#                     break
                    
#                 all_papers.extend(papers)
#                 logger.info(f"已获取第 {page} 页，当前共 {len(all_papers)} 篇论文")
                
#             except Exception as e:
#                 logger.error(f"获取第 {page} 页时出错: {str(e)}")
#                 break
        
#         return all_papers




import aiohttp
from typing import List, Dict
from bs4 import BeautifulSoup
import logging
import asyncio
import re

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class PaperCrawler:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Firefox/89.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }
    
    async def fetch_page(self, url: str) -> str:
        logger.debug(f"开始获取页面: {url}")
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(url) as response:
                html = await response.text()
                logger.debug(f"页面获取成功，长度: {len(html)}")
                return html
    
    async def parse_papers(self, html: str) -> List[Dict]:
        logger.debug("开始解析论文")
        papers = []
        soup = BeautifulSoup(html, 'html.parser')
        
        # 针对 arXiv 的解析逻辑
        paper_elements = soup.find_all('div', class_='panel paper')
        
        for element in paper_elements:
            try:
                # 获取标题
                title_element = element.find('h2', class_='title')
                title = title_element.text.strip().split('\n')[1] if title_element else ""
                
                # 获取摘要
                abstract_element = element.find('p', class_='summary notranslate')
                abstract = abstract_element.text.strip() if abstract_element else ""
                
                paper = {
                    "title": title,
                    "abstract": abstract,
                }
                papers.append(paper)
                
            except Exception as e:
                logger.error(f"解析论文时出错: {str(e)}")
                continue
        
        logger.debug(f"解析完成，找到 {len(papers)} 篇论文")
        return papers

    async def fetch_all_papers(self, base_url: str, start: int = 0, max_papers: int = 100) -> List[Dict]:
        """
        获取多页论文
        base_url: 基础URL
        start: 起始索引
        max_papers: 最大论文数量
        """
        all_papers = []
        current_start = start
        
        # 处理基础URL，确保正确的参数拼接
        if '?' in base_url:
            # 如果URL已经包含参数，使用&连接新参数
            url_template = base_url + '&skip={}&show=25'
        else:
            # 如果URL没有参数，使用?开始参数列表
            url_template = base_url + '?skip={}&show=25'
            
        while len(all_papers) < max_papers:
            try:
                # 构造正确的URL
                page_url = url_template.format(current_start)
                logger.info(f"获取页面: {page_url}")
                
                html = await self.fetch_page(page_url)
                papers = await self.parse_papers(html)
                
                if not papers:
                    logger.info("没有更多论文了")
                    break
                
                all_papers.extend(papers)
                logger.info(f"当前已获取 {len(all_papers)} 篇论文")
                
                # 更新起始索引
                current_start += 25
                
                # 添加延迟，避免请求过快
                await asyncio.sleep(1)
                
            except Exception as e:
                logger.error(f"获取论文时出错: {str(e)}")
                break
        
        return all_papers[:max_papers]