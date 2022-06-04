from duckduckgo_search import ddg
from .general import find_between_r

class ddg_manager:
    def __init__(self,url,region):
        self.region=region
        self.base_url=url


    def search(self,keyword,industr,mr=int):
        url=self.base_url
        keywords=''
        if industr == '' and keyword != '':
            keywords = '{} {}'.format(keyword,url)
        if industr != '' and keyword == '':
            keywords = '{} {}'.format(industr,url)
        if industr != '' and keyword != '':
            keywords = '{} {} {}'.format(industr, keyword,url)
        results = ddg(keywords, region=self.region, max_results=mr)

        return results

    def parse(self,url,results):
        r_=[]
        for td in results:
            href = find_between_r(td['href'], url, "")
            if href != '':
                r_.append(href)
            else:pass
        print(r_)
        return r_


