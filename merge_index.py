from os import getcwd
from os.path import join
from json import loads, dumps

current_dir = getcwd()
search_str = 'n=[o("manifest","manifest.json"+t),o("catalog","catalog.json"+t)]'

with open(join(current_dir, 'docs', 'index.html'), 'r') as f:
    index_html = f.read()
    
with open(join(current_dir, 'docs', 'manifest.json'), 'r') as f:
    manifest_json = loads(f.read())
    
with open(join(current_dir, 'docs', 'catalog.json'), 'r') as f:
    catalog_json = loads(f.read())

with open(join(current_dir, 'docs', 'index.html'), 'w') as f:
    new_str = "n=[{label: 'manifest', data: "+dumps(manifest_json)+"},{label: 'catalog', data: "+dumps(catalog_json)+"}]"
    new_index_html = index_html.replace(search_str, new_str)
    f.write(new_index_html)
