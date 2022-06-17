import sys
import os
import re

def collect_files(extensions):    
    # Get list of all files
    all_files = []
    for root, dirs, files in os.walk('./'):
        for f in files:
            all_files.append(os.path.join(root, f))
    
    # Remove invalid files
    for i in range(len(all_files)-1, -1, -1):
        ext = all_files[i].split('.')[-1]
        if ext not in extensions:
            all_files.pop(i)
        
    return all_files

def extract_css_styles(css):
    styles = set()
    for style_tag in re.findall(r'\n([^:\n@%]*)\{', css):
        styles = styles.union(set(style_tag.strip().split(' ')))
    print(len(styles), 'styles found')
    return styles
    

def remove_unused(css):
    styles = extract_css_styles(css)
    
    html_files = collect_files({'html', 'svelte', 'vue'})

    # Search through all classes and ids used across all HTML and remove used
    for file_path in html_files:
        with open(file_path, 'r') as f:
            html = f.read()
            # Remove used classes
            for classes in re.findall(r'class="(.*)"', html):
                for _class in classes.split(' '):
                    try:
                        styles.remove('.' + _class)
                    except:
                        pass
            
            # Remove used ids
            for ids in re.findall(r'id="(.*)"', html):
                for _id in ids.split(' '):
                    try:
                        styles.remove('#' + _id)
                    except:
                        pass
                    
            # HTML tags
            to_remove = set()
            for style in styles:
                if '.' not in style and '#' not in style and '<' + style in html:
                    to_remove.add(style)
            styles = styles - to_remove
    
    # CSS classes may be added using javascript
    js_files = collect_files({'js', 'mjs', 'svelte', 'vue', 'html'})
    to_remove = set()
    for file_path in js_files:
        with open(file_path, 'r') as f:
            js = f.read()
            # Any mention of style within js -> assume style used and added using js
            for style in styles:
                if style.replace('.', '').replace('#', '') in js:
                    to_remove.add(style)
    styles = styles - to_remove
    
    print('Ignoring styles mentioned in JavaScript', to_remove) 
       
    # Styles remaining in set are not found in any html file
    print('To remove', len(styles), 'styles:', styles)
    
def run(path):
    with open(path, 'r') as f:
        css = f.read()
    
    remove_unused(css)

def get_path():
    if len(sys.argv) > 1:
        return sys.argv[1]
    return None

if __name__ == '__main__':
    path = get_path()
    run(path)