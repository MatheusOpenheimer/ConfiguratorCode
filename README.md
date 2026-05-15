Aplicação desktop desenvolvida para a configuração automatizada de leitores de código de barras via DataMatrix, voltada para uso em linha de produção. O sistema gera códigos de configuração padronizados que são lidos diretamente pelos dispositivos, permitindo programar modelo e número de série de forma rápida e consistente.

Além da configuração, a aplicação realiza a validação do dispositivo conectado via USB, comparando o número de série esperado com o identificado no hardware, reduzindo erros operacionais e garantindo rastreabilidade. A interface foi projetada para uso simples e direto pelos operadores, com fluxo dividido entre modo ***Produção (configuração)*** e ***Expedição Final (verificação)***.

O sistema inicia obrigatoriamente no modo de ***validação de firmware***, etapa considerada essencial para garantir que o dispositivo esteja utilizando a versão correta antes de qualquer operação. Enquanto o firmware não é validado, os demais modos permanecem bloqueados, evitando configurações ou verificações em equipamentos incompatíveis ou desatualizados. Após a validação bem-sucedida, o operador pode acessar os módulos de Produção e Expedição Final normalmente.

Ao concluir uma configuração ou verificação, a aplicação permite retornar ao modo de validação de firmware para reiniciar o fluxo e repetir o processo em um novo dispositivo, mantendo um ciclo padronizado e seguro para a linha de produção.

O projeto foi desenvolvido para a ***Custom Brasil***, com foco em otimizar processos, diminuir falhas humanas e aumentar a eficiência na preparação de equipamentos, sendo distribuído como um executável para facilitar a instalação e uso no ambiente produtivo.

<img width="550" height="681" alt="image" src="https://github.com/user-attachments/assets/06c76cd1-1d33-4ee3-b4c0-b9ff72d0d403" />
<img width="550" height="678" alt="image" src="https://github.com/user-attachments/assets/cae30821-ab62-49bd-aa1b-afd2f3d0182f" />
<img width="550" height="677" alt="image" src="https://github.com/user-attachments/assets/617fc645-feac-4ecf-bfde-7cb64d2ac493" />
<img width="549" height="677" alt="image" src="https://github.com/user-attachments/assets/9223023d-6725-4549-a1ea-f3ee8f321ad5" />


