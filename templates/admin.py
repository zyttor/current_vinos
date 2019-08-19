import functools

from flask import (
    Blueprint, redirect, request, session, url_for,
    render_template, g, flash)

from templates.auth import login_required

bp = Blueprint('admin', __name__, url_prefix='/admin')






@bp.route('/c_nivel_estudio')
@login_required
def c_nivel_estudio():
    """
    catalogo_nivel_estudios
    :return:
    """

    from app import mysql
    cur_nivel = mysql.get_db().cursor()
    cur_nivel.execute("""call catalogo_nivel_estudios()""")
    niveles = cur_nivel.fetchall()

    print(niveles)
    return render_template('admin/c_niveles_de_estudio.html', data=niveles)


@bp.route('/agregar_nivel', methods=['POST'])
def agrenar_nivel():
    if request.method == 'POST':
        nombre = request.form['nivel']
        id = request.form['id']
        from app import mysql
        if id=='0':
            db = mysql.get_db()
            cur =db.cursor()
            cur.execute(""" call add_nivel_estudio(%s) """ , (nombre,))
            db.commit()
            flash('El nivel ' + nombre + " se ha registrado con exito", 'exito')
            #print("agrego")


        else:
            #edit_nivel_estudio

            db = mysql.get_db()
            cur = db.cursor()
            cur.execute("""call edit_nivel_estudio (%s,%s)""" , (id, nombre,))
            db.commit()

            flash('La informacion se actualizo correctamente', 'exito')

        return redirect(url_for('admin.c_nivel_estudio'))

@bp.route('/borrar_nivel/<id>')
@login_required
def eliminar_area(id):

    from app import mysql
    db = mysql.get_db()
    cur = db.cursor()

    cur.execute(""" call delete_nivel(%s)  """, (id,))
    db.commit()

    flash('La informacion ha sido eliminada', 'exito')

    return redirect(url_for('admin.c_nivel_estudio'))

#inicia el catalogo parentescos
@bp.route('/c_parentescos')
@login_required
def c_parentescos():
    """
    catalogo_nivel_estudios
    catalago_parentesco
    :return:
    """

    from app import mysql
    cur_nivel = mysql.get_db().cursor()
    cur_nivel.execute("""call catalago_parentesco()""")
    parentescos = cur_nivel.fetchall()

    print(parentescos)
    return render_template('admin/c_parentescos.html', data=parentescos)



@bp.route('/agregar_parentesco', methods=['POST'])
def agregar_par():
    if request.method == 'POST':
        nombre = request.form['parentesco']
        id = request.form['id']

        print(request.form)
        from app import mysql
        print('Entre al post')
        if id=='0':
            print('agregando')
            db = mysql.get_db()
            cur =db.cursor()
            cur.execute(""" call add_parentesco(%s) """ , (nombre,))
            db.commit()
            flash('El parentesco "' + nombre + '" se ha registrado con exito', 'exito')
            #print("agrego")


        else:
            #edit_parentesco
            print('Editandoo')
            db = mysql.get_db()
            cur = db.cursor()
            cur.execute("""call edit_parentesco (%s,%s)""" , (id, nombre,))
            db.commit()

            flash('La informacion se actualizo correctamente', 'exito')

        return redirect(url_for('admin.c_parentescos'))


@bp.route('/borrar_parentesco/<id>')
@login_required
def eliminar_parentesco(id):

    from app import mysql
    db = mysql.get_db()
    cur = db.cursor()

    cur.execute(""" call delete_parentesco(%s)  """, (id,))
    db.commit()

    flash('La informacion ha sido eliminada', 'exito')

    return redirect(url_for('admin.c_parentescos'))




#inicia el catalogo doctos
@bp.route('/c_doctos')
@login_required
def c_doctos():
    """
    catalogo_nivel_estudios
    catalago_parentesco
    :return:
    """

    from app import mysql
    cur_nivel = mysql.get_db().cursor()
    cur_nivel.execute("""call catalago_tipo_docto();""")
    parentescos = cur_nivel.fetchall()

    print(parentescos)
    return render_template('admin/c_tipo_docto.html', data=parentescos)



@bp.route('/agregar_docto', methods=['POST'])
def agregar_docto():
    if request.method == 'POST':
        nombre = request.form['docto']
        id = request.form['id']

        print(request.form)
        from app import mysql
        print('Entre al post')
        if id=='0':
            print('agregando')
            db = mysql.get_db()
            cur =db.cursor()
            cur.execute(""" call add_tipo_docto(%s) """ , (nombre,))
            db.commit()
            flash('El Documento "' + nombre + '" se ha registrado con exito', 'exito')
            #print("agrego")


        else:
            #edit_parentesco
            print('Editandoo')
            db = mysql.get_db()
            cur = db.cursor()
            cur.execute("""call  edit_tipo_docto(%s,%s)""" , (id, nombre,))
            db.commit()

            flash('La informacion se actualizo correctamente', 'exito')

        return redirect(url_for('admin.c_doctos'))


@bp.route('/borrar_docto/<id>')
@login_required
def eliminar_documento(id):

    from app import mysql
    db = mysql.get_db()
    cur = db.cursor()

    cur.execute(""" call delete_tipo_docto(%s)  """, (id,))
    db.commit()

    flash('La informacion ha sido eliminada', 'exito')

    return redirect(url_for('admin.c_doctos'))



#inicia el catalogo ayudas
@bp.route('/c_ayudas')
@login_required
def c_ayudas():
    """
    call catalogo_tipo_ayuda();
    catalago_parentesco
    :return:
    """

    from app import mysql
    cur_nivel = mysql.get_db().cursor()
    cur_nivel.execute("""call catalogo_tipo_ayuda();""")
    ayudas= cur_nivel.fetchall()

    print(ayudas)
    return render_template('admin/c_tipos_de_ayuda.html', data=ayudas)


@bp.route('/agregar_ayuda', methods=['POST'])
def agregar_ayuda():
    if request.method == 'POST':

        nombre = request.form['ayuda']
        operativo  = request.form['operativo']
        id = request.form['id']


        print(request.form)
        from app import mysql
        print('Entre al post')
        if id=='0':
            print('agregando')
            db = mysql.get_db()
            cur =db.cursor()
            cur.execute(""" call add_tipo_ayuda(%s,%s) """ , (nombre,operativo))
            db.commit()
            flash('La ayuda "' + nombre + '" se ha registrado con exito', 'exito')
            #print("agrego")


        else:
            #edit_parentesco
            print('Editandoo')
            db = mysql.get_db()
            cur = db.cursor()
            cur.execute("""call  edit_tipo_ayuda(%s,%s,%s)""" , (id, nombre,operativo,))
            db.commit()

            flash('La informacion se actualizo correctamente', 'exito')

        return redirect(url_for('admin.c_ayudas'))


@bp.route('/borrar_ayuda/<id>')
@login_required
def eliminar_ayuda(id):

    from app import mysql
    db = mysql.get_db()
    cur = db.cursor()

    cur.execute(""" call delete_tipo_ayuda(%s)  """, (id,))
    db.commit()

    flash('La informacion ha sido eliminada', 'exito')

    return redirect(url_for('admin.c_doctos'))


#inicia el catalogo justificaciones
@bp.route('/c_justificaciones')
@login_required
def c_justificaciones():
    """

    :return:
    """

    from app import mysql
    cur_nivel = mysql.get_db().cursor()
    cur_nivel.execute("""call catalago_faltas_ratardos();""")
    retardos= cur_nivel.fetchall()

    print(retardos)
    return render_template('admin/c_justificaciones.html', data=retardos)


@bp.route('/agregar_retardo', methods=['POST'])
def agregar_retardo():
    if request.method == 'POST':

        print(request.form)
        nombre = request.form['justificacion']
        aplica  = request.form['aplica']
        id = request.form['id']



        from app import mysql
        print('Entre al post')
        if id=='0':
            print('agregando')
            db = mysql.get_db()
            cur =db.cursor()
            cur.execute(""" call add_justifiacion_faltas_retardos(%s,%s) """ , (nombre,aplica))
            db.commit()
            flash('La ayuda "' + nombre + '" se ha registrado con exito', 'exito')
            #print("agrego")


        else:
            #edit_parentesco
            print('Editandoo')
            db = mysql.get_db()
            cur = db.cursor()
            cur.execute("""call  edit_faltas_retardos(%s,%s,%s)""" , (id, nombre,aplica,))
            db.commit()

            flash('La informacion se actualizo correctamente', 'exito')

        return redirect(url_for('admin.c_justificaciones'))


@bp.route('/borrar_justificacion/<id>')
@login_required
def eliminar_justificacion(id):

    from app import mysql
    db = mysql.get_db()
    cur = db.cursor()

    cur.execute(""" call delete_faltas_retardos(%s)  """, (id,))
    db.commit()

    flash('La informacion ha sido eliminada', 'exito')

    return redirect(url_for('admin.c_doctos'))

#catalogo_areas
#inicia el catalogo areas
@bp.route('/c_catalogo_areas')
@login_required
def c_catalogo_areas():
    """

    :return:
    """

    from app import mysql
    cur_nivel = mysql.get_db().cursor()
    cur_nivel.execute("""call catalogo_areas();""")
    areas= cur_nivel.fetchall()

    print(areas)
    return render_template('admin/c_areas.html', data=areas)
