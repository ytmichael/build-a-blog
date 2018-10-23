from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:Bethany765@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))

    def __init__(self, title,body):
        self.title = title
        self.body = body

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    if request.method == 'POST':
        title = request.form['blog']
        body = request.form['body']
        title_error = ''
        body_error = ''
        if len(title) == 0 and len(body) == 0:
            title_error = 'Invalid Title'
            body_error = 'Blog body can not be empty'
            return render_template('new_post.html',title_error=title_error,body_error=body_error)
        elif len(title) == 0 and len(body) != 0:
            title_error = 'Invalid Title'
            return render_template('new_post.html',title_error=title_error)
        elif len(body) == 0 and len(title) != 0:
            body_error = 'Blog body can not be empty'
            return render_template('new_post.html',body_error=body_error)
        else:
            if not title_error and not body_error:
                new_blog = Blog(title,body)
                db.session.add(new_blog)
                db.session.commit()
                return render_template('ind_blog.html',title="Build a Blog!", 
                blog=new_blog)
            else: 
                return render_template('new_post.html')
            
    return render_template('new_post.html')
  

@app.route('/blog', methods=['POST', 'GET'])
def blog():

    if (request.args.get('id')):
        x = int(request.args.get('id'))
        blog = Blog.query.get(x)
        return render_template('ind_blog.html',title="Build a Blog!", 
        blog=blog)
    else:
        blogs = Blog.query.all()
        return render_template('blog.html',title="Build a Blog!", 
        blogs=blogs)
    


if __name__ == '__main__':
    app.run()