from models.weibo import Weibo
from models.weibo import Comment
from models.user import User
from routes import *

from utils import log
# for decorators
from functools import wraps


main = Blueprint('weibo', __name__)

Model = Weibo

def current_user():
    uid = session.get('user_id')
    if uid is not None:
        u = User.query.get(uid)
        return u

# def admin_required(f):
#     @wraps(f)
#     def function(*args, **kwargs):
#         # your code
#         print('admin required')
#         if request.args.get('uid') != '1':
#             print('not admin')
#             abort(404)
#         return f(*args, **kwargs)
#     return function


@main.route('/')
def index():
    u = current_user()
    if u is None:
        return redirect(url_for('user.login_view'))
    # 查找所有的 todo 并返回
    weibos = Weibo.query.order_by(Weibo.id.desc()).all()
    for w in weibos:
        w.comment = w.load_comments()
        for c in w.comment:
            c.avatar = c.get_avatar()
        w.avatar = w.get_avatar()
    return render_template('weibo_index.html', weibos=weibos, user=u)


@main.route('/add', methods=['POST'])
def add():
    u = current_user()
    if u is not None:
        # log('weibo add', u.id, u.username, u.password)
        form = request.form
        w = Weibo(form)
        w.username = u.username
        w.user_id = u.id
        if w.valid_add():
            w.save()
        # log("save", w.user_id)
        return redirect(url_for('.index', username=u.username))
    else:
        abort(401)

@main.route('/comment', methods=['POST'])
def comment_add():
    u = current_user()
    if u is not None:
        # log('comment_add', u.id, u.username)
        form = request.form
        c = Comment(form)
        c.user_id = u.id
        c.username = u.username
        c.weibo_id = int(form.get('weibo_id', -1))
        if c.valid_add():
            c.save()
        return redirect(url_for('.index', username=u.username))
    else:
        abort(401)

@main.route('/delete/<int:id>')
# @admin_required
def delete(id):
    u = current_user()
    w = Model.query.get(id)
    if u.id == w.user_id:
        w.delete()
        return redirect(url_for('.index'))
    else:
        return redirect(url_for('.index'))
