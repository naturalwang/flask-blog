from models.user import User
from routes import *

from utils import log

main = Blueprint('user', __name__)


def current_user():
    """
    从session中获取当前用户id， 在数据库中找出用户数据
    """
    uid = session.get('user_id')
    if uid is not None:
        u = User.query.get(uid)
        return u


@main.route('/')
def login_view():
    u = current_user()
    if u is not None:
        if session.get('logged_in'):
            return redirect(url_for('.profile'))
    return render_template('user_login.html')


@main.route('/user/register', methods=['POST'])
def register():
    form = request.form
    u = User(form)
    status = u.valid_register()
    if status:
        u.save()
        session.permanent = True
        session['uid'] = u.id
        return redirect('/')
    else:
        return redirect(url_for('.login_view'))


@main.route('/user/login', methods=['POST'])
def login():
    form = request.form
    u = User(form)
    # 检查 u 是否存在于数据库中并且 密码用户 都验证合格
    user = User.query.filter_by(username=u.username).first()
    if u.valid_login(user):
        log('登录成功')
        session['user_id'] = user.id
        session['logged_in'] = True
    else:
        log('登录失败')
    return redirect(url_for('.login_view'))


@main.route('/user/logout', methods=['post'])
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('.login_view'))


@main.route('/user/update_password', methods=['POST'])
def update_password():
    u = current_user()
    password = request.form.get('password', '123')
    if u.change_password(password):
        log('修改成功')
    else:
        log('用户密码修改失败')
    return redirect('/user/profile')


@main.route('/user/update_avatar', methods=['POST'])
def update_avatar():
    u = current_user()
    avatar = request.form.get('avatar', '')
    log('avatar', avatar)
    if u.change_avatar(avatar):
        log('修改成功')
    else:
        log('用户头像修改失败')
    return redirect('/user/profile')


@main.route('/user/profile', methods=['GET'])
def profile():
    u = current_user()
    if u is not None:
        log('profile', u.id, u.username, u.password)
        return render_template('profile.html', user=u)
    else:
        abort(401)
