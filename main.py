import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import csv
import os

def myclick(driver,by,ele): #Click on the ele(ment) by ActionChains
    spot=driver.find_element(by=by,value=ele)
    ActionChains(driver).click(spot).perform()

def myenter(driver,by,ele,word): #Put the word in the ele(ment)
    spot=driver.find_element(by=by,value=ele)
    spot.send_keys(Keys.CONTROL,'a') #Select all, making sure it's empty
    spot.send_keys(word)

def generate_mutations_file(mydata):
    data_set = []
    prefix = []
    if not mydata['is_single']:
        prefix = ['M1']
    for m in mydata['mutations']:
        data = prefix + [m[1],m[0]+m[2:-1],m[-1]]
        data_set.append(data)
    # print(data_set)
    with open('temp.tsv','w',encoding='utf-8',newline='') as f:
        writer = csv.writer(f,delimiter='\t')
        writer.writerows(data_set)
    return os.path.abspath('temp.tsv')


def init():
    myoption = [
        '--headless',
        'window-size=1920x1080'
    ]
    # myoption = []
    option = webdriver.ChromeOptions()
    for i in myoption:
        option.add_argument(i)
    # option.add_experimental_option('detach',True) # 程序结束后保留浏览器窗口
    option.add_experimental_option('excludeSwitches',['enable-logging']) # 关闭selenium控制台提示
    driver = webdriver.Chrome(options=option)
    driver.implicitly_wait(20)
    driver.maximize_window() # 最大化
    return driver

def upload(driver,mydata):
    print('\t\t访问初始页面')
    driver.get('https://lilab.jysw.suda.edu.cn/research/mutabind2/research/mutabind2/')
    
    print('\t\t提交蛋白')
    myenter(driver,By.ID,'pdb_id_input',mydata['pdb'])
    if mydata['is_single']:
        myclick(driver,By.ID,'single')
    else:
        myclick(driver,By.ID,'multiple')
    
    print('\t\t设定partner')
    index = 1
    p1 = 0
    p2 = 0
    while True:
        root_xpath = '//*[@id="gallery"]/li[%d]' %(index)
        '//*[@id="gallery"]/li[1]/h5'
        li_tag = driver.find_element(by=By.XPATH,value='%s/h5' %(root_xpath))
        if li_tag.text in mydata['partner1']:
            myclick(driver,By.XPATH,'%s/a[1]' %(root_xpath))
            p1 += 1
            time.sleep(0.5)
        elif li_tag.text in mydata['partner2']:
            myclick(driver,By.XPATH,'%s/a[2]' %(root_xpath))
            p2 += 1
            time.sleep(0.5)
        else:
            index += 1
        
        if p1 >= len(mydata['partner1']) and p2 >= len(mydata['partner2']):
            break
    myclick(driver,By.ID,'submit_partners')
    
    print('\t\t设置mutation')
    file_name = generate_mutations_file(mydata)
    if mydata['is_single']:
        myclick(driver,By.XPATH,'//*[@id="myTab"]/li[2]/a')
        time.sleep(0.5)
        driver.find_element(By.XPATH,'//*[@id="uploadFile"]/div/form/div/div[2]/input').send_keys(file_name)
        myclick(driver,By.ID,'identify_submit_button')
    else:
        myclick(driver,By.ID,'optionsRadios2')
        time.sleep(0.5)
        driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/form/div[1]/div[3]/input').send_keys(file_name)
        myclick(driver,By.ID,'submit_partners')
    return driver.current_url

def single_submit():
    mydata = {
        'pdb': '1A22',
        'partner1': 'A',
        'partner2': 'B',
        'is_single': True,
        'mutations': ['YA164A']
    }
    driver = init()
    url = upload(driver=driver,mydata=mydata)
    print(url)

def batch_submit(folder):
    data_set = []
    driver = init()
    results = []
    with open('%s/input.csv' %(folder),'r',encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        table = list(reader)
        res = table[0] + ['res_url']
        results.append(res)
        with open('%s/results.csv' %(folder),'w',encoding='utf-8-sig',newline='') as g:
            writer = csv.writer(g)
            writer.writerow(res)
        cur = 0
        tot = len(table[1:])
        for row in table[1:]:
            cur += 1
            data = {
                'pdb': row[0],
                'partner1': row[1],
                'partner2': row[2],
                'is_single': len(row[3].split(';')) == 1,
                'mutations': row[3].split(';')
            }
            data_set.append(data)
            print('Processing: %d/%d\n\t%s:%s' %(cur,tot,data['pdb'],str(data['mutations'])))
            try:
                url = upload(driver=driver,mydata=data)
            except:
                url = 'Error'
            print('\turl:%s' %(url))
            res = row + [url]
            results.append(res)

            with open('%s/results.csv' %(folder),'a',encoding='utf-8-sig',newline='') as g:
                writer = csv.writer(g)
                writer.writerow(res)

def main():
    # single_submit()
    batch_submit('多突')

if __name__ == '__main__':
    main()
