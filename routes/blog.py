from models.blog import Blog
from models.user import User

from routes import *

from utils import log

# for decorators
from functools import wraps

main = Blueprint('blog', __name__)

Model = Blog


def admin_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        print('admin required')
        if request.args.get('uid') != '1':
            print('not admin')
            abort(404)
        return f(*args, **kwargs)

    return function


def current_user():
    uid = session.get('user_id')
    if uid is not None:
        u = User.query.get(uid)
        return u


@main.route('/')
def index():
    u = current_user()
    if u is None:
        return redirect(url_for('user.login_view'))
    blogs = Model.query.order_by(Model.id.desc()).all()
    for blog in blogs:
        blog.content = markdown(blog.content)
    return render_template('blog_index.html', blogs=blogs, user=u)


@main.route('/<int:user_id>')
def show(user_id):
    u = current_user()
    m = Model.query.get(user_id)
    m.content = markdown(m.content)
    print(m.content)
    return render_template('blog_show.html', blog=m, user=u)


@main.route('/add_article')
# @admin_required
def add_article():
    u = current_user()
    return render_template('blog_edit.html', user=u)


@main.route('/add', methods=['POST'])
# @admin_required
def add():
    u = current_user()
    if u is not None:
        log('blog add', u.id, u.username)
        form = request.form
        blog = Model(form)
        blog.username = u.username
        blog.user_id = u.id
        blog.save()
        # log(blog, blog.user_id, blog.save())
        return redirect(url_for('.index'))
    else:
        abort(401)


@main.route('/update/<int:id>', methods=['POST'])
def update(id):
    form = request.form
    t = Model.query.get(id)
    t.update(form)
    return redirect(url_for('.index'))


@main.route('/delete/<int:id>')
@admin_required
def delete(id):
    u = current_user()
    blog = Model.query.get(id)
    if u.id == blog.user_id:
        blog.delete()
        return redirect(url_for('.index'))
    else:
        log('删除失败', u.id, blog.user_id)
        return redirect(url_for('.index'))
