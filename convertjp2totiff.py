#!/usr/bin/python

#convert files listed in the text file to geotiff from jp2
#upload to appropriate folder on s3

import glob, os 
import subprocess 
import gdal
import osr
import ogr
import shutil
import datetime
import boto
import boto.s3.connection
import math
from filechunkio import FileChunkIO
import logging


def UploadToS3(conn,bucketname,source,target):
    b = conn.get_bucket(bucketname)
    source_size = os.stat(source).st_size
    mp = b.initiate_multipart_upload(target)
    chunk_size = 10485760
    chunk_count = int(math.ceil(source_size / chunk_size))
    for i in range(chunk_count + 1):
        offset = chunk_size * i
        bytes = min(chunk_size, source_size - offset)
        with FileChunkIO(source,'r',offset=offset,bytes=bytes) as fp:
            mp.upload_part_from_file(fp,part_num=i + 1)
    mp.complete_upload()
    
######################## Main ###################
    
gdal.AllRegister()
gdal.UseExceptions()

outputlogfilename = 'd:/temp/aerialjp2awsconversion/run.log'

#outputfilename start time
thisstarttime = str(datetime.datetime.now())
            
logger = logging.getLogger(outputlogfilename)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(outputlogfilename)
log_format = ('%(asctime)s -  %(levelname)s - %(filename)s:%(module)s:%(lineno)d - %(message)s')
formatter = logging.Formatter(log_format)
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)

#boto params
access_key=''
secret_key = ''

from boto.s3.connection import S3Connection
conn = S3Connection(access_key,secret_key)
bucket = conn.get_bucket('prod')
dirnames3root='temp/aerial/'

inputFile=open('d:/temp/aerialjp2.csv','r')

for inputLine in inputFile:
  logger.debug(inputLine)
  #need folder and filename
  jp2file = inputLine[inputLine.rfind('\\')+1:].strip()
  logger.debug(jp2file)
  print(jp2file)
  folderpath=inputLine.replace('\\' + jp2file,'')
  folder = folderpath[folderpath.rfind('\\')+1:].strip()
  logger.debug(folder)
  tiffile = jp2file.upper()
  tiffile = tiffile.replace('.JP2','.tif').strip()
  logger.debug(tiffile)
  
  s3string=dirnames3root + folder + '/'  + tiffile
  if bucket.get_key(s3string) is None:
    #gdaltranslate on image to geotiff
    gdalstring = 'gdal_translate -of GTiff -co compress=lzw ' + inputLine.strip() + ' ' + tiffile
    logger.debug(gdalstring)
    os.system(gdalstring)
    #upload to s3 via filechunk
    logger.debug(s3string)
    UploadToS3(conn, bucket, tiffile, s3string)
    print(s3string)
    logger.debug('copied to s3')
    #cleanup
    os.remove(tiffile)

  handler.flush()
  
  exit()


inputFile.close

print(datetime.datetime.now())
