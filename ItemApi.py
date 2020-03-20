import time
class ItemApi:
    endpoint = "Item.json"

    def __init__(self, client):
        self.client = client

    def get_item(self, itemId):
        r = self.client.get(self.endpoint, payload={
            'load_relations': '["ItemAttributes","Images"]',
            'itemID': itemId,

        })
        item = r.json()
        if 'Item' in item:
            return item['Item']
        return None

    def get_all_items(self):
        limit = 100
        offset = 0
        r = self.client.get(self.endpoint, payload={
            'load_relations': '["ItemAttributes","Images"]',
            'limit': limit,
            'offset': offset
        })
        if r is None:
            return []
        itemsChunk = r.json()
        if 'Item' not in itemsChunk:
            return []
        attrib = itemsChunk["@attributes"]
        if int(attrib['count']) <= 100:
            return itemsChunk["Item"]
        count = int(attrib['count'])
        items = itemsChunk['Item']
        while offset <= count:
            offset += 100
            time.sleep(2)
            r = self.client.get(self.endpoint, payload={
                'load_relations': 'all',
                'limit': limit,
                'offset': offset
            })
            time.sleep(1)
            itemsChunk = r.json()
            if 'Item' in itemsChunk:
                items = items + itemsChunk['Item']
        return items
