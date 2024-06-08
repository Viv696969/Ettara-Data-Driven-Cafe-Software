import chromadb
client=chromadb.PersistentClient("./store_db")
collection=client.get_or_create_collection("store_collection",  metadata={"hnsw:space": "cosine"}) 

from models import Product,Category
products=Product.objects.all()
print(products)