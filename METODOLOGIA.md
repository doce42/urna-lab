# Metodologia (versão 2: completa e matemática)

Este documento descreve **métodos**: o que cada teste calcula, sob qual hipótese nula, com quais pressupostos, limiares, poder e referências. Não carrega situação nem resultados: estes ficam em `testes/registro.json` (`make registro`) e no `CATALOGO.md`, para não haver versões contraditórias. Hierarquia dos documentos: `DIRETRIZ.md` (princípios) → `PROTOCOLO.md` (perguntas, modelos nulos, critérios, emendas) → este documento (matemática) → código (fonte de verdade dos números). Versão anterior: `docs/historico/METODOLOGIA_v1_2026-10-27_2050.md`.

---

## 0. Notação

**Unidades e índices.**
- **Seção** *i* (unidade de votação); município *m(i)*; zona *z(i)*; local de votação *ℓ(i)*; UF *u(i)*; turno *t* ∈ {1, 2}.

**Contagens por seção.**
- Eleitores aptos: *A*ᵢₜ. Comparecimento: *C*ᵢₜ.
- Votos no candidato *k* (número 13, 22, …): *V*ᵢₜᵏ. Brancos: *B*ᵢₜ. Nulos: *N*ᵢₜ.
- Válidos: *n*ᵢₜ = Σₖ *V*ᵢₜᵏ.

**Taxas.**
- Comparecimento: *c*ᵢₜ = *C*ᵢₜ / *A*ᵢₜ.
- Proporção do candidato 13 nos válidos: *p*ᵢₜ = *V*ᵢₜ¹³ / *n*ᵢₜ.
- Voto órfão no 1º turno (candidatos eliminados): *o*ᵢ = 1 − (*V*ᵢ₁¹³ + *V*ᵢ₁²²) / *n*ᵢ₁.

**Logit com correção de continuidade (Haldane–Anscombe),** para respeitar o teto de 0% e 100%:

  λ(*x*, *n*) = ln[(*x* + ½) / (*n* − *x* + ½)].

**Virada da seção** (2º turno menos 1º, na escala logit):

  *s*ᵢ = λ(*V*ᵢ₂¹³, *n*ᵢ₂) − λ(*V*ᵢ₁¹³, *n*ᵢ₁).

**Erro-padrão binomial da virada** (aproximação delta, tratando os turnos como independentes):

  σᵢ = √[1/(*x*₁+½) + 1/(*n*₁−*x*₁+½) + 1/(*x*₂+½) + 1/(*n*₂−*x*₂+½)].

**Escala robusta:** MAD(·) = mediana |· − mediana(·)|; o fator 1,4826 torna o MAD consistente com o desvio-padrão sob normalidade.

**Correção para muitos testes:** Benjamini–Hochberg (BH) com taxa de falsas descobertas *q*. Ordena os *p*-valores *p*₍₁₎ ≤ … ≤ *p*₍ₘ₎ e rejeita até o maior *k* com *p*₍ₖ₎ ≤ *q*·*k*/*m*.

**Critérios fixados no PROTOCOLO, seção 4:**
- α = 0,01;
- BH com *q* = 0,05;
- efeito abaixo de 0,1 ponto percentual = desprezível;
- anomalia = passa do limiar + sem explicação por acaso, geografia, demografia ou artefato + repete em dados de **origem diferente** (emenda 3).

**Sementes:** todas fixas e registradas em cada script (`numpy.random.default_rng(semente)`).

---

## 1. Regras de condução
1. **Hipótese e teste antes de rodar.** Escreva no PROTOCOLO, em emenda datada.
2. **Todo teste tem um esperado (modelo nulo):**
   - N1: contagem como sorteio;
   - N2: persistência do eleitor;
   - N3: transferência de votos;
   - N4: perfil demográfico;
   - N5: ordem de chegada aleatória;
   - N6: referência 2022;
   - N7: integridade criptográfica.
3. **Controle a geografia.** Comparações dentro do município (efeito fixo) sempre que a pergunta permitir.
4. **Tamanho de efeito e incerteza junto do *p*-valor.** Para resultado negativo, informe o intervalo de confiança e o **menor efeito detectável** (MDE).
5. **Poder e especificidade:**
   - fraude sintética injetada (T13, T23);
   - aplicação em 2022 (N6);
   - teste que acusa dado limpo é excluído da conclusão (T26).
6. **Artefato antes de anomalia.** Os casos registrados estão no CATALOGO, seção 4.
7. **Exploratório × confirmatório.** O que foi descoberto nos dados é confirmado em dados de outra origem (arquivos das urnas, outro ano, metade de municípios não usada).

---

## 2. Camada A: integridade dos arquivos (determinística)

### 2.1 Formatos (lidos com um decodificador DER mínimo, `analise/der.py`)
Cada nó DER é (classe, construído, etiqueta, conteúdo). O decodificador não usa esquema: os campos foram identificados nos dados e validados por consistência cruzada em 100% das urnas (RDV = BU = imagem do BU = publicado). Falta conferir com a especificação oficial do TSE.

- **RDV** (registro digital do voto):
  - raiz → [2] corpo → [4] lista de eleições;
  - eleição = (código; 6257 = 1º turno, 6258 = 2º turno de 2026; cargos);
  - cargo = (código; 1 = Presidente; quantidade; votos);
  - voto = (tipo; número digitado). Tipos: 2 nominal, 3 branco, 4 nulo, 6 nulo por suspensão.
- **bu.dat** (boletim digital):
  - envelope → conteúdo DER;
  - [7] habilitações = (sem biometria cadastrada, biométrica, biográfica);
  - [8] eleições = (código, aptos, …, resultados);
  - resultados = (tipo, comparecimento, cargos); cargo = (código, quantidade, votáveis);
  - votável = (tipo: 1 nominal, 2 branco, 3 nulo; quantidade; (partido, número); ordem; hash encadeado de 64 bytes);
  - o último hash da lista é assinado (132 bytes).
- **vota.vsc** (assinaturas):
  - bloco da urna `UEAO…`/`ueao…` = (data, versão, cabeçalho, lista DER, certificado);
  - cabeçalho = (…, (alg, SHA-512 da lista, assinatura da lista));
  - lista = {(nome, (tamanho, SHA-512, assinatura))}.
- **log.jez:**
  - zip com `logd.dat` (latin-1; campos: data hora, nível, id da urna, aplicação, mensagem, hash) e logs arquivados (`.jez` aninhados);
  - leitura recursiva;
  - **no 2º turno, a mesma urna física traz arquivado o log do 1º turno:** todas as contagens filtram o dia da eleição do turno.
- **imgbu.dat:** texto do boletim impresso (latin-1) num envelope binário.

### 2.2 Verificações por urna (T14–T17b, T24)
Para cada urna *j*, com lista assinada 𝓛ⱼ = {(nome, τ, *h*, σ)}:
- **Hash e tamanho (T16):** para cada arquivo publicado *f*: |*f*| = τ e SHA-512(*f*) = *h*.
- **Assinatura da lista:** SHA-512(𝓛ⱼ) = *h*_lista, e Verify(*pk*ⱼ, *h*_lista, σ_lista) = verdadeiro.
- **Assinatura de cada arquivo:** Verify(*pk*ⱼ, *h*, σ) = verdadeiro.
- **RDV (T17):** para cada votável *k*, #{votos tipo 2 com número *k*} = *V*ⱼᵏ; #{tipo 3} = *B*ⱼ; #{tipo 4} + #{tipo 6} = *N*ⱼ (Presidente).
- **bu.dat (T17b):** as contagens do bu.dat são iguais às do RDV e às publicadas. Votável com 0 votos não aparece no bu.dat e é tratado como 0.
- **Log (T14):**
  - #"O voto do eleitor foi computado" no dia da eleição = *C*ⱼ;
  - #"Voto confirmado para [Presidente]" + #"Atribuido voto nulo por suspensão [Presidente]" = total apurado de Presidente.
- **Imagem do BU (T15):** as contagens do texto impresso são iguais às publicadas.
- **Urna substituída (T24):**
  - o conjunto de ids de urna que registraram "voto computado" tem mais de 1 elemento quando houve troca;
  - o certificado da urna tem de estar nesse conjunto.

### 2.3 Algoritmos de assinatura
**UE2013/UE2015: ECDSA sobre P-521 com SHA-512** (FIPS 186).
- Mensagem: o hash *h* de 64 bytes.
- Verificação padrão: dado (*r*, *s*), *e* = SHA-512(*h*), *w* = *s*⁻¹ mod *n*, *u*₁ = *e w*, *u*₂ = *r w*, *R* = *u*₁*G* + *u*₂*Q*; válida se *x*(*R*) ≡ *r* (mod *n*).
- Certificado X.509 em DER, com bytes de preenchimento após o fim: recorta-se no tamanho declarado.

**UE2020/UE2022: Ed521**, EdDSA sobre a curva de Edwards E-521.
- **Curva e parâmetros:**
  - *x*² + *y*² = 1 + *d* *x*² *y*² sobre 𝔽ₚ, com *p* = 2⁵²¹ − 1 e *d* = −376014 (SafeCurves);
  - ponto base *B* = (*G*ₓ, 12), de ordem *L* = 2⁵¹⁹ − 337554763258501705789107630418782636071904961214051226618635150085779108655765.
- **Codificação:**
  - pontos: 66 bytes little-endian de *y*, com o bit 527 = paridade de *x*;
  - chave pública *A*: 66 bytes; assinatura (*R*, *S*): 66 + 66 bytes;
  - *S* < *L*, little-endian.
- **Desafio:**

  *k* = SHAKE256("SigEd521" ‖ 0x00 ‖ 0x00 ‖ *R* ‖ *A* ‖ *M*, 132 bytes) interpretado little-endian, mod *L*,

  com *M* = SHA-512(*h*) (a urna assina o hash do hash).
- **Válida se** [*S*]*B* = *R* + [*k*]*A*, em coordenadas estendidas.
- **Como os parâmetros foram identificados:**
  - chave, ponto *R* e certificado estão na curva (decodificação válida);
  - entre as variantes plausíveis (hash, domínio, ordem dos bytes, mensagem), só uma valida;
  - uma assinatura de esquema seguro não valida por acaso.
- **Controles (T16c, `analise/controles/ed521_controles.py`):** em 300 urnas reais, assinaturas legítimas são todas válidas, e cada um destes casos é 0% válido:
  - 1 bit da assinatura alterado;
  - 1 bit do hash alterado;
  - chave de outra urna;
  - mensagem aleatória;
  - assinatura de outro arquivo.
- **Limites:**
  - falta conferir com a especificação oficial e vetores de teste oficiais;
  - a cadeia de certificados até a raiz (certificados das ACs `AC UE2020`, `AC UE2022`, `AC URNA`) não foi verificada.

### 2.4 Ligação urna ↔ seção ↔ preparação (T34, T35)
- **T34:** para cada seção, a urna efetivada na correspondência oficial (CEFT) é igual à `NR_URNA_EFETIVADA` do BU na Web e igual ao id no certificado da urna (sufixo numérico do CN `UEAO0NNNNNNN`), e esse id está entre os ids do log. Também são contados:
  - esperada ≠ efetivada (troca declarada) e se essas trocas aparecem como duas urnas no log;
  - a origem do voto (urna eletrônica, BU gerado por recuperação de dados, sistema de apuração em cédula).
- **T35:** cada máquina geradora de mídia citada no CEFT (nome, serial TPM, serial de instalação) tem log publicado do GEDAI-UE. Para esses logs, são contadas as versões ("Abertura do GEDAI-UE - Versão …") e as fases ("Fase: OFICIAL").

### 2.5 Totalização (T01, T32)
- **T01:** para cada votável e turno, Σᵢ (BU na Web) = Σᵢ (votação por seção).
- **T32:** Σᵢ (BU) por abrangência (BR, cada UF, exterior) = total no arquivo oficial do site de resultados (`<abr>-c0001-e00<ele>-u.json`), item a item:
  - votos de cada candidato (`vap`);
  - brancos (`vb`), nulos (`vn`);
  - votos em candidato com registro indeferido ou anulado (`vnt` + `van` + `vansj`);
  - comparecimento (`e.c`) e eleitorado (`e.te`).
- **Independência:** T01 e T32 são **internos**. Mostram coerência do TSE consigo mesmo, não verificação independente da contagem. A verificação mais independente disponível é a camada criptográfica (2.2–2.3).

---

## 3. Camada C: contrafactual pelo 1º turno (modelos N2, N3)

### 3.1 Resíduo da virada e z robusto (T02)
- Resíduo em relação ao município: *r*ᵢ = *s*ᵢ − mediana_{*j* ∈ *m*(*i*)} *s*ⱼ.
- Padronização: *z̃*ᵢ = *r*ᵢ / σᵢ.
- Escala robusta: *z*ᵢ = (*z̃*ᵢ − mediana *z̃*) / (1,4826 · MAD(*z̃*)).

  O fator MAD absorve a dispersão real: os eleitores de uma seção mudam entre turnos (abstenção diferente), e a independência entre turnos usada em σᵢ não vale. Na prática a escala fica ≈ 0,47–0,51 (menor que 1).
- Estatística: #{*z*ᵢ > 5} e #{*z*ᵢ < −5}, e a assimetria.
- **Nulo realista (INC):** ajusta-se uma *t* de Student (ν, μ, τ) por máxima verossimilhança aos *z*ᵢ. Valores esperados nas caudas: *n*·P(*T* > 5) e *n*·P(*T* < −5). O excesso numa cauda é anomalia estatística (classe B) a confirmar em dados de outra origem.
- Inclusão: seções com *n*ᵢ₁, *n*ᵢ₂ ≥ 20 (sensibilidade: ≥ 50).

### 3.2 Curva real × prevista (T10, T11)
- **Previsão da urna *i*:**

  *V̂*ᵢ₂¹³ = *n*ᵢ₂ · logit⁻¹(λ(*V*ᵢ₁¹³, *n*ᵢ₁) + δ),

  com δ = virada média das **outras** seções do município (deixa-uma-fora) ou a mediana da UF.
- **Ordenação:** as urnas são ordenadas pela hora de chegada ao TSE e somadas por minuto *τ*. Curva real: *P*(*τ*) = Σ_{chegou ≤ τ} *V*¹³ / Σ *n*; curva prevista: *P̂*(*τ*), idem com *V̂*¹³.
- **T10:** max_τ |*P*(*τ*) − *P̂*(*τ*)|, a partir de 5% apurado.
- **T11:** número de mudanças de sinal de Δ*P*(*τ*), comparado com 200 simulações: *V*¹³ = *V̂*¹³ + resíduo reamostrado (permutação dos resíduos reais *V*¹³ − *V̂*¹³), mesma ordem de chegada.

### 3.3 Transferência de votos (C06), inferência ecológica de Goodman com restrição
- **Linhas** (frações do eleitorado apto no 1º turno): *X*ᵢ = (Lula, adversário, cada um dos 4 maiores eliminados, outros, branco+nulo, abstenção).
- **Colunas** (destino no 2º turno): *Y*ᵢ = (Lula, adversário, branco+nulo, abstenção).
- **Modelo:** *Y*ᵢ ≈ *X*ᵢ β, com βⱼₖ ≥ 0 e Σₖ βⱼₖ = 1.
- **Estimação** por UF, com pesos *w*ᵢ = *A*ᵢ₁ normalizados:

  min_β Σᵢ *w*ᵢ ‖*Y*ᵢ − *X*ᵢ β‖²,

  um programa quadrático resolvido com SLSQP (gradiente analítico 2(*X*ᵀ*WX*β − *X*ᵀ*WY*)).
- **Combinação** das UFs ponderada pelo eleitorado de cada grupo; a faixa de incerteza são os percentis 10 e 90 entre UFs.
- **Conferência obrigatória:** Σᵢ *X*ᵢ β̂ reproduz o total observado do 2º turno, com erro abaixo de 0,1%.
- **Pressuposto:** homogeneidade das taxas dentro da UF.
- **Limite:** falácia ecológica. É uma média de grupos, nunca comportamento individual.

### 3.4 Divergências e agrupamento (E01–E03)
- **Esperado por UF (OLS):**

  *s*ᵢ = *X*ᵢγ + ε,

  com *X*ᵢ = (1, *p*ᵢ₁, *p*ᵢ₁², *o*ᵢ) no modelo simples, e no completo acrescentando:
  - a fração de cada eliminado;
  - branco+nulo do 1º turno;
  - Δ*c*ᵢ;
  - ln(eleitores do município);
  - o perfil (idosos, jovens, baixa escolaridade, superior, mulheres).
- **Padronização:** *z*ᵢ = (*s*ᵢ − *X*ᵢγ̂) / σᵢ, padronizado de forma robusta.
- **E01:** fração da variância dos *z* entre grupos (local, zona, município, UF): Var(média do grupo) / Var(*z*).
- **E02:** para o grupo *g* com *k* seções, *Z*_g = √*k* · *z̄*_g, que sob o nulo de independência é ~ N(0, 1). Calculam-se *p*-valores bilaterais, BH com *q* = 0,05 por nível, e o desvio-padrão de *Z*_g (1 sem agrupamento).
- **Calibração:** o mesmo cálculo em 2022. O normal do comportamento local é o nível de 2022, não o 1 teórico.
- **E03:** os grupos mais extremos, com características (tamanho, *p*₁, *o*, perfil).

  São achados **exploratórios**: só sobem de classe com confirmação em dados de outra origem (logs das urnas da própria seção, 2022, metade de municípios não usada).

### 3.5 Hora de chegada (T03) e urna trocada (T04)
- **T03:** Spearman ρ entre *r*ᵢ e o posto percentual da hora de chegada dentro do município (municípios com ≥ 20 seções).
  - Intervalo de 95% por Fisher: tanh(atanh ρ ± 1,96/√(*n*−3)).
  - Menor ρ detectável (α = 0,01 bilateral, poder de 80%): tanh[(*z*₀,₉₉₅ + *z*₀,₈)/√(*n*−3)].
- **T04:** diferença de médias de *z* entre seções com urna trocada e as demais.
  - Mann–Whitney e intervalo de 95% por bootstrap de municípios (200 réplicas, semente 5).
  - MDE = (*z*₀,₉₉₅ + *z*₀,₈) · EP_bootstrap.

---

## 4. Camada D: forense estatística

### 4.1 Último dígito (T05, T27), Beber e Scacco (2012), com correção de inclinação
- **Hipótese nula:** último dígito uniforme **dada a densidade local** das contagens.
- **Esperado:** para cada década [10*a*, 10*a*+9] ajusta-se, numa janela [10*a*−15, 10*a*+25), log *h*(*x*) = α + β*x* (densidade exponencial local). O peso de cada dígito *d* na década é proporcional a e^{β(10*a*+*d*)}.
- **Estatística:** χ² do observado contra a soma dos esperados (contagens ≥ 100).
- **Motivo:** a densidade decrescente favorece dígitos baixos; o uniforme puro acusaria dado limpo.

### 4.2 2º dígito de Benford (T26), Mebane
- **Esperado:** P(*d*) = Σ_{*k*=1}^{9} log₁₀(1 + 1/(10*k* + *d*)), com média ≈ 4,187.
- **Estatística:** χ² e média do 2º dígito, contagens ≥ 10.
- **Limite:** reage a contagens pequenas e a comportamento estratégico. **Acusa os dois anos e os dois candidatos, e por isso fica excluído da conclusão.**

### 4.3 Percentuais inteiros (T21), Kobak, Shpilkin e Pshenichnikov (2016) e Rozenas (2017)
- **Estatística:** *S* = #{*i*: 100·*k*ᵢ ≡ 0 (mod *n*ᵢ)}, ou seja, seções com percentual inteiro exato. É calculada para comparecimento (*k* = *C*, *n* = *A*) e para cada candidato (*k* = *V*, *n* = válidos).
- **Nulo:** 200 réplicas com *k*ᵢ* ~ Binomial(*n*ᵢ, *k*ᵢ/*n*ᵢ), que preservam o tamanho e a proporção de cada seção.
- **Teste:** *z* = (*S* − média*) / dp*.

### 4.4 Impressão digital e fraude incremental (T07, T22, T25), Klimek et al. (2012)
- **T07:** #{*c*ᵢ ≥ 0,95 e *V*ᵏ/*n* ≥ 0,90} por candidato; #{*c*ᵢ > 1}.
- **T25:** histograma 2D (*c*, *p*) em 50×50 classes; taxa logarítmica ν = ln[(1−*v*)/*v*], com assimetria e curtose em excesso; fração no canto (≥ 0,95, ≥ 0,95).
- **T22:** Spearman entre *c*ᵢ − *c̄*_*m* e *p*ᵢ − *p̄*_*m* (dentro do município).

  Fraude incremental (votos acrescentados ao favorecido) produz correlação positiva para o favorecido. Correlação pequena e simétrica entre os candidatos, e igual a 2022, é comportamento.

### 4.5 Poder com fraude sintética (T13)
- **Cenários aplicados ao 2º turno real:**
  - troca de uma fração *f* dos válidos de um candidato para o outro, em urnas sorteadas (0,1% a 20% das urnas; *f* de 2% a 20%), em todas as urnas de um estado (1% a 5%) ou uniforme no país (0,5% a 2%);
  - enchimento com uma fração das abstenções (0,1% a 5% das urnas; 50% e 100%).
- **Testes:**
  - T1: #{*z* > 5} (z robusto);
  - T2: max |*P* − *P̂*| com a virada da UF;
  - T3: canto do T07;
  - T4: virada da UF fora do esperado por (*p*₁, *p*₁², *o*), em z robusto entre UFs.
- **Limiares** calibrados para não acusar os dados reais:
  - T1 > base + max(5, 5√base);
  - T2 > 3 × base;
  - T3 > base + max(5, 5√base);
  - T4 > 3,5.
- **Resultado estrutural:** a troca uniforme nacional não altera diferenças entre urnas e é invisível a qualquer teste deste tipo.

### 4.6 Classificador com fraude sintética (T23), Zhang, Alvarez e Levin (2019)
- **Mundo simulado sem fraude (N2):**
  - *Ĉ*ᵢ₂ = round[(*c*ᵢ₁ + Δ*c*̃_*m* + ε^c_*π*(*i*)) *A*ᵢ₂];
  - *V̂*ᵢ₂¹³ ~ Binomial(*Ĉ*ᵢ₂ − *B*ᵢ₂ − *N*ᵢ₂, logit⁻¹(λ₁ + *s̃*_*m* + ε^s_*π*(*i*))).

  Aqui *s̃*_*m* e Δ*c*̃_*m* são as medianas do município, e (ε^s, ε^c) os resíduos reais reamostrados conjuntamente por uma permutação *π* (semente 23).
- **Fraude:** os cenários do T13 injetados em 10% das seções simuladas, metade a favor de cada lado.
- **Variáveis:** *c*₁, *c*₂, Δ*c*, *p*₁, *p*₂, *s*, branco+nulo, habilitação biográfica / *C*, ln *A* e os resíduos de *s*, *p*₂ e Δ*c* em relação ao município.
- **Classificador:** HistGradientBoosting (200 iterações), treinado em metade dos municípios e testado na outra.
- **Limiar:** quantil de 99% das seções limpas simuladas de teste. A medida principal é a fração das seções **reais** acima do limiar, comparada com 1% e com 2022.
- **Versão 1 (inválida, preservada):** usava os dados reais como classe limpa, o que é circular.

### 4.7 Sequência dos logs (T28–T31, T33), `analise/seqlog.py`
Para cada eleitor, no dia da eleição, a sequência de eventos tem:
- hora da habilitação *t*ʰ;
- tipo de habilitação:
  - biométrica;
  - biográfica (o mesário autoriza com a própria digital);
  - sem biometria cadastrada;
  - manual (dado pessoal);
- hora do voto *t*ᵛ.

O que cada teste calcula:
- **T28 (rajada no fim do dia):**
  - *U* = votos nos últimos 30 min de votação da urna; *X* = habilitações não biométricas entre eles;
  - taxa da própria urna no resto do dia: π̂ = (*X*_resto + ½)/(*U*_resto + 1);
  - *p* = P(Binomial(*U*, π̂) ≥ *X*); BH entre urnas;
  - *z* = (*X* − *U*π̂)/√(*U*π̂(1−π̂)).
  - **Explicações legítimas** a descartar antes de concluir: fila de idosos e problemas de leitor no fim do dia.
- **T29:** distribuição de *t*ᵛ − *t*ʰ (mínimo, percentil 1, mediana) e menor intervalo entre votos consecutivos.
- **T30:** votos "computado" fora do dia da eleição.
- **T31:** votos sem habilitação desde o voto anterior.
- **T33:** versões da aplicação e verificações de assinatura de software com e sem "SUCESSO".

### 4.8 Modelo de urna (T20)
Resíduo da virada menos a média do município, por modelo (lido do log): médias com intervalo de 95% e Kruskal–Wallis.

### 4.9 Biometria com controles (T12)
- **Regressão dentro do município:** (*y*, *x*) − média do município, com *y* = virada e *x* = (fração com habilitação biográfica; % idosos, jovens, baixa escolaridade, superior, mulheres; *p*₁; *o*; Δ*c*).
- **Erro-padrão** sanduíche agrupado por município: (*X*ᵀ*X*)⁻¹ (Σ_*m* *X*_*m*ᵀ*ê*_*m* *ê*_*m*ᵀ*X*_*m*) (*X*ᵀ*X*)⁻¹.
- **Nota:** o campo "sem habilitação biométrica" do BU na Web corresponde à habilitação **biográfica** do bu.dat (verificado em 100% das urnas do AC).

---

## 5. Armadilhas conhecidas (erros comuns, inclusive os nossos)
- **Curva acumulada que "vira":** é composição de lotes regionais, não voto mudando. Teste certo: curva prevista (3.2).
- **Comparar modelos de urna sem controlar região:** foi o caso do relatório de 2022 que pediu anular urnas.
- **Teto de 0/100%:** use logit, não diferença de percentual.
- **Último dígito contra uniforme puro:** falso positivo. Use a correção de inclinação (4.1).
- **Benford no 1º dígito:** não serve para votos (Deckert, Myagkov e Ordeshook, 2011).
- **Fuso horário:** horários do BU e do log são locais; fuso do município = 8 − hora local da abertura (moda das urnas que abriram nos primeiros 15 min).
- **Log do 2º turno contendo o do 1º:** filtre o dia.
- **Classe limpa = dados reais num classificador:** circular (T23 v1).
- **Reordenar a base no meio do script e usar vetores antigos:** desalinhamento (INC v1).
- ***p*-valor com meio milhão de seções:** sempre "significativo". Olhe o efeito e o MDE.

## Fontes
Bibliografia completa e classificada em `REFERENCIAS.md`. Principais:
- Klimek et al. (2012), PNAS;
- Beber e Scacco (2012), Political Analysis;
- Deckert, Myagkov e Ordeshook (2011), Political Analysis;
- Kobak, Shpilkin e Pshenichnikov (2016), Annals of Applied Statistics;
- Rozenas (2017), Political Analysis;
- Mebane (eforensics) e Kim (2025, crítica);
- Zhang, Alvarez e Levin (2019), PLOS ONE;
- Anwar, Jain e Kettler (2026);
- Lindeman e Stark (RLA);
- Goodman (1953) e King (1997), inferência ecológica;
- Benjamini e Hochberg (1995);
- Bernstein et al. (2012) e RFC 8032 (EdDSA);
- SafeCurves (E-521);
- FIPS 186 e 180-4.


## Fase 2, primeira sessão (T37 a T39)
- **T37:** X = frações reais por seção; taxa da seção B_i = softmax(log B0 + γ·s·z_m·d), com d = (+1 Lula, −1 adversário, 0, 0), B0 = matriz C06 gravada, z_m = ruído por município (S1) ou z-score do % de Lula do município dentro da UF (S2±). Y ~ Multinomial(aptos_2, X_i B_i). Verdade nacional T_jk = Σ X_ij w_i B_i,jk / Σ X_ij w_i. Erro = estimado − verdadeiro nas células Abs→Lula, Abs→Adversário e na razão.
- **T38:** z robusto do T02 por seção; mudança de comparecimento relativa à mediana do município; fração de valores positivos nas seções acima de 5 desvios, contra 50% no conjunto; votos excedentes = L2 − p_esperado·V2.
- **T39:** para cada seção, SHA-512 e tamanho de cada arquivo contra a lista assinada; assinatura da lista e de cada arquivo com a chave do certificado da urna; inteiros do `bu.dat` contêm seção, zona e município; RDV, imagem do BU e BU na Web comparados voto a voto (nulos por suspensão somados).
