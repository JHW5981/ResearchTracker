import arxiv
import yaml
import logging
import argparse

logging.basicConfig(format='[%(asctime)s %(levelname)s] %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S',
                    level=logging.INFO)

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
        EXCAPE = '\"'
        OR = 'OR' 
        def parse_filters(filters:list):
            ret = ''
            for idx in range(0,len(filters)):
                filter = filters[idx]
                ret += (EXCAPE + filter + EXCAPE)  
                if idx != len(filters) - 1:
                    ret += OR
            return ret
        for k,v in config['keywords'].items():
            keywords[k] = parse_filters(v['filters'])
        return keywords
    with open(config_file,'r') as f:
        config = yaml.load(f,Loader=yaml.FullLoader) 
        config['kv'] = pretty_filters(**config)
        logging.info(f'config = {config}')
    return config 



def get_daily_papers(topic,query="ocr", max_results=20):
    """
    from `Vincentqyw/cv-arxiv-daily`, used for get daily papers
    @param topic: str
    @param query: str
    @return paper_with_code: dict
    """
    # output 
    content = dict() 

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
        primary_category    = result.primary_category
        publish_time        = result.published.date()
        update_time         = result.updated.date()


        logging.info(f"Time = {update_time} title = {paper_title}")

        # eg: 2108.09112v1 -> 2108.09112
        ver_pos = paper_id.find('v')
        if ver_pos == -1:
            paper_key = paper_id
        else:
            paper_key = paper_id[0:ver_pos]    
        paper_url = arxiv_url + 'abs/' + paper_key
        
        try:
            content[paper_key] = "|**{}**|**{}**|{}|[{}]({})|\n".format(
                    update_time,paper_title,paper_abstract,paper_key,paper_url)
        except Exception as e:
            logging.error(f"exception: {e} with id: {paper_key}")

    data = {topic:content}
    return data 

def tracker(**config):
    # collector
    data_collector = []
    # configs
    user_name = config["user_name"]
    repo_name = config["repo_name"]
    max_results = config["max_results"]
    md_readme_path = config["md_readme_path"]
    keywords = config["kv"]
    
    logging.info(f"GET daily papers begin")
    for k, v in keywords.items():
        data = get_daily_papers(topic=k, query=v, max_results=max_results)
        data_collector.append(data)
    logging.info(f"GET daily papers end")

    # write data into README.md
    logging.info(f"Write data into README.md begin")
    with open(md_readme_path,"w") as f:
        # badge
        f.write("![Static Badge](https://img.shields.io/badge/build-passing-brightgreen?style=plastic) ")
        f.write("![Static Badge](https://img.shields.io/badge/ref-url-blue?style=plastic&logo=github&color=blue&link=https%3A%2F%2Fgithub.com%2FVincentqyw%2Fcv-arxiv-daily)\n")

        # contents
        for item in data_collector:
            for key, value in item.items():
                f.write(f"## {key}\n")
                f.write("| Update Date | Title | Abstract | Link |\n")
                f.write("|-------------|-------|----------|------|\n")
                for _, v in value.items():
                    f.write(f"{v}")
                f.write("\n")
    logging.info(f"Write data into README.md end")


def main():
    args = get_arguments()
    config = load_config(args.config_path)
    tracker(**config)


if __name__ == "__main__":
    main()
