from zipfile import ZipFile
import time, sys

#vscode 사용시 파일 입출력에 관련해서 해당 파일의 위치를 정확하게 지정해주어야 함.
#vscode외의 편집기에서 사용시 아래 두 줄 코드 comment 처리
#os.chdir("../../") #현재 폴더의 위치에서 c 루트까지 이동
#os.chdir("C:/Users/Home/Desktop/포렌식") #원하는 폴더까지 

#120171838_진병욱_포렌식_분석_프로그램
def get_gps_info():
    from PIL import Image
    from PIL.ExifTags import TAGS
    import simplekml

    print()
    print('kml 파일 생성 프로그램입니다.\n')

    kml = simplekml.Kml()

    while True:
        try:
            img_name = input('이미지 파일 명을 입력하세요 (확장자 포함) : ')
            if img_name == 'over':
                break
            print('\n* 이미지를 더 이상 추가하지 않으려면 over를 입력하세요 *\n')
            image = Image.open(img_name)
            info = image._getexif()
            image.close()
        except FileNotFoundError:
            print('\n* 해당 이미지 파일이 존재하지 않습니다 *\n\n')
            return False

        taglabel = {} #tag사전

        try:
            for tag, value in info.items(): #이미지 정보를 태그와 값으로 분류
                decoded = TAGS.get(tag, tag)
                taglabel[decoded] = value
        except AttributeError as e:
            err = "'NoneType' object has no attribute"
            if err in str(e):
                print('\n* 이미지 정보를 불러올 수 없습니다 *\n\n')
                return False
        
        try:
            exifGPS = taglabel['GPSInfo']
        except KeyError as e:
            err = "'GPSInfo'"
            if err in str(e):
                print('\n* GPS 정보가 존재하지 않습니다 *\n\n')
                return False

        latData = exifGPS[2] #위도
        lonData = exifGPS[4] #경도

        #위도
        latDeg = latData[0] #도
        latMin = latData[1] #분
        latSec = latData[2] #초

        #경도
        lonDeg = lonData[0] #도
        lonMin = lonData[1] #분
        lonSec = lonData[2] #초


        lat = float(latDeg) + (float(latMin)/60) + (float(latSec)/3600) #위도 좌표값으로 표현
        lon = float(lonDeg) + (float(lonMin)/60) + (float(lonSec)/3600) #경도 좌표값으로 표현

        print('> 위도 :',lat,', 경도 :',lon,'\n')

        kml.newpoint(name=img_name, coords=[(lon,lat)])

    # 도, 분, 초로 나타내기
    #Lat = str(int(latDeg)) + "°" + str(int(latMin)) + "'" + str(latSec) + "\"" + exifGPS[1] #위도
    #Lon = str(int(lonDeg)) + "°" + str(int(lonMin)) + "'" + str(lonSec) + "\"" + exifGPS[3] #경도

    project = input("\n파일 명 : ")
    kml.save(project + ".kml")
    print('\n* 파일이 생성되었습니다. *\n\n')

    #print('\n2초 후 구글 지도에 해당 GPS 장소를 표시합니다.\n\n\n')
    #time.sleep(2)
    #webbrowser.open_new("https://www.google.com/maps/place/" + Lat + "+" + Lon)
            

def compression_release(): #압축해제
    print('\n압축해제 프로그램입니다.\n')
    #file_name = "Autoexec.zip"

    file_name = input('압축 파일 명을 입력하세요 (확장자는 입력 X) : ')
    pwd = input('패스워드 파일명을 입력하세요 (확장자는 입력 X) : ')
    file_name = file_name + '.zip'
    path2 = file_name[:-4]
    pwd = pwd +'.txt'
    
    try:
        f = open(pwd, 'r', encoding='utf-8')
        
    except FileNotFoundError:
        print('\n* 해당 패스워드 파일이 존재하지 않습니다 *\n')
        return False

    
    line = f.readlines()

    passwd = [] #리스트 생성

    for i in line:
        if i != '\n':
            i = i.rstrip('\n') #끝에 \n제거
            passwd.append(i)
        
    f.close()
    print('\n압축 해제를 시작합니다.')
    cnt = 0

    try :
        with ZipFile(file_name, 'r') as zip:
            #zip.printdir() #압축파일 내 파일 확인
            for i in range(len(passwd)): #passwd길이만큼 반복
                try: #압축 해제 시도
                    zip.extractall(path = path2, pwd = passwd[i].encode()) #압축 해제, 경로 및 비밀번호 설정
                    
                except RuntimeError as e: #에러 발생시
                    err2 = 'Bad password'
                    err3 = 'That compression method is not supported'
                    if err2 in str(e):
                        cnt += 1
                        print('{}은(는) 비밀번호가 아닙니다.'.format(passwd[i]))
                        if cnt == len(passwd):
                            print('\n* 비밀번호가 존재하지 않습니다. *\n\n')
                        
                    elif err3 in str(e):
                        print('\n* 압축 해제가 불가능한 압축 파일입니다 *\n* zipcrypto 방식만 해제가 가능합니다 *\n\n')
                        break
                    
                else: #압축해제시
                    print()
                    print('************************************************************************')
                    print('* 정상적으로 압축이 해제되었습니다. 비밀번호는 {}입니다. *'.format(passwd[i]))
                    print('************************************************************************\n\n')
                    break
                
    except FileNotFoundError:
        print('\n* 해당 압축 파일이 존재하지 않습니다 *\n\n')
        return False

def main(): #메인 함수
    print("▶▶▶▶▶ 포렌식 분석 프로그램 Ver 1.0 ◀◀◀◀◀")
    print("created by JBU\n")
    while True:
        #print('*************************')
        print('1. 압축파일 해제')
        print('2. kml 파일 생성')
        print('3. MBR 자동 복구')
        print('4. 네트워크')
        print('5. 프로그램 종료\n')
        #print('*************************\n')
        menu = input('메뉴를 선택하세요 ex) 1 : ')
            
        if menu == '1':
            compression_release()
        elif menu == '2':
            get_gps_info()
        elif menu == '3':
            print('MBR 자동 복구')
        elif menu == '4':
            print('네트워크')
        elif menu == '5':
            print('\n3초 후 프로그램을 종료합니다.\n')
            time.sleep(3)
            sys.exit()
        else:
            print('\n* 메뉴를 다시 선택해 주세요* \n')

if __name__ == "__main__":
    main()

