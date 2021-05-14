import os
import requests as req
def download():
    hardhatLoc = 'http://www.image-net.org/api/text/imagenet.synset.geturls?wnid=n03492922'

    hardhatImages = req.get(hardhatLoc).text
    noOfImages = 0

    if not os.path.exists('hardhat'):
        os.makedirs('hardhat')

    for i in hardhatImages.split('\n'):
        try:
            r = req.get(i, timeout=0.5)
            file = i.split("/")[-1].split('\r')[0]
            if 'image/jpeg' in r.headers['Content-Type']:
                if len(r.content) > 8192:
                    with open('hardhat\\' + file, 'wb') as outfile:
                        outfile.write(r.content)
                        noOfImages += 1
                        print('Success: ' + file)
                else:
                    print('Failed: ' + file + ' -- Image too small')
            else:
                print('Failed: ' + file + ' -- Not an image')

        except Exception as e:
            print('Failed: ' + file + ' -- Error')

    print('*********** Download Finished **************')
