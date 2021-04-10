#
# Licensed using a creative Commons Attribution-ShareAlike
#
#    https://creativecommons.org/licenses/by-sa/3.0/deed.es
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# Starting point of the solution here scraping is done.
# Coding was created trying to use PIP 8 Style guide for Python (https://www.python.org/dev/peps/pep-0008/)

from interface_class import *
from helper_class import *

# Main class 
class AMAZONCLASS():

    def __init__(self):
        self.interface = INTERFACING()
        self.helper = Helper()
        self.config = self.helper.read_json_file('./config.json')

        self.output_data_folder = self.helper.checking_folder_existence(self.config['output_data_folder'])
        self.output_data_folder = self.helper.checking_folder_existence(self.output_data_folder + self.helper.get_timestamp() + '/')
        self.log_folder = self.helper.checking_folder_existence(self.output_data_folder + 'log/')

        self.current_marketplace = self.config['current_marketplace']
        self.base_url = 'https://www.amazon.' + self.current_marketplace
        self.page_limit = self.config['page_limit']

    def get_info(self,jInfo, key):
        if jInfo is None:
            return ''
        if key in jInfo:
            return jInfo[key]
        else:
            return ''
    
    def get_list_info(self,li, index):
        if index <= len(li)-1:
            return li[index]
        else:
            return ''


    def get_search_results(self,current_url,page_number):
        
        soup = self.interface.make_soup_url(current_url,True)
        if not soup:
            print("No response?")
            return []

        products = soup.find_all(attrs={"data-component-type": "s-search-result"})
        products_list = []
        for product in products:
            products_list.append(product.find("a")['href'].split('/ref')[0])

        try:
            products_list = [[page_number,p] for p in products_list if p != "/gp/slredirect/picassoRedirect.html"]
        except:
            pass

        print("Total Scraped Links: ",len(products_list))

        return products_list

    def get_product_information(self,url):

        count = 1
        vendor_price = ''
        while count < 2:
            soup_product = self.interface.make_soup_url(url,True)

            try:
                vendor_price = soup_product.find('span',id='priceblock_ourprice').text.strip().replace(' ',' ')
                break
            except:
                count += 1

        print("Product Price: ",vendor_price)

        try:
            product_id = url.split('/dp/')[1].split('/')[0]
        except:
            product_id = ''

        try:
            product_title = soup_product.select("#productTitle")[0].text.replace('\n','')
        except:
            product_title = ''

        print('Product Title: ',product_title)

        try:
            product_rating = soup_product.select("#acrPopover")[0].i.text.strip().split()[0].strip()
        except:
            product_rating = ''

        print('Product Rating: ',product_rating)

        try:
            product_rating_count = soup_product.select("#acrCustomerReviewLink")[0].text.strip().split()[0].strip()
        except:
            product_rating_count = ''
        print('Rating Count: ',product_rating_count)

        try:
            product_image = list(json.loads(soup_product.select("#landingImage")[0].attrs['data-a-dynamic-image']).keys())[0]
        except:
            product_image = ''
        print('Product Image: ',product_image)

        try:
            product_brand = soup_product.find('div',id='productOverview_feature_div').find('span',text='Marca').parent.find_next_sibling('td').span.text.strip()
        except:
            product_brand = ''
        print('Product Brand: ',product_brand)

        try:
            product_os = soup_product.find('div',id='productOverview_feature_div').find('span',text='Sistema operativo').parent.find_next_sibling('td').span.text.strip()
        except:
            product_os = ''
        print('Product OS: ',product_os)

        if vendor_price:
            stock_status = 'in stock'
        else:
            stock_status = 'out of stock'

        try:
            screen_size = soup_product.find('div',id='productOverview_feature_div').find('span',text=re.compile('de pantalla')).parent.find_next_sibling('td').span.text.strip()
        except:
            screen_size = ''
        print('Screen Size: ',screen_size)

        try:
            memory_size = soup_product.find('div',id='productOverview_feature_div').find('span',text=re.compile(' memoria')).parent.find_next_sibling('td').span.text.strip()
        except:
            memory_size = ''
        print('Memory Size: ',memory_size)

        try:
            question_answered = soup_product.find('span',text=re.compile('preguntas respondida')).text.strip().split()[0]
        except:
            question_answered = ''

        print('Question Answered: ',question_answered)

        return [product_id,url,product_title,product_brand,product_rating,
                product_rating_count, product_image,stock_status,vendor_price,product_os,screen_size,memory_size,question_answered]


    def start_scraping_products(self):
        
        processed_json_file = self.log_folder + 'processed.json'
        processed_json_data = self.helper.json_exist_data(processed_json_file)

        headers = ['page_number','extracted_urls']

        input_urls_file = self.config['input_urls_file']

        if not self.helper.is_file_exist(input_urls_file):
            print("Input file not exist..")
            return False

        input_urls_data = self.helper.reading_csv(input_urls_file)

        for _url in range(len(input_urls_data)):
            current_url = input_urls_data[_url][0]

            if 'https://www.amazon' not in current_url:
                continue

            current_filename = self.output_data_folder + 'scraped_urls_data.csv'
            
            print(_url + 1," / ",len(input_urls_data))

            if current_url not in processed_json_data:

                page_number = 1
                blank_page_count = 0

                while 1:
                    _current_url = f'{current_url}&page={page_number}'

                    if _current_url  not in processed_json_data:
                        search_results = self.get_search_results(_current_url,page_number)

                        if len(search_results) > 0:
                            blank_page_count = 0
                            self.helper.writing_output_file(search_results,headers,current_filename)
                            
                            processed_json_data.append(_current_url)
                            self.helper.write_json_file(processed_json_data,processed_json_file)
                            
                            page_number += 1
                        else:
                            blank_page_count += 1
                            print("Blank Page: ",blank_page_count)

                        
                        if blank_page_count == 3:
                            print("Got 3 blank pages, so breaking from the loop...")
                            break
                    else:
                        page_number += 1
                        print(_current_url, ' already processed...')


                    if page_number > self.page_limit:
                        print('Reched Limit of 50 Pages...')
                        break

                processed_json_data.append(current_url)
                self.helper.write_json_file(processed_json_data,processed_json_file)

            else:
                print(current_url," already processed...")

            print('*'*50)
            print()

        return True

    def start_scraping_each_product_details(self):

        processed_json_file = self.log_folder + 'products_processed.json'
        processed_json_data = self.helper.json_exist_data(processed_json_file)

        headers = ['product_id','url','product_title','product_brand','product_rating',
                'product_rating_count', 'product_image','stock_status','vendor_price','product_os','screen_size','memory_size','question_answered'] 
        
        all_files = self.helper.list_all_files(self.output_data_folder,'.csv')

        for _file in range(len(all_files)):

            current_filename = all_files[_file]

            if 'product' in current_filename:
                continue

            current_file_data = self.helper.reading_csv(current_filename)

            output_file_name = self.output_data_folder + 'product_complete_data.csv'

            for data in range(1,len(current_file_data)):
                current_url = current_file_data[data][1]

                current_url = self.base_url + current_url

                print(data + 1," / ",len(current_file_data))

                if current_url not in processed_json_data:

                    product_data = self.get_product_information(current_url)

                    self.helper.writing_output_file([product_data],headers,output_file_name)

                    processed_json_data.append(current_url)
                    self.helper.write_json_file(processed_json_data,processed_json_file)

                else:
                    print(current_url, " Already Processed....")

                print('-'*50)
                print()


if __name__ == "__main__":

    handle = AMAZONCLASS()

    print("Scraping Input URLs....")
    handle.start_scraping_products()

    print()
    print("Scraping Each Product's Details...")
    handle.start_scraping_each_product_details()
