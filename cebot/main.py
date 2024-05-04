import pyautogui
import random
import time
import datetime
import winsound
import sys


class NoExpectedImageFoundException(Exception):
    "Raised when none of the expected images could be found."
    pass


def alert_sound_screenshot(reasonString=''):
    print("异常截屏：" + reasonString)
    time.sleep(0.5)
    freq = 1000
    dur = 250
    winsound.Beep(freq, dur)
    pyautogui.screenshot("screenshots/" + time.strftime("%Y%m%d-%H%M%S", time.localtime()) + ".png")


def sleep_at_least(minSec, maxDelaySec=2):
    sleepTime = round(minSec + random.uniform(0, 1) * maxDelaySec, 2)
    sleepTimeInt = int(sleepTime)
    sleepTimeExtra = sleepTime - sleepTimeInt
    if sleepTime <= 10:
        time.sleep(sleepTime)
    else:
        print("Sleep for " + str(round(sleepTime/60, 2)) + " minutes")
        for remaining in range(sleepTimeInt, 0, -1):
            sys.stdout.write("\r")
            sys.stdout.write("\033[K")
            sys.stdout.write(str(round(remaining/60, 2)) + " minutes remaining")
            sys.stdout.flush()
            time.sleep(1)
        time.sleep(sleepTimeExtra)
        print("")


def locate_till_exist(path, maxTryTime=20, delayBetweenTriesSec=1):
    tryTime = 0
    while tryTime < maxTryTime:
        tryTime += 1
        try:
            return pyautogui.center(pyautogui.locateOnScreen(path, confidence=0.85))
        except pyautogui.ImageNotFoundException:
            time.sleep(delayBetweenTriesSec)
            continue
    raise pyautogui.ImageNotFoundException


def locate_till_whichever_exist(path0, path1, path2=None, maxTryTime=20, delayBetweenTriesSec=1):
    tryTime = 0
    while tryTime < maxTryTime:
        tryTime += 1
        try:
            x, y = pyautogui.center(pyautogui.locateOnScreen(path0, confidence=0.85))
            return 0, x, y
        except pyautogui.ImageNotFoundException:
            try:
                x, y = pyautogui.center(pyautogui.locateOnScreen(path1, confidence=0.85))
                return 1, x, y
            except pyautogui.ImageNotFoundException:
                if path2 != None:
                    try:
                        x, y = pyautogui.center(pyautogui.locateOnScreen(path2, confidence=0.85))
                        return 2, x, y
                    except pyautogui.ImageNotFoundException:
                        time.sleep(delayBetweenTriesSec)
                        continue
                else:
                    time.sleep(delayBetweenTriesSec)
                    continue
    raise pyautogui.ImageNotFoundException


def click(x, y):
    sleep_at_least(0.2, 3)
    pyautogui.moveTo(x, y, 0.5, pyautogui.easeInQuad)
    sleep_at_least(0.2, 0)
    pyautogui.click(x, y)
    sleep_at_least(0.2, 0)
    pyautogui.moveTo(1000, 50, 0.5, pyautogui.easeInQuad)


def find_click(path):
    x, y = locate_till_exist(path)
    sleep_at_least(0.1, maxDelaySec=1)
    click(x, y)


def check_has_energy():
    try:
        index, x, y = locate_till_whichever_exist("home_attack.png", "home_no_energy.png")
        if index == 0:
            return True, x, y
        elif index == 1:
            return False, -1, -1
    except pyautogui.ImageNotFoundException:
        alert_sound_screenshot("找不到左侧栏有/无能量按钮")
        raise NoExpectedImageFoundException


def check_has_target():
    try:
        index, x, y = locate_till_whichever_exist("no_target.png", "active.png")
        if index == 0:
            return False, -1, -1
        elif index == 1:
            return True, x, y
    except pyautogui.ImageNotFoundException:
        alert_sound_screenshot("既没有左侧栏无目标，也没有Active")
        raise NoExpectedImageFoundException


def check_is_hosped_or_jailed(isRefresh=True):
    if isRefresh:
        try:
            print("寻找书签CE")
            find_click("page_ce.png")
            print("已点击书签CE")
        except pyautogui.ImageNotFoundException:
            alert_sound_screenshot("找不到书签CE")
            raise NoExpectedImageFoundException

    try:
        index, x, y = locate_till_whichever_exist("icon_jail.png", "icon_hosp.png", "status_active.png")
        if index == 0:
            print("正在监狱")
            return True
        elif index == 1:
            print("正在住院")
            return True
        elif index == 2:
            print("状态正常")
            return False
    except pyautogui.ImageNotFoundException:
        alert_sound_screenshot("找不到住院/入狱/正常状态图标")
        raise NoExpectedImageFoundException


def google():
    try:
        print("稍等进入Google")
        sleep_at_least(5, 5)
        print("寻找书签Google")
        find_click("page_google.png")
        print("已点击书签Google")
    except pyautogui.ImageNotFoundException:
        alert_sound_screenshot("找不到书签Google")


def handle_attacks():
    global nextAttackAt
    global attackDoneCount
    global jobDurationMinute
    global loopMaxDelayMinute

    if nextAttackAt != 0 and time.time() + jobDurationMinute * 60 + loopMaxDelayMinute * 60 <= nextAttackAt:
        print("进攻未到时间")
        return
    print("开始进攻")
    nextAttackAt = time.time() + 120 * 60 + random.randint(-60 * 60, 0)

    count = 0
    while count < 12:
        count += 1
        print("检查是否有能量")
        hasEnergy, x, y = check_has_energy()
        if hasEnergy == False:
            print("没有能量，正常结束")
            return
        print("有能量，点击左侧栏Home")
        click(x, y)

        print("检查是否有目标")
        hasTarget, x, y = check_has_target()
        if hasTarget == False:
            print("提示：没有目标，结束但不报错")
            return
        print("有目标，点击目标Active")
        click(x, y)

        try:
            print("寻找Pistol")
            index, x, y = locate_till_whichever_exist("pistal.png", "pistol_empty.png", None)
            if index == 0:
                print("找到Pistol，点击Pistol")
                click(x, y)
            elif index == 1:
                alert_sound_screenshot("仅找到空Pistal，但之前步骤已排除无能量和住院入狱")
                raise NoExpectedImageFoundException
        except pyautogui.ImageNotFoundException:
            alert_sound_screenshot("找不到满的或者空的Pistal")
            raise NoExpectedImageFoundException

        try:
            print("寻找Attack")
            find_click("attack.png")
            print("已点击Attack")
        except pyautogui.ImageNotFoundException:
            alert_sound_screenshot("找不到Attack")
            raise NoExpectedImageFoundException

        try:
            print("等待战斗报告")
            locate_till_exist("report.png")
            print("发现战斗报告")
            attackDoneCount += 1
        except pyautogui.ImageNotFoundException:
            alert_sound_screenshot("找不到战斗报告")
            raise NoExpectedImageFoundException
    alert_sound_screenshot("进攻循环次数过多")
    raise NoExpectedImageFoundException


def handle_jobs():
    global failedLoop
    global jobDoneCount
    global isMakeNextLoopSooner

    print("开始Job")

    try:
        print("寻找左侧栏Jobs")
        find_click("menu_jobs.png")
        print("已点击左侧栏Jobs")
    except pyautogui.ImageNotFoundException:
        alert_sound_screenshot("找不到左侧栏Jobs")
        raise NoExpectedImageFoundException

    try:
        print("寻找完成/开始/取消按钮")
        index, x, y = locate_till_whichever_exist("start_0.png", "complete_0.png", "cancel_0.png")
        print("稍等Jobs页面加载")
        sleep_at_least(2, 2)
        index, x, y = locate_till_whichever_exist("start_0.png", "complete_0.png", "cancel_0.png")
        if index == 0:
            print("发现开始按钮，点击")
            click(x, y)
            try:
                print("等待取消按钮")
                locate_till_exist("cancel_0.png")
                print("发现取消按钮，Job进行中，成功")
                jobDoneCount += 1
            except pyautogui.ImageNotFoundException:
                alert_sound_screenshot("开始后找不到取消键")
                raise NoExpectedImageFoundException
        elif index == 1:
            print("发现完成按钮，点击")
            click(x, y)
            try:
                print("稍等后检查状态")
                sleep_at_least(5, 2)
                isHospedOrJailed = check_is_hosped_or_jailed(False)
                if isHospedOrJailed:
                    print("完成后发现住院或入狱，正常结束，提前下次轮询")
                    isMakeNextLoopSooner = True
                    return
            except pyautogui.ImageNotFoundException:
                alert_sound_screenshot("完成后找不到状态")
                raise NoExpectedImageFoundException

            try:
                print("寻找开始按钮")
                find_click("start_0.png")
                print("已点击开始按钮")
            except pyautogui.ImageNotFoundException:
                alert_sound_screenshot("完成后找不到开始按钮")
                raise NoExpectedImageFoundException
            try:
                print("等待取消按钮")
                locate_till_exist("cancel_0.png")
                print("发现取消按钮，Job进行中，成功")
                jobDoneCount += 1
            except pyautogui.ImageNotFoundException:
                alert_sound_screenshot("开始后找不到取消键")
                raise NoExpectedImageFoundException
        elif index == 2:
            print("提示：有正在进行中的Job，结束但不报错")
            return

    except pyautogui.ImageNotFoundException:
        alert_sound_screenshot("找不到Jobs完成/开始/取消按钮")
        raise NoExpectedImageFoundException


def handle_expeditions():
    global nextExpeAt
    global expeDoneCount
    global jobDurationMinute
    global loopMaxDelayMinute
    global expeditionDurationMinute

    if nextExpeAt != 0 and time.time() + jobDurationMinute * 60 + loopMaxDelayMinute * 60 <= nextExpeAt:
        print("远征未到时间")
        return
    print("开始远征")
    nextExpeAt = time.time() + expeditionDurationMinute * 60 + random.randint(-60 * 60, 0)

    try:
        print("寻找左侧栏Expeditions")
        find_click("expe.png")
        print("已点击左侧栏Expeditions")
    except pyautogui.ImageNotFoundException:
        alert_sound_screenshot("找不到左侧栏Expeditions")
        raise NoExpectedImageFoundException

    count = 0
    while count <= 5:
        count += 1
        try:
            print("寻找远征开始按钮")
            index, x, y = locate_till_whichever_exist("no_expe.png", "start_expe.png", None)
            print("稍等远征页面更新")
            sleep_at_least(2, 2)
            index, x, y = locate_till_whichever_exist("no_expe.png", "start_expe.png", None)
            if index == 0:
                print("没有可开始的远征，正常结束")
                return
            elif index == 1:
                print("找到开始远征按钮，点击开始")
                click(x, y)
                expeDoneCount += 1
                print("稍等远征开始后页面更新")
                sleep_at_least(2, 2)
        except pyautogui.ImageNotFoundException:
            alert_sound_screenshot("即找不到开始远征按钮，也找不到左侧栏没有远征")
            raise NoExpectedImageFoundException

    alert_sound_screenshot("远征循环次数过多")
    raise NoExpectedImageFoundException


##### Configs #####
jobDurationMinute = 24
expeditionDurationMinute = 24
ShortenedLoopTimeMinute = 20
loopMaxDelayMinute = 1
##### Configs #####

nextAttackAt = 0
nextExpeAt = 0
isMakeNextLoopSooner = False

startTime = time.time()
totalLoopCount = 0
failedLoop = 0
successiveFailedLoop = 0

attackDoneCount = 0
attackFailedLoopCount = 0
jobDoneCount = 0
jobFailedLoopCount = 0
expeDoneCount = 0
expeFailedLoopCount = 0


pyautogui.moveTo(1000, 50, 0.5, pyautogui.easeInQuad)
while True:
    timestamp = datetime.datetime.now().time()
    start = datetime.time(0)
    end = datetime.time(5)
    if start < timestamp < end:
        print("睡觉时间")
        sleep_at_least(5 * 60 * 60, 1 * 60 * 60)
        continue

    totalLoopCount += 1
    isCurrentLoopHasProblem = False
    isMakeNextLoopSooner = False
    print("----- 轮询开始 ----- " + time.strftime("%H:%M:%S", time.localtime()))

    try:
        isHospedOrJailed = check_is_hosped_or_jailed()
        if isHospedOrJailed:
            print("轮询前发现正在住院或入狱，结束轮询，提前下次轮询")
            failedLoop += 1
            successiveFailedLoop += 1
            google()
            print("【运行：" + str(round((time.time() - startTime)/60/60, 2)) + "小时 轮询：" + str(totalLoopCount) + "(" + str(failedLoop) + ")  进攻：" + str(attackDoneCount) + "(" + str(attackFailedLoopCount) +
                  ")  启动Job: " + str(jobDoneCount) + "(" + str(jobFailedLoopCount) + ")  启动远征：" + str(expeDoneCount) + "(" + str(expeFailedLoopCount) + ")】 当前连续失败轮询：" + str(successiveFailedLoop))
            if successiveFailedLoop > 3:
                alert_sound_screenshot("连续异常轮询次数过多，终止整个程序")
                break
            sleep_at_least(ShortenedLoopTimeMinute * 60, loopMaxDelayMinute * 60)
            continue
    except NoExpectedImageFoundException:
        print("轮询前检查入院/监狱/正常状态失败，结束轮询，提前下次轮询")
        failedLoop += 1
        successiveFailedLoop += 1
        google()
        print("【运行：" + str(round((time.time() - startTime)/60/60, 2)) + "小时 轮询：" + str(totalLoopCount) + "(" + str(failedLoop) + ")  进攻：" + str(attackDoneCount) + "(" + str(attackFailedLoopCount) +
              ")  启动Job: " + str(jobDoneCount) + "(" + str(jobFailedLoopCount) + ")  启动远征：" + str(expeDoneCount) + "(" + str(expeFailedLoopCount) + ")】 当前连续失败轮询：" + str(successiveFailedLoop))
        if successiveFailedLoop > 3:
            alert_sound_screenshot("连续异常轮询次数过多，终止整个程序")
            break
        sleep_at_least(ShortenedLoopTimeMinute * 60, loopMaxDelayMinute * 60)
        continue

    try:
        handle_attacks()
    except NoExpectedImageFoundException:
        isCurrentLoopHasProblem = True
        attackFailedLoopCount += 1

    try:
        handle_expeditions()
    except NoExpectedImageFoundException:
        isCurrentLoopHasProblem = True
        expeFailedLoopCount += 1

    try:
        handle_jobs()
    except NoExpectedImageFoundException:
        isCurrentLoopHasProblem = True
        jobFailedLoopCount += 1

    if isCurrentLoopHasProblem:
        failedLoop += 1
        successiveFailedLoop += 1
        isMakeNextLoopSooner = True
    else:
        successiveFailedLoop = 0

    google()
    print("【运行：" + str(round((time.time() - startTime)/60/60, 2)) + "小时 轮询：" + str(totalLoopCount) + "(" + str(failedLoop) + ")  进攻：" + str(attackDoneCount) + "(" + str(attackFailedLoopCount) +
          ")  启动Job: " + str(jobDoneCount) + "(" + str(jobFailedLoopCount) + ")  启动远征：" + str(expeDoneCount) + "(" + str(expeFailedLoopCount) + ")】 当前连续失败轮询：" + str(successiveFailedLoop))

    if successiveFailedLoop >= 5:
        alert_sound_screenshot("连续异常轮询次数过多，终止整个程序")
        break

    if isMakeNextLoopSooner:
        sleep_at_least(ShortenedLoopTimeMinute * 60, loopMaxDelayMinute * 60)
    else:
        sleep_at_least(jobDurationMinute * 60, loopMaxDelayMinute * 60)
