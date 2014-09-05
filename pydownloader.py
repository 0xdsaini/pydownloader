#!/usr/bin/env python

import urllib2

import pickle

import os

BLOCKSIZE = (1024**2) # 1024 Kibibytes in 1 packet.

url = raw_input("Download File : ")

metadata = (urllib2.urlopen(url)).info()

file_size = int(metadata.getheaders('Content-Length')[0])

try:
	start = pickle.load(open('downloaded_meta.pdmd', 'r'))
	start+=1
	
	end = start+BLOCKSIZE-1

	os.remove('downloaded_meta.pdmd')

except IOError:

	start = 0

	if BLOCKSIZE - 1 > file_size:

		end = file_size

	else:

		end = BLOCKSIZE - 1

def get_filename():

	temp = url.split('/')

	filename = "/".join(temp[-1:])

	return filename

def downloader():

	req = urllib2.Request(url)

	req.headers['Range'] = 'bytes=%s-%s' % (start, end)

	f = urllib2.urlopen(req)

	complete = f.read()

	return complete

def start_download():

	global url, BLOCKSIZE, start, end

	while end <= file_size:

		packet = downloader()

		f = open(filename, 'ab')

		f.write(packet)

		f.close()

		if end==file_size: #Breaking the loop after complete download, finished download of end BLOCKSIZE bytes.
			break

		start += BLOCKSIZE

		if end + BLOCKSIZE - 1 >= file_size: #Equal to too because in else condition, it will download 1 less than total size i.e. the last byte will be left.
			end = file_size

		else:
			end += BLOCKSIZE

	os.rename(filename, ".".join(filename.split('.')[:-1]))

filename = get_filename()+'.pdt' #.pdt = pydownloader temperory.

print "\nStarting Download...\n"

try:
	start_download()

except KeyboardInterrupt:

	pickle.dump(end, open('downloaded_meta.pdmd', 'w')) #.pdmd = pydownloader meta data file.

print "Download Complete!\n"
