from noise_detection import *
from tqdm import tqdm
from bs4 import BeautifulSoup
import random


class RuleCleaner(object):
    def __init__(self, raw_code_list, raw_comment_list):
        """
        :param raw_code_list: list of raw code
        :param raw_comment_list: list of raw comments
        """
        assert len(raw_code_list) == len(raw_comment_list)
        self.raw_code_list = raw_code_list
        self.raw_comment_list = raw_comment_list
        self.output_dict = {}
        self.cleaned_code_list = []
        self.cleaned_comment_list = []
        # since detecting `Partial Sentence', `Verbose Sentence', `Over-Splitting' noise requires comparing
        # the updated comment with the benchmark comment, users can detect these noises using the functions defined
        # in the `noise_detection' file
        self.noisy_data = {'ContentTamper': [], 'NonLiteral': [], 'Interrogation': [], 'UnderDevelop': [],
                           'EmptyFunc': [], 'CommentOut': [], 'BlockComment': [], 'AutoCode': [], 'DuplicatedCode': []}

    def get_clean_data(self):
        count = 0
        for raw_code, raw_comment in tqdm(zip(self.raw_code_list, self.raw_comment_list)):
            firstSentence = getFirstSentence(raw_comment)
            updated_comment = self.update_ContentTamper(firstSentence)
            if updated_comment != firstSentence:
                self.noisy_data['ContentTamper'].append((raw_code, raw_comment))
            # remove rules
            if if_ContentTamper(updated_comment):
                self.noisy_data['ContentTamper'].append((raw_code, raw_comment))
                continue
            if if_NonLiteral(updated_comment):
                self.noisy_data['NonLiteral'].append((raw_code, raw_comment))
                continue
            if if_Interrogation(updated_comment):
                self.noisy_data['Interrogation'].append((raw_code, raw_comment))
                continue
            if if_UnderDevelop(updated_comment):
                self.noisy_data['UnderDevelop'].append((raw_code, raw_comment))
                continue
            if if_AutoCode_by_comment(updated_comment, raw_comment):
                self.noisy_data['AutoCode'].append((raw_code, raw_comment))
                continue

            if if_CommentedOut(raw_code):
                self.noisy_data['CommentOut'].append((raw_code, raw_comment))
                continue
            updated_code = self.update_BlockComment(raw_code)
            if if_AutoCode_by_code(updated_code):
                count += 1
                self.noisy_data['AutoCode'].append((raw_code, raw_comment))
                continue
            if updated_code != raw_code:
                self.noisy_data['BlockComment'].append((raw_code, raw_comment))
            if if_EmptyFunc(updated_code):
                self.noisy_data['EmptyFunc'].append((raw_code, raw_comment))
                continue

            if self.output_dict.get(updated_code) is None:
                self.output_dict[updated_code] = [updated_comment]
            else:
                self.output_dict[updated_code].append(updated_comment)
        # remove duplicated code
        for updated_code in self.output_dict:
            self.cleaned_code_list.append(updated_code)
            updated_comment_list = self.output_dict[updated_code]
            if len(updated_comment_list) > 1:
                self.noisy_data['DuplicatedCode'].append((updated_code, updated_comment_list))
                self.cleaned_comment_list.append(random.choice(updated_comment_list))
            else:
                self.cleaned_comment_list.append(updated_comment_list[0])

        return self.cleaned_code_list, self.cleaned_comment_list

    def get_noisy_data(self):
        return self.noisy_data

    def update_BlockComment(self, raw_code):
        p = re.compile('^(\s+//)|(//)')
        new_list = []
        for row in raw_code.split('\n'):
            if not p.search(row):
                new_list.append(row)
        return '\n'.join(new_list)

    def update_ContentTamper(self, comment):
        # we reject comments which contain javadocTag or url
        # And remove the htmlTag from the comments and retain the wrapped content
        return BeautifulSoup(comment, "html.parser").get_text()


if __name__ == '__main__':
    with open('./test.data', 'r') as f:
        data_lines = f.readlines()
    import json

    raw_code_list, raw_comment_list = [], []
    for line in data_lines:
        json_line = json.loads(line.strip())
        raw_code_list.append(json_line['raw_code'])
        raw_comment_list.append(json_line['raw_comment'])

    cleaner = RuleCleaner(raw_code_list, raw_comment_list)
    cleaned_code, cleaned_comment = cleaner.get_clean_data()
    print(len(cleaned_code))
    print(cleaner.get_noisy_data()['UnderDevelop'])
