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


crawler = keibado.Keibado()

# Collect issue number urls
if os.path.exists('issue_number_urls.pkl'):
    issue_number_urls = load_file('issue_number_urls.pkl')
    print 'loaded issune_number_urls.'
    print issue_number_urls
else:
    # issue_number_urls = ['http://www.keibado.ne.jp/keibabook/itw/index.html']
    issue_number_urls = []
    backnumber_years = range(2017, 2001, -1)  # 2017-2002
    for year in backnumber_years:
        url = 'http://www.keibado.ne.jp/keibabook/bn/%d.html' % year
        print url
        urls = crawler.getIssueNumberList(url)
        print urls
        issue_number_urls.extend(urls)
        sleep(0.1)
    save_file('issue_number_urls.pkl', issue_number_urls)
    print 'Saved issue_number_urls.pkl'

# Collect horse names and their urls
if os.path.exists('names_and_urls.pkl'):
    names_and_urls = load_file('names_and_urls.pkl')
    print 'loaded names_and_urls.'
    for item in names_and_urls:
        print item['name'], item['url']
else:
    names_and_urls = []

    for url in issue_number_urls:
        results = crawler.getHorseUrlList(url)
        for item in results:
            print item['name'], item['url']
        names_and_urls.extend(results)
        sleep(0.1)
    save_file('names_and_urls.pkl', names_and_urls)
    print 'Saved names_and_urls.pkl'

# Collect horse padock photo urls
if os.path.exists('padock_photo_urls.pkl'):
    print 'padock_photo_urls.pkl is already created.'
else:
    data = []
    resume_data_urls = []
    if os.path.exists('padock_photo_urls.tmp.pkl'):
        resume_data = load_file('padock_photo_urls.tmp.pkl')
        data = resume_data
        resume_data_urls = [x['url'] for x in resume_data]
        print resume_data_urls
    count = len(resume_data_urls)
    for name_url in names_and_urls:
        name = name_url['name']
        url = name_url['url']
        if url not in resume_data_urls:
            padock_url, _name = crawler.getPadockPhotoUrl(url)
            print name, padock_url
            data.append({'name': name, 'url': url, 'padock_photo_url': padock_url})
            count = count + 1
            if count % 100 == 0:
                save_file('padock_photo_urls.tmp.pkl', data)
                print 'Saved temporal file (count=%d, data size=%d)' % (count, len(data))
            sleep(0.1)
    save_file('padock_photo_urls.pkl', data)
    print 'Saved padock_photo_urls.pkl'
print 'done.'
