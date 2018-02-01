from .model.user import User
from datetime import datetime, date, timedelta


# 选择教练信息展示data封装
def data_choose_teacher_info(data, teacher_list):
    for each in teacher_list:
        info = {}
        info['teacher_id'] = each.id
        info['t_work_time'] = each.t_work_time
        user_id = each.t_u_id
        user = User.query.get(user_id)
        info['user_id'] = user_id
        info['real_name'] = user.real_name
        info['t_gender'] = user.t_gender
        info['phone'] = user.phone
        info['email'] = user.email
        info['username'] = user.username
        info['image_url'] = "/static/img/" + user.username + ".jpg"
        data.append(info)
    return data


# 封装当前一周列表
def make_week_list(Week_list):
    today = date.today()
    Monday = today - timedelta(today.weekday())
    for i in range(7):
        Week_list.append(Monday + timedelta(i))
    return Week_list
