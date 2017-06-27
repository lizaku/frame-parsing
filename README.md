## Репозиторий с файлами проекта "Фрейм-парсер".

### Скрипты:
* [parse_framebank.py](https://github.com/ElizavetaKuzmenko/frame-parsing/blob/master/parse_framebank.py) - обрабатывает Фреймбанк (совмещает примеры и разметку ролей) и переводит его в табличную форму. Этот скрипт использует файлы [exampleindex.csv](https://cloud.mail.ru/public/8SfR/AEDFqVAf4) и [framebank_anno_ex_items_fixed.txt](https://cloud.mail.ru/public/4LwA/1eKkTMfAQ).
* [create_features.py](https://github.com/ElizavetaKuzmenko/frame-parsing/blob/master/create_features.py) - превращает данные фреймбанка в таблички с фичами для классификаторов. Можно генерировать таблички для распознавания предикатов и их аргументов, а также для классификации уже распознанных аргументов по ролям. Фичи такие:
       * морфология (часть речи, грамматические признаки текущего и предыдущего слова)
       * лексическая информация (лемма слова, лемма предыдущего слова)
       * синтаксическая информация (длина пути от корня до текущего слова, синтО между текущим словом и его родителем, лемма предиката). Синтаксическая информация берётся из [модели](https://github.com/ElizavetaKuzmenko/frame-parsing/blob/master/ru.udpipe), обученной на [UD for Russian](https://github.com/UniversalDependencies/UD_Russian)
* [classify.py](https://github.com/ElizavetaKuzmenko/frame-parsing/blob/master/classify.py) - классифицирует данные при помощи SGDClassifier.
* [parser.py](https://github.com/ElizavetaKuzmenko/frame-parsing/blob/master/parser.py) - полный пайплайн, от текста, введенного пользователем, к ролям. Использует натренированные модели, которые создаются скриптом classify.py ([frame_parser.pkl](https://github.com/ElizavetaKuzmenko/frame-parsing/blob/master/frame_parser.pkl) и [feature_transformer.pkl](https://github.com/ElizavetaKuzmenko/frame-parsing/blob/master/feature_transformer.pkl))
       
Результаты распознавания предикатов и аргументов:

![alt-text](https://github.com/ElizavetaKuzmenko/frame-parsing/blob/master/predicates_and_arguments.png "Метрики качества")


Результаты по ролям:

![alt-text](https://github.com/ElizavetaKuzmenko/frame-parsing/blob/master/ml.png "Метрики качества по ролям")
