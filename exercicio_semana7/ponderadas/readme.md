### Explicação do exercício
A Ponderada 4 enfoca a integração entre um front-end simples desenvolvido pelo aluno e o bucket do Supabase, permitindo o envio de imagens para o Supabase por meio dessa integração.
A solução foi implementada em um único script, que inclui a criação de uma rota usando o Flask. O script também retorna um front-end básico assim que a imagem é enviada.
No código, importamos as bibliotecas necessárias e criamos uma instância do Flask. Em seguida, configuramos as credenciais do Supabase, como a URL e a chave de acesso.
Definimos uma rota para a página inicial e verificamos se o método de requisição é POST. Se for, obtemos a imagem enviada pelo aluno, enviamos essa imagem para o bucket do Supabase e retornamos o front-end renderizado com a imagem enviada.
Caso o método de requisição seja GET, renderizamos o front-end inicial sem nenhuma imagem.
Finalmente, executamos o servidor Flask para que a solução fique disponível.

Observações: A estilização foi realizada na própria página sem necessidade de criar um arquivo próprio para estilização.

### Vídeo de demonstração
<br>

[![IMAGE ALT TEXT HERE](print.png)](https://drive.google.com/file/d/1vzWPcxzJLQGnF4QhGM3FGjodN0otpR_E/view?usp=drive_link)





