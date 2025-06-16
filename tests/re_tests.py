import re

# Determine if Markdown text has any tags at the beginning of the line.
text = """
### An h3 header ###

Now a nested list:

 1. First, get these ingredients:

      * carrots
      * celery
      * lentils

 2. Boil some water.
 [image] Water boiling.
 `code goes here`
"""
# pattern = r"^[#\d\*\`\->\[]"
pattern = r"^[#`-]|^\*|^\d|^\[|^\!"
"""for line in text.splitlines() :
    line.strip()
    print(line)
    print(re.match(pattern, line))"""
text = "`code"
print(re.match(pattern, text) != None)
text = "# Header 1"
print(re.match(pattern, text) != None)
text = "Fun"
print(re.match(pattern, text) != None)
text = """`code
    # Header 1
Fun
    * celery
    1. Go
- Bullet
[image]
!alt text
"""
for line in text.splitlines() :
    print(re.match(pattern, line.strip()) != None)