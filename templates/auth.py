import functools

from flask import (
    Blueprint, redirect, request, session, url_for,
    render_template, g)

from werkzeug.utils import secure_filename, escape

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/')
def index():
    usuario =None
    if 'username' in session:
        usuario = escape(session['username'])
    print(usuario)
    return render_template('index.html', data = usuario)
    #return 'You are not logged in'

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['user']
        #session['username'] = request.form['user']

        return redirect(url_for('auth.index'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@bp.route('/log2', methods=['GET', 'POST'])
def login_2():

    if request.method == 'POST':
        #session['username'] = request.form['user']
        usuario = request.form['user']
        clave = request.form['clave']

        print([usuario,clave])
        from app import mysql
        cur = mysql.get_db().cursor()
        cur.execute("""call getUsuario (%s, %s)""", (usuario,clave,))
        #print(cur.fetchone())
        session['username'] = cur.fetchone()[0]
        print(session['username'])

        return redirect(url_for('auth.index'))


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('username')

    if user_id is None:
        g.user = None
    else:
        from app import mysql
        cur = mysql.get_db().cursor()
        cur.execute(
            'select * from usuarios_del_sistema where id_usuario  = %s', (user_id,)
        )
        g.user = cur.fetchone()[0]


@bp.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('auth.index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.index'))

        return view(**kwargs)

    return wrapped_view

