import decimal
import functools
import json
from ast import dump
from datetime import datetime, timedelta
import statistics

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,
    jsonify)
from flask_cors import CORS, cross_origin

from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('ws', __name__)

@bp.route('/hist_sucursales_rango_periodo/<fecha_ini>/<fecha_fin>/<periodo>')
@cross_origin(origin='*')
def historico_sucursles_por_fechas_periodo(fecha_ini, fecha_fin, periodo):
    d_fecha_ini = datetime.strptime(fecha_ini, '%Y-%m-%d').date()
    d_fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()

    fecha_actual = d_fecha_ini

    fechas_ini = []

    for result in perdelta(d_fecha_ini, d_fecha_fin, timedelta(days=int(periodo))):
        fechas_ini.append(result)

    fechas = []

    for i in range(len(fechas_ini) - 1):
        fechas.append([fechas_ini[i] , fechas_ini[i + 1]])

    for i in fechas:
        print(i)

    from app import mysql
    cur_sucursales = mysql.get_db().cursor()
    cur_sucursales.execute("call get_all_empresas(); ")
    data = cur_sucursales.fetchall()

    list_sucursales = []
    for i in data:
        list_sucursales.append([i, []])

    for i in fechas:
        cur_historial = mysql.get_db().cursor()
        cur_historial.execute("""call get_ventas_por_fechas(%s ,%s );""", (i[0], i[1],))
        data_hist = cur_historial.fetchall()
        # print(data_hist)# data_his almaceda los puntos obtenidos en las graficas
        for it_data in data_hist:
            for it_suc in list_sucursales:
                if it_data[0] == it_suc[0][0]:
                    it_suc[1].append([str(it_data[2]), i[1]])
    print(fecha_ini)
    print(d_fecha_ini)
    #print(list_sucursales)
    return jsonify({'ventas': list_sucursales,
                    'fecha_ini': fecha_ini,
                    'fecha_fin': fecha_fin})



@bp.route('/historico_hist_suc_name_rango_fechas_periodo/<nombre>/<fecha_ini>/<fecha_fin>/<periodo>')
@cross_origin(origin='*')
def historico_suc_name_rango_fechas_periodo(nombre,fecha_ini,fecha_fin,periodo):

    d_fecha_ini = datetime.strptime(fecha_ini, '%Y-%m-%d').date()
    d_fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()

    fecha_actual = d_fecha_ini

    fechas_ini = []


    for result in perdelta(d_fecha_ini, d_fecha_fin, timedelta(days=int(periodo))):
        fechas_ini.append(result)

    fechas = []

    for i in range(len(fechas_ini) - 1):
        fechas.append([fechas_ini[i] + timedelta(days=1), fechas_ini[i + 1]])

    for i in fechas:
        print(i)

    from app import mysql
    cur_sucursales = mysql.get_db().cursor()
    cur_sucursales.execute ("""call _get_sucursal_by_name (%s)""",(nombre,))
    data_sucursales  = cur_sucursales.fetchall()[0]

    list_historico=[]
    for  i in fechas:
        cur_venta = mysql.get_db().cursor()
        cur_venta.execute("""call  _get_venta_suc_by_fecha (%s,%s,%s) """ , (data_sucursales[0], i[0],i[1],))
        list_historico.append(cur_venta.fetchall()[0])
    print(list_historico)

    val_max=list_historico[0][2]
    val_min=list_historico[0][2]

    for i in list_historico:
        if i[2]> val_max:
            val_max = i[2]
        if i[2]< val_min:
            val_min = i[2]

    print([val_max, val_min])

    list_json = []
    for i in list_historico:
        estado  = 0
        if i[2] == val_max:
            estado =1
        if i[2] == val_min:
            estado =-1
        list_json.append([i[0],i[1], str(i[2]), estado])

    return jsonify ( {'historico': list_json,
                      'ini':fecha_ini,
                      'fin':fecha_fin,
                        'ID': data_sucursales[0],
                      'nombre': nombre} )


@bp.route('/hist_suc_venta_art_fechas/<suc>/<fecha_ini>/<fecha_fin>')
@cross_origin(origin='*')
def hist_suc_venta_fechas(suc,fecha_ini,fecha_fin):

    d_fecha_ini = datetime.strptime(fecha_ini, '%Y-%m-%d').date()
    d_fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()

    from app import mysql
    cur_sucursales = mysql.get_db().cursor()
    cur_sucursales.execute("""call _get_sucursal_by_name (%s)""", (suc,))
    data_sucursales = cur_sucursales.fetchall()[0]

    cur_venta = mysql.get_db().cursor()
    cur_venta.execute(""" call _get_venta_articulos_por_fechas(%s, %s , %s,%s)""", (data_sucursales[0],
                                                                                    d_fecha_ini,
                                                                                    d_fecha_fin,10))
    
    data  =  cur_venta.fetchall()
    data_json =[]

    for i in data:
        data_json.append([i[0], i[1],i[2], str(i[3])])

    print(data_json)
    return jsonify ( {'ventas': data_json ,
                      'sucursal':data_sucursales[1],
                     'fecha_ini': fecha_ini,
                     'fecha_fin': fecha_fin })


@bp.route('/hist_suc_emp_fechas_periodo/<suc>/<fecha_ini>/<fecha_fin>/<periodo>')
@cross_origin(origin='*')
def hist_suc_fechas_periodo(suc,fecha_ini,fecha_fin, periodo):
    print('inicia')
    id= -1;
    error=[]
    from app import mysql

    cur = mysql.get_db().cursor()
    cur.execute("""select id_sucursal,nombre from sucursales where nombre =  %s;""" , (suc))
    id= cur.fetchall()[0][0]


    cur_empleados = mysql.get_db().cursor()
    cur_empleados.execute(""" select id_empleado from empleados where id_sucursal = %s """ , (id,))
    #cur_empleados.execute(""" select id_empleado from empleados where id_empleado  in (1,2)""")

    data_empleados = cur_empleados.fetchall()
    print(data_empleados)

    if id==-1:
        error.append("ID")
    print(id)

    list = []

    d_fecha_ini = datetime.strptime(fecha_ini, '%Y-%m-%d').date()
    d_fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()

    fecha_actual = d_fecha_ini

    fechas_ini = []

    for result in perdelta(d_fecha_ini, d_fecha_fin, timedelta(days=int(periodo))):
        fechas_ini.append(result)

    for i in range(len(fechas_ini) - 1):
        list.append([fechas_ini[i] + timedelta(days=1), fechas_ini[i + 1]])

    for i in list:
        print(i)


    historico = []
    for id_empleado in data_empleados:
        historico_empleado =[]
        for i in list:
            #print((id_empleado[0] , i[0], ))
            cur_historico = mysql.get_db().cursor()
            cur_historico.execute("""call get_historial_empleados_suc_fecha(%s,%s , %s ); """,
                                  (id_empleado[0], i[0], i[1] , ))
            data= cur_historico.fetchall()
            c_data =[]

            for i in data:
                c_data.append([i[1],i[2],i[3],str(i[4])])
            historico_empleado.append(c_data)
        historico.append(historico_empleado)

    return jsonify ( {'ventas':historico,
                      'Fecha_ini': fecha_ini,
                      'Fecha_fin': fecha_fin,
                      'ID': id,
                      'suc':suc,
                      'error': error} )



# ayuda para manejo de fechas
def perdelta(start, end, delta):
    curr = start
    while curr < end:
        yield curr
        curr += delta



class DecimalEncoder(json.JSONEncoder):
    def _iterencode(self, o, markers=None):
        if isinstance(o, decimal.Decimal):
            # wanted a simple yield str(o) in the next line,
            # but that would mean a yield on the line with super(...),
            # which wouldn't work (see my comment below), so...
            return (str(o) for o in [o])
        return super(DecimalEncoder, self)._iterencode(o, markers)

