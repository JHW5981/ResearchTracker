# ResearchTracker

## Feature
- 适配[papers.cool](https://papers.cool)论文前端界面的【爬取-解析-筛选】流程
- 全栈代码【后端+前端】
- 开箱即用

## Usage
- ``git clone https://github.com/JHW5981/ResearchTracker.git``
- 在项目跟目录下创建.env文件，里面存放OPENAI_API_KEY=sk-ZqN9I********8f。
- 开两个终端，一个终端 `cd` 到 `ResearchTracker` 路径下，一个终端 `cd` 到 `ResearchTracker/frontend`下。
- 前者运行 `uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000` 运行后端代码。
- 后者运行 `npm run dev` 运行前端代码，这个时候前端会有一个localhost的链接，打开就可以用了。
- 如果想将本地服务映射到公网的话，先运行 `ngrok http 8000`，再将 `frontend/src/views/Home.vue` 第100行的代码改成ngrok的地址，再到 `frontend` 路径下运行 `npm run build`，生成 `dist` 文件，再运行 `npm run dev`。

## Q&A

1. Api key是openai官方的吗？

    不是，是第三方api，需要换一下域名，在 `ResearchTracker/backend/services/llm_service.py` 第12行代码，如果用官方api的话删了这行就行。

2. 修改前端代码之后，本地前端服务界面变化了，ngrok映射的地址么变？

    ngrok依赖的是前端编译后的静态文件，每次修改前端后，需要重新运行`npm run build`。

## Demo

Demo视频在 `assets/demo.mp4`，有问题的可以去瞅瞅。

# Future Work
- 支持更多论文网站（如 arXiv, IEEE Xplore）
- 增加入库功能
- 优化查询时间