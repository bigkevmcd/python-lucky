def parse_card(filename):
    try:
        with open(filename, "r") as f:
            result = {}
            lines = f.read().split("----\n")
            result["title"] = lines[0].strip()
            result["body"] = lines[1]
            result["link_url"] = lines[2].strip()
        return result
    except IOError:
        return
