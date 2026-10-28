# R1: revisão independente da V1.0-rc1 (Codex, 28/10/2026)

Primeira auditoria externa da Fase 1. O revisor (Codex, outro agente de IA, em sessão separada) leu o projeto, o registro de testes, o código, as saídas e a conclusão, e comparou o projeto com seis projetos públicos semelhantes. O relatório não emite veredito sobre fraude. Ele mede o alcance de cada verificação.

- **[`original/RELATORIO.md`](original/RELATORIO.md):** o relatório como foi entregue, junto com os controles mínimos que o revisor rodou (`controle_ed521.json`, `comparacao_ed521.json`, `controles_revisao.py`) e os manifestos das fontes que ele leu.
  - Os SHA-256 dos arquivos originais estão em [`SHA256SUMS.txt`](SHA256SUMS.txt).
  - Na cópia publicada no GitHub, os caminhos da máquina do autor (`~) foram trocados por `~` pela trava de privacidade da publicação. O original byte a byte fica no disco local.
  - A pasta `fontes/` do revisor tem cópias de repositórios de terceiros e do próprio projeto. Ela não é publicada, por causa das licenças de terceiros e da duplicação, mas está listada com SHA-256 em `manifesto_fontes_pesquisa.json`.
- **[`achados.json`](achados.json):** um registro por achado, com seção do relatório, testes afetados, classificação, o que verificamos, nossa resposta, ações e situação.

**O que conferimos por conta própria antes de responder:**
- **Ed521 aceitava entrada degenerada:** reproduzido.
- **`.ok` do download sem hash oficial:** conferido no código. Reconstruímos o estado real: 331 arquivos com hash oficial conferido e 173 marcados por engano.
- **T01 era só soma nacional:** conferido e refeito seção a seção, com 0 diferenças em 5,7 milhões de pares.
- **T35, T27, scripts "(a fazer)", ausência de Moran's I, eleitorado do T32:** todos conferidos.
- **Versão revisada:** a conclusão que o revisor leu tem o mesmo SHA-256 do retrato congelado da rc1.

**Resultado no registro:**
- 41 provas: 1 resistiu, 29 ajustadas, 9 em andamento e 2 caíram.
- As duas que caíram são a frase "uma fraude localizada que mudasse o vencedor muito provavelmente apareceria" e o alcance declarado do T27 (brancos e nulos não foram testados).
- O resumo das mudanças está em [`CONCLUSAO.md`](../../CONCLUSAO.md#mudanças-em-relação-à-v10-rc1).
