import pyaudio
import wave
import paramiko
from scp import SCPClient
from datetime import datetime
import os


def record_audio(filename, duration=5, rate=22050):
    """Запись аудио 5 секунд"""
    chunk = 1024  # Размер фрейма
    format = pyaudio.paInt16  # Формат записи
    channels = 1  # Количество каналов (моно)
    
    p = pyaudio.PyAudio()

    stream = p.open(format=format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)

    print("-" * 50)
    print(f"Запись началась... Длительность записи: {duration} секунд")

    frames = []

    for i in range(0, int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    print("Запись завершена")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()


def transfer_file(local_filepath, remote_filepath, remote_host, remote_user, remote_password):
    """Отправка файла по SSH"""
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(remote_host, username=remote_user, password=remote_password)

    with SCPClient(ssh.get_transport()) as scp:
        scp.put(local_filepath, remote_filepath)
    print(f"Файл {local_filepath} передан успешно!")


def delete_file(filepath):
    """Удаление файла"""
    try:
        os.remove(filepath)
        print(f"Файл {filepath} удален успешно!")
    except OSError as e:
        print(f"Ошибка удаления файла {filepath} {e}")


def record_and_transmit_ssh():
    """Запись аудиофайла, передача его по SSH и последующее удаление (Объединяющая функция)"""
    # Получаем текущую временную метку и формируем имя файла
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    local_filepath = f'm1_{timestamp}.wav'

    # Передаем записанный файл на другой компьютер
    remote_host = '192.168.1.59'  # IP-адрес Windows-компьютера
    remote_user = 'AI-WIN'  # Имя пользователя на Windows
    remote_password = '123456'  # Пароль пользователя на Windows
    remote_filepath = f'D:/Exchange_folder/Audio_recieved/{local_filepath}'  # Путь на удаленном компьютере

    record_audio(local_filepath)  # Записываем аудио

    try:
        transfer_file(local_filepath, remote_filepath, remote_host, remote_user, remote_password)  # Передаем файл
    except Exception as e:
        print(f"Ошибка передачи файла {local_filepath}: {e}")
    finally:
        delete_file(local_filepath)  # Удаляем файл в любом случае
