import enum
import sys
import os
import re

def html_files():
    valid_extensions = {'html', 'svelte', 'vue'}
    
    # Get list of all files
    all_files = []
    for root, dirs, files in os.walk('./'):
        for f in files:
            all_files.append(os.path.join(root, f))
    
    # Remove invalid files
    for i in range(len(all_files)-1, -1, -1):
        ext = all_files[i].split('.')[-1]
        if ext not in valid_extensions:
            all_files.pop(i)
        
    return all_files
    
def run(path):
    styles = set()
    with open(path, 'r') as f:
        css = f.read()
        for style_tag in re.findall(r'\n([^:\n@%]*)\{', css):
            styles.add(style_tag.strip())
    print(len(styles), 'styles found')
            
    
    files = html_files()

    for file_path in files:
        with open(file_path, 'r') as f:
            html = f.read()
            # Cover classes
            for classes in re.findall(r'class="(.*)"', html):
                for _class in classes.split(' '):
                    try:
                        styles.remove('.' + _class)
                    except:
                        pass
            
            # Cover ids
            for ids in re.findall(r'id="(.*)"', html):
                for _id in ids.split(' '):
                    try:
                        styles.remove('#' + _id)
                    except:
                        pass
    
    # Styles remaining in set are not found in any html file
    print('To remove', len(styles), 'styles:', styles)

def get_path():
    if len(sys.argv) > 1:
        return sys.argv[1]
    return None

if __name__ == '__main__':
    path = get_path()
    run(path)