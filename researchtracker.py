import arxiv
import yaml
import logging
import argparse
from chat import Chat

logging.basicConfig(format='[%(asctime)s %(levelname)s] %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S',
                    # level=logging.INFO)
                    level=logging.CRITICAL)         

arxiv_url = "http://arxiv.org/"

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config_path", type=str, default="./config.yaml", help="path to config file")
    args = parser.parse_args()
    return args

def load_config(config_file:str) -> dict:
    '''
    from Vincentqyw/cv-arxiv-daily, used for parse config.yaml
    config_file: input config file path
    return: a dict of configuration
    '''
    # make filters pretty
    def pretty_filters(**config) -> dict:
        keywords = dict()
        OR = 'OR' 
        def parse_filters(filters:list):
            ret = ''
            for idx in range(0,len(filters)):
                filter = filters[idx]
                ret += ("\""  + filter + "\"" + " ") 
                if idx != len(filters) - 1:
                    ret += (OR + " ")
            return ret
        for k,v in config['keywords'].items():
            keywords[k] = parse_filters(v['filters'])
        return keywords
    with open(config_file,'r') as f:
        config = yaml.load(f,Loader=yaml.FullLoader) 
        config['kv'] = pretty_filters(**config)
        logging.info(f'config = {config}')
    return config 

def analyzer(abs:str) -> str:
    chat = Chat("你是一个帮助我Summarize文章摘要的助手")
    conversation_list = chat.ask(f"请帮我简化一下文章的摘要，告诉我他们做了什么事情就行，摘要如下：{abs}")
    response = conversation_list[-1]['content']
    return response.replace('\n', '<br>')


def get_daily_papers(topic,query="ocr", max_results=20, gpt=False):
    """
    from `Vincentqyw/cv-arxiv-daily`, used for get daily papers
    @param topic: str
    @param query: str
    @return paper_with_code: dict
    """
    # output 
    content = dict() 
    num = 1

    # Construct the default API client.
    client = arxiv.Client()
    search_engine = arxiv.Search(
        query = query,
        max_results = max_results,
        sort_by = arxiv.SortCriterion.SubmittedDate
    )

    for result in client.results(search_engine):

        paper_id            = result.get_short_id()
        paper_title         = result.title
        paper_url           = result.entry_id
        paper_abstract      = result.summary.replace("\n"," ")
        update_time         = result.updated.date()


        logging.info(f"Time = {update_time} title = {paper_title}")

        if gpt:
            response = analyzer(paper_abstract)
        else:
            response = "Not GPT"

        # eg: 2108.09112v1 -> 2108.09112
        ver_pos = paper_id.find('v')
        if ver_pos == -1:
            paper_key = paper_id
        else:
            paper_key = paper_id[0:ver_pos]    
        paper_url = arxiv_url + 'abs/' + paper_key
        
        try:
            content[paper_key] = "|**{}**|**{}**|**{}**|**{}**|**[{}]({})**|\n".format(
                    num, update_time,paper_title,response,paper_id,paper_url)
            num = num + 1
        except Exception as e:
            logging.error(f"exception: {e} with id: {paper_key}")

    data = {topic:content}
    return data 

def tracker(**config):
    # collector
    data_collector = []
    # configs
    max_results = config["max_results"]
    md_readme_path = config["md_readme_path"]
    keywords = config["kv"]
    
    logging.info(f"GET daily papers begin")
    for k, v in keywords.items():
        data = get_daily_papers(topic=k, query=v, max_results=max_results, gpt=config["gpt"])
        data_collector.append(data)
    logging.info(f"GET daily papers end")

    # write data into README.md
    logging.info(f"Write data into README.md begin")
    with open(md_readme_path,"w") as f:
        # badge
        f.write("<a><img src='https://img.shields.io/badge/build-passing-brightgreen?style=plastic'></a>")
        f.write("<a href='https://github.com/Vincentqyw/cv-arxiv-daily'><img src='https://img.shields.io/badge/ref-url-blue?style=plastic&logo=github'></a>\n")

        # contents
        for item in data_collector:
            f.write("<details>\n")
            for key, value in item.items():
                f.write(f"  <summary><b>{key}</b></summary>\n\n")
                f.write("| Num | Update Date | Title | GPT | Paper ID |\n")
                f.write("|-----|-------------|-------|-----|----------|\n")
                for _, v in value.items():
                    f.write(f"{v}")
                f.write("\n")
            f.write("</details>\n")
    logging.info(f"Write data into README.md end")


def main():
    args = get_arguments()
    config = load_config(args.config_path)
    tracker(**config)


if __name__ == "__main__":
    main()
