Este arquivo é destinado a explicar a implementação do código.
Alguns apontamentos: 
- código documentado passo a passo especificando tudo que foi feito.
- Acurácia de detecção de rostos baixa por conta dos filtros aplicados.

A parte prática dessa prova foi requisitado um script em Python que carregasse um vídeo disponibilizado pelo professor. Com isso, ao carregar o vídeo, escolheríamos uma forma de encontrar a face presente no mesmo por meio do OpenCV. A forma que escolhi foi o haarcascade, uma biblioteca que possui um padrão já treinado para encontrar faces. Essa bibiloteca importa seus padrões do github e aplica no vídeo, sendo passível de alterações em seus parâmetros. Por fim, foi nos pedido um vídeo de saída gravando o script de detecção trabalhando, arquivo gerado em .avi.
