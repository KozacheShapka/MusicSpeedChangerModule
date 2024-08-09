from hikkatl.types import Message
from .. import loader, utils
from telethon import types
import string
import random
import os
import eyed3
import cv2

# requires: opencv-python eyed3
# and requires ffmpeg in system
# meta developer: @MusicSpeedChangerModule

@loader.tds
class MusicSpeedChanger(loader.Module):
    """v20240809.beta - Changes speed of music"""
    prefix = '[Music Speed Changer]'

    strings = {
        "name": "MusicSpeedChanger",
        'downloading': f'{prefix} Downloading...',
        'working': f'{prefix} Working...',
        'sending': f'{prefix} Sending...',
        'error': f'{prefix} Error... :(',
        'no_args_speed': f'{prefix} Not specified speed',
        'no_args_pitch': f'{prefix} Not specified pitch',
        'no_args_bass': f'{prefix} Not specified bass',
        'no_args_volume': f'{prefix} Not specified volume',
        'no_args_rate': f'{prefix} Not specified rate',
        'no_args': f'{prefix} Arguments not specified',
        'no_reply': f'{prefix} Need to reply to audio or voice',
        'no_effect': f'{prefix} This effect does not exist',
        'effects': f'{prefix} Available effects: \n\n⏩nc or nightcore - NightCore\n⏳dc or daycore - DayCore',
        'bass_too_high': f'{prefix} Value too high. Max: 18',
        'bass_too_low': f'{prefix} Value too low. Min: 2',
        'rate_too_high': f'{prefix} Value too high. Max: 2.00',
        'rate_too_low': f'{prefix} Value too low. Min: 0.50',
        'volume_too_high': f'{prefix} Value too high. Max: 2.00',
        'volume_too_low': f'{prefix} Value too low. Min: 0.01',
        'pitch_too_high': f'{prefix} Value too high. Max: 2.00',
        'pitch_too_low': f'{prefix} Value too low. Min: 0.50',
        'speed_too_high': f'{prefix} Value too high. Max: 2.00',
        'speed_too_low': f'{prefix} Value too low. Min: 0.50',
        '1': '1',
        '2': '2',
        '3': '3',
        '4': '4',
    }
    
    strings_ru = {
        'downloading': f'{prefix} Скачиваю...',
        'working': f'{prefix} Работаю...',
        'sending': f'{prefix} Отправляю...',
        'error': f'{prefix} Произошла ошибка... :(',
        'no_args_speed': f'{prefix} Не указана скорость',
        'no_args_pitch': f'{prefix} Не указан тон',
        'no_args_bass': f'{prefix} Не указан басс',
        'no_args_volume': f'{prefix} Не указана громкость',
        'no_args_rate': f'{prefix} Не указан рейт',
        'no_args': f'{prefix} Аргументы не указаны',
        'no_reply': f'{prefix} Нужно ответить на аудио или войс',
        'no_effect': f'{prefix} Такого эффекта не существует',
        'effects': f'{prefix} Доступные эффекты: \n\n⏩nc или nightcore - NightCore\n⏳dc или daycore - DayCore',
        'bass_too_high': f'{prefix} Значение слишком высокое допустимого. Максимально: 25',
        'bass_too_low': f'{prefix} Значение слишком низкое допустимого. Минимально: 2',
        'rate_too_high': f'{prefix} Значение слишком высокое допустимого. Максимально: 2.00',
        'rate_too_low': f'{prefix} Значение слишком низкое допустимого. Минимально: 0.50',
        'volume_too_high': f'{prefix} Значение слишком высокое допустимого. Максимально: 1.50',
        'volume_too_low': f'{prefix} Значение слишком низкое допустимого. Минимально: 0.01',
        'pitch_too_high': f'{prefix} Значение слишком высокое допустимого. Максимально: 2.00',
        'pitch_too_low': f'{prefix} Значение слишком низкое допустимого. Минимально: 0.50',
        'speed_too_high': f'{prefix} Значение слишком высокое допустимого. Максимально: 2.00',
        'speed_too_low': f'{prefix} Значение слишком низкое допустимого. Минимально: 0.50',
        '1': '1',
        '2': '2',
        '3': '3',
        '4': '4',
    }
    
    strings_ua = {
        'downloading': f'{prefix} Завантажую...',
        'working': f'{prefix} Працюю...',
        'sending': f'{prefix} Відправляю...',
        'error': f'{prefix} Помилка... :(',
        'no_args_speed': f'{prefix} Не вказано швидкість',
        'no_args_pitch': f'{prefix} Не вказано тональність',
        'no_args_bass': f'{prefix} Не вказан бас',
        'no_args_volume': f'{prefix} Не вказано гучність',
        'no_args_rate': f'{prefix} Не вказан рейт',
        'no_args': f'{prefix} Аргументи не вказані',
        'no_reply': f'{prefix} Потрібно відповісти на аудіо чи войс',
        'no_effect': f'{prefix} Такого ефекту не існує',
        'effects': f'{prefix} Доступні ефекти: \n\n⏩nc або nightcore - NightCore\n⏳dc або daycore - DayCore',
        'bass_too_high': f'{prefix} Значення занадто високе допустимого. Максимально: 18',
        'bass_too_low': f'{prefix} Значення занадто низьке допустимого. Мінімально: 2',
        'rate_too_high': f'{prefix} Значення занадто високе допустимого. Максимально: 2.00',
        'rate_too_low': f'{prefix} Значення занадто низьке допустимого. Мінімально: 0.50',
        'volume_too_high': f'{prefix} Значення занадто високе допустимого. Максимально: 1.50',
        'volume_too_low': f'{prefix} Значення занадто низьке допустимого. Мінімально: 0.01',
        'pitch_too_high': f'{prefix} Значення занадто високе допустимого. Максимально: 2.00',
        'pitch_too_low': f'{prefix} Значення занадто низьке допустимого. Мінімально: 0.50',
        'speed_too_high': f'{prefix} Значення занадто високе допустимого. Максимально: 2.00',
        'speed_too_low': f'{prefix} Значення занадто низьке допустимого. Мінімально: 0.50',
        '1': '1',
        '2': '2',
        '3': '3',
        '4': '4',
    }
    
    async def get_performer_title(self, reply, message):
        
        if reply and reply.file and reply.file.mime_type.split("/")[0] == "audio":
            performer = "Неизвестен"
            title = "Неизвестен"
            messages = await message.client.get_messages(reply.chat_id, ids=[reply.id])
            if messages:
                message_with_audio = messages[0]
                if message_with_audio.media and hasattr(message_with_audio.media, 'document'):
                    audio = message_with_audio.media.document
                    for attribute in audio.attributes:
                        if isinstance(attribute, types.DocumentAttributeAudio):
                            if attribute.performer:
                                performer = attribute.performer
                            if attribute.title:
                                title = attribute.title
                            duration = attribute.duration
                                
            return {'performer': performer, 'title': title, 'duration': duration}
            
    
    async def get_info_file(self, filename: str, filetype: str):
        if filetype == "audio":
            audiofile = eyed3.load(filename)
            song_length_seconds = audiofile.info.time_secs
            duration = int(song_length_seconds)
        
            return {'duration': duration}
        elif filetype == "video":
            cap = cv2.VideoCapture(filename)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            duration = int(frame_count / fps)
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            cap.release()
            return {'duration': duration, 'height': height, 'width': width}
        
    
    async def change_speed(self, request_type: str, filename: str, filetype: str, speed: float, performer: str = None, title: str = None):
        
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        outputfile = f'{performer or title}-{random_string}-(rate {speed}).mp3'
        new_performer = f'{performer or title}'
        if request_type == 'rate':
            if filetype == 'audio':
                new_title = f'{title} (rate {speed})'
                os.system(f'ffmpeg -i "{filename}" -filter:a "aresample=44100,asetrate=44100*{speed}" -b:a 320k -metadata artist="{new_performer}" -metadata title="{new_title}" "{outputfile}"')
            if filetype == 'video':
                outputfile = f'video-{random_string}-(rate {speed}).mp4'
                os.system(f'ffmpeg -i "{filename}" -vf "setpts=PTS/{speed}" -af "rubberband=tempo={speed}:pitch={speed}" -c:a libmp3lame -b:a 192k "{outputfile}"')
        elif request_type == 'speed':
            new_title = f'{title} (speed {speed})'
            if filetype == 'audio':
                outputfile = f'{performer or title}-{random_string}-(speed {speed}).mp3'
                os.system(f'ffmpeg -i "{filename}" -filter:a "aresample=44100,atempo={speed}" -b:a 320k -metadata artist="{new_performer}" -metadata title="{new_title}" "{outputfile}"')
            elif filetype == 'video':
                outputfile = f'video-{random_string}-(speed {speed}).mp4'
                os.system(f'ffmpeg -i "{filename}" -vf "setpts=PTS/{speed}" -af "rubberband=tempo={speed}" -c:a libmp3lame -b:a 192k "{outputfile}"')
                
        elif request_type.startswith('effect-'):
            effect = request_type.split('-')[1]
            if effect == 'nc':
                if filetype == 'audio':
                    new_title = f'{title} (nightcore)'
                    outputfile = f'{performer or title}-{random_string}-(nightcore).mp3'
                    os.system(f'ffmpeg -i "{filename}" -af "aresample=44100,asetrate=44100*{speed}" -b:a 320k -metadata artist="{new_performer}" -metadata title="{new_title}" "{outputfile}"')
                elif filetype == 'video':
                    new_title = f'{title} (nightcore)'
                    outputfile = f'video-{random_string}-(nightcore).mp4'
                    os.system(f'ffmpeg -i "{filename}" -vf "setpts=PTS/{speed}" -af "rubberband=tempo={speed}:pitch={speed}" -c:a libmp3lame -b:a 192k "{outputfile}"')
            elif effect == 'dc':
                if filetype == 'audio':
                    new_title = f'{title} (daycore)'
                    outputfile = f'{performer or title}-{random_string}-(daycore).mp3'
                    os.system(f'ffmpeg -i "{filename}" -af "aresample=44100,asetrate=44100*{speed}" -b:a 320k -metadata artist="{new_performer}" -metadata title="{new_title}" "{outputfile}"')
                elif filetype == 'video':
                    new_title = f'{title} (daycore)'
                    outputfile = f'video-{random_string}-(daycore).mp4'
                    os.system(f'ffmpeg -i "{filename}" -vf "setpts=PTS/{speed}" -af "rubberband=tempo={speed}:pitch={speed}" -c:a libmp3lame -b:a 192k "{outputfile}"')
        
        if filetype == 'audio':
            getinfo = await self.get_info_file(filename=outputfile, filetype="audio")
            return {'filename': outputfile, 'performer': new_performer, 'title': new_title, 'duration': getinfo['duration']}
        elif filetype == 'video':
            getinfo = await self.get_info_file(filename=outputfile, filetype="video")
            return {'filename': outputfile, 'height': getinfo['height'], 'width': getinfo['width'], 'duration': getinfo['duration']}
            
    async def change_pitch(self, filename: str, filetype: str, pitch: float, performer: str = None, title: str = None):
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        if filetype == "audio":
            outputfile = f'{performer or title}-{random_string}-(pitch {pitch}).mp3'
            new_performer = f'{performer or title}'
            new_title = f'{title} (pitch {pitch})'
            os.system(f'ffmpeg -i "{filename}" -af "rubberband=pitch={pitch}" -b:a 320k -metadata artist="{new_performer}" -metadata title="{new_title}" "{outputfile}"')
            
            sec = await self.get_info_file(filename=outputfile, filetype="audio")
            
            return {'filename': outputfile, 'performer': new_performer, 'title': new_title, 'duration': sec['duration']}
        elif filetype == "video":
            outputfile = f'{performer or title}-{random_string}-(pitch {pitch}).mp4'
            os.system(f'ffmpeg -i "{filename}" -af "rubberband=pitch={pitch}" -c:a libmp3lame -b:a 192k "{outputfile}"')
            
            getinfo = await self.get_info_file(filename=outputfile, filetype="video")
            return {'filename': outputfile, 'height': getinfo['height'], 'width': getinfo['width'], 'duration': getinfo['duration']}
    
    async def change_bass(self, filename: str, filetype: str, bass: int, performer: str = None, title: str = None):
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        if filetype == "audio":
            outputfile = f'{performer or title}-{random_string}-(bass {bass}db).mp3'
            new_performer = f'{performer or title}'
            new_title = f'{title} (bass {bass})'
            os.system(f'ffmpeg -i "{filename}" -af "bass=g={bass}:f=105:m=1.00,acompressor=threshold=-4dB:ratio=4:attack=10:release=2000:makeup=1.6" -b:a 320k "{outputfile}"')
            
            sec = await self.get_info_file(outputfile, filetype="audio")
            
            return {'filename': outputfile, 'performer': new_performer, 'title': new_title, 'duration': sec['duration']}
        elif filetype == "video":
            outputfile = f'video-{random_string}-(bass {bass}db).mp4'
            os.system(f'ffmpeg -i "{filename}" -af "bass=g={bass}:f=105:m=1.00,acompressor=threshold=-4dB:ratio=4:attack=10:release=2000:makeup=1.6" -c:a libmp3lame -b:a 192k "{outputfile}"')
             
            getinfo = await self.get_info_file(filename=outputfile, filetype="video")
            return {'filename': outputfile, 'height': getinfo['height'], 'width': getinfo['width'], 'duration': getinfo['duration']}
            
            
    async def change_volume(self, filename: str, filetype: str, volume: float, performer: str = None, title: str = None):
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        if filetype == "audio":
            outputfile = f'{performer or title}-{random_string}-(volume {volume}db).mp3'
            new_performer = f'{performer or title}'
            new_title = f'{title} (volume {volume})'
            os.system(f'ffmpeg -i "{filename}" -af "volume={volume}" -b:a 320k -metadata artist="{new_performer}" -metadata title="{new_title}" "{outputfile}"')
            
            sec = await self.get_info_file(outputfile, filetype="audio")
            
            return {'filename': outputfile, 'performer': new_performer, 'title': new_title, 'duration': sec['duration']}
        
        elif filetype == "video":
            outputfile = f'video-{random_string}-(volume {volume}db).mp4'
            os.system(f'ffmpeg -i "{filename}" -af "volume={volume}" -b:a 320k "{outputfile}"')

             
            getinfo = await self.get_info_file(filename=outputfile, filetype="video")
            return {'filename': outputfile, 'height': getinfo['height'], 'width': getinfo['width'], 'duration': getinfo['duration']}
            
    async def reverse(self, filename: str, filetype: str,performer: str = None, title: str = None):
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        if filetype == "audio":
            outputfile = f'{performer or title}-{random_string}-reversed.mp3'
            new_performer = f'{performer or title}'
            new_title = f'{title} (reversed)'
            os.system(f'ffmpeg -i "{filename}" -af "areverse" -b:a 320k -metadata artist="{performer}" -metadata artist="{new_performer}" -metadata title="{new_title}" "{outputfile}"')
            
            sec = await self.get_info_file(outputfile, filetype="audio")
            
            return {'filename': outputfile, 'performer': new_performer, 'title': new_title, 'duration': sec['duration']}
        elif filetype == "video":
            outputfile = f'video-{random_string}-reversed.mp4'
            os.system(f'ffmpeg -i "{filename}" -vf reverse -af "areverse" -b:a 192k "{outputfile}"')
            
             
            getinfo = await self.get_info_file(filename=outputfile, filetype="video")
            return {'filename': outputfile, 'height': getinfo['height'], 'width': getinfo['width'], 'duration': getinfo['duration']}
            
    async def apply_effects(self, request_type: str, filename: str, filetype: str, performer: str = None, title: str = None):
        if request_type == 'nightcore':
            if filetype == 'audio':
                proc = await self.change_speed(request_type='effect-nc', filename=filename, filetype=filetype, speed=1.5, performer=performer, title=title)   
                return {'filename': proc['filename'], 'performer': proc['performer'], 'title': proc['title'], 'duration': proc['duration']} 
            elif filetype == 'video':
                proc = await self.change_speed(request_type='effect-nc', filename=filename, filetype=filetype, speed=1.5)
                return {'filename': proc['filename'], 'height': proc['height'], 'width': proc['width'], 'duration': proc['duration']}
        elif request_type == 'daycore':
            if filetype == 'audio':
                proc = await self.change_speed(request_type='effect-dc', filename=filename, filetype=filetype, speed=0.75, performer=performer, title=title)
                return {'filename': proc['filename'], 'performer': proc['performer'], 'title': proc['title'], 'duration': proc['duration']}
            elif filetype == 'video':
                proc = await self.change_speed(request_type='effect-dc', filename=filename, filetype=filetype, speed=0.75)
                return {'filename': proc['filename'], 'height': proc['height'], 'width': proc['width'], 'duration': proc['duration']}
        
    @loader.command(
        en_doc="<arg> <reply> Speed up or slow down the audio with the tonality. 1.00 = 1x",
        ru_doc="<arg> <reply> Ускорить или замедлить аудио с привязкой тональности. 1.00 = 1x",
        ua_doc="<arg> <reply> Збільшує або зменшує аудіо з прив'язаною тональністю. 1.00 = 1x",
    )
    async def ratecmd(self, message):
        args = message.text.split(' ')[1:]
        reply = await message.get_reply_message()
        if not args:
            await utils.answer(message, self.strings('no_args'))
            return
        
        if float(args[0]) >= 2.01:
            await utils.answer(message, self.strings('rate_too_high'))
            return
        
        if float(args[0]) <= 0.49:
            await utils.answer(message, self.strings('rate_too_low'))
            return
        
        if reply and reply.file and reply.file.mime_type.split("/")[0] == "audio":
            
            
            random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            tg_file_info = await self.get_performer_title(reply, message)
        
            file_name = f'{tg_file_info["performer"] or tg_file_info["title"]}-{random_string}.mp3'
        
            downloading = await utils.answer(message, self.strings('downloading'))
            await reply.download_media(file=file_name)
        
            processing = await utils.answer(downloading, self.strings('working'))
            proc = await self.change_speed(request_type='rate', filename=file_name, filetype="audio", speed=args[0], performer=tg_file_info['performer'], title=tg_file_info['title'])
        
            sending = await utils.answer(processing, self.strings('sending'))
            await utils.answer_file(message, proc['filename'], voice_note=True, attributes=[types.DocumentAttributeAudio(duration=proc['duration'], performer=proc['performer'], title=proc['title'])], reply_to=reply.id)
            await sending.delete()
            
        elif reply and reply.file and reply.file.mime_type.split("/")[0] == "video":
            
            random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        
            file_name = f'video-{random_string}.mp4'
        
            downloading = await utils.answer(message, self.strings('downloading'))
            await reply.download_media(file=file_name)
            
            processing = await utils.answer(downloading, self.strings('working'))
            proc = await self.change_speed(request_type='rate', filename=file_name, filetype="video", speed=args[0])
            sending = await utils.answer(processing, self.strings('sending'))
            await utils.answer_file(message, proc['filename'], attributes=[types.DocumentAttributeVideo(duration=proc['duration'], w=proc['width'], h=proc['height'])], reply_to=reply.id)
            await sending.delete()
        
        os.remove(file_name)
        os.remove(proc['filename'])
            
        
    
    @loader.command(
        en_doc="<arg> <reply> speed up or slow down the song with the tonality of the audio. 1.00 = 1x",
        ru_doc="<arg> <reply> Ускорить или замедлить аудио. 1.00 = 1x",
        ua_doc="<arg> <reply> Збільшує або зменшує аудіо. 1.00 = 1x",
    )    
    async def speedcmd(self, message):
        args = message.text.split(' ')[1:]
        reply = await message.get_reply_message()
        if not args:
            await utils.answer(message, self.strings('no_args'))
            return
        
        if float(args[0]) >= 2.01:
            await utils.answer(message, self.strings('speed_too_high'))
            return
        
        if float(args[0]) <= 0.49:
            await utils.answer(message, self.strings('speed_too_low'))
            return
        
        if reply and reply.file and reply.file.mime_type.split("/")[0] == "audio":
            
            
            random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            tg_file_info = await self.get_performer_title(reply, message)
        
            file_name = f'{tg_file_info["performer"] or tg_file_info["title"]}-{random_string}.mp3'
        
            downloading = await utils.answer(message, self.strings('downloading'))
            await reply.download_media(file=file_name)
        
            processing = await utils.answer(downloading, self.strings('working'))
            proc = await self.change_speed(request_type='speed', filename=file_name, filetype="audio", speed=args[0], performer=tg_file_info['performer'], title=tg_file_info['title'])
        
            sending = await utils.answer(processing, self.strings('sending'))
            await utils.answer_file(message, proc['filename'], voice_note=True, attributes=[types.DocumentAttributeAudio(duration=proc['duration'], performer=proc['performer'], title=proc['title'])], reply_to=reply.id)
            await sending.delete()
            
        elif reply and reply.file and reply.file.mime_type.split("/")[0] == "video":
            
            random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        
            file_name = f'video-{random_string}.mp4'
        
            downloading = await utils.answer(message, self.strings('downloading'))
            await reply.download_media(file=file_name)
            
            processing = await utils.answer(downloading, self.strings('working'))
            proc = await self.change_speed(request_type='speed', filename=file_name, filetype="video", speed=args[0])
            sending = await utils.answer(processing, self.strings('sending'))
            await utils.answer_file(message, proc['filename'], attributes=[types.DocumentAttributeVideo(duration=proc['duration'], w=proc['width'], h=proc['height'])], reply_to=reply.id)
            await sending.delete()
            
        os.remove(file_name)
        os.remove(proc['filename'])
    
    @loader.command(
        en_doc="<arg> <reply> Increase or decrease the tonality of the audio. 1.00 = normal",
        ru_doc="<arg> <reply> Увелить или уменьшить тональность аудио. 1.00 = normal",
        ua_doc="<arg> <reply> Збільшує або зменшує тональність аудіо. 1.00 = normal",
    )    
    async def pitchcmd(self, message):
        args = message.text.split(' ')[1:]
        reply = await message.get_reply_message()
        if not args:
            await utils.answer(message, self.strings('no_args'))
            return
        
        if float(args[0]) >= 2.01:
            await utils.answer(message, self.strings('pitch_too_high'))
            return
        
        if float(args[0]) <= 0.49:
            await utils.answer(message, self.strings('pitch_too_low'))
            return
        
        if reply and reply.file and reply.file.mime_type.split("/")[0] == "audio":
            
            
            random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            tg_file_info = await self.get_performer_title(reply, message)
        
            file_name = f'{tg_file_info["performer"] or tg_file_info["title"]}-{random_string}.mp3'
        
            downloading = await utils.answer(message, self.strings('downloading'))
            await reply.download_media(file=file_name)
        
            processing = await utils.answer(downloading, self.strings('working'))
            proc = await self.change_pitch(filename=file_name, filetype="audio", pitch=args[0], performer=tg_file_info['performer'], title=tg_file_info['title'])
        
            sending = await utils.answer(processing, self.strings('sending'))
            await utils.answer_file(message, proc['filename'], voice_note=True, attributes=[types.DocumentAttributeAudio(duration=proc['duration'], performer=proc['performer'], title=proc['title'])], reply_to=reply.id)
            await sending.delete()
            
        elif reply and reply.file and reply.file.mime_type.split("/")[0] == "video":
            
            random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        
            file_name = f'video-{random_string}.mp4'
        
            downloading = await utils.answer(message, self.strings('downloading'))
            await reply.download_media(file=file_name)
            
            processing = await utils.answer(downloading, self.strings('working'))
            proc = await self.change_pitch(filename=file_name, filetype="video", pitch=args[0])
            sending = await utils.answer(processing, self.strings('sending'))
            await utils.answer_file(message, proc['filename'], attributes=[types.DocumentAttributeVideo(duration=proc['duration'], w=proc['width'], h=proc['height'])], reply_to=reply.id)
            await sending.delete()

            
        os.remove(file_name)
        os.remove(proc['filename'])
    
    @loader.command(
        en_doc="<arg> <reply> Increase or decrease the bass of the audio. From 2 to 25",
        ru_doc="<arg> <reply> Увелить или уменьшить тональность аудио. От 2 до 25",
        ua_doc="<arg> <reply> Збільшує або зменшує тональність аудіо. Від 2 до 25",
    ) 
    async def basscmd(self, message):
        args = message.text.split(' ')[1:]
        reply = await message.get_reply_message()
        if not args:
            await utils.answer(message, self.strings('no_args'))
            return
        
        if int(args[0]) > 25:
            await utils.answer(message, self.strings('bass_too_high'))
            return
        
        if int(args[0]) <= 1:
            await utils.answer(message, self.strings('bass_too_low'))
            return
        
        if reply and reply.file and reply.file.mime_type.split("/")[0] == "audio":
            print('audio')
            
            
            random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            tg_file_info = await self.get_performer_title(reply, message)
        
            file_name = f'{tg_file_info["performer"] or tg_file_info["title"]}-{random_string}.mp3'
        
            downloading = await utils.answer(message, self.strings('downloading'))
            await reply.download_media(file=file_name)
        
            processing = await utils.answer(downloading, self.strings('working'))
            proc = await self.change_bass(filename=file_name, filetype="audio", bass=args[0], performer=tg_file_info['performer'], title=tg_file_info['title'])
        
            sending = await utils.answer(processing, self.strings('sending'))
            await utils.answer_file(message, proc['filename'], voice_note=True, attributes=[types.DocumentAttributeAudio(duration=proc['duration'], performer=proc['performer'], title=proc['title'])], reply_to=reply.id)
            await sending.delete()
        
            
        elif reply and reply.file and reply.file.mime_type.split("/")[0] == "video":
            
            random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        
            file_name = f'video-{random_string}.mp4'
        
            downloading = await utils.answer(message, self.strings('downloading'))
            await reply.download_media(file=file_name)
            
            processing = await utils.answer(downloading, self.strings('working'))
            proc = await self.change_bass(filename=file_name, filetype="video", bass=args[0])
            sending = await utils.answer(processing, self.strings('sending'))
            await utils.answer_file(message, proc['filename'], attributes=[types.DocumentAttributeVideo(duration=proc['duration'], w=proc['width'], h=proc['height'])], reply_to=reply.id)
            await sending.delete()
            
        os.remove(file_name)
        os.remove(proc['filename'])
    
    @loader.command(
        en_doc="<arg> <reply> Increase or decrease the volume of the audio. 1.00 = 100%",
        ru_doc="<arg> <reply> Увелить или уменьшить тональность аудио. 1.00 = 100%",
        ua_doc="<arg> <reply> Збільшує або зменшує тональність пісні. 1.00 = 100%",
    )  
    async def volumecmd(self, message):
        args = message.text.split(' ')[1:]
        reply = await message.get_reply_message()
        if not args:
            await utils.answer(message, self.strings('no_args'))
            return
        
        if float(args[0]) >= 2.01:
            await utils.answer(message, self.strings('volume_too_high'))
            return
        
        if float(args[0]) <= 0.00:
            await utils.answer(message, self.strings('volume_too_low'))
            return
        
        if reply and reply.file and reply.file.mime_type.split("/")[0] == "audio":
            
            
            random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            tg_file_info = await self.get_performer_title(reply, message)
        
            file_name = f'{tg_file_info["performer"] or tg_file_info["title"]}-{random_string}.mp3'
        
            downloading = await utils.answer(message, self.strings('downloading'))
            await reply.download_media(file=file_name)
        
            processing = await utils.answer(downloading, self.strings('working'))
            proc = await self.change_volume(filename=file_name, filetype="audio", volume=args[0], performer=tg_file_info['performer'], title=tg_file_info['title'])
        
            sending = await utils.answer(processing, self.strings('sending'))
            await utils.answer_file(message, proc['filename'], voice_note=True, attributes=[types.DocumentAttributeAudio(duration=proc['duration'], performer=proc['performer'], title=proc['title'])], reply_to=reply.id)
            await sending.delete()

        elif reply and reply.file and reply.file.mime_type.split("/")[0] == "video":
            
            random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        
            file_name = f'video-{random_string}.mp4'
        
            downloading = await utils.answer(message, self.strings('downloading'))
            await reply.download_media(file=file_name)
            
            processing = await utils.answer(downloading, self.strings('working'))
            proc = await self.change_volume(filename=file_name, filetype="video", volume=args[0])
            sending = await utils.answer(processing, self.strings('sending'))
            await utils.answer_file(message, proc['filename'], attributes=[types.DocumentAttributeVideo(duration=proc['duration'], w=proc['width'], h=proc['height'])], reply_to=reply.id)
            await sending.delete()

            
        os.remove(file_name)
        os.remove(proc['filename'])
        
        
    @loader.command(
        en_doc="<reply> Reverse the audio",
        ru_doc="<reply> Отреверсить аудио",
        ua_doc="<reply> Перевернути аудіо",
    )  
    async def reversecmd(self, message):
        reply = await message.get_reply_message()
        
        if reply and reply.file and reply.file.mime_type.split("/")[0] == "audio":
            
            
            random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            tg_file_info = await self.get_performer_title(reply, message)
        
            file_name = f'{tg_file_info["performer"] or tg_file_info["title"]}-{random_string}.mp3'
        
            downloading = await utils.answer(message, self.strings('downloading'))
            await reply.download_media(file=file_name)
        
            processing = await utils.answer(downloading, self.strings('working'))
            proc = await self.reverse(filename=file_name, filetype="audio", performer=tg_file_info['performer'], title=tg_file_info['title'])
        
            sending = await utils.answer(processing, self.strings('sending'))
            await utils.answer_file(message, proc['filename'], voice_note=True, attributes=[types.DocumentAttributeAudio(duration=proc['duration'], performer=proc['performer'], title=proc['title'])], reply_to=reply.id)
            await sending.delete()

            
        elif reply and reply.file and reply.file.mime_type.split("/")[0] == "video":
            
            random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        
            file_name = f'video-{random_string}.mp4'
        
            downloading = await utils.answer(message, self.strings('downloading'))
            await reply.download_media(file=file_name)
            
            processing = await utils.answer(downloading, self.strings('working'))
            proc = await self.reverse(filename=file_name, filetype="video")
            sending = await utils.answer(processing, self.strings('sending'))
            await utils.answer_file(message, proc['filename'], attributes=[types.DocumentAttributeVideo(duration=proc['duration'], w=proc['width'], h=proc['height'])], reply_to=reply.id)
            await sending.delete()

        
        os.remove(file_name)
        os.remove(proc['filename'])
        
    
    @loader.command(
        en_doc="<arg> <reply> Add or remove effects to the audio",
        ru_doc="<arg> <reply> Добавить или удалить эффекты в аудио",
        ua_doc="<arg> <reply> Додати або видалити ефекти до аудіо",
    )  
    async def effectcmd(self, message):
        args = message.text.split(' ')[1:]
        reply = await message.get_reply_message()
        if not args:
            await utils.answer(message, self.strings('effects'))
            return
        
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        tg_file_info = await self.get_performer_title(reply, message)
        if reply and reply.file and reply.file.mime_type.split("/")[0] == "audio":
        
            file_name = f'{tg_file_info["performer"] or tg_file_info["title"]}-{random_string}.mp3'
            
            downloading = await utils.answer(message, self.strings('downloading'))
            await reply.download_media(file=file_name)
            
            if args[0] in ['nc', 'nightcore']:
                
            
                processing = await utils.answer(downloading, self.strings('working'))
                proc = await self.apply_effects(filename=file_name, request_type='nightcore', filetype='audio', performer=tg_file_info['performer'], title=tg_file_info['title'])
                
            elif args[0] in ['dc', 'daycore']:
                
                processing = await utils.answer(downloading, self.strings('working'))
                proc = await self.apply_effects(filename=file_name, request_type='daycore', filetype='audio', performer=tg_file_info['performer'], title=tg_file_info['title'])
                
            
            sending = await utils.answer(processing, self.strings('sending'))
            await utils.answer_file(message, proc['filename'], voice_note=True, attributes=[types.DocumentAttributeAudio(duration=proc['duration'], performer=proc['performer'], title=proc['title'])], reply_to=reply.id)
            await sending.delete()
        elif reply and reply.file and reply.file.mime_type.split("/")[0] == "video":
            file_name = f'video-{random_string}.mp4'
            
            downloading = await utils.answer(message, self.strings('downloading'))
            await reply.download_media(file=file_name)
            
            if args[0] in ['nc', 'nightcore']:
                
            
                processing = await utils.answer(downloading, self.strings('working'))
                proc = await self.apply_effects(filename=file_name, request_type='nightcore', filetype='video')
                
            elif args[0] in ['dc', 'daycore']:
                
                processing = await utils.answer(downloading, self.strings('working'))
                proc = await self.apply_effects(filename=file_name, request_type='daycore', filetype='video')
                
            
            sending = await utils.answer(processing, self.strings('sending'))
            await utils.answer_file(message, proc['filename'], attributes=[types.DocumentAttributeVideo(duration=proc['duration'], w=proc['width'], h=proc['height'])], reply_to=reply.id)
            await sending.delete()
        
        os.remove(file_name)
        os.remove(proc['filename'])
    
