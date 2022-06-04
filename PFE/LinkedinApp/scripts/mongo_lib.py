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


    def create_collection(self,name):
        dbname=self.dbname
        collection_name = dbname[name]
        return collection_name
    def get_collection(self,name):
        dbname=self.dbname
        collection_name = dbname[name]
        return collection_name
    def insert(self,collection,data=dict):
        collection_name=collection
        collection_name.insert(data)
        return True
    def insert_many(self,collection,data=list):
        collection_name=collection
        collection_name.insert_many(data)
        return True




