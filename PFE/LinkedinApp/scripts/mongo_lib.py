import pymongo


class mongo_manager:
    def __init__(self,db_name):
        self.connect= self.get_client('localhost',27017,'username','password')
        self.dbname = self.connect[db_name]

    def get_client(self,host, port, username, password):
        client = pymongo.MongoClient(host=host,
                                     port=int(port),
                                     username=username,
                                     password=password
                                     )
        return client

    def kwargs_to_doc(self,**kwargs):
        data={}
        for key,value in kwargs:
            data[key]=value
        return data
    def df_to_doc(self,collection,dataframe):
        l_d=dataframe.to_dict('records')
        self.insert_many(collection,l_d)
        return True

    def create_collection(self,name):
        dbname=self.dbname
        collection_name = dbname[name]
        return collection_name
    def get_collection(self,name):
        dbname=self.dbname
        collection_name = dbname[name]
        return collection_name
    def insert(self,collection,data):
        collection_name=collection
        collection_name.insert(data)
        return True

    def insert_many(self,collection,data):
        collection_name=collection
        collection_name.insert_many(data)
        return True



