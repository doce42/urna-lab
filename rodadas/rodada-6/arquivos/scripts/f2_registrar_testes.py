"""Registra os testes da primeira sessão da Fase 2 (28/10/2026): T37, T38, T39. Uso único; idempotente."""
import json, os
REG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "testes", "registro.json")
r = json.load(open(REG, encoding="utf-8"))
base = {"modulo": "G", "modelo_nulo": "—", "situacao": "concluido", "referencia": "", "pressupostos": "", "anotacoes": [], "provas": [], "versoes": [],
        "metodo_versao": 1, "pre_especificacao": "protocolo_ou_emenda", "interpretacao": None, "revisoes": [], "mudancas": [], "origem_fase2": "sessão limitada de 28/10/2026"}
novos = [
 {"id": "T37", "pergunta": "O estimador C06 recupera a verdade quando as taxas de transferência variam entre municípios?",
  "metodo": "Dados sintéticos com X real e taxas conhecidas (homogêneo, aleatório, correlacionado ao voto), 10 réplicas por cenário, γ = 0,5 e 1,0, 2026 e 2022 separados; estimador C06 copiado literalmente",
  "script": "fase2/sessao_limitada_2026-10-28/p1_c06_adversarial.py", "comando": ".venv/bin/python fase2/sessao_limitada_2026-10-28/p1_c06_adversarial.py principal|sensibilidade",
  "saida": "fase2/sessao_limitada_2026-10-28/p1_resultado_{principal,sensibilidade}.json",
  "hipotese_nula": "O C06 recupera a razão Abs→Lula : Abs→Adversário com erro relativo ≤ 25% e erro absoluto ≤ 0,03 por célula mesmo com heterogeneidade contextual",
  "limitacoes": "A intensidade da heterogeneidade (γ) não é calibrada à realidade; uma única família (logit linear em um contexto); 10 réplicas",
  "afirmacao": "estatística", "independencia": "interna", "natureza": "confirmatório", "classe_evidencia": "G",
  "evidencia": "Reproduz o C06 gravado (diferença máxima 5e-5). Com taxas homogêneas a razão 2026 é recuperada (4,12 contra 4,01). Com heterogeneidade contextual a razão estimada vai de 2,3 a 10,6 (γ=0,5) e de 1,7 a 11,8 (γ=1,0) contra 3 a 4 verdadeiro; o erro absoluto por célula é ≤ 0,02 com γ=0,5 e chega a 0,046 com γ=1,0. O total do 2º turno é reproduzido em todos os cenários (erro < 1,3%): reproduzir margens não discrimina. A ordem Abs→Lula > Abs→Adversário de 2026 e o contraste com 2022 (razão 0,56) se mantêm.",
  "resultado_atual": "A magnitude '4:1' do C06 não é robusta a heterogeneidade contextual de estresse; ordem e contraste 2022 × 2026 resistem.",
  "interpretacao": "Corrige o alcance do C06: estimativa condicionada ao pressuposto de taxas homogêneas por UF. Não mede a heterogeneidade real.",
  "impacto_votos": "Erro da célula Abs→Lula de ±0,5 mi de votos (estresse moderado) a ±1,5 mi (forte), contra a estimativa de 3,18 mi e o ganho total de Lula de 10,33 mi."},
 {"id": "T38", "pergunta": "O excesso de seções pró-Lula entre turnos tem a assinatura de enchimento de urna (comparecimento subindo junto)?",
  "metodo": "Seções acima de 5 desvios (definição do T02) nos dois sentidos; mudança de comparecimento relativa ao município, fração positiva, tamanho, UF e votos excedentes; 2026 e 2022 como réplica",
  "script": "fase2/sessao_limitada_2026-10-28/h1_outliers_lula.py", "comando": ".venv/bin/python fase2/sessao_limitada_2026-10-28/h1_outliers_lula.py",
  "saida": "fase2/sessao_limitada_2026-10-28/h1_resultado.json",
  "hipotese_nula": "As seções pró-Lula atípicas não diferem das demais em mudança de comparecimento",
  "limitacoes": "Só cobre enchimento que altere o comparecimento; não vê troca em urna sem mudança de comparecimento nem alteração uniforme; sem teste formal de assimetria",
  "afirmacao": "estatística", "independencia": "interna", "natureza": "exploratório", "classe_evidencia": "A",
  "evidencia": "Nas seções pró-Lula acima de 5 desvios (32 em 2026, 90 em 2022) a mudança de comparecimento relativa ao município tem média −1,8 pp e −0,6 pp, com 44% e 48% positivas (50% no conjunto). A assimetria de cauda existe também a 3 e 4 desvios (1.997×692 e 190×53 em 2026). Em 2026 nas seções acima da mediana de tamanho são 6 pró-Lula e 8 pró-outro; em 2022 são 46 e 2 (SP 32 de 90).",
  "resultado_atual": "A assinatura prevista pelo enchimento não aparece em 2026 nem em 2022; a assimetria de cauda do T02 segue sem causa.",
  "interpretacao": "Refuta a hipótese de enchimento localizado via ausentes naquilo que ela prevê (comparecimento). Não exclui outros mecanismos; não atribui intenção.",
  "impacto_votos": "Votos excedentes nessas seções: cerca de 740 (2026) e 2.600 (2022), contra ganhos de Lula entre turnos de 10,33 mi e 3,07 mi (0,007% e 0,08%)."},
 {"id": "T39", "pergunta": "Em 20 seções (10 exceções documentadas e 10 aleatórias), os arquivos da urna, as assinaturas e a publicação concordam?",
  "metodo": "Tamanho e SHA-512 de BU, log, RDV e imagem contra a lista assinada; assinatura da lista e dos arquivos; chave da seção no BU; RDV = BU = imagem = BU na Web; log = comparecimento. Seleção fixada antes (default_rng 2026 e 2027)",
  "script": "fase2/sessao_limitada_2026-10-28/v_a_secoes.py", "comando": ".venv/bin/python fase2/sessao_limitada_2026-10-28/v_a_secoes.py",
  "saida": "fase2/sessao_limitada_2026-10-28/va_resultado.json",
  "hipotese_nula": "Algum arquivo, assinatura ou total das seções amostradas diverge entre si ou da publicação",
  "limitacoes": "Amostra estratificada de conveniência de 20 seções do 1º turno de 2026; verificador interno (mesmas funções do pipeline); certificado não validado até âncora TSE; BU, RDV e log podem ter origem comum",
  "afirmacao": "determinística", "independencia": "criptográfica", "natureza": "confirmatório", "classe_evidencia": "A",
  "evidencia": "19 seções com arquivos: tamanho, SHA-512 e assinatura conferem com a lista assinada em todas; BU = imagem = BU na Web em todas; RDV = BU em 18 (AL 28339/13/118 difere em 1 nulo por suspensão, falha do comparador e não do dado); log = comparecimento em 18 (RJ 58971/87/184: 256 contra 258, caso documentado no T36). A seção do exterior (ZZ 29564/1/91) é do Sistema de Apuração, sem lista de urna.",
  "resultado_atual": "Nenhuma divergência objetiva nova nas 20 seções; vale só para a amostra. A Verificação B (confronto independente) não pôde ser feita: não há material externo disponível.",
  "interpretacao": "Consistência interna e coerência com a assinatura apresentada pela urna; não demonstra autenticidade da chave nem exclui alteração anterior à assinatura.",
  "impacto_votos": "0 votos de diferença entre BU, imagem e BU na Web nas 19 seções; a diferença de 2 votos entre log e comparecimento (RJ 58971/87/184) já está no T36."},
]
ids = {t["id"] for t in r["testes"]}
for n in novos:
    if n["id"] not in ids:
        r["testes"].append({**base, **n})
json.dump(r, open(REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(r["testes"]))
