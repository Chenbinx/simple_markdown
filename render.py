from parser import *


class Render(object):
    def __init__(self):
        pass

    def render_markdown(self, md_text):
        parser = Parser(md_text)
        return ''.join([str(x) for x in parser.parse()])


def main():
    text = '''
    # **Windows** & *comp*

    + [intro](#1)
    + [hello](#2)
    + [chap](#3)
    + [ref](#3)

1. hello
2. world

## intro

introduce the production

example:
```
guard @check voiagent else {
    @svn checkout http://xx.xx.x.xxx/svn/ZXCCP-VPlat_xxxx/trunk/source.repo/src/vx.x/windows/voiagent/
}
# test
```

PROJECT_DIR = @search_file_path voiagent.sln
OUTPUT_DIR = $PROJECT_DIR\Output\
INSTALLER_DIR = @search_file_path voi_windows_client_setup.nsi
***

![img](http://10.74.120.140:8080/docs/notes/cdsp/images/flocker/converge_fsm.png)

hello

We're happy to announce the latest course for raywenderlich.com subscribers - an update to our Beginning iOS Animations course!

    In this course, *you'll* **learn** how to create delightful animations for your iOS apps. Along the way, you'll learn **about** Auto *Layout* constraint [hello](http://www.zte.com.cn) animations, view controller transitions, troubleshooting animations gone wrong, and more!

```
class Strong(object):
    def __init__(self, content):
        self.content = content

    def __str__(self):
        return '<strong>{}</strong>'.format(self.content)
```
'''
    print(Render().render_markdown(text))

if __name__ == '__main__':
    main()    
