from duckduckgo import ddg_manager
from linkd_api import linkedin_manager
from mongo_lib import mongo_manager
from time import sleep
import multiprocessing
import sys







if __name__  == '__main__':
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    if len(sys.argv) == 2:
        print(len(sys.argv),'arguments')
        ind=sys.argv[1]

    elif len(sys.argv)>=3:
        print(len(sys.argv),'arguments')
        ind=sys.argv[2]
    else:
        ind='graphic design'

    mdb_m=mongo_manager('mongo')
    accounts_c=mdb_m.get_collection('LinkedinApp_linkedin_account')
    print(accounts_c)
    d_m=ddg_manager('site:linkedin.com allinurl:["/in/"]','ma-ma')
    results=d_m.search('',ind,200)
    print('linkdin')
    v_n=d_m.parse('https://www.linkedin.com/in/',results)
    l_m=linkedin_manager(accounts_c,ind,v_n)
    dfs=l_m.profile_compilation(return_dict)

    #save results in db





