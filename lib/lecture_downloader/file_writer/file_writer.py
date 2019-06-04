import json

class FileWriter:

    def __init__(self, lecture_link_file) -> None:
        super().__init__()
        self.lecture_url_list = None
        self.default_file_name = lecture_link_file
        self.exclude_filename_characters = '<>|\\:&;: ' #<, >, |, \, :, (, ), &, ;,
        self.replaced_character = '_'*len(self.exclude_filename_characters)
        self.complete_lecture_url_list = None

    def setting_lecture_list(self, url_list):
        self.lecture_url_list = url_list
        return self

    def filter_pattern(self, row):
        lecture_name: str = row['title']
        transtab = str.maketrans(self.exclude_filename_characters, self.replaced_character)
        filtered_lecture_name = lecture_name.strip().translate(transtab)
        # 링크에서 윈도우 파일시스템 -> 파일명으로 불가능한 공백이나 슬래시 값들 대체
        row['title'] = filtered_lecture_name

        return row

    def do_file_name_filtering(self, target_list):
        return list(map(self.filter_pattern, target_list))

    def save_file(self):
        self.complete_lecture_url_list = self.do_file_name_filtering(self.lecture_url_list)

        with open(self.default_file_name, "w") as f:
            f.write(json.dumps(self.complete_lecture_url_list))

    def load_file(self):
        with open(self.default_file_name, "r") as f:
            self.lecture_url_list = json.loads(f.read())







