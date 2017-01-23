## Keibado padock images crawler

### What is this?

A tool for collecting padock photo images from [Keibado](http://www.keibado.ne.jp/).

### Data structure

Data is saved as pickle file.
Data consists of an array of objects. 

One object is like this.

```
{
  'url': u'http://www.keibado.ne.jp/keibabook/170109/photo01.html', 
  'padock_photo_url': u'http://www.keibado.ne.jp/keibabook/170109/images/pp01.jpg', 
  'name': u'\u30ac\u30ea\u30d0\u30eb\u30c7\u30a3'
}
```

### Usage

```
$ python keibado_crawler.py
$ python download.py -o output_directory
```

If you run the script later, you can update your dataset.

