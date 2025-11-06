def get_cats_info(path: str) -> list[dict]:
    """
    Reads a file with cat information and returns a list of dictionaries.

    Args:
        path (str): Path to the text file containing cat data in "id,name,age" format.

    Returns:
        list[dict]: A list of dictionaries with keys "id", "name", and "age".
    """
    try:
        with open(path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        cats_info_list = []
        for line in lines:
            if line.strip():
                cat_id, name, age = line.strip().split(",")
                cats_info_list.append({"id": cat_id, "name": name, "age": age})
        return cats_info_list

    except FileNotFoundError:
        print("File not found.")
        return []


cats_info = get_cats_info("cats_file.txt")
print(cats_info)
