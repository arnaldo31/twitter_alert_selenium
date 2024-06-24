from playwright.sync_api import sync_playwright
import json
import time
import requests
import os
import html
from datetime import datetime,timedelta
from dotenv import load_dotenv
import pytz

load_dotenv()
telegram_api_key = os.getenv('telegram_api_key')
keyword = os.getenv('keyword')

pastfile = []
save = []
tweet_save = []
stopper = 0
ongoing_requests = set()

def call_tweet(page,url):
    if save == []:
        return False
    page.goto(url)
    trial = 0
    while True:
        if trial == 12:
            break
        Reply_div = page.get_by_text("Reply",exact=True).is_visible()
        if Reply_div == False:
            time.sleep(1)
            trial += 1
            continue
        break
    time.sleep(2)
    
def intercept_response(response):
    global stopper
    url = response.url
    
    if 'https://x.com/i/api/graphql' in url and 'rawQuery' in url and 'SearchTimeline' in url:
        response_str = response.body().decode('utf-8')
        try:
            data = json.loads(response_str)['data']['search_by_raw_query']['search_timeline']['timeline']['instructions'][0]['entries']
        except:
            data = []

        for item in data:
            try:
                result = item['content']['itemContent']['tweet_results']['result']
            except Exception as e:
                continue
            try:
                itemContent = result['legacy']
            except:
                continue
            full_text = itemContent['full_text'].strip()
            print('text:',full_text.replace('\n','').strip())
            #tt.append({'tt':full_text})
            split_full_text = full_text.split(' ')
            if len(split_full_text) > 3:
                continue
            if len(split_full_text) == 2:
                if split_full_text[1].lower() != 'based':
                    continue
            if len(split_full_text) == 3:
                if split_full_text[2].lower() != 'based':
                    continue

            in_reply_to_screen_name = itemContent.get('in_reply_to_screen_name')
            if in_reply_to_screen_name == '' or in_reply_to_screen_name == None:
                continue
            
            post_id = itemContent['in_reply_to_status_id_str']
            post_owner_name = itemContent['in_reply_to_screen_name']
            post_url = f'https://x.com/{post_owner_name}/status/{post_id}'
            dic = {
                'post_id':post_id,
                'post_username':post_owner_name,
                'post_url':post_url
            }
            user = result['core']['user_results']['result']['legacy']
            reply_name = user['screen_name']
            reply_text = full_text
            reply_created = itemContent['created_at']
            dic.update({
                'reply_name': reply_name,
                'reply_text': reply_text,
                'reply_created': reply_created
            })
            try:
                date_format = "%a %b %d %H:%M:%S %z %Y"
                datetime_object = datetime.strptime(reply_created, date_format)
                
                desired_format = "%Y-%m-%d %H:%M"
                date_tweet = datetime_object.strftime(desired_format)
                script_date = past_time_minute.strftime(desired_format)
            except Exception as e:
                print(e)
            
            print(date_tweet,script_date,sep=' | ')
            if past_time_minute > datetime_object:
                stopper = 1
            save.append(dic)

        #pandas.DataFrame(tt).to_excel('tt.xlsx',index=0)
        #input('?')
        
    if 'https://x.com/i/api' in url and 'TweetDetail' in url:
        response_str = response.body().decode('utf-8')
        try:
            data = json.loads(response_str)['data']['threaded_conversation_with_injections_v2']['instructions'][0]['entries']
        except:
            data = []
        
        for item in data:
            try:
                entryId = item['entryId']
                for saveItem in save:
                    id = saveItem['post_id']
                    if id in entryId:
                        content = item['content']['itemContent']['tweet_results']['result']['legacy']
                        created_at = content['created_at']
                        full_text_tweet = content['full_text']
                        likes = content['favorite_count']
                        saveItem['post_created'] = created_at
                        saveItem['post_text'] = full_text_tweet
                        saveItem['post_likes'] = likes
                        try:
                            media = content['entities']['media'][0]
                        except:
                            continue
                        
                        type = media['type']
                        url = None
                        if 'photo' in type:
                            url = media['media_url_https']
                        if 'video' in type or 'animated_gif' in type:
                            url = media['media_url_https']
                            try:
                                variants = media['video_info']['variants']
                                for var in variants:
                                    content_type = var['content_type']
                                    if 'video/mp4' in content_type:
                                        url = var['url']
                            except:
                                url = media['media_url_https']
                        
                        if url != None:
                            id = saveItem['post_id']
                            file = download_media(url,id)
                            if file != None:
                                saveItem['media'] = file
                                print(saveItem['post_id'])
                                keys = ['post_id','post_text','post_username','post_likes','post_url','post_created','reply_name','reply_text','reply_created','media']
                                DIC = {}
                                for k in keys:
                                    DIC[k] = saveItem[k]
                                tweet_save.append(DIC)
            except:
                pass
def download_media(url,id):
    if '.jpg' in url:
        filename = f'.\\media\\{id}.jpg'
        response = requests.get(url)
        with open(filename,mode='wb') as file:
            file.write(response.content)
        return filename
    if '.png' in url:
        filename = f'.\\media\\{id}.png'
        response = requests.get(url)
        with open(filename,mode='wb') as file:
            file.write(response.content)
        return filename
    if '.mp4' in url:
        filename = f'.\\media\\{id}.mp4'
        response = requests.get(url)
        with open(filename,mode='wb') as file:
            file.write(response.content)
        return filename
            
def on_request_finished(request):
    ongoing_requests.discard(request)

def on_request_failed(request):
    ongoing_requests.discard(request)
    
def main():
    global past_time_minute
    
    read_twitter_alert_file()
    current_date = datetime.now(pytz.utc)
    past_time_minute = current_date - timedelta(minutes=20)

    with sync_playwright() as p:
        
        browser = p.chromium.launch_persistent_context(user_data_dir=r'C:\\Users\\art\\AppData\\Local\\Google\\Chrome\\User Data', headless=False,channel='chrome')     
        pages = browser.pages
        page = browser.new_page()
        if pages:
            pages[0].close()
        page.set_viewport_size({'width':1020,'height':820})
        url = 'https://x.com/search?q=%22%22'+keyword+'%22%22%20filter%3Areplies&src=typed_query&f=live'
        page.on("response", intercept_response)
        page.goto(url)
        scroll_height = 500
        sc = 0
        while stopper == 0 and sc < 100:
            # Scroll the page
            page.evaluate(f'window.scrollBy(0, {scroll_height})')
            print("Collecting data after scroll")
            time.sleep(1)
            sc += 1

        tweets = []
        temp = []
        for data in save:
            post_url = data['post_url']
            if post_url not in tweets:
                tweets.append(post_url)
                temp.append(data)
                
        for data_item in temp:
            call_tweet(page,data_item['post_url'])
            
        try:
            page.wait_for_load_state('networkidle',timeout=20000)
        except:
            pass
        
        browser.close()
    
    file_path = ".\\save\\twitter_alerts.txt"
    sorted_tweets = sorted(tweet_save, key=lambda x: (x['post_likes'], 'media' in x), reverse=True)
    final_save = []
    for tweet in sorted_tweets:
        final_save.append(tweet)
    
    send_telegram(savelist=final_save)
    if pastfile != []:
        for pastdata in pastfile:
            final_save.append(pastdata)
            
    with open(file_path, "w",encoding='UTF-8') as text_file:
        text_file.write(json.dumps(final_save, indent=4)) 
        
def send_telegram(savelist:list):
    if len(savelist) > 2:
        savelist = savelist[:2]
    groups = open('telegram_groups_ids.txt',encoding='utf-8').read().split('\n')
    for group in groups:
        group = group.strip()
        for item in savelist:
            media = item['media']
            if '.jpg' in media or '.png' in media:
                send_photo(data=item,group=group)
            if '.mp4' in media:
                send_video(data=item,group=group)
                
def send_photo(data:dict,group:str):
    caption = html.unescape(data['post_text'][:900]) + '\n\n' + data['post_url']
    payload = {"chat_id": group, "caption": caption}
    url = "https://api.telegram.org/bot{}/sendPhoto".format(telegram_api_key)
    filename = data['media']
    image = open(filename,mode='rb')
    res = requests.post(url, data=payload, files={"photo": image})
    if res.status_code == 200:
        print('success message on telegram !')
    else:
        print('Error!')
        print(f'group: {group} not found or the bot is not member')
        
def send_video(data:dict,group:str):
    caption = html.unescape(data['post_text'][:900]) + '\n\n' + data['post_url']
    payload = {"chat_id": group, "caption": caption}
    url = "https://api.telegram.org/bot{}/sendVideo".format(telegram_api_key)
    filename = data['media']
    image = open(filename,mode='rb')
    res = requests.post(url, data=payload, files={"video": image})
    if res.status_code == 200:
        print('success message on telegram !')
    else:
        print('Error!')
        print(f'group: {group} not found or the bot is not member')

def read_twitter_alert_file():
    
    try:
        twitter_alert_file = open('.\\save\\twitter_alerts.txt',encoding='UTF-8').read()
        dataFrame = json.loads(twitter_alert_file)
        for data in dataFrame:
            pastfile.append(data)
    except FileNotFoundError:
        pass
    except Exception:
        pass
    

if __name__ == '__main__':
    try:os.mkdir('media')
    except:pass
    try:os.mkdir('save')
    except:pass
    main()