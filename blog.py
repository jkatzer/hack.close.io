import os
import re
import codecs
import shutil
import markdown
from jinja2 import Environment, FileSystemLoader

OUTPUT_DIR = '../public_html'
POSTS_DIR = 'posts'
POST_OUTPUT_DIR = os.path.join(OUTPUT_DIR, POSTS_DIR)

def generate():
    # remove previously generated content directory
    shutil.rmtree(OUTPUT_DIR, ignore_errors=True)

    # create our new directory structure
    if not os.path.exists(POST_OUTPUT_DIR):
        os.makedirs(POST_OUTPUT_DIR)

    jinja_env = Environment(loader=FileSystemLoader('templates'))

    posts = os.listdir(POSTS_DIR) 
    generated_posts = []

    post_template = jinja_env.get_template('post.html')

    for post in posts:
        filepath = os.path.join(POSTS_DIR, post)

        with codecs.open(filepath, mode="r", encoding="utf-8") as input_file:
            text = input_file.read()

        def _parse(text):
            m = re.match(r'^\s*(?:---(.*?)---)?\s*(.*)$', text, flags=re.DOTALL)
            fm = {}
            if m.groups()[0]:
                # todo fugly
                fm = dict([line.split(':', 1)[0].strip().lower(), line.split(':', 1)[1].strip()] for line in m.groups()[0].splitlines() if line)
            return fm, m.groups()[1].strip()

        context, md_text = _parse(text)

        if not context.get('title'):
            context['title'] = md_text.split('\n', 1)[0]

        # create a datetime from our date string
        if context.get('date'):
            import dateutil.parser as parser
            context['date'] = parser.parse(context['date'])
        
        if not context.get('published') in ['true', 'True', 'yes', 'Yes']:
            print "%s is a draft." % post
            continue
        if not context.get('title'):
            print "%s has no title." % post
            continue
        if not context.get('date'):
            print "%s has no publish date." % post
            continue

        md_html = markdown.markdown(md_text, extensions=['fenced_code', 'codehilite'])
        context['post'] = md_html
        html = post_template.render(context) 

        # remove any previous file extension (ie, post.md)
        output_filepath = os.path.join(POST_OUTPUT_DIR, "%s.html" % os.path.splitext(post)[0])

        with codecs.open(output_filepath, "w", encoding="utf-8") as output_file:
            output_file.write(html)

        generated_posts.append({'date': context['date'], 'title': context['title'], 'url': '%s/%s' % (POSTS_DIR, os.path.splitext(post)[0])})

    generated_posts.sort(key=lambda x: x['date'])
    print "\n\n========================================="
    print "Generated %d posts." % len(generated_posts)
    print "=========================================\n\n"

    index_template = jinja_env.get_template('index.html')
    html = index_template.render({'posts': generated_posts}) 

    with codecs.open(os.path.join(OUTPUT_DIR, 'index.html'), "w", encoding="utf-8") as output_file:
        output_file.write(html)


if __name__ == "__main__":
    generate()
