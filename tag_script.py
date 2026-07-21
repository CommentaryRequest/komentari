import json

def write_tag_script(output, tag_script):
    with open(output, "w") as output_file:
        json.dump(tag_script, output_file)
