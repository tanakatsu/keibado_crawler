# encoding: utf-8
import os
import pickle
import urllib2
from time import sleep
from argparse import ArgumentParser


def load_file(filename):
    with open(filename, 'r') as f:
        data = pickle.load(f)
    return data


def download_image(url, filename):
    try:
        img = urllib2.urlopen(url).read()
        with open(filename, 'wb') as f:
            f.write(img)
    except urllib2.HTTPError as e:
        if e.code == 404:
            print 'Not found: ', url
            pass

parser = ArgumentParser()
parser.add_argument('--output', '-o', action='store', type=str, default=None, help='output directory')
args = parser.parse_args()

if os.path.exists('padock_photo_urls.pkl'):
    data = load_file('padock_photo_urls.pkl')
    for d in data:
        params = d['padock_photo_url'].replace('http://', '').split('/')
        output_filename = '%s_%s' % (params[2], params[4])
        if args.output:
            output_filename = os.path.join(args.output, output_filename)
        if not os.path.exists(output_filename):
            print 'Download', d['name'], d['padock_photo_url']
            download_image(d['padock_photo_url'], output_filename)
            sleep(0.1)
