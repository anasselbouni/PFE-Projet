from duckduckgo_search import ddg

# Class pour recherche des id profiles sur duckduckgo go
class ddg_manager:
    def __init__(self,url,region):
        self.region=region
        self.base_url=url

    def find_between_r(self,s, first, last):
        try:
            start = s.rindex(first) + len(first)
            end = s.rindex(last, start)
            return s[start:end]
        except ValueError:
            return ""

    #### Recherche des liens linkedin
    def search(self,keyword,industr,mr=int):
        url=self.base_url
        keywords=''
        if industr == '' and keyword != '':
            keywords = '{} {}'.format(keyword,url)
        if industr != '' and keyword == '':
            keywords = '{} {}'.format(industr,url)
        if industr != '' and keyword != '':
            keywords = '{} {} {}'.format(industr, keyword,url)

        keywo = 'Bella Ciao'
        test = ddg(keywo, region='wt-wt', safesearch='Moderate', time='y', max_results=28)

        results = ddg(keywords, region=self.region, max_results=mr)
        return results


    ### Extraction de vanityname de lien
    def parse(self,url,results):
        r_=[]
        d_m = ddg_manager('site:linkedin.com allinurl:["/in/"]', 'ma-ma')
        for td in results:
            
            href = d_m.find_between_r(td['href'], url, "")
            print(href)

            if td['href'] != '':
                r_.append(td['href'])
            else:pass
        return r_



