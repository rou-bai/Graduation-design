from .model.user import User


# 选择教练信息展示data封装
def data_choose_teacher_info(data, teacher_list):
    number = 1
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

        info['image_url'] = "/static/img/" + "t" + str(number) + ".jpg"
        number += 1
        data.append(info)
    return data
