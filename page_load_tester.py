import requests
import time
from datetime import datetime
import argparse
from selenium import webdriver
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def load_page(page_url, remote_server, max_load_seconds, proxy_url, loopnum):

    load_timeout = 10
    is_ok = True

    desired_capabilities = webdriver.DesiredCapabilities.CHROME.copy()
    if proxy_url != "NOPROXY":
        desired_capabilities['proxy'] = {
            'httpProxy': proxy_url,
            'sslProxy': proxy_url,
            'ftpProxy': proxy_url,
            'noProxy': None,
            'proxyType': 'MANUAL',
            'class': 'org.openqa.selenium.Proxy',
            'autodetect': True
        }

    count = 1
    while count <= loopnum:

        # Create fresh Chrome Driver instance
        driver = webdriver.Remote(command_executor=remote_server, desired_capabilities=desired_capabilities)
        driver.set_page_load_timeout(load_timeout)

        # Cache Cleanup
        driver.delete_all_cookies()

        # Start Test
        start_clock = time.clock()
        page = driver.get(page_url)
        end_clock = time.clock()
        elapsed_time = ((end_clock - start_clock))

        # print raw time to stdout
        print str(elapsed_time) + ' || ' + str(datetime.now())

        # Send data to InfluxDB database 'mydb'
        # payload = 'LoadTime,site=youtube.com timeToLoad=' + str(elapsed_time)
        # r = requests.post('http://127.0.0.1:8086/write?db=mydb', data=payload)
        # print r

        '''
        -----------------------------------------------
        SAVE FOR LATER
        -----------------------------------------------
        all_warnings = driver.get_log('browser')
        critical_errors = []

        for warning in all_warnings:
            if warning['level'] == 'SEVERE':
                critical_errors.append(warning)

        if len(critical_errors) != 0:
            print 'ERROR: Severe errors have happened when loading the page. Details:\n\t%s' \
                  % '\n\t'.join([str(error) for error in critical_errors])

        # driver.get_screenshot_as_file('test.png')
        -----------------------------------------------
        '''

        # Increment counter, clear current WebDriver session, and continue
        count += 1
        driver.quit()
        time.sleep(2)

# -----------------------------------------------------------------------------------------------

if __name__ == '__main__':
    print "\n"
    parser = argparse.ArgumentParser()
    parser.add_argument('--page_url', required=True, help="URL for the web page to test", type=str)
    parser.add_argument('--loop', required=False, default=1, help="Number of times to perform the test", type=int)
    parser.add_argument('--proxy_url', required=False, default="NOPROXY", help="URL for HTTP(S) PROXY to use", type=str)
    parser.add_argument('--remote_server', required=False, default="http://127.0.0.1:4444/wd/hub",
                        help="Remote selenium server to run the test", type=str)
    parser.add_argument('--max_load_seconds', required=False, default=30,
                        help="If page load takes too long, quit the test", type=int)

    args = parser.parse_args()
    page_url = args.page_url
    proxy_url = args.proxy_url
    remote_server = args.remote_server
    max_load_seconds = args.max_load_seconds
    loopnum = args.loop

    load_page(page_url, remote_server, max_load_seconds, proxy_url, loopnum)
    print "\n"
