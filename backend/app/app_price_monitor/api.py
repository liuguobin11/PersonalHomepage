import time
import json
import requests
import datetime
import traceback
import urllib.request
from . import app_price_monitor
from flask_cors import cross_origin
from flask import session, redirect, url_for, current_app, flash, Response, request, jsonify
from ..model.app_model import app as app_table
from ..login.login_funtion import User
from ..privilege.privilege_control import permission_required

URL_PREFIX = '/app'
DAY_HOUR = 24


# 获取用户id下有效的app
def app_get(user_id):
    app_table_query = app_table.select().where((app_table.user_id == user_id) & (app_table.is_valid == 1)).order_by(app_table.order).dicts()
    result = [{
        row['id'], row['name'], row['except_price'], row['notify'], row['notify_method'], row['notify_interval_raw'], row['notify_interval_unit'], row['notify_interval'], row['notify_trigger_time'],
        row['update_time']
    } for row in app_table_query]
    return result


# 将用户id下的app置为删除状态
def app_del_all(user_id):
    app_table.update(is_valid=0, update_time=datetime.datetime.now()).where((app_table.user_id == user_id) & (app_table.is_valid == 1)).execute()


@app_price_monitor.route('/get', methods=['GET'])
@cross_origin()
def get():
    try:
        user_name = request.get_json()['user']
        user = User(user_name)
        user_id = user.user_id
        response = {'code': 200, 'msg': '成功！', 'data': app_get(user_id)}
        return jsonify(response)

    except Exception as e:
        traceback.print_exc()
        response = {'code': 500, 'msg': '失败！错误信息：' + str(e) + '，请联系管理员。', 'data': []}
        return jsonify(response), 500


@app_price_monitor.route('/add', methods=['POST'])
@cross_origin()
def add():
    pass

@app_price_monitor.route('/delete', methods=['POST'])
@cross_origin()
def delete():
    pass

@app_price_monitor.route('/edit', methods=['POST'])
@cross_origin()
def edit():
    try:
        user_name = request.get_json()['user']
        user = User(user_name)
        user_id = user.user_id
        apps = request.get_json()['apps']
        app_del_all(user_id)
        for app in apps:
            notify_interval_raw = app['notify_interval_raw']
            notify_interval_unit = app['notify_interval_unit']
            notify_interval = notify_interval_raw * DAY_HOUR if notify_interval_unit == 1 else notify_interval_raw
            app_table.create(
                name=app['name'],
                url=app['url'],
                user_id=app['user_id'],
                expect_price=app['expect_price'],
                order=app['order'],
                is_valid=1,
                notify=app['notify'],
                notify_method=app['notify_method'],
                notify_interval_raw=notify_interval_raw,
                notify_interval_unit=notify_interval_unit,
                notify_interval=notify_interval,
                notify_trigger_time=datetime.datetime.now() + datetime.timedelta(hours=notify_interval),
                update_time=datetime.datetime.now(),
            )
        response = {'code': 200, 'msg': '成功！'}
        return jsonify(response)

    except Exception as e:
        traceback.print_exc()
        response = {'code': 500, 'msg': '失败！错误信息：' + str(e) + '，请联系管理员。', 'data': []}
        return jsonify(response), 500