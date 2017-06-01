#!/usr/bin/python
# -*- coding: utf-8 
from googleplaces import GooglePlaces, types, lang
from transitions.extensions import GraphMachine
import xml.dom.minidom
import sys
import urllib.request
from urllib.parse import urlparse
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import random
import codecs
import json

class Near:
    YOUR_API_KEY = 'AIzaSyDomABgA1RgXQaE31JakIQi9Cw66nhHGAc'

    google_places = GooglePlaces(YOUR_API_KEY)

    def get_near_park(self,locationlat,locationlng):
        # You may prefer to use the text_search API, instead.
        lat=str(locationlat)
        lng=str(locationlng)
        arr_to_return=[]
        query_result = self.google_places.nearby_search(
                lat_lng={'lat': locationlat, 'lng': locationlng},keyword='park',
                radius=2000, types=[types.TYPE_PARK])

        if query_result.has_attributions:
            print (query_result.html_attributions)


        for place in query_result.places:
            # Returned places from a query are place summaries.
            print (place.name)
            text=(place.name+'\n')

            #print place.geo_location
            #print place.reference

            # The following method has to make a further API call.
            place.get_details()

            # Referencing any of the attributes below, prior to making a call to
            # get_details() will raise a googleplaces.GooglePlacesAttributeError.
            #print place.details # A dict matching the JSON response from Google.
            #print (place.local_phone_number)
            #print place.international_phone_number
            if place.website != None:
                arr_to_return.append(text+place.website+'\n')

        return arr_to_return
            #print place.url
    def get_near_gym(self,locationlat,locationlng):
        # You may prefer to use the text_search API, instead.
        lat=str(locationlat)
        lng=str(locationlng)
        arr_to_return=[]
        query_result = self.google_places.nearby_search(
                lat_lng={'lat': locationlat, 'lng': locationlng},keyword='gym',
                radius=2000, types=[types.TYPE_GYM])

        if query_result.has_attributions:
            print (query_result.html_attributions)


        for place in query_result.places:
            # Returned places from a query are place summaries.
            text=(place.name+'\n')
            #print place.geo_location
            #print place.reference

            # The following method has to make a further API call.
            place.get_details()

            # Referencing any of the attributes below, prior to making a call to
            # get_details() will raise a googleplaces.GooglePlacesAttributeError.
            #print place.details # A dict matching the JSON response from Google.
            #print (place.local_phone_number)
            #print place.international_phone_number
            if place.website != None:
                arr_to_return.append(text+place.website+'\n')
            #print place.url
        return arr_to_return

class GeocodeQuery:
    def __init__(self, language=None, region=None):
        self.url = 'https://maps.googleapis.com/maps/api/geocode/json?language={0}&region={1}&sensor=false'.format(language, region)
        self.jsonResponse = {}
        

    def get_geocode(self, addr):
        addr = urllib.parse.quote(addr)
        url = self.url + '&address={}'.format(addr)
        response = urllib.request.urlopen(url)
        reader = codecs.getreader("utf-8") 
        self.jsonResponse = json.loads(reader(response).read())
        return self.jsonResponse
        
    def get_lat(self):
        if len(self.jsonResponse["results"]) is not 0:
            return self.jsonResponse["results"][0]["geometry"]["location"]["lat"]

    def get_lng(self):
        if len(self.jsonResponse["results"]) is not 0:
            return self.jsonResponse["results"][0]["geometry"]["location"]["lng"]
    
    def get_cuntry(self):
        if len(self.jsonResponse["results"]) is not 0:
            return self.jsonResponse["results"][0]["address_components"][4]["long_name"]

    def get_area(self):
        if len(self.jsonResponse["results"]) is not 0:
            return self.jsonResponse["results"][0]["address_components"][3]["long_name"]


class TAIWAN_WEATHER_URL(object):

    response = urllib.request.urlopen('http://www.cwb.gov.tw/V7/forecast/week/week.htm')
    html = response.read().decode('utf-8')

    soup = BeautifulSoup(html,"lxml")
    link =soup.find("table",{"class":"BoxTableInside"})
    
    food_doc=xml.dom.minidom.parse('nutrition2.xml')
    food_Lib=food_doc.getElementsByTagName('Worksheet1')[0]
    nutrition_tags=[]
    
    Nutrition_=food_Lib.getElementsByTagName('Row')[0]
    tags=Nutrition_.getElementsByTagName('Cell')
    for tag in tags:
        t=tag.getElementsByTagName('Data')
        if t!=None:
            for tt in t:
                nutrition_tags.append(tt.firstChild.data)
        '''f=tag.getElementsByTagName('Font')
                                if f !=None:
                                    nutrition_tags.append(f)'''
        f=tag.getElementsByTagName('ss:Data')
        if f!=None:
            for ff in f:
                font=ff.getElementsByTagName('Font')[0].firstChild.data
                nutrition_tags.append(font)

    all_food=[]
    FOODS_LIST=food_Lib.getElementsByTagName('Row')
    for FOODS in FOODS_LIST[1:]:
        cells=FOODS.getElementsByTagName('Cell')
        nutr_tag_cnt=0
        firstitem=''
        first=0
        temp=[]
        for datas in cells:
            d=datas.getElementsByTagName('Data')
            if len(d)>=1:
                for data in d:
                    temp.append(nutrition_tags[nutr_tag_cnt]+': '+data.firstChild.data)
                    nutr_tag_cnt+=1
            else:
                got_data=0
                ss_datas=datas.getElementsByTagName('ss:Data')
                for ss_data in ss_datas:
                    fonts=ss_data.getElementsByTagName('Font')
                    if len(fonts)>=1:
                        text=''
                        for font in fonts:
                            text+=font.firstChild.data
                        temp.append(nutrition_tags[nutr_tag_cnt]+': '+text)
                        nutr_tag_cnt+=1
                        got_data=1
                if got_data==0:
                    temp.append(nutrition_tags[nutr_tag_cnt]+': '+'null')
                    nutr_tag_cnt+=1
                    
        all_food.append(temp)


    def get_cities_arr(self):
        arr_city=[]
        cities_list = TAIWAN_WEATHER_URL.link.find_all(rowspan='2') 
        for cities in cities_list:
            arr_city.append(cities.text)
        print(arr_city)
        return arr_city
            


    def get_forecast_data(self,city_requested):

        days_list = TAIWAN_WEATHER_URL.link.find('tr')
        arr_day_morning=[]
        arr_day_night=[]

        days = days_list.find_all(width='11%')
        for day in days:
            arr_day_morning.append(day.text+' 早上')
            arr_day_night.append(day.text+' 下午')

        for el in TAIWAN_WEATHER_URL.link.select('th'):
            k = el.parent
            r=el.parent.findNext('tr')
            cntmorning=1
            cntnight=1

            if el.text==city_requested:
                morning_result=[]
                evening_result=[]
                print('city: '+el.text)
                for kk in k.select('img'):
                    morning_result.append(arr_day_morning[cntmorning]+':  '+kk.get('alt'))
                    cntmorning+=1
                #print(arr_day_morning[cntmorning+1])
                #print(kk.get('alt'))
                
                #=el.parent.findNext('tr')
                for rr in r.select('img'):
                    evening_result.append(arr_day_night[cntnight]+':  '+rr.get('alt'))
                    cntnight+=1
                #print(rr.get('alt'))
                insert_pos=1
                for evening in evening_result:
                    morning_result.insert(insert_pos,evening)
                    insert_pos+=2
                
                insert_pos=2
                while insert_pos <= 20:
                    morning_result.insert(insert_pos,'\n')
                    insert_pos+=3
                return morning_result

    def training_menu(self,position):
        if position=='腿':
            print('into 1')
            menu_give=[]
            menu_give.append('深蹲 4-5組 10-15RM 休息1分鐘'+'\n'+'https://goo.gl/Cm28sS'+' (館長示範你不看？)')
            menu_give.append('腿推舉 3組 12-15RM 休息1分鐘'+'\n'+'https://goo.gl/mF16mj'+' (館長說話快看！)')
            menu_give.append('Swing 3組 各1分鐘 休息1分'+'\n'+'https://goo.gl/NzjsT8')
            menu_give.append('勾腿 3組 8-12RM 休息1分')
            menu_give.append('Lunge 3組 負重每腳輪流20下 休息1分'+'\n'+'https://goo.gl/X4B8Bv') 
            print(menu_give)
            return menu_give

        elif position=='背':
            print('into 2')
            menu_give=[]
            menu_give.append('Pull Up 3組 12-15下 休息1分'+'\n'+'https://goo.gl/cDi7bA')
            menu_give.append('曲體划船 3組 12-15下 休息1分'+'\n'+'https://goo.gl/DXteQw')
            menu_give.append('滑輪下拉 3組 12-15下 休息1分'+'\n'+'https://goo.gl/Y8cWhh')
            menu_give.append('坐姿划船 3組 12-15下 休息1分'+'\n'+'https://goo.gl/KkCuu8')
            menu_give.append('二頭彎舉 3組 15-20下做到力竭 休息1分'+'\n'+'https://goo.gl/jpkchW'+' 我館威武')        
            print(menu_give)
            return menu_give

        elif position=='胸':
            print('into 3')
            menu_give=[]
            menu_give.append('槓鈴握推 3組 12-15RM 休息1分'+'\n'+'https://goo.gl/8Q9RkR')
            menu_give.append('斜啞鈴握推 3組 12-15RM 休息1分'+'\n'+'https://goo.gl/fEGXHb')
            menu_give.append('纜繩飛鳥 3組 12-15RM 休息1分'+'\n'+'https://goo.gl/sWn5uX')
            menu_give.append('斜啞鈴飛鳥 3組 12-15RM 休息1分'+'\n'+'https://goo.gl/zTqTqN')
            menu_give.append('上斜握推 3組 12-15RM 休息1分'+'\n'+'https://goo.gl/KUvwzB')
            print(menu_give)
            return menu_give
        
        elif position=='核心':
            print('into 4')
            menu_give=[]
            menu_give.append('Plank 3組 各一分鐘 休息30秒'+'\n'+'https://goo.gl/DfMOr0')
            menu_give.append('Bird Dog 3組 各1分鐘 休息30秒'+'\n'+'https://goo.gl/sfjnDt')
            menu_give.append('側邊撐體 3組 左右各1分鐘 休息1分鐘'+'\n'+'https://goo.gl/P5xBzI')
            menu_give.append('伏地挺身 3組 各15下 休息1分鐘'+'\n'+'https://goo.gl/aJUmaK')
            menu_give.append('登山者動作'+'\n'+'https://goo.gl/vdlMRo')
            print(menu_give)
            return menu_give            
        
    def IDIOM_GET(self):
        doc=xml.dom.minidom.parse('chinese.xml')
        Lib=doc.getElementsByTagName('Worksheet1')[0]
        idioms=[]
        library=Lib.getElementsByTagName('Row')
        for words in library:
            Cell=words.getElementsByTagName('Data')[1].firstChild.data
            if len(Cell) ==4:
                idioms.append(Cell)     

        #print('\n'.join(idioms))
        return idioms

    

        


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model = self,
            **machine_configs
        )
        self.idiot=0
        self.city='臺南市'
        self.height=170
        self.weight=60
        self.workout_time=1.5
        self.sex_reply=['male','巨巨','男生','female','G奶','女生']
        self.training_exercise=['腿','背','胸','核心']        
        self.cities_arr=TAIWAN_WEATHER_URL().get_cities_arr()
        self.taiwan=TAIWAN_WEATHER_URL()
        self.original_idioms=self.taiwan.IDIOM_GET()
        self.idioms=self.original_idioms
        self.Q=''
        self.Re=''
        self.advice=[]
        self.firstinto=0
        self.wrong=0
        self.wrongcnt=0
        self.already_right=0
        self.height=0
        self.weight=0
        self.age=0
        self.sex='巨巨'
        self.BMR=0.0
        self.TDEE=0.0
        self.CHO=0.0
        self.P=0.0
        self.F=0.0
        self.whatfortdee=''
        self.request_food=''
        self.food_weight=0
        self.got_asked_food=[]
        self.gq = GeocodeQuery("zh-tw", "tw")
        self.addr =''




    def go_exercise(self,update):
        text = update.message.text
        return text.lower()=='exercise' or text.lower()=='運動'

    def is_going_to_state2(self, update):
        text = update.message.text
        print('into state2')
        return text.lower() == 'y'

    def Dont_workout(self, update):
        text = update.message.text
        return text.lower() == 'n'

    def want_park_info(self,update):
        text=update.message.text
        if text.lower()!=None and text.lower()!=None:
            self.addr=text.lower()
            return 1

    def Male_Female(self, update):
        print('into male female')
        text = update.message.text
        if (text.lower()=='male')or (text.lower()=='巨巨') or (text.lower()=='男生'):
            print('boy')
            self.idiot=0
            return 1
        elif (text.lower()=='female')or (text.lower=='G奶') or (text.lower()=='女生'):
            print('girl')
            self.sex='G奶'
            self.idiot=0
            return 1 

    def S5_to_S2(self,update):
        print('into S2')
        text=update.message.text
        self.idiot=1
        return text.lower() not in self.sex_reply and text.lower()!=None and text.lower()!='quit'

    def City_Request(self,update):
        text=update.message.text
        if text.lower() in self.cities_arr:
            self.city=text.lower()
            self.idiot=0
            return 1
    
    def S4_to_S4(self,update):
        text=update.message.text
        self.idiot=1
        return text.lower() not in self.cities_arr and text.lower()!=None and text.lower()!='quit'   
    
    def want_to_work_inside(self,update):
        text=update.message.text
        return text.lower()=='y'

    def satisfied(self,update):
        text=update.message.text
        return text.lower()=='y'
        
    def not_satisfied(self,update):
        text=update.message.text
        return text.lower()=='n'

    def play_game(self,update):
        text=update.message.text
        return text.lower()=='game'or text.lower()=='遊戲'

    def other_from_YorN(self,update):
        text=update.message.text
        return text.lower()!='y' and text.lower()!='n' and text.lower()!='quit'

    def get_answer_right(self,update):
        print('into right answer')
        text=update.message.text
        if text.lower()!=None and text.lower()!='quit':
            self.Re=text.lower()
            if self.Re in self.idioms and self.Re[0]==self.Q[3] and self.Re!=self.Q:
                self.already_right=1
                return 1
    
    def get_answer_wrong(self,update):
        print('into wrong answer')
        text=update.message.text
        if text.lower()!=None and text.lower()!='quit':
            self.Re=text.lower()
            if self.already_right==0 and (len(self.Re)!=4 or self.Re[0]!=self.Q[3] or self.Re not in self.idioms):
                return 1

    def count_Calorie(self,update):
        text=update.message.text
        return text.lower()=='health' or text.lower()=='健康'

    def get_height(self,update):
        text=update.message.text
        print('int height')
        if (text.lower()).isdigit()==True:
            print('true')
            self.height=(int)(text.lower())
            return 1

    def get_weight(self,update):
        text=update.message.text
        if (text.lower()).isdigit()==True:
            self.weight=(int)(text.lower())
            return 1  

    def get_age(self,update):
        text=update.message.text
        if (text.lower()).isdigit()==True:
            self.age=(int)(text.lower())
            return 1        
    def get_workouttime(self,update):
        text=update.message.text
        if(text.lower()).isdigit()==True:
            tempnum=(int)(text.lower())
            if tempnum>=1 and tempnum<=4:
                self.workout_time=tempnum
                return 1

    def get_sex(self,update):
        text=update.message.text
        if text.lower()=='male' or text.lower()=='female':
            self.sex=text.lower()
            return 1

    def to_start(self,update):
        text=update.message.text
        if text.lower()=='/start':
            return 1

    def how_to_deal_tdee(self,update):
        text=update.message.text
        if text.lower()=='增肌' or text.lower()=='減脂' or text.lower()=='維持體態':
            self.whatfortdee=text.lower()
            return 1

    def get_food(self,update):
        text=update.message.text
        if text.lower()!=None and text.lower()!='quit' and text.lower().isdigit()==False:
            self.request_food=text.lower()
            return 1
    def  get_food_weight(self,update):
        text=update.message.text
        if text.lower().isdigit()==True :
            self.food_weight=(int)(text.lower())
            return 1

    def to_quit(self,update):
        text=update.message.text
        if text.lower()=='quit':
            return 1
    
    def on_enter_state0(self,update):
        update.message.reply_text('Hi!\n'+'打『運動』or 『exercise』進入運動建議bot'+'\n打『game』or『遊戲』進到成語接龍遊戲\n'+'打『健康』or『health』得知tdee以及生活中食物的營養價值')

    def on_enter_state1(self, update):
        update.message.reply_text("安安，想要動起來嗎？(y/n)")


    def on_enter_state2(self, update):
        if self.idiot==1:
            update.message.reply_text('你是智障嗎？好吧我再問一次...')
            self.idiot=0
        first_=['那我們開始第1類接觸吧','那我們開始身家調查吧','讓我多了解你一點']
        second_=['你是巨巨還是G奶？','你是男生還是女生R？','male or female?']
        num1_random=random.randint(0,2)
        num2_random=random.randint(0,2)
        update.message.reply_text(first_[num1_random])
        update.message.reply_text(second_[num2_random])

    def on_enter_state3(self,update):
        update.message.reply_text('...')
        recipe=['我不知道要說什麼了\n 所以來教大家做簡單的壽司\n\n 食材調味： \n白飯、肉鬆、海苔、蛋、太白粉、水、 壽司醋 (糖、白醋、鹽)。\n \n食譜作法：\n1.飯煮熟趁熱倒入壽司醋拌勻放涼。 \n2.蛋打散太白粉和水攪拌均勻。 \n3.倒入平底鍋煎成薄蛋皮。 \n4.煎好蛋皮去邊切成方形。 \n5.捲壽司竹簾放上蛋皮。 \n6.上面再鋪整片海苔。 \n7.再舖薄白飯(前後預留不鋪)。 \n8.米飯上再放上肉鬆。 \n9.竹簾卷起壓緊往前推。 \n10.食用切段即可。 \n要注意米量 跟口味\n','我不知道要說什麼了\n 所以來教大家做簡單的涼拌麻辣脆筍\n1. 把筍殼剝除，表皮較老的部份稍微修除一下\n2. 切成薄片後用熱水川燙約1分鐘，撈起沖冷水後再泡在冰開水裡！\n3. 把所有的材料都加在裡面\n4. 攪拌均勻後放在冰箱裡靜置一晚待入味\n 5.吃的時候加些香菜灑上白芝麻，一道清脆痲辣的.....涼拌麻辣脆筍完成！','我不知道要說什麼了\n 所以來教大家做簡單的鮮蝦粉絲煲\n1. 事前準備： 冬粉以冷水泡軟(約5分鐘左右) 蝦子挑去腸泥 蒜頭磨成蒜泥或蒜碎(建議磨成泥) 蔥及辣椒切小段 洋蔥切絲\n2. 冷鍋下油後下洋蔥略炒至半透明\n3. 加入1/3蒜泥拌炒2分鐘後將洋蔥盛起\n4. 加入蝦子煎至8分熟後(蝦殼變紅即可)，將蝦子盛起備用， 煎蝦子的油千萬別倒掉，它可是這道菜的美味關鍵\n5. 加入一大匙油，將剩餘的2/3蒜頭及辣椒倒入爆香\n6. 倒入洋蔥拌炒\n7. 加入泡軟的粉絲，可以跟鍋中的材料稍作攪拌\n8. 加入二大匙蠔油(葷/素皆可)\n9. 加入400ml的水攪拌後以中火煮至7分乾\n10. 加入2大匙烹大師或1大匙的鹽，再將蝦子倒入一起煮直到水收至9分乾即可盛盤\n11. 撒上蔥花及少許辣椒，香噴噴美味上桌']
        num2_random=random.randint(0,2)        
        update.message.reply_text(recipe[num2_random])
        update.message.reply_text('回去吧，這裡不是你該來的地方，以後再來找我吧')
        self.firstinto=0
        self.go_back(update)


        

    def on_enter_state4(self, update):
        if self.idiot==1:
            update.message.reply_text('你是智障嗎？好吧我再問一次...')
            self.idiot=0
        update.message.reply_text('Hi '+self.sex+'!')
        update.message.reply_text('你住那阿？(從下面的城市裏面選一個~)\n(直接複製貼上你的城市就好 ex:臺南市)')
        cities_="  ".join(self.cities_arr)
        update.message.reply_text(cities_)
        

    def on_enter_state5(self,update):
        print('into state5:city')
        print(self.city)
        update.message.reply_text('以下是【%s】的一週氣象預報：'%(self.city))
        weather_arr=self.taiwan.get_forecast_data(self.city)
        weather='\n'.join(weather_arr)
        update.message.reply_text(weather)
        recommand_list=[]

        for w in weather_arr:
            if w.find('雨')==-1 and w.find('\n')==-1:
                temp=w.split(':')[0]
                #print(temp)
                recommand_list.append(temp)
        if len(recommand_list)!=0:
            update.message.reply_text('\n'+'小建議啦，在\n'+'\n'.join(recommand_list)+'\n做戶外運動較適合，碰到雨天的機率比較小！\n')
        else:
            update.message.reply_text('Oops,'+'感覺最近都會下雨ㄟ...')
        update.message.reply_text('想知道你附近有哪些運動的好地方嗎？如果想的話就給我你的地址吧！不要的話就打\'n\'' )
    
    def on_enter_state_park(self,update):
        self.gq.get_geocode(self.addr)
        print(self.gq.get_lat())
        print(self.gq.get_lng())
        get_park_info=Near().get_near_park(self.gq.get_lat(),self.gq.get_lng())
        update.message.reply_text('你真是太上進了！\n以下是距離你兩公里內的公園:\n'+'\n'.join(get_park_info)+'\n\n')
        get_gym_info=Near().get_near_gym(self.gq.get_lat(),self.gq.get_lng())
        update.message.reply_text('若下雨的話還有室內的運動場所！地點我都幫你找好ㄌ，我就是這麼的貼心，才抓的住小燕子的心阿～～～\n')
        update.message.reply_text('距離你兩公里內的室內運動場:\n'+'\n'.join(get_gym_info)+'\n\n'+'想要來點健身菜單嗎（y/n）？')

    def on_enter_state_no_park(self,update):
        update.message.reply_text('要不要來一點室內的訓練R（y/n）？')


    def on_enter_state6(self,update):
        update.message.reply_text('http://cdn2.ettoday.net/images/2260/d2260401.jpg')
        num_random=random.randint(0,3)
        update.message.reply_text('來練個'+self.training_exercise[num_random]+'好了')
        train_=self.taiwan.training_menu(self.training_exercise[num_random])
        random.shuffle(train_)
        train_.insert(0,'熱身10分鐘')
        train_.append('休息拉拉筋')
        to_print_train='\n'.join(train_)
        update.message.reply_text('以下是給你的建議菜單：')
        update.message.reply_text(to_print_train)
        update.message.reply_text('你有滿意嗎？(y/n)')


    def on_enter_state7(self,update):
        update.message.reply_text('真假 重訓也是很重要的ㄟ'+'\n'+'練了可以讓身體更強，老了才不會坐高級敞蓬車！')
        update.message.reply_text('think twice plz')
        update.message.reply_text('want to workout?(y/n)')



    def on_enter_state8(self,update):
        reply_arr=['哭了，謝謝貴'+self.sex+'的支持','感恩大大，你一定會友好報的','THANK U VERY MUCH！']
        rand_num=random.randint(0,2)
        update.message.reply_text(reply_arr[rand_num]+'\n'+'Bye~')
        self.go_back(update)

        
    def on_enter_state9(self,update):
        update.message.reply_text('ㄎㄎ那我也沒辦法了\n'+'bye')
        self.go_back(update)


    def on_enter_state10(self,update):
        self.wrongcnt=0
        self.wrong=0
        update.message.reply_text('準備好要玩成語接龍了嗎?(y/n)')

    
    def on_enter_state11(self,update):
        print('into state11')
        update.message.reply_text('你真的很棒!\n'+'接下來說明遊戲規則\n\n'+'首先由我出題，我們雙方都必須以成語來回應對方的題目，並且回應的成語開頭必須跟對方答案最後一個字一模一樣\n\n'+'範例：\n我說『一石二鳥』\n你回『鳥盡弓藏』（o）\n'+'你回『袅娜娉婷』（x）')
        update.message.reply_text('這樣子你有懂嗎？（y/n）')


    def on_enter_state12(self,update):
        self.idioms=self.original_idioms
        update.message.reply_text('Start!')
        randly_choose=random.sample(self.idioms,5)
        print(randly_choose)
        tobreak=0
        del self.advice[:]
        for item in randly_choose:
            for parent_item in self.idioms:
                if item[3]==parent_item[0]:
                    self.advice.append(parent_item)
                    if len(self.advice)>=5:
                        self.Q=item

                        tobreak=1
                        break
            if tobreak==1:
                break
            else:
                del self.advice[:]
        update.message.reply_text(self.Q)
        self.idioms.remove(self.Q)
        print(self.advice)        


    def on_enter_state13(self,update):
        self.already_right=0
        self.idioms.remove(self.Re)
        if_right=['好像很厲害','猛','跪了']
        del self.advice[:]
        n=random.randint(0,2)
        ass_word=['等等，我去找紫薇幫我','我都要慢出來了','讓我去御書房瞧瞧']
        update.message.reply_text(if_right[n]+'\n'+ass_word[n])
        re_last=self.Re[3]
        tobreak=0
        found=0
        
        #make sure at least one reply can be given
        for item in self.idioms:
            if item[0]==re_last:
                found=1
                self.Q=item
                tobreak=1
                for pre_advice in self.idioms:
                    if pre_advice[0]==item[3]:
                        self.advice.append(pre_advice)
                        tobreak=1
                        break
            if tobreak==1:
                break
        
        #try to find if there is a better reply
        try_list=[]
        for item in self.idioms:
            if item[0]==re_last:
                found=1
                try_list.append(item)
            if len(try_list)>4:
                break
        print(try_list) 
        temp=[]
        tobreak=0
        better=0
        for item in try_list:
            for parent_item in self.idioms:
                if item[3]==parent_item[0]:
                    temp.append(parent_item)
                    if len(temp)>3:
                        self.Q=item
                        del self.advice[:]
                        self.advice=temp
                        tobreak=1
                        break
            if tobreak==1:
                break
            else:
                del temp[:]

        
        if found==1:
            update.message.reply_text(self.Q)
            self.idioms.remove(self.Q)
            print(self.advice)
        else:
            update.message.reply_text('你中文系的？？太猛了啦我完全輸到脫褲 受不了ㄌ88')
            self.go_back(update)


    def on_enter_state14(self,update):
        if self.wrongcnt>3:
            update.message.reply_text('你回去學好中文再來找我吧ㄎㄎ 這樣下去只是在羞辱你自己而已，加油啦掰掰')
            self.go_back(update)
        else:
            if_wrong=['不要now了你！','跟我開玩笑？','我真的很同情你媽...','...你國文老師在哭了la','...左轉笨版謝謝']
            pic=['https://goo.gl/Ki5zwY','https://goo.gl/tL8S7l','https://goo.gl/jK0Jp8']
            n=random.randint(0,2)
            update.message.reply_photo(pic[n])
            n=random.randint(0,4)
            update.message.reply_text(if_wrong[n])
            self.wrongcnt+=1
            update.message.reply_text('要不要給你一點提示阿...（y/n）')
            update.message.reply_text('不要提示的話我就重新出題吧\n不然我看你也答不出來了ㄎㄎ')

    def on_enter_state15(self,update):
        random.shuffle(self.advice)
        update.message.reply_text(self.advice[0])


    def on_enter_state16(self,update):
        update.message.reply_text('ready to count your TDEE?(y/n)')

    def on_enter_state17(self,update):
        update.message.reply_text('Cool! 敢問您幾尺高呢（公分）, ex:170')

    def on_enter_state18(self,update):
        update.message.reply_text('佩服佩服, 閣下果然不是等閒之輩呢，等等叫小燕子幫你泡個茶。對了，您的體重幾公斤呢？, ex:65')

    def on_enter_state19(self,update):
        update.message.reply_text('敢問您今年貴庚? ex:21')

    def on_enter_state20(self,update):
        update.message.reply_text('我需要知道你的活動力'+'\n'
            +'1. 文職、久坐者（一日走不到5000步）\n'+'2.  日走5000-7499步\n'+'3. 日走7500-9999步者（或運動1小時）\n'+'4. 日走10000步up（or運動2小時）\n')
        update.message.reply_text('請給我你活動力的級別即可 ex: 假如你是日走5000-7499步者，輸入2就好')
    
    def on_enter_state21(self,update):
        update.message.reply_text('male or female?')

    def on_enter_state22(self,update):
        update.message.reply_text('Great!')
        update.message.reply_text('現在開始計算你的你的基礎代謝率（bmr）與每日消耗熱量（tdee）\n'+'若對tdee不了解，可上 https://goo.gl/uEesE6 了解此方面的訊息'+'\n以下計算是基於Mifflin-St. Jror研究得到的公式')
        if self.sex=='male':
            self.BMR=10*(self.weight)+6.25*(self.height)-5*(self.age)+5
        else:
            self.BMR=10*(self.weight)+6.25*(self.height)-5*(self.age)-161
	
        text='你的基礎代謝率為：'+ str(round(self.BMR,1)) +'\n'
        if self.workout_time==1:
            self.TDEE=self.BMR*1.27
            text+='依據你的活動力，你目前的TDEE為：'+ str(round(self.TDEE,1)) +'\n'
            text+='若您改變活動力級別至2，tdee為'+str(round(self.BMR*1.4,1))+'\n'
            text+='若您改變活動力級別至3，tdee為'+str(round(self.BMR*1.7,1))+'\n'   
            text+='若您改變活動力級別至4，tdee為'+str(round(self.BMR*2.0,1))+'\n'
        elif self.workout_time==2:
            self.TDEE=self.BMR*1.4
            text+='依據你的活動力，你目前的TDEE為：'+ str(round(self.TDEE,1)) +'\n'
            text+='若您改變活動力級別至1，tdee為'+str(round(self.BMR*1.27,1))+'\n'
            text+='若您改變活動力級別至3，tdee為'+str(round(self.BMR*1.7,1))+'\n'   
            text+='若您改變活動力級別至4，tdee為'+str(round(self.BMR*2.0,1))+'\n'            
        elif self.workout_time==3:
            self.TDEE=self.BMR*1.7
            text+='依據你的活動力，你目前的TDEE為：'+ str(round(self.TDEE,1)) +'\n'
            text+='若您改變活動力級別至1，tdee為'+str(round(self.BMR*1.27,1))+'\n'
            text+='若您改變活動力級別至2，tdee為'+str(round(self.BMR*1.4,1))+'\n'   
            text+='若您改變活動力級別至4，tdee為'+str(round(self.BMR*2.0,1))+'\n'
        elif self.workout_time==4:
            self.TDEE=self.BMR*2.0
            text+='依據你的活動力，你目前的TDEE為：'+ str(round(self.TDEE,1)) +'\n'
            text+='若您改變活動力級別至1，tdee為'+str(round(self.BMR*1.27,1))+'\n'
            text+='若您改變活動力級別至2，tdee為'+str(round(self.BMR*1.4,1))+'\n'   
            text+='若您改變活動力級別至3，tdee為'+str(round(self.BMR*1.7,1))+'\n'
        
        self.CHO=self.TDEE*0.25/4
        self.P=self.TDEE*0.2/4
        self.F=self.TDEE*0.55/9
        update.message.reply_text(text+'\n\n請告訴我您目前是想 維持體態 or 減脂 or 增肌')
        
        
    def on_enter_state23(self,update):
        if self.whatfortdee=='減脂':
            update.message.reply_text('建議減脂期熱量至少攝取'+(self.TDEE-self.BMR*0.3)+'kcals')
            temp_tdee=self.TDEE-self.BMR*0.3
            self.CHO=temp_tdee*0.25/4
            self.F=temp_tdee*0.2/4
            self.P=temp_tdee*0.55/9
        elif self.whatfortdee=='維持體態':
            temp_tdee=self.TDEE
            self.CHO=temp_tdee*0.25/4
            self.F=temp_tdee*0.2/4
            self.P=temp_tdee*0.55/9
        elif self.whatfortdee=='增肌':
            temp_tdee=self.TDEE+self.BMR*0.3
            self.CHO=temp_tdee*0.25/4
            self.F=temp_tdee*0.2/4
            self.P=temp_tdee*0.55/9            
        update.message.reply_text('若以低碳飲食來說，建議您每日攝取 \n'
            +str(round(self.CHO,1))+ ' g的碳水化合物\n'+str(round(self.P,1))
            +' g的蛋白質\n'+str(round(self.F,1))+' g的油脂\n\n')
        update.message.reply_text('現在可以開始跟我說你吃了什麼了 ex:白飯, 打\'quit\'表結束')
    

    def on_enter_state24(self,update):
        temp_result=[]
        for search in self.taiwan.all_food:
            if self.request_food in search[1] or self.request_food in search[2] or self.request_food in search[3]:
                temp_result.append(search)
        if len(temp_result)>1:    
            update.message.reply_text('以下是可能的搜索結果，請確認並且再輸入一次完整的名稱：')
            to_check_arr=[]
            for item in temp_result:
                to_check=item[1]+'\n'+item[2]+'\n'+item[3]+'\n'
                to_check_arr.append(to_check)
            update.message.reply_text('\n'.join(to_check_arr))
        elif len(temp_result)==1:
            update.message.reply_text('以下是搜索結果，以每100克作為計算標準')
            update.message.reply_text('\n'.join(temp_result[0]))
            self.got_asked_food=temp_result[0]
            update.message.reply_text('你可以跟我說你吃了幾克（ex:100）或者直接查詢新的食物營養')
        elif len(temp_result)==0:
            update.message.reply_text('Sorry, I can not find what you want...')
            update.message.reply_text('Try to figure out more!')

    def on_enter_state25(self,update):
        t_kcal=(float)(self.got_asked_food[4].split(':')[1])/100*self.food_weight
        print(t_kcal)
        self.TDEE-=t_kcal
        t_cho=(float)(self.got_asked_food[9].split(':')[1])/100*self.food_weight
        self.CHO-=t_cho
        t_p=(float)(self.got_asked_food[6].split(':')[1])/100*self.food_weight
        self.P-=t_p
        t_f=(float)(self.got_asked_food[7].split(':')[1])/100*self.food_weight
        self.F-=t_f
        update.message.reply_text('OK, after you ate'+str(round(self.food_weight,1))+'g '+self.request_food+'\n'+'You would get\n'
            +str(round(t_kcal,1))+' kcal\n'+str(round(t_cho,1))+' g cho\n'+str(round(t_p,1))+' g protein\n'+str(round(t_f,1))+' g fat\n\n'+'Figure out more!')
        update.message.reply_text('您還有'+str(round(self.TDEE,1))+'kcal的餘額：\n'+str(round(self.CHO,1))+' g 碳水\n'+str(round(self.P,1))+' g 蛋白質\n'+str(round(self.F,1))+' g 油脂')

    def on_exit_state26(self,update):
        print('bye 26')

    def on_exit_state3(self,update):
        print('bye 3')

    def on_exit_state8(self,update):
        print('bye 8')

    def on_exit_state9(self,update):
        print('bye 9')

    def on_exit_state13(self,update):
        print('bye 13')

    def on_exit_state14(self,update):
        print('bye 14')




        


