import requests
import re


def upload(mydata):
    s = requests.session()

    # 0. 打开第一页面

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,en-GB;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Referer': 'https://www.google.com/',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.35',
        'sec-ch-ua': '"Microsoft Edge";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    response = s.get('https://lilab.jysw.suda.edu.cn/research/mutabind2/', headers=headers)
    cookies = response.cookies.get_dict()
    print(cookies) # {'csrftoken': 'M1yYBP6EwCcYnucFugZheZqlmFB9uTTZ'}

    # 1.1. 上传pdb upload_pdb

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,en-GB;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryAbBNSZsMutrEuvss',
        'DNT': '1',
        'Origin': 'https://lilab.jysw.suda.edu.cn',
        'Referer': 'https://lilab.jysw.suda.edu.cn/research/mutabind2/research/mutabind2/',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.35',
        'sec-ch-ua': '"Microsoft Edge";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    data = '''\
------WebKitFormBoundaryAbBNSZsMutrEuvss
Content-Disposition: form-data; name="csrfmiddlewaretoken"

%s
------WebKitFormBoundaryAbBNSZsMutrEuvss
Content-Disposition: form-data; name="example"

0
------WebKitFormBoundaryAbBNSZsMutrEuvss
Content-Disposition: form-data; name="pdb_container_asu"


------WebKitFormBoundaryAbBNSZsMutrEuvss
Content-Disposition: form-data; name="pdb_container_bio"


------WebKitFormBoundaryAbBNSZsMutrEuvss
Content-Disposition: form-data; name="isNMR"

0
------WebKitFormBoundaryAbBNSZsMutrEuvss
Content-Disposition: form-data; name="pdb_id"

%s
------WebKitFormBoundaryAbBNSZsMutrEuvss
Content-Disposition: form-data; name="pdb_mol"

bio
------WebKitFormBoundaryAbBNSZsMutrEuvss
Content-Disposition: form-data; name="bioassembly"

1
------WebKitFormBoundaryAbBNSZsMutrEuvss
Content-Disposition: form-data; name="pdb_file"; filename=""
Content-Type: application/octet-stream


------WebKitFormBoundaryAbBNSZsMutrEuvss
Content-Disposition: form-data; name="type"

0
------WebKitFormBoundaryAbBNSZsMutrEuvss--
''' %(cookies['csrftoken'], mydata['pdb'])

    print(data)
    response = s.post('https://lilab.jysw.suda.edu.cn/research/mutabind2/upload_pdb', cookies=cookies, headers=headers, data=data)
    location_url = response.headers['Location']
    print(location_url)
    job_id = re.search('mutabind2/(.*)/set_partners', location_url).group(1)
    print(job_id)
    raise
    
    # 1.2. 转到set partners

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,en-GB;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Referer': 'https://lilab.jysw.suda.edu.cn/research/mutabind2/research/mutabind2/',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.35',
        'sec-ch-ua': '"Microsoft Edge";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    response = s.get(location_url, cookies=cookies, headers=headers)
    
    # 2.1. save_partners

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,en-GB;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Origin': 'https://lilab.jysw.suda.edu.cn',
        'Referer': location_url,
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.35',
        'sec-ch-ua': '"Microsoft Edge";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    data = {}
    data['csrfmiddlewaretoken'] = cookies['csrftoken']
    chain = 0
    for i in mydata['partner1']:
        chain += 1
        data['chains.%d' %(chain)] = '%s_1.P1' %(i)
    for i in mydata['partner2']:
        chain += 1
        data['chains.%d' %(chain)] = '%s_1.P2' %(i)
    
    response = s.post('https://lilab.jysw.suda.edu.cn/research/mutabind2/2022110907313542420157215/save_partners', cookies=cookies, headers=headers, data=data)

    # 2.2. set_mutations

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,en-GB;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Referer': 'https://lilab.jysw.suda.edu.cn/research/mutabind2/2022110907313542420157215/set_partners',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.35',
        'sec-ch-ua': '"Microsoft Edge";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    response = requests.get('https://lilab.jysw.suda.edu.cn/research/mutabind2/2022110907313542420157215/set_mutations', cookies=cookies, headers=headers)


def main():
    mydata = {
        'pdb': '1A22',
        'partner1': 'A',
        'partner2': 'B',
        'is_single': True,
        'mutations': ['YA164A']
    }
    upload(mydata=mydata)

if __name__ == '__main__':
    main()
