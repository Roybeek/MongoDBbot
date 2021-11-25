

def insert_document(collection, data):
    """ Функция для вставки документа в коллекцию
    возращает id документа.
    """
    return collection.insert_one(data).inserted_id


def find_document(collection, elements, multiple=False):
    """ Функция для поиска документа в зависимости от параметра multiple вернет список или один елемент
    """
    if multiple:
        results = collection.find(elements)
        return [r for r in results]
    else:
        return collection.find_one(elements)


def update_document(collection, query_elements, new_values):
    """ Обновить документ в коллекции
    """
    collection.update_one(query_elements, {'$set': new_values})


def delete_document(collection, query):
    """ Удалить документ в коллекции
    """
    collection.delete_one(query)