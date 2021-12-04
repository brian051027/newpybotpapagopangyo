#Papago API Reference : https://developers.naver.com/docs/nmt/reference/

import discord
import asyncio
import os
from discord.ext import commands
import urllib
from urllib.request import URLError
from urllib.request import HTTPError
from urllib.request import urlopen
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from urllib.parse import quote
import re # Regex for youtube link
import warnings
import requests
import unicodedata
import json

#디스코드 봇 토큰
token = ''
#Naver Open API application ID
client_id = "Rj2TZHYsoVvt0s6MLqWW"
#Naver Open API application token
client_secret = "MJkS7xnRud"

client = discord.Client()
@client.event # 이벤트 상태 반영
async def on_ready(): # on_ready() event : when the bot has finised logging in and setting things up
    await client.change_presence(status=discord.Status.online, activity=discord.Game("번역기 가동중!"))
    print("New log in as {0.user}".format(client))

@client.event
async def on_message(message): # on_message() event : 봇이 메시지를 받을때
    #메시지를 보낸 사람에게 전송
    # await message.author.send(msg)
    print(message.content)
    if message.author == client.user:
        return

    '''
    #네이버에서 클라이언트 id와 암호화키 가져오기
    client_id = "Rj2TZHYsoVvt0s6MLqWW"
    client_secret = "MJkS7xnRud"

    #번역할 단어/문장
    entData = quote("")

    dataParmas = "source=en&target=id&text=" + entData
    baseurl = "https://openapi.naver.com/v1/papago/n2mt"

    #Make a Request Instance
    request = Request(baseurl)

    #페킷에 헤더 넣기
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urlopen(request,data=dataParmas.encode("utf-8"))

    responsedCode = response.getcode()
    if(responsedCode==200):
        response_body = response.read()
        #response_body -> byte string : decode to utf-8
        api_callResult = response_body.decode('utf-8')

        #JSON 타입의 정보가 출력. 그래서 다시 JSON 타입으로 변경(사전처럼)
        stringConvertJSON = api_callResult.replace("'","\"")
        api_callResult = json.loads(stringConvertJSON)
        translatedText = api_callResult['message']['result']["translatedText"]
        print(translatedText)
    else:
        print("Error Code : " + responsedCode)
    '''

    if message.content.startswith("!한영번역"):
        baseurl = "https://openapi.naver.com/v1/papago/n2mt"
        #띄어쓰기 : split처리후 [1:]을 for문으로 붙인다.
        trsText = message.content.split(" ")
        try:
            if len(trsText) == 1:
                await message.channel.send("단어 혹은 문장이 입력되지 않았어요. 다시한번 확인해주세요.")
            else:
                trsText = trsText[1:]
                combineword = ""
                for word in trsText:
                    combineword += " " + word
                # 만약 입력된 값이 문장인 경우 다시 조립하여 양쪽의 빈칸을 제거한다.
                savedCombineword = combineword.strip()
                combineword = quote(savedCombineword)
                print(combineword)
                # 쿼티 문자열 만들기
                dataParmas = "source=ko&target=en&text=" + combineword
                # Make a Request Instance
                request = Request(baseurl)
                # 페킷에 헤더 추가하기
                request.add_header("X-Naver-Client-Id", client_id)
                request.add_header("X-Naver-Client-Secret", client_secret)
                response = urlopen(request, data=dataParmas.encode("utf-8"))

                responsedCode = response.getcode()
                if (responsedCode == 200):
                    response_body = response.read()
                    # response_body -> byte string : decode to utf-8
                    api_callResult = response_body.decode('utf-8')
                    # JSON 타입의 정보가 출력. 그래서 다시 JSON 타입으로 변경(사전처럼)
                    api_callResult = json.loads(api_callResult)
                    # 최종 결과물
                    translatedText = api_callResult['message']['result']["translatedText"]
                    embed = discord.Embed(title="Translate | Korean -> English", description="", color=0x5CD1E5)
                    embed.add_field(name="Korean to translate", value=savedCombineword, inline=False)
                    embed.add_field(name="Translated English", value=translatedText, inline=False)
                    embed.set_thumbnail(url="https://papago.naver.com/static/img/papago_og.png")
                    embed.set_footer(text='by 설준서. API provided by Naver Open API',
                                     icon_url='https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2F20161011_288%2Fjasara59_1476165827672d3iAL_JPEG%2Fimage.jpg&type=sc960_832')
                    await message.channel.send("Translate complete", embed=embed)
                else:
                    await message.channel.send("Error Code : " + responsedCode)
        except HTTPError as e:
            await message.channel.send("Translate Failed. HTTPError Occured.")


    if message.content.startswith("!영한번역"):
        baseurl = "https://openapi.naver.com/v1/papago/n2mt"
        # 띄어쓰기 : split처리후 [1:]을 for문으로 붙인다.
        trsText = message.content.split(" ")
        try:
            if len(trsText) == 1:
                await message.channel.send("단어 혹은 문장이 입력되지 않았어요. 다시한번 확인해주세요.")
            else:
                trsText = trsText[1:]
                combineword = ""
                for word in trsText:
                    combineword += " " + word
                # 입력된 값이 문장인 경우 다시 조립하여 양쪽의 빈칸을 제거한다.
                savedCombineword = combineword.strip()
                combineword = quote(savedCombineword)
                # 쿼티 문자열 만들기
                dataParmas = "source=en&target=ko&text=" + combineword
                # Make a Request Instance
                request = Request(baseurl)
                # 페킷에 헤더 추가하기
                request.add_header("X-Naver-Client-Id", client_id)
                request.add_header("X-Naver-Client-Secret", client_secret)
                response = urlopen(request, data=dataParmas.encode("utf-8"))

                responsedCode = response.getcode()
                if (responsedCode == 200):
                    response_body = response.read()
                    # response_body -> byte string : decode to utf-8
                    api_callResult = response_body.decode('utf-8')

                    # JSON 타입의 정보가 출력. 그래서 다시 JSON 타입으로 변경(사전처럼)
                    api_callResult = json.loads(api_callResult)
                    # 최종 결과물
                    translatedText = api_callResult['message']['result']["translatedText"]
                    embed = discord.Embed(title="Translate | English -> Korean", description="", color=0x5CD1E5)
                    embed.add_field(name="English to translate", value=savedCombineword, inline=False)
                    embed.add_field(name="Translated Korean", value=translatedText, inline=False)
                    embed.set_thumbnail(url="https://papago.naver.com/static/img/papago_og.png")
                    embed.set_footer(text='by 설준서. API provided by Naver Open API',
                                     icon_url='https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2F20161011_288%2Fjasara59_1476165827672d3iAL_JPEG%2Fimage.jpg&type=sc960_832')
                    await message.channel.send("Translate complete", embed=embed)
                else:
                    await message.channel.send("Error Code : " + responsedCode)
        except HTTPError as e:
            await message.channel.send("Translate Failed. HTTPError Occured.")

    if message.content.startswith("!한일번역"):
        baseurl = "https://openapi.naver.com/v1/papago/n2mt"
        # 띄어쓰기 : split처리후 [1:]을 for문으로 붙인다.
        trsText = message.content.split(" ")
        try:
            if len(trsText) == 1:
                await message.channel.send("단어 혹은 문장이 입력되지 않았어요. 다시한번 확인해주세요.")
            else:
                trsText = trsText[1:]
                combineword = ""
                for word in trsText:
                    combineword += " " + word
                # 입력된 값이 문장인 경우 다시 조립하여 양쪽의 빈칸을 제거한다.
                savedCombineword = combineword.strip()
                combineword = quote(savedCombineword)
                # 쿼티 문자열을 만든다
                dataParmas = "source=ko&target=ja&text=" + combineword
                # Make a Request Instance
                request = Request(baseurl)
                # 페킷에 헤더 추가하기
                request.add_header("X-Naver-Client-Id", client_id)
                request.add_header("X-Naver-Client-Secret", client_secret)
                response = urlopen(request, data=dataParmas.encode("utf-8"))

                responsedCode = response.getcode()
                if (responsedCode == 200):
                    response_body = response.read()
                    # response_body -> byte string : decode to utf-8
                    api_callResult = response_body.decode('utf-8')

                    # JSON 타입의 정보가 출력. 그래서 다시 JSON 타입으로 변경(사전처럼)
                    api_callResult = json.loads(api_callResult)
                    # 최종 결과물
                    translatedText = api_callResult['message']['result']["translatedText"]
                    embed = discord.Embed(title="Translate | Korean -> Japanese", description="", color=0x5CD1E5)
                    embed.add_field(name="Korean to translate", value=savedCombineword, inline=False)
                    embed.add_field(name="Translated Japanese", value=translatedText, inline=False)
                    embed.set_thumbnail(url="https://papago.naver.com/static/img/papago_og.png")
                    embed.set_footer(text='by 설준서. API provided by Naver Open API',
                                     icon_url='https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2F20161011_288%2Fjasara59_1476165827672d3iAL_JPEG%2Fimage.jpg&type=sc960_832')
                    await message.channel.send("Translate complete", embed=embed)
                else:
                    await message.channel.send("Error Code : " + responsedCode)
        except HTTPError as e:
            await message.channel.send("Translate Failed. HTTPError Occured.")

    if message.content.startswith("!일한번역"):
        baseurl = "https://openapi.naver.com/v1/papago/n2mt"
        # 띄어쓰기 : split처리후 [1:]을 for문으로 붙인다.
        trsText = message.content.split(" ")
        try:
            if len(trsText) == 1:
                await message.channel.send("단어 혹은 문장이 입력되지 않았어요. 다시한번 확인해주세요.")
            else:
                trsText = trsText[1:]
                combineword = ""
                for word in trsText:
                    combineword += " " + word
                # 입력된 값이 문장인 경우 다시 조립하여 양쪽의 빈칸을 제거한다.
                savedCombineword = combineword.strip()
                combineword = quote(savedCombineword)
                # 쿼티 문자열을 만든다
                dataParmas = "source=ja&target=ko&text=" + combineword
                # Make a Request Instance
                request = Request(baseurl)
                # 페킷에 헤더 추가하기
                request.add_header("X-Naver-Client-Id", client_id)
                request.add_header("X-Naver-Client-Secret", client_secret)
                response = urlopen(request, data=dataParmas.encode("utf-8"))

                responsedCode = response.getcode()
                if (responsedCode == 200):
                    response_body = response.read()
                    # response_body -> byte string : decode to utf-8
                    api_callResult = response_body.decode('utf-8')

                    # JSON 타입의 정보가 출력. 그래서 다시 JSON 타입으로 변경(사전처럼)
                    api_callResult = json.loads(api_callResult)
                    # 최종 결과물
                    translatedText = api_callResult['message']['result']["translatedText"]
                    embed = discord.Embed(title="Translate | Japanese -> Korean", description="", color=0x5CD1E5)
                    embed.add_field(name="Japanese to translate", value=savedCombineword, inline=False)
                    embed.add_field(name="Translated Korean", value=translatedText, inline=False)
                    embed.set_thumbnail(url="https://papago.naver.com/static/img/papago_og.png")
                    embed.set_footer(text='by 설준서. API provided by Naver Open API',
                                     icon_url='https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2F20161011_288%2Fjasara59_1476165827672d3iAL_JPEG%2Fimage.jpg&type=sc960_832')
                    await message.channel.send("Translate complete", embed=embed)
                else:
                    await message.channel.send("Error Code : " + responsedCode)
        except HTTPError as e:
            await message.channel.send("Translate Failed. HTTPError Occured.")

    if message.content.startswith("!한중번역"):
        baseurl = "https://openapi.naver.com/v1/papago/n2mt"
        # 띄어쓰기 : split처리후 [1:]을 for문으로 붙인다.
        trsText = message.content.split(" ")
        try:
            if len(trsText) == 1:
                await message.channel.send("단어 혹은 문장이 입력되지 않았어요. 다시한번 확인해주세요.")
            else:
                trsText = trsText[1:]
                combineword = ""
                for word in trsText:
                    combineword += " " + word
                # 입력된 값이 문장인 경우 다시 조립하여 양쪽의 빈칸을 제거한다.
                savedCombineword = combineword.strip()
                combineword = quote(savedCombineword)
                # 쿼티 문자열을 만든다

                #중국어 간체자
                dataParmas = "source=ko&target=zh-CN&text=" + combineword

                # Make a Request Instance
                request = Request(baseurl)
                # 페켓에 헤더 추가하기
                request.add_header("X-Naver-Client-Id", client_id)
                request.add_header("X-Naver-Client-Secret", client_secret)
                response = urlopen(request, data=dataParmas.encode("utf-8"))

                responsedCode = response.getcode()
                if (responsedCode == 200):
                    response_body = response.read()
                    # response_body -> byte string : decode to utf-8
                    api_callResult = response_body.decode('utf-8')
                    # JSON 타입의 정보가 출력. 그래서 다시 JSON 타입으로 변경(사전처럼)
                    api_callResult = json.loads(api_callResult)
                    # 최종 결과물
                    translatedText = api_callResult['message']['result']["translatedText"]
                    embed = discord.Embed(title="Translate | Korean -> Chinese(Simplified Chinese)", description="", color=0x5CD1E5)
                    embed.add_field(name="Korean to translate", value=savedCombineword, inline=False)
                    embed.add_field(name="Translated Chinese(Simplified)", value=translatedText, inline=False)
                    embed.set_thumbnail(url="https://papago.naver.com/static/img/papago_og.png")
                    embed.set_footer(text='by 설준서. API provided by Naver Open API',
                                     icon_url='https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2F20161011_288%2Fjasara59_1476165827672d3iAL_JPEG%2Fimage.jpg&type=sc960_832')
                    await message.channel.send("Translate complete", embed=embed)
                else:
                    await message.channel.send("Error Code : " + responsedCode)
        except HTTPError as e:
            await message.channel.send("Translate Failed. HTTPError Occured.")

    if message.content.startswith("!중한번역"):
        baseurl = "https://openapi.naver.com/v1/papago/n2mt"
        # 띄어쓰기 : split처리후 [1:]을 for문으로 붙인다.
        trsText = message.content.split(" ")
        try:
            if len(trsText) == 1:
                await message.channel.send("단어 혹은 문장이 입력되지 않았어요. 다시한번 확인해주세요.")
            else:
                trsText = trsText[1:]
                combineword = ""
                for word in trsText:
                    combineword += " " + word
                # 입력된 값이 문장인 경우 다시 조립하여 양쪽의 빈칸을 제거한다.
                savedCombineword = combineword.strip()
                combineword = quote(savedCombineword)
                # 쿼티 문자열을 만든다
                # 중국어 간체자
                dataParmas = "source=zh-CN&target=ko&text=" + combineword


                # Make a Request Instance
                request = Request(baseurl)
                # add header to packet
                request.add_header("X-Naver-Client-Id", client_id)
                request.add_header("X-Naver-Client-Secret", client_secret)
                response = urlopen(request, data=dataParmas.encode("utf-8"))

                responsedCode = response.getcode()
                if (responsedCode == 200):
                    response_body = response.read()
                    # response_body -> byte string : decode to utf-8
                    api_callResult = response_body.decode('utf-8')
                    # JSON 타입의 정보가 출력. 그래서 다시 JSON 타입으로 변경(사전처럼)
                    api_callResult = json.loads(api_callResult)
                    # 최종 결과물
                    translatedText = api_callResult['message']['result']["translatedText"]
                    embed = discord.Embed(title="Translate | Chinese -> Korean", description="", color=0x5CD1E5)
                    embed.add_field(name="Chinese to translate", value=savedCombineword, inline=False)
                    embed.add_field(name="Translated Korean", value=translatedText, inline=False)
                    embed.set_thumbnail(url="https://papago.naver.com/static/img/papago_og.png")
                    embed.set_footer(text='by 설준서. API provided by Naver Open API',
                                     icon_url='https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2F20161011_288%2Fjasara59_1476165827672d3iAL_JPEG%2Fimage.jpg&type=sc960_832')
                    await message.channel.send("Translate complete", embed=embed)
                else:
                    await message.channel.send("Error Code : " + responsedCode)
        except HTTPError as e:
            await message.channel.send("Translate Failed. HTTPError Occured.")
access_token = os.environ["BOT_TOKEN"]
client.run(access_token)

