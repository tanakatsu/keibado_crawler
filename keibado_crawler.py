# encoding: utf-8
import os
import pickle
from time import sleep
import keibado


def save_file(filename, data):
    with open(filename, 'w') as f:
        pickle.dump(data, f)


def load_file(filename):
    with open(filename, 'r') as f:
        data = pickle.load(f)
    return data


LATEST_YEAR = 2017
FETCH_INTERVAL = 0.1

crawler = keibado.Keibado()

# Collect issue number urls
issue_number_urls = []
if os.path.exists('issue_number_urls.pkl'):
    issue_number_urls = load_file('issue_number_urls.pkl')
    print 'Loaded issune_number_urls. %d urls in list.' % len(issue_number_urls)

if issue_number_urls:
    backnumber_years = range(LATEST_YEAR, LATEST_YEAR - 1, -1)  # LATEST_YEAR only
else:
    backnumber_years = range(LATEST_YEAR, 2001, -1)  # LATEST_YEAR ~ 2002

for year in backnumber_years:
    url = 'http://www.keibado.ne.jp/keibabook/bn/%d.html' % year
    print 'Checking', url
    results = crawler.getIssueNumberList(url)
    for result in results:
        if result not in issue_number_urls:
            print 'Found', result
            issue_number_urls = [result] + issue_number_urls
    sleep(FETCH_INTERVAL)
save_file('issue_number_urls.pkl', issue_number_urls)
print 'Saved issue_number_urls.pkl (%d urls)' % len(issue_number_urls)

# Collect horse names and their urls
names_and_urls = []
if os.path.exists('names_and_urls.pkl'):
    names_and_urls = load_file('names_and_urls.pkl')
    print 'Loaded names_and_urls. %d names in list' % len(names_and_urls)

bn_list = [x['url'].replace('http://', '').split('/')[2] for x in names_and_urls]

for url in issue_number_urls:
    bn = url.replace('http://', '').split('/')[2]  # example: 170109
    if bn not in bn_list:
        results = crawler.getHorseUrlList(url)
        for item in results:
            print 'Found', item['name'], item['url']
        names_and_urls = results + names_and_urls
        sleep(FETCH_INTERVAL)
save_file('names_and_urls.pkl', names_and_urls)
print 'Saved names_and_urls.pkl (%d names)' % len(names_and_urls)

# Collect horse padock photo urls
data = []
resume_data_urls = []
if os.path.exists('padock_photo_urls.pkl'):
    data = load_file('padock_photo_urls.pkl')
    resume_data_urls = [x['url'] for x in data]
    print 'Loaded padock_photo_urls.pkl. %d samples in list' % len(data)
elif os.path.exists('padock_photo_urls.tmp.pkl'):
    data = load_file('padock_photo_urls.tmp.pkl')
    resume_data_urls = [x['url'] for x in data]
    print 'Loaded padock_photo_urls.tmp.pkl. %d samples in list' % len(data)
count = len(resume_data_urls)
for name_url in names_and_urls:
    name = name_url['name']
    url = name_url['url']
    if url not in resume_data_urls:
        padock_url, _name = crawler.getPadockPhotoUrl(url)
        print 'Found', name, padock_url
        data.append({'name': name, 'url': url, 'padock_photo_url': padock_url})
        count = count + 1
        if count % 100 == 0:
            save_file('padock_photo_urls.tmp.pkl', data)
            print 'Saved temporal file (count=%d)' % count
        sleep(FETCH_INTERVAL)
save_file('padock_photo_urls.pkl', data)
print 'Saved padock_photo_urls.pkl (%d samples)' % len(data)
print 'done.'
