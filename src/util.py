from io import DEFAULT_BUFFER_SIZE
import logging


def getLogger(name, *, level= logging.DEBUG, saveName= None, dir='log'):
    #フォーマットの定義
    formatter = logging.Formatter(
            '{asctime};{name};{levelname};{message}',
            style='{'
            )
    #ロガーの定義
    def_logger = logging.getLogger(name)
    def_logger.setLevel(level)
    #ファイル書き込み用
    fh = logging.FileHandler(f'{dir}/{saveName or name}.log', encoding='utf-8')
    fh.setFormatter(formatter)
    fh.setLevel(logging.NOTSET)
    def_logger.addHandler(fh)
    if not '.' in name:
        #最上位ロガー専用
        warnSaveName = f'{dir}/warning_{saveName or name}.log'
        fhw = logging.FileHandler(warnSaveName, encoding='utf-8')
        fhw.setFormatter(formatter)
        fhw.setLevel(logging.WARNING)
        #コンソール出力用
        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        sh.setLevel(logging.NOTSET)
        #それぞれロガーに追加
        def_logger.addHandler(sh)
        def_logger.addHandler(fhw)
    #return def_logger
    return def_logger


DEFAULT_PREFIX = '!'
with open('data/prefix.yaml')as f:
    prefix_dict = f.read()
def prefix(_,msg):
    if (id_ := msg.guild.id) in prefix_dict:
        return str(prefix_dict[id_])
    else:
        return DEFAULT_PREFIX
