# Human Flow Detector

## Sobre

O presente trabalho tem o objetivo de propor um software para auxílio no controle organizacionais de shoppings por meio do processamentos das imagens geradas por câmeras
de segura. Com os dados obtidos, é possível criar mapas de calor e definir tendências de comportamento populacional em áreas comerciais.

## Funcionamento

O esquemático da utilização do Software de detecção de fluxo de pessoas pode ser descrito de acordo com o diagrama apresentado a seguir:

<img src="/docs/schematic.png" alt="Esquemático do serviço.">

Como pode ser observado, o funcionamento do software para o usuário é feito de forma simples. Faz-se necessário o envio de determinado vídeo do ambiente real a ser estudado, e então após processamento do software, é retornado os dados processados e uma imagem representando o mapa de calor encontrado pelo vídeo em uma imagem.

Uma vez enviado o vídeo, o software o recebe e o formata para o formato de vídeo mais apropriado. Após isso, é utilizado, por meio de um programa em python, um sistema de detecção de objetos chamado YOLO (You Only Look Once). A utilização deste sistema será feita por meio de bibliotecas python do mesmo em colaboração com outras como o numpy e OpenCV. A escolha deste se baseou na sua grande popularidade com relação aos métodos de detecção de objetos e pelo fato de que a técnica de detecção de objetos deste já foi considerada estado da arte nos últimos anos.

Assim, utilizando o YOLOV5 (YOLO Versão 5), o processamento dos frames do vídeo é feito a partir de métricas de verificação pré configuradas, de modo a capturar de forma mais precisa possível os pontos onde são encontradas pessoas. Ressalta-se aqui que o programa não faz a identificação de pessoas e não retem qualquer frame do vídeo, de modo que nenhuma imagem seja gravada pelo software.

<img src="/docs/detecção.png" alt="Exemplo de detecção.">

A partir dessas informações, o código faz o processamento dos dados e retorna para o usuário uma lista de informações sobre o que foi observado no vídeo e um mapa de calor do conjunto de imagens que compõem o mesmo, de forma que seja possível para o usuário identificar as áreas da imagem em que há maior fluxo de pessoas.

<img src="/docs/mapa_de_calor.jpeg" alt="Mapa de Calor.">

Exemplo de funcionamento:

https://user-images.githubusercontent.com/53785989/164055753-2836c556-00b2-4253-a716-40c0c452d69c.mp4

