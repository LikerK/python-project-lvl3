import re

a = '<link rel="stylesheet" media="all" href="/assets/application.css">'

b = re.search(r'(?<=href="\/)([^\'"])*|(?<=src="\/)([^\'"])*', a)
d = re.sub(r"\/", '-', b.group())
print(d)
