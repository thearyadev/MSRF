ECHO OFF
ECHO deleting dist directory
del dist
flet pack main.py --name msrf --product-name "Microsoft Rewards Farmer" --product-version 0.9 --file-description "Microsoft Rewards Farmer" --icon "assets/msrf.ico"
mkdir dist/bin
xcopy bin "dist/bin" /e
xcopy configuration.yaml dist
ECHO build complete