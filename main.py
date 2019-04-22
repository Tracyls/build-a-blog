from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app= Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql+pymysql://build-a-blog:Assignment2.11@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120))
    post = db.Column(db.String(120))

    def __init__(self, title, post):
        self.title = title
        self.post = post

@app.route('/')
def index():
    return redirect('/blog')

@app.route('/blog')
def display_blogs():
    post_id = request.args.get('id')
    if (post_id):
        indiv_post = Blog.query.get(post_id)
        return render_template('indiv_post.html', indiv_post=indiv_post)
    else:
        all_blog_posts = Blog.query.all()
        return render_template('blog.html', posts=all_blog_posts)



def no_text(text):
    if text == "":
        return True
    else:
        return False


@app.route('/newpost', methods=['POST', 'GET'])
def add_entry():

    if request.method == 'POST':
        title_error = ""
        blog_entry_error = ""

        post_title = request.form['blog_title']
        post_entry = request.form['blog_post']
        post_new = Blog(post_title, post_entry)

        
        if not no_text(post_title) and not no_text(post_entry):
            db.session.add(post_new)
            db.session.commit()
            post_link = "/blog?id=" + str(post_new.id)
            return redirect(post_link)
        else:
            if no_text(post_title) and no_text(post_entry):
                title_error = "Please enter text for blog title"
                blog_entry_error = "Please enter text for blog entry"
                return render_template('new_post.html', blog_entry_error=blog_entry_error, title_error=title_error)
            elif no_text(post_title):
                title_error = "Please enter text for blog title"
                return render_template('new_post.html', title_error=title_error, post_entry=post_entry)
            elif no_text(post_entry):
                blog_entry_error = "Please enter text for blog entry"
                return render_template('new_post.html', blog_entry_error=blog_entry_error, post_title=post_title)

    else:
        return render_template('new_post.html')



if __name__ == '__main__':
    app.run()