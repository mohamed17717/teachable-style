from scraper.File import File
import re
from pprint import pprint

coursesIds = ["893769", "893768", "893767", "893766", "893765", "893764", "893763", "893762", "893761", "893760", "893759", "893758", "893757", "893756", "893755", "893753", "893752", "893751", "893750", "893749", "893748", "893747", "893746", "893745", "893744", "893743", "893742", "893741", "893740", "893739", "893738", "893737", "893736", "893735", "893734", "893733", "893732", "893731", "893730", "893729", "893728", "893727", "893726", "893725", "893724", "893723", "893722", "893721", "893720", "893719", "893718", "893717", "893716", "893715", "893714", "893713", "893712", "882201", "882197"]

for courseId in coursesIds:
  course = File.read(f'./tz-combine/{courseId}.json', toJson=True)

  for i, section in enumerate(course['curriculum']):
    for j, lecture in enumerate(section['lectures']):
      content = lecture['content']
      content = re.sub(r'[\n\t]', '', content)
      content = re.sub(
        r'^<div id="header">.*?</div>',
        '',
        content)

  #     print(course['curriculum'][i]['lectures'][j]['content'], '\n')
      course['curriculum'][i]['lectures'][j]['content'] = content
  #     print(course['curriculum'][i]['lectures'][j]['content'])
  #     print('\n\n')

  # break

  print(courseId)
  File.write(course, f'./tz-cleaned/{courseId}.json')