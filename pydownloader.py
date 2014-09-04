import urllib2

from os import rename

BLOCKSIZE = (1024**2) + 1 # 1024 Kibibytes in 1 packet.

url = "http://localhost/firefox-29.0.tar.bz2"

metadata = (urllib2.urlopen(url)).info()

file_size = int(metadata.getheaders('Content-Length')[0])

start = 0

if BLOCKSIZE - 1 > file_size:

	end = file_size

else:

	end = BLOCKSIZE - 1

def get_filename():

	temp = url.split('/')

	filename = "/".join(temp[-1:])

	return filename

def downloader(url, start, end):

	req = urllib2.Request(url)

	req.headers['Range'] = 'bytes=%s-%s' % (start, end)

	f = urllib2.urlopen(req)

	complete = f.read()

	return complete

def start_download(url, BLOCKSIZE, start, end):

	while end <= file_size:

		packet = downloader(url, start, end)

		f = open(filename, 'aw')

		f.write(packet)

		f.close()

		if end==file_size: #Breaking the loop after complete download, finished download of end BLOCKSIZE bytes.
			break

		start += BLOCKSIZE

		if end + BLOCKSIZE - 1 >= file_size: #Equal to too because in else condition, it will download 1 less than total size i.e. the last byte will be left.
			end = file_size

		else:
			end += BLOCKSIZE

	rename(filename, ".".join(filename.split('.')[:-1]))

filename = get_filename()+'.pdt'

print "\nStarting Download...\n"

start_download(url, BLOCKSIZE, start, end)

print "Download Complete!\n"