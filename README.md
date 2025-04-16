# ResearchTracker

## Feature
- 适配[papers.cool](https://papers.cool)论文前端界面的【爬取-解析-筛选】流程
- 全栈代码【后端+前端】
- 开箱即用

## Usage
1. 克隆项目
```bash
git clone https://github.com/JHW5981/ResearchTracker.git
```

2. 配置环境变量
- 复制 `.env.example` 文件并重命名为 `.env`
- 在 `.env` 文件中填入你的 OpenAI API Key
```bash
cp .env.example .env
# 编辑 .env 文件，填入你的 API Key
```

3. 运行项目
- 开两个终端：
  - 终端1（后端）：
    ```bash
    cd ResearchTracker
    uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
    ```
  - 终端2（前端）：
    ```bash
    cd ResearchTracker/frontend
    npm run dev
    ```
- 打开浏览器访问前端提供的 localhost 链接即可使用

4. （可选）公网映射
- 运行 `ngrok http 8000`
- 将 `frontend/src/views/Home.vue` 第100行的代码改成 ngrok 地址
- 到 `frontend` 路径下运行：
  ```bash
  npm run build
  npm run dev
  ```

## Q&A

1. Api key是openai官方的吗？

    不是，是第三方api，需要换一下域名，在 `ResearchTracker/backend/services/llm_service.py` 第12行代码，如果用官方api的话删了这行就行。

2. 修改前端代码之后，本地前端服务界面变化了，ngrok映射的地址么变？

    ngrok依赖的是前端编译后的静态文件，每次修改前端后，需要重新运行`npm run build`。

## 安全说明

- `.env` 文件包含敏感信息（API密钥），已被添加到 `.gitignore`
- 请勿将 `.env` 文件提交到版本控制系统
- 请参考 `.env.example` 文件进行本地环境配置

## Demo

Demo视频在 `assets/demo.mp4`，有问题的可以去瞅瞅。

# Future Work

- 增加入库功能
- 优化查询时间