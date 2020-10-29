# get cookies from chrome
from scraper.Browser import Browser
from scraper.File import File
from time import sleep, time

from selenium.common.exceptions import NoSuchElementException

import json
import psutil


def selectElm(B, selector, many=False, parent=None):
    print('select elm triggered')
    p = B.driver
    if parent:
        p = parent

    s = p.find_element_by_css_selector
    if many:
        s = p.find_elements_by_css_selector

    try:
        print('try select', selector)
        return s(selector)
    except NoSuchElementException:
        print(f'{selector} -- elm not found')
        return ''
    except Exception as e:
        print('not recognized error: ', e)
        return ''


def sleepUntil(B, selector=None, dynamicBreaker=lambda: True, interval=.7, maxIteration=30, msg=""):
    print('\n\n### SLEEP START ###\n\n')
    start = time()

    if selector:
        def dynamicBreaker(): return bool(selectElm(B, selector))

    iterationNum = 0
    while not dynamicBreaker():
        print(f'\n{iterationNum}- SLEEP UNTIL: {msg}')

        if iterationNum >= maxIteration:
            print('reach max iteration')
            break

        sleep(interval)

        iterationNum += 1

    print(f'\n\n### SLEEP END in {time() - start} ###\n\n')

def read(fileName):
    data = ''
    with open(fileName) as f:
        data = f.read()

    return data

def authenticateTeachable():
    # return browser with homebage of logined teachable
    cookies = File.read('cookies.txt', toJson=True)
    print(cookies)

    # open teachable with selenium
    url = 'https://teachable.com/'
    B = Browser(hide=False)
    B.get(url)
    # set cookies to selenium firefox brrowser
    B.set_cookies(cookies)

    print("cookies has been set")
    sleep(5)

    url = 'https://sso.teachable.com/secure/teachable_accounts/profile/'
    B.get(url)
    sleep(3)

    return B


def getSchool(B):
    url = 'https://sso.teachable.com/secure/teachable_accounts/school_redirect/sk_7t737sj8'
    B.get(url)
    # B.click_btn('a[href$="sk_7t737sj8"]')
    # sleepUntil(B, '.tch-school-onboarding-header-text')
    sleepUntil(B, '.admin-sidebar .school-link a.school-link-name')


def goToCreateNewCourses(B):
    B.get('https://www.thegoodzone.org/admin/courses/new')
    sleepUntil(B, 'input#course-name')


def repeaAction(B, action, times, interval=None, dynamicInterval=lambda: sleep(2)):
    for i in range(times):
        action()

        if interval:
            sleep(interval)
        else:
            dynamicInterval()


# make sure page two is loaded
def fillPageOneOfCreateNewCourse(B, courseInfo):
    name = courseInfo.get('name')
    subtitle = courseInfo.get('subtitle')

    B.fill_input('form input#course-name', name)
    B.fill_input('form input#course-heading', subtitle)

    js = '''document.querySelector('form select option[value="number:671877"]').setAttribute("selected", true)'''
    B.exec_js(js)
    sleep(2)

    # click submit
    B.click_btn('button[type="submit"]')
    # make sure iam in page 2
    sleepUntil(
        B, selector='tch-button[what="new section btn"]', msg='page 2 load')


# page 2
# create tree
def addNewLecture(B, sectionNum):
    sleepUntil(B, '.section-item a')

    print('add new lecture in section number ', sectionNum)
    lecturesCount = len(selectElm(B, '.lecture-item', many=True))
    print('current count: ', lecturesCount)

    btns = selectElm(B, '.section-item a', many=True)
    btn = btns[sectionNum]

    B.click_btn(btn=btn)

    # sleep until num of lectures elms increased
    sleepUntil(B, dynamicBreaker=lambda: len(
        selectElm(B, '.lecture-item', many=True)) > lecturesCount, msg='wait lectures increased')
    print('lectures become', len(selectElm(B, '.lecture-item', many=True)))


def editLectureName(B, indexes, lectureName):
    print('edit lecture: ', indexes)

    sectionIndex, lectureIndex = indexes

    sleepUntil(B, '.section-item')
    section = selectElm(B, '.section-item', many=True)[sectionIndex]

    sleepUntil(B, dynamicBreaker=lambda: len(
        selectElm(B, '.lecture-item', many=True, parent=section)) > lectureIndex)

    lectures = selectElm(B, '.lecture-item', many=True, parent=section)
    lecture = lectures[lectureIndex]
    btn = selectElm(B, 'button[what="edit lecture name"]', parent=lecture)
    # click btn
    B.click_btn(btn=btn)

    # wait until input appear
    sleepUntil(B, dynamicBreaker=lambda: bool(selectElm(
        B, 'form button[type="submit"]', parent=lecture)), msg='wait input area')
    # fill inout
    lectureNameInput = selectElm(B, 'form input', parent=lecture)
    lectureNameInput.clear()
    lectureNameInput.send_keys(lectureName)

    sleep(1)
    # save
    lectureSaveBtn = selectElm(B, 'form button[type="submit"]', parent=lecture)
    B.click_btn(btn=lectureSaveBtn)

    # wait until there is no btns appear
    sleepUntil(B, dynamicBreaker=lambda: not selectElm(
        B, 'form button[type="submit"]', parent=lecture), msg='wait btns to disappear.')
    print('btn disappeared.')


def addNewSection(B, sectionName):
    # click create new section btn
    B.click_btn('tch-button[what="new section btn"]')
    # wait until input appear
    sleepUntil(B, 'div[form="newSectionForm"]')
    # fill the input
    B.fill_input('input[what="name"]', sectionName)
    # save
    B.click_btn('button[type="submit"]')
    # wait until return me to the edit course page
    sleepUntil(B, 'tch-button[what="new section btn"]')


def editSectionName(B, sectionIndex, sectionName):
    section = selectElm(B, '.section-item .section-heading',
                        many=True)[sectionIndex]
    # get btn
    btn = selectElm(B, 'button[what="edit section name"]', parent=section)
    # click btn
    B.click_btn(btn=btn)

    sleepUntil(B, dynamicBreaker=lambda: selectElm(
        B, '.editable-buttons', parent=section), msg="wait until input appear")
    # fill input
    sectionNameInput = selectElm(B, 'input', parent=section)
    sectionNameInput.clear()
    sectionNameInput.send_keys(sectionName)

    sleep(1)
    # save
    lectureSaveBtn = selectElm(B, 'form button[type="submit"]', parent=section)
    # lectureSaveBtn.click()
    B.click_btn(btn=lectureSaveBtn)

    # wait until there is no btns appear
    sleepUntil(B, dynamicBreaker=lambda: not selectElm(
        B, 'form button[type="submit"]', parent=section))


def deleteFirstSection(B):
    sectionsCount = len(selectElm(B, '.section-item', many=True))

    B.click_btn('input[ng-change="selectLectureSection(lectureSection)"]')
    sleepUntil(B, 'button[what="delete-bulk"]')
    B.click_btn('button[what="delete-bulk"')
    sleepUntil(B, 'tch-button[what="ok button"]')
    B.click_btn('tch-button[what="ok button"]')
    # sleep(5)
    # # sleep until section count less by one from old

    # sleep until num of sections elms decreased
    sleepUntil(B, dynamicBreaker=lambda: len(
        selectElm(B, '.section-item', many=True)) < sectionsCount)

# go throw lectures, set its content


def openLectureEditor(B, indexes):
    print('openLectureEditor()')
    sectionIndex, lectureIndex = indexes
    section = selectElm(B, '.section-item', many=True)[sectionIndex]

    # lecture = selectElm(B, '.lecture-item', many=True,
    #                     parent=section)[lectureIndex]
    lectures = selectElm(B, '.lecture-item', many=True, parent=section)
    lecture = lectures[lectureIndex]

    lectureId = lecture.get_attribute('id').split('_')[-1]
    lecture_url = B.get_url().strip('/') + f'/lectures/{lectureId}'

    print('lectureURL: ', lecture_url)
    B.get(lecture_url)
    print('got lecture: ', lecture_url)
    sleepUntil(B, '.lecture__block-editor tabs', msg='waiting aside tabs')


def fillLectureEditor(B, content):
    # add text
    print('goto text tab')
    B.click_btn('li[heading="Add Text"]')
    sleepUntil(B, '.bootstrap-switch-container', msg='wait toggle button')

    # toggle old version of box editor
    if not selectElm(B, 'a[aria-label="HTML"]'):
        # B.click_btn('.bootstrap-switch-on input')
        # 'span.bootstrap-switch-label'
        print('start clicking toggle')
        B.exec_js("document.querySelector('.bootstrap-switch-on input').click()")
        print('end clicking toggle')

        sleepUntil(B, 'a[aria-label="HTML"]', msg='wait to classic richbox')

    # get html edit
    B.click_btn('a[aria-label="HTML"]')
    # fill with content
    B.fill_input('textarea[what="text form"]', content)
    # save text
    B.click_btn('button[what="save text button"]')
    # wait until tabs
    # sleepUntil(B,  '.lecture__block-editor-container--closed')
    sleepUntil(B, '.growl .growl-item', interval=.3, msg="sleep to growl msg")
    if selectElm(B, '.growl-item.alert-error'):
        print('there is an error, will tyy to set this lecture again.')
        fillLectureEditor(B, content)


def setLecture(B, indexes, content):
    print('start open lecture editor: ', indexes)
    openLectureEditor(B, indexes)
    print('start fill lecture: ', indexes)
    fillLectureEditor(B, content)
    # go to curriculum home
    print('goto curriculum home.')
    B.click_btn(
        'a[tooltip="Create and publish at least one lecture to complete this step"]')

    # sleep until back to curriculum home
    sleepUntil(
        B, selector='tch-button[what="new section btn"]', msg="wait to page 1 loaded.")


def checkRAM():
    if psutil.virtual_memory().percent > 88:
        exit()


B = authenticateTeachable()
getSchool(B)



coursesIds = ["978686", "1024147", "1024154", "1024190", "1024196", "1027072", "1087672", "1130521", "1132920", "1133173", "1133332", "1133582", "1133864", "1134020", "1134119", "1134255", "1134408", "1134807", "1135100", "1135211", "1136269", "1136555", "1136645", "1136825", "1137365", "1137478", "1137770", "1137890", "1138174", "1138788", "1138909", "1139493", "1139917", "1168796", "1168905", "1169269", "1169718", "1169790", "1169865", "1169886", "1169913", "1169930", "1169990", "1170002", "1170567", "1171028", "1171110", "1171424", "1171476", "1177107", "1177119", "1177183", "1177351", "1177587", "1178166", "1178226", "1178290", "1178394", "1178459", "1179316", "1179383", "1179440", "1180073", "1180356", "1180407", "1180444", "1180550"]
def getCourseURL(courseId):
    url = f'https://www.thegoodzone.org/admin/courses/{courseId}/pages'
    print(url)
    return url

def openCourse(B, courseId):
    url = getCourseURL(courseId)
    B.get(url)

    sleepUntil(B, 'table[class*="CoursePages_table"]')

def getCourseEditURLs(B):
    print('get edit urls')
    elms = selectElm(B, 'a[href$="edit"]', many=True)
    return [elm.get_attribute('href') for elm in elms]

def checkCourseEditorBlocksSet(B, expected):
    print('check expected blocks')
    print(expected)
    blocksNames = selectElm(B, 'div.BlockList ul li [title="go to block"]', many=True)
    names = [block.text.strip() for block in blocksNames]

    return names == expected


def removeCourseEditorBlocks(B):
    print('not match expected blocks, delete all blocks')
    blocksBtns = selectElm(B, 'div.BlockList ul li button[data-test="menu-dropdown-button"]', many=True)

    print(blocksBtns)
    blocksBtnsLength = len(blocksBtns)
    while blocksBtns:
        blockBtn = blocksBtns[0]

        print(f'there is {blocksBtnsLength} block remain')
        B.click_btn(btn=blockBtn)
        sleep(.5)
        B.click_btn('#Delete')
        sleep(.5)

        B.click_btn('button[data-test="confirm-dialog-btn"]')
        # funcWrapper = lambda func: blocksBtnsLength < len(func())
        # sleepUntil(B, dynamicBreaker=lambda: funcWrapper(getBlockBtns))
        sleep(1.3)

        blocksBtns = selectElm(B, 'div.BlockList ul li button[data-test="menu-dropdown-button"]', many=True)

        blocksBtnsLength -= 1


def addCourseEditorBlock(B, blockName, data=None):
    print(f'add block {blockName}')
    # click on add new block btn
    B.click_btn('button[data-test="add-block"]')
    # get all blocks
    blocks = selectElm(B, 'aside section ul li', many=True)
    # filter on block name
    block = list(filter(lambda b: b.text.strip() == blockName, blocks))[0]
    # click on block
    B.click_btn(btn=block)
    # sleep
    sleep(.5)
    # click on add
    addBtn = selectElm(B, 'button', parent=block)
    B.click_btn(btn=addBtn)
    # sleep until
    # sleepUntil(B, dynamicBreaker=lambda: len(list(filter(lambda item: item.text == 'Delete Block', selectElm(B, 'aside button', many=True)))) >= 1)
    sleep(2)
    # set data it exist
    if data:
        # set data
        B.exec_js(f'''
            textarea = document.querySelector('form textarea')
            textarea.value = `{data}`
            event = new Event('input');
            textarea.dispatchEvent(event);
        ''')

    sleep(1)
    # back
    B.click_btn('button[data-test="back-button"]')
    # sleep
    sleep(1)



def handleCourseSalesPage(B, salesPage):
    print(salesPage)
    B.get(salesPage)
    sleepUntil(B, 'div.BlockList')

    expected = [ "Custom HTML", "Course Curriculum", "Custom HTML", "Pricing", "Custom HTML" ]
    if checkCourseEditorBlocksSet(B, expected):
        return
    
    blockFiles = ["intro.html", '', 'instructor.html', '', 'feedback.html']
    # remove all blocks
    removeCourseEditorBlocks(B)
    # add blocks in order
    # add blocks data
    dataFolder = './pages/sales/'
    for block, dataFileName in zip(expected, blockFiles):
        data = None
        if block == "Custom HTML":
            data = File.read(dataFolder + dataFileName)

        addCourseEditorBlock(B, block, data)
    # click update
    B.click_btn('button[data-test="button-publish"]')
    sleepUntil(B, '.growl .growl-item')

def handleCourseThanksPage(B, thanksPage):
    print(thanksPage)
    B.get(thanksPage)
    sleepUntil(B, 'div.BlockList')

    expected = [ "Custom HTML" ]
    if checkCourseEditorBlocksSet(B, expected):
        return

    blockFiles = ['main.html']
    # remove all blocks
    removeCourseEditorBlocks(B)
    # add blocks in order
    # add blocks data
    dataFolder = './pages/thanks/'
    for block, dataFileName in zip(expected, blockFiles):
        data = None
        if block == "Custom HTML":
            data = File.read(dataFolder + dataFileName)

        addCourseEditorBlock(B, block, data)
    # click update
    B.click_btn('button[data-test="button-publish"]')
    sleepUntil(B, '.growl .growl-item')


styledLog = File.read('./styled.json', toJson=True)


for courseId in coursesIds:
    print(f'course {courseId} start')
    courseLog = styledLog.get(courseId, {})
    if courseLog.get('done'):
        continue

    openCourse(B, courseId)
    salesPage, thanksPage = getCourseEditURLs(B)

    if courseLog.get('sales', None) == None:
        handleCourseSalesPage(B, salesPage)
        # log
        courseLog['sales'] = True
        styledLog.update({courseId: courseLog})
        File.write(styledLog, './styled.json')

    if courseLog.get('thanks', None) == None:
        handleCourseThanksPage(B, thanksPage)
        # log
        courseLog['thanks'] = True
        styledLog.update({courseId: courseLog})
        File.write(styledLog, './styled.json')

    # log
    courseLog['done'] = True
    styledLog.update({courseId: courseLog})
    File.write(styledLog, './styled.json')


