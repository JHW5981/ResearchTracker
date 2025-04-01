from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict
import logging
from .scraper.crawler import PaperCrawler
from .services.llm_service import LLMService

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建 FastAPI 应用
app = FastAPI(
    title="Research Paper Tracker",
    description="一个用于爬取、分析和筛选研究论文的API",
    version="1.0.0"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化服务
crawler = PaperCrawler()
llm_service = LLMService()

# 请求模型
class PaperRequest(BaseModel):
    url: str
    criteria: Optional[str] = None
    max_papers: Optional[int] = 50

# 响应模型
class Paper(BaseModel):
    title: str
    abstract_en: str
    abstract_zh: Optional[str] = None
    url: str
    problems_solved: Optional[List[str]] = None
    innovations: Optional[List[str]] = None

class PaperResponse(BaseModel):
    papers: List[Paper]
    total: int
    filtered: int

@app.post("/api/papers", response_model=PaperResponse)
async def get_papers(request: PaperRequest):
    try:
        # 1. 爬取论文
        logger.info(f"开始爬取论文: {request.url}")
        papers = await crawler.fetch_all_papers(
            request.url,
            max_papers=request.max_papers
        )
        total_papers = len(papers)
        logger.info(f"爬取完成，共获取 {total_papers} 篇论文")

        # 2. 如果提供了筛选标准，使用LLM进行筛选和分析
        if request.criteria:
            logger.info(f"开始使用标准进行筛选: {request.criteria}")
            filtered_papers = await llm_service.filter_papers(papers, request.criteria)
            logger.info(f"筛选完成，符合标准的论文数量: {len(filtered_papers)}")
        else:
            filtered_papers = papers
            logger.info("未提供筛选标准，保留所有论文")

        # 确保返回的数据符合模型定义
        response_data = {
            "papers": [
                {
                    "title": paper.get("title", ""),
                    "abstract_en": paper.get("abstract_en", ""),
                    "abstract_zh": paper.get("abstract_zh", ""),
                    "url": paper.get("url", ""),
                    "problems_solved": paper.get("problems_solved", []),
                    "innovations": paper.get("innovations", [])
                }
                for paper in filtered_papers
            ],
            "total": total_papers,
            "filtered": len(filtered_papers)
        }

        return JSONResponse(content=response_data)

    except Exception as e:
        logger.error(f"处理请求时出错: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "detail": "处理请求时发生错误"}
        )
    
@app.get("/api/health")
async def health_check():
    """健康检查接口"""
    return {"status": "healthy"}

# 调试接口
@app.post("/api/debug/fetch")
async def debug_fetch(url: str, max_papers: int = Query(default=10, le=50)):
    """
    调试用：仅爬取论文
    """
    try:
        papers = await crawler.fetch_all_papers(url, max_papers=max_papers)
        return {"total": len(papers), "papers": papers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/debug/filter")
async def debug_filter(papers: List[Dict], criteria: str):
    """
    调试用：仅进行LLM筛选
    """
    try:
        filtered_papers = await llm_service.filter_papers(papers, criteria)
        return {"total": len(filtered_papers), "papers": filtered_papers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
