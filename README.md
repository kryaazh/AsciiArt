# ASCII Art

### asciiart.py :

	Программа для преобразования изображения в ASCII Art
    Программа получается на вход изображение, результатом работы является текстовый файл
	Работает через консоль, имеет несколько входных параметров:

#### 	Обязательные:
		-i, --input  : исходный файл изображения

#### 	Необязательные:
######		-o, --output : результат работы программы, в виде изображения
				(default : вывод в консоль) 
######		-W, --width  : ширина преобразованного изображения
######      -H, --height : высота преобразованного изображения
######		-c, --contrast: уровень контрастности [-127; 127]
       
            Контраст изменяется по формуле : 
                contrast_img = f * (img - 127) + 127
            В методе изменения контраста вычисляется фактор f : 
                При уровне констраста -127: f = 0 
                    и на выходе получается серое изображение
                Если значения меньше -127, то f — отрицательный и 
                    контраст изображения становится выше
                    
                При уровне контраста 127 получается 
                    изображение максимального контраста,
                    так как при значениях выше изображение инвертируется
                 
######      --invert: инвертирование изображения

#### 	Примеры ввода:
		asciiart.py -i in.jpg
		asciiart.py -i in.jpg -o out.jpg -x 1500 -y 1500 -c 200 --invert
		asciiart.py --input in.jpg --output out.jpg --width 1500 --height 1500 --contrast 150

# Модули:

### CharDictionary:
	Создает файл chars.npy, в котором находятся все символы в байтовом виде.

### ImageConverter:
	1. Получает на вход изображение
	2. Изменяет параметры ширины и высоты относительно входных параметров
		По умолчанию: width = 800, 
			      height = ratio * 800, где ratio — отношение исходной высоты изображения к ширине
	3. Преобразует изображение в черно-белый формат
	4. Переводит изображение к ASCII Art, исходя из его похожести на символ

# asciivideo.py :

	Данный модуль преобразует в ASCIIArt видео с веб-камеры и выводит его в консоль.
####	Имеет несколько входных параметров:
            -С, --camera-id : номер выбранной веб-камеры
            --invert : инвертировать преобразуемое изображение
            -с, --contrast : возможность изменить контраст изображения,
                                допустимые значения [-127, 127] 