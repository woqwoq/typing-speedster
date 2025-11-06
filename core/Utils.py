def remove_if_greater(set: set, j: int):       
        to_remove = []

        for item in set:
            to_remove.append(item) if(item > j) else None

        [set.remove(removed_item) for removed_item in to_remove]

        return set

