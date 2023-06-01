# Entrega robô simulado no ambiente Gazebo
O código é uma integração dos conceitos abordados em dois vídeos disponibilizados pelo professor. Um dos vídeos trata da obtenção da posição do robô simulado no ambiente de simulação Gazebo usando odometria, enquanto o outro vídeo aborda a lógica de obtenção de uma fila de posições a partir de um arquivo CSV usando uma fila.

A parte relacionada à obtenção da posição do robô simulado no Gazebo envolve a subscrição do tópico de odometria (`/odom`) e a extração e conversão dos valores de posição (x, y, z) e ângulo (theta) a partir da mensagem recebida usando ("from tf_transformations import euler_from_quaternion"). 


link do vídeo de demonstração: https://drive.google.com/drive/folders/1H44I2xeg0r18DZc3c3UYUJX9qavQDvoz?usp=share_link


