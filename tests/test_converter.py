import unittest
from md2html.converter import MarkdownConverter

class MarkdownConverterTest(unittest.TestCase):
    def test_sample_markdown_conversion(self):
        markdown = """An h2 header
---------

An h1 header
=====

Now a nested list:

 1. First, get these ingredients:

      * carrots
      * celery
      * lentils


 2. Boil some water.
 [image] Water boiling.
 `code goes here`
"""
        converter = MarkdownConverter()
        html = converter.convert(markdown)
        self.assertIn('<h2>An h2 header</h2>', html)
        self.assertIn('<h1>An h1 header</h1>', html)
        self.assertIn('<ol>', html)
        self.assertIn('<ul>', html)
        self.assertIn('<code>code goes here</code>', html)

    def test_fenced_code_block(self):
        markdown = """```
<tag>This is a code block</tag>
```
"""
        converter = MarkdownConverter()
        html = converter.convert(markdown)
        self.assertIn('<pre><code>', html)
        self.assertIn('&lt;tag&gt;This is a code block&lt;/tag&gt;', html)

if __name__ == '__main__':
    unittest.main()
