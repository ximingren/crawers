import subprocess
import os
import common_crawer.common_crawer.settings
if __name__ == '__main__':
    output=subprocess.Popen('scrapy crawl ebotapp2',cwd=os.getcwd(),shell=True)
    print(output.wait())
