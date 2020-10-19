# ASCII Art

### asciiart.py :

	Программа для преобразования изображения в ASCII Art

	Программа работает через консоль, имеет несколько входных параметров:

#### 	Обязательные:
		-i, --input  : исходный файл изображения

#### 	Необязательные:
		-o, --output : результат работы программы, в виде изображения
				(default : вывод в 
		-W, --width  : ширина преобразованного изображения
		-H, --height : высота преобразованного изображения
		-c, --contrast: уровень контрастности (до 255)
		--invert: инвертирование изображения

#### 	Примеры ввода:
		asciiart.py -i in.jpg
		asciiart.py -i in.jpg -o out.jpg -x 1500 -y 1500 -c 200 --invert
		asciiart.py --input in.jpg --output out.jpg --width 1500 --height 1500 --contrast 150

	Программа получается на вход изображение, результатом работы является текстовый файл

# Модули:

### CharDictionary:
	Создает файл chars.npy, в котором находятся все символы в байтовом виде.

### ImageConverter:
	1. Получает на вход изображение
	2. Изменяет параметры ширины и высоты относительно входных параметров
		По умолчанию: width = 1200, 
			      height = ratio * 1200, где ratio — отношение исходной высоты изображения к ширине
	3. Преобразует изображение в черно-белый формат
	4. Переводит изображение к ASCII Art, исходя из его похожести на символ

### ParserArguments:
	Преобразует полученные из консоли параметры в переменные 
		input_file, output_file, width, height, invert, contrast

### ParserVideoArguments:
	Преобразует полученные из консоли параметры в переменные
		invert, contrast, id_cam

# asciivideo.py :

	Данный модуль преобразует в ASCIIArt видео с веб-камеры и выводит его в консоль.