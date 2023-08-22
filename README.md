![Captura de tela 2023-08-22 103340](https://github.com/ArthurClaro/2-Projeto-Python-Selenium/assets/124170421/e78f52de-ea95-41cf-9d71-bba6f7cb5382)
# Projeto Automação Web - Busca de Preços -- Selenium
Vídeo : https://www.linkedin.com/posts/arthur-claro-dev_python-empresas-vendasonline-activity-7099743973941911552-QjIj?utm_source=share&utm_medium=member_desktop
### Objetivo: treinar um projeto em que a gente tenha que usar automações web com `Selenium` para buscar as informações que precisamos

### Como vai funcionar:

- Imagina que você trabalha na área de compras de uma empresa e precisa fazer uma comparação de fornecedores para os seus insumos/produtos.

- Nessa hora, você vai constantemente buscar nos sites desses fornecedores os produtos disponíveis e o preço, afinal, cada um deles pode fazer promoção em momentos diferentes e com valores diferentes.

- Seu objetivo: Se o valor dos produtos for abaixo de um preço limite definido por você, você vai descobrir os produtos mais baratos e atualizar isso em uma planilha.
- Em seguida, vai enviar um e-mail com a lista dos produtos abaixo do seu preço máximo de compra.

- No nosso caso, vamos fazer com produtos comuns em sites como Google Shopping e Buscapé, mas a ideia é a mesma para outros sites.

### Outra opção:

- APIs

### O que temos disponível?

- Planilha de Produtos, com os nomes dos produtos, o preço máximo, o preço mínimo (para evitar produtos "errados" ou "baratos de mais para ser verdade" e os termos que vamos querer evitar nas nossas buscas.

### O que devemos fazer:

- Procurar cada produto no Google Shopping e pegar todos os resultados que tenham preço dentro da faixa e sejam os produtos corretos
- O mesmo para o Buscapé
- Enviar um e-mail para o seu e-mail (no caso da empresa seria para a área de compras por exemplo) com a notificação e a tabela com os itens e preços encontrados, junto com o link de compra. (Vou usar o e-mail 0123456789arthur+compras@gmail.com. Use um e-mail seu para fazer os testes para ver se a mensagem está chegando)
