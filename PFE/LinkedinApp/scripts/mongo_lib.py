import pymongo

import pprint

class mongo_manager:
    def __init__(self,db_name):
        self.connect= self.get_client('localhost',27017)
        self.dbname = self.connect[db_name]

    def get_client(self,host, port):
        client = pymongo.MongoClient(host=host,
                                     port=int(port),
                                     )
        return client

    def kwargs_to_doc(self,**kwargs):
        data={}
        for key,value in kwargs:
            data[key]=value
        return data


    def create_collection(self,name):
        dbname=self.dbname
        collection_name = dbname[name]
        return collection_name

    def get_collection(self,name):
        dbname=self.dbname
        collection_name = dbname[name]
        cursor = collection_name.find()
        r=[]
        for _ in cursor:
            r.append(_)
            print(_)

        return r

    def insert(self,collection,data):
        collection_name=collection
        collection_name.insert(data)
        return True

    def insert_many(self,collection,data):
        collection_name=collection
        collection_name.insert_many(data)
        return True


    def df_to_doc(self,collection,dataframe):
        l_d=dataframe.to_dict('records')
        self.insert_many(collection,l_d)
        return True



