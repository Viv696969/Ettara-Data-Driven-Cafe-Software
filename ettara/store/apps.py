from django.apps import AppConfig
import chromadb

class StoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store'
    # client=chromadb.PersistentClient("./store_db")
    # collection=client.get_collection("store_collection")
    collection=None


