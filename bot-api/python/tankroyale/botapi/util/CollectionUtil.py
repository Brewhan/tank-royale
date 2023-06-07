
class CollectionUtil:
    # Create a mutable list that is a copy of another list
    @staticmethod
    def toMutableList(collection):
        return list(collection)
    
    # create a mutable set that copies all items from a collection but removes duplicates
    @staticmethod
    def toMutableSet(collection):
        return set(collection)
    