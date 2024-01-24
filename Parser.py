from telethon import TelegramClient, events
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import PeerChannel
import csv
import re

api_id = 2
api_hash = ''
phone = ''
sys_version= '4.16.30-vxCUSTO'


client  = TelegramClient(phone, api_id, api_hash, system_version = sys_version)
client.start()
 
chats = []
last_date = None
chunk_size = 200
groups=[]

result = client(GetDialogsRequest(
            offset_date=last_date,
            offset_id=0,
            offset_peer=InputPeerEmpty(),
            limit=chunk_size,
            hash = 0
        ))
chats.extend(result.chats)

'''for chat in chats:                      #добавление чатов в список
    try:
        #if chat.megagroup== True:
            groups.append(chat)
    except:
        continue
   
print("Выберите группу для парсинга сообщений и членов группы:")
i=0
for g in groups:
   print(str(i) + "- " + g.title)
   i+=1
g_index = input("Введите нужную цифру: ")
target_group=groups[int(g_index)] '''


offset_id = 0
limit = 1
all_messages = []
total_messages = 0
total_count_limit = 30
iterat = 1

@client.on(events.NewMessage(chats=19))

async def normal_handler(event):
    mes_id = event.message.to_dict()['id']
    messs = event.message.to_dict()['message']

    if (('Направление'in messs) and ('Цели' in messs)):
        match = re.search(r'(?s)^(.*?Цели[\s\S]*?)\n\n', messs)
        if match:
           extracted_text = match.group(1)
           with open("message_signal.csv", "w", encoding="UTF-8") as f:
            writer=csv.writer(f, delimiter=",", lineterminator="\n")
            writer.writerow([extracted_text])

    elif (('Направление'in messs) and  ('Тейк' in messs)):
        match = re.search(r'(?s)^(.*?Тейк[\s\S]*?)\n\n', messs)
        if match:
           extracted_text = match.group(1)
           with open("message_signal.csv", "w", encoding="UTF-8") as f:
            writer=csv.writer(f, delimiter=",", lineterminator="\n")
            writer.writerow([extracted_text])

            

'''
while True:
   history = client(GetHistoryRequest(
       peer=1968591334,
       offset_id=offset_id,
       offset_date=None,
       add_offset=0,
       limit=limit,
       max_id=0,
       min_id=0,
       hash=0
   ))
   if not history.messages:
       break
   messages = history.messages
   for message in messages:
       all_messages.append(message)
   offset_id = messages[len(messages) - 1].id
   total_messages+=1
   if total_count_limit != 0 and total_messages >= total_count_limit:
       break

all_messages.reverse()'''


client.run_until_disconnected()



