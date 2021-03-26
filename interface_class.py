from helper_class import *


class INTERFACING():

    def __init__(self):
        self._MAX_TRIAL_REQUESTS = 10
        self._WAIT_TIME_BETWEEN_REQUESTS = 5

    def check_page_validity(self, html_content):

        valid_page = False
        try:
            if "Sign in for the best experience" in html_content:
                print("++++++++++++Page Source is InValid-Option-1...")
                valid_page = False

            elif "The request could not be satisfied." in html_content:
                print("++++++++++++Page Source is InValid-Option-2...")
                valid_page = False

            elif "Robot Check" in html_content:
                print("++++++++++++Page Source is InValid-Option-3...")
                valid_page = False

            elif len(html_content) < 100:
                print("++++++++++++Page Source is InValid-Option-4...")
                valid_page = False

            else:
                # print()
                # print("------------------Page Source is Valid...")
                # print()
                valid_page = True
        except:
            pass

        return valid_page

    def get_url_response(self, url,premium_proxies):

        print("Getting HTML Response of: ",url)
        scrapeowl_url = "https://api.scrapeowl.com/v1/scrape"
        object_of_data = {
                "api_key": "9XED1IgCiSyUrUCMIBujNYVZ5Mtt9As8MD5Qo4vTxFs8n9IZ2RvGAhaETQeM",
                "url": url,
                "premium_proxies": premium_proxies,
                "country": "es"
                }

        data = json.dumps(object_of_data)

        status_code = 999 
        count = 0
        
        while status_code != 200 and count < self._MAX_TRIAL_REQUESTS:
            try:
                response = requests.post(scrapeowl_url, data)
                status_code = response.status_code
                if status_code == 200:
                    # print(json.dumps(response.json()['credits'],indent=4))
                    html = response.json()['html'].encode('latin-1').decode('utf-8')
                    try: 
                        html[20]
                        return html
                    except Exception as e: 
                        print(e)
                        status_code = 999
            except Exception as e: 
                print(e)
                status_code = 999
                
            print("STATUS CODE:", status_code)
            count += 1
        
        return response.json()['html']

    def get_page_html(self,search_url,premium_proxies):

        trials = 0
        res = None

        print("-"*50)
        print()
        while trials < 2:

            res = self.get_url_response(search_url,premium_proxies)
            if not res:
                return False

            valid_page = self.check_page_validity(res)
            trials += 1

            if valid_page:
                break

            time.sleep(self._WAIT_TIME_BETWEEN_REQUESTS)

        return res

    def make_soup_url(self,page_url,premium_proxies=False):
        html_response = self.get_page_html(page_url,premium_proxies)
        if not html_response:
            return html_response

        return BeautifulSoup(html_response, 'lxml')

if __name__ == "__main__":
    interface = INTERFACING()