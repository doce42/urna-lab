# Como contribuir (e como discordar)

Este projeto é livre: você pode **baixar, reproduzir, fazer fork, alterar, publicar resultados diferentes e contradizer o estudo**. Discordar com dados e código é bem-vindo e faz parte do método.

## Quem altera este repositório
Só quem mantém (`doce42`) escreve aqui. **Nada entra sem validação**, como em qualquer projeto de código aberto:

1. Faça um **fork** do repositório.
2. Crie uma branch no seu fork e faça a mudança.
3. Abra um **pull request**. A pessoa que mantém revisa, pode pedir ajustes e decide se entra.

Você também pode, sem pedir nada, manter o seu próprio fork com outras conclusões e linkar este repositório.

## O que uma boa contribuição traz
Siga o [`DIRETRIZ.md`](DIRETRIZ.md) e o [`AGENTS.md`](AGENTS.md):
- **Teste novo:** escreva a hipótese, o modelo nulo e o limiar no `PROTOCOLO.md` (emenda datada) e no `testes/registro.json` **antes** de olhar o resultado.
- **Calibração:** rode em 2022 e com fraude sintética (poder); investigue artefatos antes de chamar algo de anomalia.
- **Resultados negativos, inconclusivos e contrários** às conclusões atuais são tão bem-vindos quanto os demais.
- **Reprodutível:** tudo sai de código executável (`make`), com sementes fixas; `make verificar` precisa passar. O texto de um agente de IA nunca é fonte de número.
- **Sem dados pessoais, sem dados brutos, sem Git LFS** e sem GitHub Actions (a computação roda na máquina de cada pessoa).
- Documente no `CATALOGO.md` e cite as fontes no `REFERENCIAS.md`.

## Discordância metodológica
Abra uma *issue* descrevendo o ponto, com o código e os dados que o sustentam. Se a crítica estiver certa, o erro e a correção entram no `CATALOGO.md`, como já acontece com os erros do próprio projeto.

## Licenças
Ao contribuir, você concorda que o seu código fica sob a licença MIT e os seus textos e resultados sob a CC BY 4.0 (ver `LICENSE`, `LICENSE-DOCS` e `THIRD_PARTY.md`).
