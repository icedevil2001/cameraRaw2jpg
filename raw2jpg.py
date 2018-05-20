#!/usr/bin/env python
import rawpy
import imageio
#import os, sys 
import logging 
from pathlib import Path
import argparse
import concurrent.futures
#from tqdm import tqdm
from functools import partial
import re
from datetime import timedelta
from time import time 

parser = argparse.ArgumentParser(description='Converts RAW images in the JPG low and high res')
parser.add_argument('--input',
                    '-i',
                    required=True, 
                    help='input dir')
parser.add_argument('--recursive',
                    '-r',
                    action='store_true',
                    required=False,
                    help='search for file recersivly')
parser.add_argument('--output',
                    '-o',
                    required=False,
                    default='thumbnail',
                    help='output path') 

parser.add_argument('--threads',
                    '-t',
                    required=False,
                    default=2,
                    type=int,
                    help='threads default[2]')

parser.add_argument('--quality',
                    '-q',
                    required=False,
                    default=15,
                    type=int,
                    help='JPG quality range from 0-100.  default[15] ')

args = parser.parse_args()
print(args)


## mkdir low and high
output =  Path(args.output)
if not output.exists():
    output.mkdir(parents=True, exist_ok=False)

#for f in ['low', 'high']:
#    (output/f).mkdir(parents=True, exist_ok=True)
logging.basicConfig(filename=str(output/'Raw2jpg.log'),
                     format='[%(asctime)s] %(message)s',
                     level=logging.DEBUG,
                     datefmt='%m/%d/%Y %I:%M:%S %p',
                     filemode='w')
if args.recursive:
    lof = Path(args.input).glob('**/*')
else:
    lof = Path(args.input).glob('*')

lof = [str(x) for x in lof if re.compile('.*(DNG|CR2|ARW|NEF)$',re.DOTALL|re.IGNORECASE).search(str(x))]
logging.info('found {} file'.format(len(lof)))

print ('found %d files' % len(lof))
def process_image(img_file, output=output, quality=args.quality):
    name = Path(img_file).stem
    output = Path(output)
    #low = str(output/'low'/name)
    #high= str(output/'high'/name)
    try:
        with rawpy.imread(img_file) as raw:
            rgb = raw.postprocess()
        
        imageio.imwrite(str(output/name)+'.jpg', rgb, baseline=False, quality=quality, optimize=True)
        #imageio.imwrite(high+'.jpg', rgb, baseline=False, quality=75, optimize=True)
        #imageio.imwrite(low+'.jpg', rgb, baseline=False, quality=25, optimize=True)
        logging.info(F'produced: {img_file}')
        return True
    except:
        logging.info('skipping {img_file}')
        return False
## https://techoverflow.net/2017/05/18/how-to-use-concurrent-futures-map-with-a-tqdm-progress-bar/

fn = partial(process_image, output=output, quality=args.quality)
skipped=0
process = 0
t0 = time()
with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
    for processed in executor.map(fn, lof):
         if processed:
             process +=1
             #print('\rprocessed: {}'.format(process), flush=True)
         else:
             skippped +=1
logging.info('time taken: {}'.format(str(timedelta(seconds=(time()-t0)))))
logging.info(F'Processed files: {process}')
logging.info(F'Skipped files: {skipped}')
print('time taken: {}'.format(str(timedelta(seconds=(time()-t0)))))
print (F'Processed files: {process}\nSkipped files: {skipped}')

