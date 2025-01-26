import os
import csv
import datetime

class LogManager:
    def __init__(self, log_file_name="everytime_autoLike_log.csv"):
        self.log_file = os.path.join(os.getcwd(), log_file_name)
        
        # 파일이 없을 때 헤더 추가
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Timestamp', 'level', 'module', 'message', 'details'])

    def append_log_msg(self, level, module, message, details):
        now = datetime.datetime.now()
        nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')
        log_data = [nowDatetime, level, module, message, details]
        with open(self.log_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(log_data)
    
    def read_log(self):
        try:
            with open(self.log_file, 'r', encoding="utf-8") as file:
                logs = list(csv.reader(file))
                return sorted(logs[1:], key=lambda x: x[0])  # 헤더 제외 후 정렬
        except FileNotFoundError:
            print("Log file not found.")
            return []
        except Exception as e:
            print(f"Error reading log file: {e}")
            return []
    
    def clear_log(self):
        if os.path.exists(self.log_file):
            os.remove(self.log_file)
            print("Log file cleared.")
        else:
            print("Log file does not exist.")

    def log_info(self, module, message, details=""):
        return self.append_log_msg(level="INFO", module=module, message=message, details=details)

    def log_error(self, module, message, details=""):
        return self.append_log_msg(level="ERROR", module=module, message=message, details=details)
