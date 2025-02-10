Se o seu projeto utiliza o **Firebase** como banco de dados, é importante destacar isso no README para que os usuários e colaboradores saibam como o sistema está estruturado e como configurar o Firebase corretamente. Abaixo está uma versão atualizada do README com a inclusão do Firebase como banco de dados:

---

# Assistente de Ensino UFPA Cametá

Este repositório contém o projeto **Assistente de Ensino UFPA Cametá**, uma ferramenta de apoio acadêmico desenvolvida para atender dúvidas frequentes dos estudantes da Faculdade de Sistemas de Informação da Universidade Federal do Pará (UFPA) - Campus Cametá. O assistente utiliza inteligência artificial e processamento de linguagem natural para fornecer respostas precisas e acessíveis sobre disciplinas e outros tópicos relacionados ao curso.

---

## Sobre o Projeto

O **Assistente de Ensino UFPA Cametá** foi criado para facilitar a vida dos alunos, automatizando respostas a perguntas recorrentes e fornecendo informações claras e úteis sobre o curso de Sistemas de Informação. Com o uso de modelos avançados de linguagem, como **Sabiá 3**, **Gemini** e outros, o sistema é capaz de interpretar consultas em linguagem natural e gerar respostas contextualizadas.

O objetivo principal é reduzir a sobrecarga dos professores e coordenadores com perguntas repetitivas, permitindo que os alunos tenham acesso rápido e eficiente às informações necessárias para sua jornada acadêmica.

---

## Funcionalidades Principais

- **Respostas Automatizadas**: Utiliza modelos de linguagem avançados para fornecer respostas rápidas e precisas às perguntas dos alunos.
- **Fácil Acesso**: Disponível como uma ferramenta online, garantindo que os alunos possam acessar as informações de qualquer lugar.
- **Suporte Multimodelo**: Compatível com diferentes modelos de linguagem, como **Sabiá 3**, **Gemini** e outros, permitindo flexibilidade na escolha do modelo mais adequado.
- **Escalabilidade**: Projetado para ser facilmente expandido com novas funcionalidades e integrações futuras.
- **Banco de Dados em Tempo Real**: Utiliza o **Firebase** para armazenar e gerenciar dados de forma eficiente e escalável.

---

## Tecnologias Utilizadas

O projeto foi desenvolvido utilizando as seguintes tecnologias:

- **Python**: Linguagem principal para processamento de linguagem natural e automação.
- **LLM (Large Language Models)**: Modelos de linguagem como **Sabiá 3**, **Gemini** e outros para geração de respostas.
- **Firebase**: Banco de dados em tempo real para armazenamento de perguntas frequentes, logs e outras informações relevantes.
- **APIs de IA**: Integração com APIs externas para processamento de linguagem e geração de conteúdo.
- **Arquitetura Modular**: Divisão clara entre cliente, servidor e API para facilitar manutenção e escalabilidade.

---

## Estrutura do Projeto

A arquitetura do sistema é dividida em três módulos principais:

1. **Cliente**:
   - Interface de interação com o usuário (pode ser uma interface web ou CLI).
   - Responsável por capturar as perguntas dos alunos e exibir as respostas geradas pelo sistema.

2. **Servidor e Dataset**:
   - Processamento de dados e armazenamento das informações utilizadas pelo assistente.
   - Gerenciamento do banco de dados **Firebase** e integração com modelos de linguagem.

3. **API**:
   - Integração com modelos de linguagem para fornecer respostas em tempo real.
   - Comunicação entre o cliente e os modelos de IA.

---

## Instalação e Configuração

Para rodar o projeto localmente, siga os passos abaixo:

### Pré-requisitos
- Python 3.8 ou superior instalado.
- Git instalado no sistema.
- Chaves de API válidas para os modelos de linguagem utilizados (Sabiá 3, Gemini, etc.).
- Conta no [Firebase](https://firebase.google.com/) para configurar o banco de dados.

### Passo a Passo

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/eltonsarmanho/AssistenteEnsinoUFPA_Cameta.git
   cd AssistenteEnsinoUFPA_Cameta
   ```

2. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure o Firebase**:
   - Crie um projeto no Firebase Console.
   - Adicione um banco de dados Firestore ou Realtime Database ao seu projeto.
   - Baixe o arquivo de configuração JSON (`serviceAccountKey.json`) do Firebase e coloque-o na pasta raiz do projeto.
   - Atualize o arquivo `.env` com as credenciais do Firebase:
     ```env
     FIREBASE_DATABASE_URL=https://seu-projeto.firebaseio.com
     FIREBASE_SERVICE_ACCOUNT_KEY=serviceAccountKey.json
     ```

4. **Configure as variáveis de ambiente**:
   - Crie um arquivo `.env` na raiz do projeto e adicione suas chaves de API conforme o exemplo abaixo:
     ```env
     MARITALK_API_KEY=sua_chave_api_maritalk
     GOOGLE_API_KEY=sua_chave_api_google
     OPENAI_API_KEY=sua_chave_api_openai
     FIREBASE_DATABASE_URL=https://seu-projeto.firebaseio.com
     FIREBASE_SERVICE_ACCOUNT_KEY=serviceAccountKey.json
     ```

5. **Execute o assistente**:
   - Para iniciar o assistente, execute o script principal:
     ```bash
     python Interface/InterfaceStreamlit.py
     ```

6. **Teste o sistema**:
   - Interaja com o assistente via terminal ou interface web (dependendo da implementação).

---

## Contribuição

Contribuições são bem-vindas! Se você deseja melhorar o projeto ou adicionar novas funcionalidades, siga os passos abaixo:

1. **Fork** o repositório.
2. Crie uma nova branch para sua contribuição:
   ```bash
   git checkout -b feature/nome-da-feature
   ```
3. Faça suas alterações e envie um **Pull Request** detalhando suas modificações.
4. Certifique-se de seguir as diretrizes de codificação e documentação do projeto.

Se você encontrar bugs ou tiver sugestões, abra uma issue na seção de **Issues** do repositório.

---

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE). Você pode usar, modificar e distribuir o código conforme necessário, desde que mantenha os créditos originais.

---

## Contato

Para dúvidas, sugestões ou colaborações, entre em contato com o autor:

- **Elton Sarmanho**
- Email: [eltonss@ufpa.br](mailto:eltonss@ufpa.br)
