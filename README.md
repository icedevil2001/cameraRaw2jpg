# cameraRaw2jpg
Convert raw to jpg

## installation 
```
conda env create -f  environment.yml
```
## how to excute
```
source activate raw2jpg


python raw2jpg.py -h
usage: raw2jpg.py [-h] --input INPUT [--recursive] [--output OUTPUT]
                  [--threads THREADS] [--quality QUALITY]

Converts RAW images in the JPG low and high res

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT, -i INPUT
                        input dir
  --recursive, -r       search for file recersivly
  --output OUTPUT, -o OUTPUT
                        output path
  --threads THREADS, -t THREADS
                        threads default[2]
  --quality QUALITY, -q QUALITY
                        JPG quality range from 0-100. default[15]
```
