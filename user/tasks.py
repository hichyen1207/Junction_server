from __future__ import absolute_import, unicode_literals
from celery import task
from .models import User, MatchAlgorithmScore
from apns2.client import APNsClient
from apns2.payload import Payload
import random
# from Server.settings import APNS_CERT, APNS_TOPIC, USE_SANDBOX
from Server.setting.base import APNS_CERT, APNS_TOPIC, USE_SANDBOX


@task()
def draw_card():
    userList = list()
    users = User.objects.all()
    users.update(card_drawer=None, friend_invitation=None, is_draw_card=False)

    for user in users:
        # remove Thomas
        if user.user_id != '10102347454878415':
            userList.append(user)

    # need to handle this issue
    removed_user = ''
    if len(userList)%2 != 0:
        print('remove one user')
        removed_user = random.SystemRandom().choice(userList)
        print(removed_user)
        for user_index in range(len(userList)):
            if userList[user_index].user_id == removed_user.user_id:
                lastUser = userList.pop(user_index)
                print(lastUser)
                break

        # give a card to removed user
        find_new_card = True
        while find_new_card:
            removed_user_card = random.SystemRandom().choice(userList)
            removed_user_instance = User.objects.get(user_id=removed_user.user_id)
            removed_user_friends = removed_user_instance.friends
            is_friend = False
            for friend in removed_user_friends:
                if friend.user_id == removed_user_card.user_id:
                    is_friend = True
                    break
            if not is_friend:
                removed_user_instance.update(card_drawer=removed_user_card.user_id)
                find_new_card = False

    # assign removed user id to 'removed_user_id' if there is removed user
    if removed_user != '':
        removed_user_id = removed_user.user_id
    else:
        removed_user_id = ''

    loopTime = len(userList)/2 - 1
    count = 0
    while count < loopTime:
        print(len(userList))
        pairUser = random.SystemRandom().sample(userList, 2)
        print(pairUser)

        firstUserId = str(pairUser[0])
        secondUserId = str(pairUser[1])

        firstUser = User.objects.get(user_id=firstUserId)
        friends = list(firstUser.friends)

        is_friend = False
        for friend in friends:
            if friend.user_id == secondUserId:
                print("these two users are already friends.")
                is_friend = True
                break
        if is_friend:
            continue

        firstUser.update(card_drawer=secondUserId)
        secondUser = User.objects.get(user_id=secondUserId)
        secondUser.update(card_drawer=firstUserId)

        for user in pairUser:
            userList.remove(user)
        print(len(userList))
        count += 1


    #   match last two users:
    #   need to check if last two users are already friends
    print('start to match last two users')
    is_friend = False
    first_user = User.objects.get(user_id=str(userList[0]))
    second_user = User.objects.get(user_id=str(userList[1]))
    first_user_friends = first_user.friends
    second_user_friends = second_user.friends

    for friend in first_user_friends:
        print('first user:', first_user)
        print('friend id:', friend.user_id)
        print('second user:', second_user)
        if str(friend.user_id) == str(second_user):
            print("these two users are already friends.")
            is_friend = True
            break
    print('is_friend:', is_friend)

    if is_friend:
        check_list = list()
        check_list.append(str(first_user))
        check_list.append(str(second_user))
        for friend in first_user_friends:
            check_list.append(str(friend.user_id))

        for friend in second_user_friends:
            if not str(friend.user_id) in check_list:
                check_list.append(str(friend.user_id))

        selected_user_list = list()
        users = User.objects.all()
        removed_user_list = [str(first_user), str(second_user), removed_user_id, '10102347454878415']
        for user in users:
            if user.user_id not in removed_user_list and user.card_drawer != '':
                selected_user_list.append(user)
        print(selected_user_list)

        first_selected_user = None
        second_selected_user = None
        check_first_selected_user = False
        check_second_selected_user = False
        count_rematch_time = 0
        while not check_first_selected_user or not check_second_selected_user:
            count_rematch_time += 1
            print("check if the selected users are in the check list.")
            check_first_selected_user = False
            check_second_selected_user = False

            first_selected_user = random.SystemRandom().choice(selected_user_list)
            second_selected_user_id = User.objects.get(user_id=str(first_selected_user)).card_drawer
            second_selected_user = User.objects.get(user_id=str(second_selected_user_id))

            if not str(first_selected_user.user_id) in check_list:
                check_first_selected_user = True
                print("first selected user is not in the check list.")
            if not str(second_selected_user.user_id) in check_list:
                check_second_selected_user = True
                print("second selected user is not in the check list.")
            if count_rematch_time > 20:
                print('restart')
                return draw_card()

        first_user.update(card_drawer=str(first_selected_user.user_id))
        first_selected_user.update(card_drawer=str(first_user.user_id))
        second_user.update(card_drawer=str(second_selected_user.user_id))
        second_selected_user.update(card_drawer=str(second_user.user_id))
        print("first: ", first_user)
        print("first select: :", first_selected_user)
        print("second: ", second_user)
        print("second select: :", second_selected_user)
        print("match last two users with other two users.")

    else:
        print("match last two users.")
        second_user.update(card_drawer=str(first_user))
        first_user.update(card_drawer=str(second_user))

    print('start to send notifications')
    try:
        user_list = User.objects.all()
        for user in user_list:
            if user.device.ios != '':
                # print(user.device.ios)
                custom_payload = {
                    'type': 'card'
                }
                payload = Payload(alert='已經有新的卡片囉！', sound="default", badge=1, custom=custom_payload)
                client = APNsClient(APNS_CERT, use_sandbox=USE_SANDBOX, use_alternative_port=False)
                client.send_notification(user.device.ios, payload, APNS_TOPIC)
        # me = User.objects.get(user_id='10210833777112798')
        # if me.device.ios != '':
        #     custome_payload = {
        #         'type': 'card'
        #     }
        #     payload = Payload(alert='已經有新的卡片囉！', sound="default", badge=1, custom=custome_payload)
        #     client = APNsClient(APNS_CERT, use_sandbox=USE_SANDBOX, use_alternative_port=False)
        #     client.send_notification(me.device.ios, payload, APNS_TOPIC)
    except Exception as e:
        print(e)
    print('finished')

@task()
def draw_card_with_algorithm():
    try:
        print('start')
        MatchAlgorithmScore.objects.delete()
        userList = list()
        users = User.objects.all()
        users.update(card_drawer_of_next_day=None)

        for user in users:
            # job_type_score:
            #   Engineering:   10
            #   IT:            09
            #   Data analysis: 08
            #   pm:            07
            #   uiux:          06
            #   strategy:      05
            #   marketing:     04
            #   sales:         03
            #   finance:       02
            #   other:         00
            job_type = user.job_type
            if job_type == '產品管理':
                job_type_score = 7
            elif job_type == '使用者體驗':
                job_type_score = 6
            elif job_type == '數據分析':
                job_type_score = 8
            elif job_type == '行銷':
                job_type_score = 4
            elif job_type == '銷售':
                job_type_score = 3
            elif job_type == '工程':
                job_type_score = 10
            elif job_type == '資訊科技':
                job_type_score = 9
            elif job_type == '金融':
                job_type_score = 2
            elif job_type == '策略':
                job_type_score = 5
            else:
                job_type_score = 0

            # industry_type_score:
            #   software:           17
            #   hardware:           16
            #   consumer:           14
            #   traditional:        12
            #   finance:            08
            #   law & accounting:   06
            #   media:              04
            #   tourism:            02
            #   other:              00
            industry_type = user.industry_type
            if industry_type == '軟體網路':
                industry_type_score = 17
            elif industry_type == '半導體及電子':
                industry_type_score = 16
            elif industry_type == '消費性產品':
                industry_type_score = 14
            elif industry_type == '傳產製造':
                industry_type_score = 12
            elif industry_type == '金融服務':
                industry_type_score = 8
            elif industry_type == '法律及會計':
                industry_type_score = 6
            elif industry_type == '文教傳播':
                industry_type_score = 4
            elif industry_type == '旅遊休閒':
                industry_type_score = 2
            else:
                industry_type_score = 0

            matchAlgorithmScore = MatchAlgorithmScore(
                user_id=user.user_id,
                pm_profession_score=user.professional_field.pm,
                marketing_profession_score=user.professional_field.marketing,
                data_analysis_profession_score=user.professional_field.data_analysis,
                uiux_profession_score=user.professional_field.uiux,
                startup_profession_score=user.professional_field.startup,
                sales_profession_score=user.professional_field.sales,
                finance_profession_score=user.professional_field.finance,
                information_technology_profession_score=user.professional_field.information_technology,
                business_profession_score=user.professional_field.business,
                pm_interest_score=user.interest_issue.pm,
                marketing_interest_score=user.interest_issue.marketing,
                data_analysis_interest_score=user.interest_issue.data_analysis,
                uiux_interest_score=user.interest_issue.uiux,
                startup_interest_score=user.interest_issue.startup,
                sales_interest_score=user.interest_issue.sales,
                finance_interest_score=user.interest_issue.finance,
                information_technology_interest_score=user.interest_issue.information_technology,
                business_interest_score=user.interest_issue.business,
                job_type_score=job_type_score,
                industry_type_score=industry_type_score
            )
            matchAlgorithmScore.save()

        print('start matching')
        userList = list()
        users = User.objects.all()
        for user in users:
            userList.append(user)
        # remove Thomas
        for user in userList:
            if user.user_id == '10102347454878415':
                userList.remove(user)

        # start matching user
        while (len(userList) > 2):
            print(userList)
            # print(len(userList), random.randint(0,len(userList)))
            score_list = list()
            random_index = random.randint(0,len(userList))
            try:
                self_user = userList[random_index]
            except Exception as e:
                print('error:', e)
                return draw_card_with_algorithm()
            self_user_instance = User.objects.get(user_id=self_user.user_id)
            self_user_score = MatchAlgorithmScore.objects.get(user_id=self_user.user_id)
            for index in range(0, len(userList)):
                partner_user_score = MatchAlgorithmScore.objects.get(user_id=userList[index].user_id)
                profession_score = (
                        abs(self_user_score.pm_profession_score - partner_user_score.pm_profession_score) +
                        abs(self_user_score.marketing_profession_score - partner_user_score.marketing_profession_score) +
                        abs(self_user_score.data_analysis_profession_score - partner_user_score.data_analysis_profession_score) +
                        abs(self_user_score.uiux_profession_score - partner_user_score.uiux_profession_score) +
                        abs(self_user_score.startup_profession_score - partner_user_score.startup_profession_score) +
                        abs(self_user_score.sales_profession_score - partner_user_score.sales_profession_score) +
                        abs(self_user_score.finance_profession_score - partner_user_score.finance_profession_score) +
                        abs(self_user_score.information_technology_profession_score - partner_user_score.information_technology_profession_score) +
                        abs(self_user_score.business_profession_score - partner_user_score.business_profession_score)
                )
                interest_score = (
                        abs(self_user_score.pm_interest_score - partner_user_score.pm_interest_score) +
                        abs(self_user_score.marketing_interest_score - partner_user_score.marketing_interest_score) +
                        abs(self_user_score.data_analysis_interest_score - partner_user_score.data_analysis_interest_score) +
                        abs(self_user_score.uiux_interest_score - partner_user_score.uiux_interest_score) +
                        abs(self_user_score.startup_interest_score - partner_user_score.startup_interest_score) +
                        abs(self_user_score.sales_interest_score - partner_user_score.sales_interest_score) +
                        abs(self_user_score.finance_interest_score - partner_user_score.finance_interest_score) +
                        abs(self_user_score.information_technology_interest_score - partner_user_score.information_technology_interest_score) +
                        abs(self_user_score.business_interest_score - partner_user_score.business_interest_score)
                )
                if self_user_score.job_type_score != 0 and partner_user_score.job_type_score != 0:
                    job_type_score = abs(self_user_score.job_type_scor - partner_user_score.job_type_score)
                else:
                    job_type_score = None
                if self_user_score.industry_type_score != 0 and partner_user_score.industry_type_score != 0:
                    industry_type_score = abs(self_user_score.industry_type_score - partner_user_score.industry_type_score)
                else:
                    industry_type_score = None
                if job_type_score != None and industry_type_score != None:
                    score = (3 * profession_score + 3 * interest_score + job_type_score + industry_type_score)/8
                elif job_type_score == None and industry_type_score != None:
                    score = (3 * profession_score + 3 * interest_score + industry_type_score) / 7
                elif job_type_score != None and industry_type_score == None:
                    score = (3 * profession_score + 3 * interest_score + job_type_score) / 7
                else:
                    score = (3 * profession_score + 3 * interest_score) / 6
                if partner_user_score.user_id != self_user_instance.user_id:
                    score_list.append((partner_user_score.user_id, score))
            sorted_score_list = sorted(score_list, key=lambda x: x[1])
            self_friend_list = self_user_instance.friends
            partner_user_instance = None
            for user_score_tuple in sorted_score_list:
                is_friend = False
                for friend in self_friend_list:
                    if user_score_tuple[0] == friend.user_id or user_score_tuple[0] == self_user_instance.card_drawer:
                        is_friend = True
                        break
                if not is_friend:
                    partner_user_instance = User.objects.get(user_id=user_score_tuple[0])
                    partner_user_instance.card_drawer_of_next_day = self_user_instance.user_id
                    self_user_instance.card_drawer_of_next_day = partner_user_instance.user_id
                    partner_user_instance.save()
                    self_user_instance.save()
                    print('1.', self_user_instance.user_id)
                    print('2.', partner_user_instance.user_id)
                    break
            for user in userList:
                if user.user_id == self_user_instance.user_id:
                    userList.remove(user)
                    break
            for user in userList:
                if user.user_id == partner_user_instance.user_id:
                    userList.remove(user)
                    break

        # match last 2 users
        print(userList)
        if len(userList) == 2:
            print('match last 2 users')
            self_user = userList[0]
            self_user_instance = User.objects.get(user_id=self_user.user_id)
            self_friend_list = self_user_instance.friends
            is_friend = False
            for friend in self_friend_list:
                if userList[1].user_id == friend.user_id:
                    is_friend = True
                    break
            if not is_friend:
                print('last two user are not friends')
                partner_user_instance = User.objects.get(user_id=userList[1].user_id)
                partner_user_instance.card_drawer_of_next_day = self_user_instance.user_id
                self_user_instance.card_drawer_of_next_day = partner_user_instance.user_id
                partner_user_instance.save()
                self_user_instance.save()
                print('1.', self_user_instance.user_id)
                print('2.', partner_user_instance.user_id)
            else:
                print('last two users are friends')

                first_user = User.objects.get(user_id=userList[0].user_id)
                second_user = User.objects.get(user_id=userList[1].user_id)
                first_user_friends = first_user.friends
                second_user_friends = second_user.friends
                check_list = list()
                check_list.append(userList[0].user_id)
                check_list.append(userList[1].user_id)
                for friend in first_user_friends:
                    check_list.append(str(friend.user_id))

                for friend in second_user_friends:
                    if not str(friend.user_id) in check_list:
                        check_list.append(str(friend.user_id))

                selected_user_list = list()
                users = User.objects.all()
                removed_user_list = [str(first_user), str(second_user), '10102347454878415']
                for user in users:
                    if user.user_id not in removed_user_list and user.card_drawer != '':
                        selected_user_list.append(user)
                print(selected_user_list)

                first_selected_user = None
                second_selected_user = None
                check_first_selected_user = False
                check_second_selected_user = False
                count_rematch_time = 0
                while not check_first_selected_user or not check_second_selected_user:
                    count_rematch_time += 1
                    print("check if the selected users are in the check list.")
                    check_first_selected_user = False
                    check_second_selected_user = False

                    first_selected_user = random.SystemRandom().choice(selected_user_list)
                    second_selected_user_id = User.objects.get(user_id=str(first_selected_user)).card_drawer
                    second_selected_user = User.objects.get(user_id=str(second_selected_user_id))

                    if not str(first_selected_user.user_id) in check_list:
                        check_first_selected_user = True
                        print("first selected user is not in the check list.")
                    if not str(second_selected_user.user_id) in check_list:
                        check_second_selected_user = True
                        print("second selected user is not in the check list.")
                    if count_rematch_time > 20:
                        print('restart')
                        return draw_card_with_algorithm()

                first_user.update(card_drawer_of_next_day=str(first_selected_user.user_id))
                first_selected_user.update(card_drawer_of_next_day=str(first_user.user_id))
                second_user.update(card_drawer_of_next_day=str(second_selected_user.user_id))
                second_selected_user.update(card_drawer_of_next_day=str(second_user.user_id))
                print("first: ", first_user)
                print("first select: :", first_selected_user)
                print("second: ", second_user)
                print("second select: :", second_selected_user)
                print("match last two users with other two users.")
        else:
            print('there is only one left user')
            self_user_instance = User.objects.get(user_id=userList[0].user_id)
            user_list = User.objects.all()
            is_friend = True
            random_user = None
            while is_friend:
                is_friend = False
                random_user = random.SystemRandom().choice(user_list)
                self_user_friends = self_user_instance.friends
                for friend in self_user_friends:
                    if friend.user_id == random_user.user_id:
                        is_friend = True
                        break
                if random_user.user_id == self_user_instance.user_id or random_user.user_id == self_user_instance.card_drawer:
                    is_friend = True
            self_user_instance.card_drawer_of_next_day = random_user.user_id
            self_user_instance.save()
    except:
        return draw_card_with_algorithm()

@task()
def update_card():
    print('start update card')
    users = User.objects.all()
    for user in users:
        if user.card_drawer_of_next_day != '10102347454878415':
            user.update(card_drawer=None, draw_card_status='undraw')
        user.card_drawer = user.card_drawer_of_next_day
        user.card_drawer_of_next_day = None
        user.save()

    # send push notification
    print('send notification')
    try:
        user_list = User.objects.all()
        for user in user_list:
            if user.card_drawer != '10102347454878415':
                if user.device.ios != '':
                    custom_payload = {
                        'type': 'card'
                    }
                    payload = Payload(alert='已經有新的卡片囉！', sound="default", badge=1, custom=custom_payload)
                    client = APNsClient(APNS_CERT, use_sandbox=USE_SANDBOX, use_alternative_port=False)
                    client.send_notification(user.device.ios, payload, APNS_TOPIC)
        print('succeed')
    except Exception as e:
        print(e)

    # For test: send to myself
    # try:
    #     me = User.objects.get(user_id='10210833777112798')
    #     if me.device.ios != '':
    #         custome_payload = {
    #             'type': 'card'
    #         }
    #         payload = Payload(alert='已經有新的卡片囉！', sound="default", badge=1, custom=custome_payload)
    #         client = APNsClient(APNS_CERT, use_sandbox=USE_SANDBOX, use_alternative_port=False)
    #         client.send_notification(me.device.ios, payload, APNS_TOPIC)
    # except Exception as e:
    #     print(e)