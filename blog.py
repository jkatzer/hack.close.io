import os
import re
import codecs
import shutil
import markdown
from jinja2 import Environment, FileSystemLoader

OUTPUT_DIR = '.generated'
POSTS_DIR = 'posts'
POST_OUTPUT_DIR = os.path.join(OUTPUT_DIR, POSTS_DIR)

def generate():
    # remove previously generated content directory
    shutil.rmtree(OUTPUT_DIR, ignore_errors=True)

    jinja_env = Environment(loader=FileSystemLoader('templates'))

    posts = os.listdir(POSTS_DIR) 
    generated_posts = []

    post_template = jinja_env.get_template('post.html')

    for post in posts:
        filepath = os.path.join(POSTS_DIR, post)
        date_created = int(os.path.getctime(filepath)) #really last modified on *nux

        with codecs.open(filepath, mode="r", encoding="utf-8") as input_file:
            text = input_file.read()

        def _parse(text):
            m = re.match(r'^\s*(?:---(.*?)---)?\s*(.*)$', text, flags=re.DOTALL)
            fm = {}
            if m.groups()[0]:
                fm = dict([v.strip() for v in line.split(':', 1)] for line in m.groups()[0].splitlines() if line)
            return fm, m.groups()[1].strip()

        context, md_text = _parse(text)

        if not context.get('title'):
            context['title'] = md_text.split('\n', 1)[0]

        if not context.get('published', True) or not context.get('title'):
            continue

        md_html = markdown.markdown(md_text)
        context['post'] = md_html
        html = post_template.render(context) 

        # remove any previous file extension (ie, post.md)
        output_filepath = os.path.join(POST_OUTPUT_DIR, "%s.html" % os.path.splitext(post)[0])

        if not os.path.exists(POST_OUTPUT_DIR):
            os.makedirs(POST_OUTPUT_DIR)

        with codecs.open(output_filepath, "w", encoding="utf-8") as output_file:
            output_file.write(html)

        generated_posts.append({'date_created': date_created, 'title': context['title'], 'url': '%s/%s.html' % (POSTS_DIR, os.path.splitext(post)[0])})

    generated_posts.sort(key=lambda x: x['date_created'])
    print generated_posts

    index_template = jinja_env.get_template('index.html')
    html = index_template.render({'posts': generated_posts}) 

    with codecs.open(os.path.join(OUTPUT_DIR, 'index.html'), "w", encoding="utf-8") as output_file:
        output_file.write(html)


if __name__ == "__main__":
    generate()
