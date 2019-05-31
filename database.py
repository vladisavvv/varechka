import pymongo


class DataBase:
    def __init__(self):
        self.client = pymongo.MongoClient('localhost:123')
        self.database = self.client['pixelation']
        self.history = self.database['history']

    def add_image(self, name_file, colors, size_block):
        self.history.save({'name_file': name_file, 'colors': colors, 'size_block': size_block})

    def delete_image(self, name_file):
        self.history.remove({'name_file': name_file})

    def get_all_history(self):
        answer = []
        for description_image in self.history.find():
            del description_image['_id']
            answer.append(description_image)
        return answer

    def clean_history(self):
        self.history.remove({})
