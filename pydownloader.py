#!/usr/bin/env python

import urllib2
import pickle
import os
import hashlib

BLOCKSIZE = (1024**2)/2 # 512 Kibibytes in 1 packet.

def get_info_dict():

	if os.path.isfile(pdtmd):
		
		f = open(pdtmd, 'r')

		info_dict = pickle.load(f)			

		f.close()

	else:

		info_dict = {}

	return info_dict	

def update_pdtmd(filepath=None, packet_hash=None, downloaded_bytes=None): #Update pydownloader temperory metadata

	global info_dict

	if not info_dict.__len__()==0:

		for _filepath in info_dict.keys():

			if not os.path.isfile(_filepath):

				info_dict.pop(_filepath)

		f = open(pdtmd, 'w')

		pickle.dump(info_dict, f)

		f.close()

	#Updating with the provided key, values

	if (filepath and packet_hash and downloaded_bytes):
		
		info_dict[filepath] = (packet_hash, downloaded_bytes)

		f = open(pdtmd, 'w')
		
		pickle.dump(info_dict, f)

		f.close()

	else:

		return False

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

	global url, BLOCKSIZE, start, end, packet_hash, downloaded_bytes

	packet_hash = hashlib.sha256('')

	while end <= file_size:
		
		packet = downloader() #Download single packet	

		packet_hash.update(packet) #Seeding the hash with BLOCKSIZE size of packet.

		f = open(temp_filename, 'ab')

		f.write(packet) #Appending packet data into a file.

		f.close()
		
		downloaded_bytes = end #When 'end' bytes are downloaded and stored on the disk

		print "\n Downloaded %s KiB" %((downloaded_bytes/1024)+1)

		if end==file_size: #Breaking the loop after complete download, finished download of end BLOCKSIZE bytes.
			break

		start += BLOCKSIZE

		if end + BLOCKSIZE - 1 >= file_size: #Equal to too because in else condition, it will download 1 less than total size i.e. the last byte will be left undownloaded.

			end = file_size

		else:
			end += BLOCKSIZE

	os.rename(temp_filename, filename)


url = raw_input("Download File : ")

metadata = (urllib2.urlopen(url)).info()

file_size = int(metadata.getheaders('Content-Length')[0])

home = os.environ['HOME']

pdtmd = home+'/'+'.pdtmd'

current_dir = os.getcwd()

info_dict = get_info_dict()

filename = get_filename()

filepath = current_dir+'/'+filename

temp_filename = filename+'.pdt' #.pdt = pydownloader temperory.

temp_filepath = current_dir+'/'+temp_filename

update_pdtmd()

try:
	start = info_dict[temp_filepath][1]
	start+=1
	
	end = start+BLOCKSIZE-1
	
except KeyError:

	start = 0

	if BLOCKSIZE - 1 > file_size:

		end = file_size

	else:

		end = BLOCKSIZE - 1

print "\nStarting Download...\n"

try:
	start_download()

except KeyboardInterrupt:
	
	os.system('clear')

	packet_hash = packet_hash.hexdigest()

	update_pdtmd(filepath=temp_filepath, packet_hash=packet_hash, downloaded_bytes=downloaded_bytes)
	
	print "\n File : "+filename+"\n"+" Download Paused!\n"

	exit()
print "Download Complete!\n"
