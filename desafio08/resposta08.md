adapter (adaptador):
    o padrão adapter é um padrão estrutural que permite que sistemas ou componentes que possuem interfaces diferentes se comuniquem. ele funciona como um "tradutor", transformando uma interface em outra que o sistema espera. no caso de integrar serviços de terceiros, como envio de e-mails ou sms, as apis desses serviços podem ter diferentes formatos e métodos. o adapter ajuda a criar uma interface comum para todas essas interações, permitindo que o sistema principal se comunique de forma padronizada, sem precisar se preocupar com os detalhes de cada api

    por exemplo, você tem diferentes serviços para enviar e-mails e sms, mas ambos precisam ser usados da mesma maneira no seu sistema. o adapter cria uma camada de abstração que adapta a api de cada serviço para uma interface única, como o método 'enviarmensagem', por exemplo assim, não importa qual serviço está sendo usado; o sistema sempre interage da mesma forma


strategy (estratégia):
    o padrão strategy é um padrão comportamental que permite selecionar um comportamento (ou estrategia) de acordo com as necessidades do momento ele é usado quando você tem diferentes formas de realizar uma tarefa, mas quer escolher qual delas usar de forma flexível, sem alterar o código que chama essas operações

    No cenário de envio de e-mails ou sms, o strategy seria usado para escolher qual serviço utilizar em tempo de execução ou seja, se o cliente precisar enviar um sms ou um email, o sistema pode decidir automaticamente qual "estratégia" (ou serviço) deve ser usada sem precisar de alterações manuais no código


como eles se encaixam na situação problema:

    no caso de integrar diferentes serviços de terceiros para disparo de e-mails ou sms, a ideia é garantir que o sistema tenha uma interface única e simples para interagir com esses serviços, independentemente das diferenças nas apis

    uso do adapter:
        cada serviço de e-mail ou sms tem uma api própria, com métodos e parâmetros específicos
        o adapter é responsável por fazer a tradução desses métodos para uma interface unificada, que o sistema principal entende, como por exemplo, 'enviarmensagem'
        isso facilita a integração com novos serviços, pois o sistema principal não precisa ser alterado, só seria necessário criar um novo adapter para o novo serviço

    uso do strategy:
        o strategy seria responsável por decidir, em tempo de execução, qual serviço (ou adapter) deve ser utilizado isso pode depender de vários fatores, como o tipo de mensagem (e-mail ou sms), a disponibilidade do serviço ou preferências do cliente
        assim, o strategy escolhe o adapter correto, permitindo que o sistema envie a mensagem de forma adequada, sem precisar saber qual serviço específico está sendo usado

por que escolher esses padrões:

    flexibilidade:
        o adapter permite que novos fornecedores de serviço sejam integrados facilmente se surgir um novo serviço de e-mail ou sms, basta criar um adapter para ele, sem a necessidade de mexer no código do sistema principal
        o strategy dá a flexibilidade de escolher qual serviço utilizar em tempo de execução, adaptando-se às necessidades do momento

    manutenibilidade:
        o código do sistema principal fica mais fácil de manter, porque as mudanças nas apis dos fornecedores de serviço não afetam a lógica do sistema se um fornecedor mudar sua api, só o adapter precisa ser ajustado, sem tocar no código que usa esse serviço
        com o strategy, é fácil mudar de fornecedor ou adicionar novos, sem impactar diretamente o fluxo principal da aplicação

    desacoplamento:
        o sistema principal fica desacoplado dos detalhes específicos de cada serviço ele só precisa interagir com a interface padrão (como 'enviarmensagem'), sem se preocupar com como cada serviço funciona
        isso permite que você altere a implementação do serviço, ou até adicione novos serviços, sem ter que modificar o código que interage com eles