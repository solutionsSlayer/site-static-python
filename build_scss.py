import sass
import os

def compile_scss():
    scss_path = 'scss/main.scss'
    css_path = 'public/styles.css'
    
    css_content = sass.compile(filename=scss_path)
    
    with open(css_path, 'w') as f:
        f.write(css_content)

if __name__ == '__main__':
    compile_scss()
