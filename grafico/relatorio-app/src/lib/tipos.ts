// Tipos dos arquivos gerados por build-dados.mjs
export type Teste = {
  id: string; modulo: string; pergunta: string; metodo: string; modelo_nulo: string; script: string; comando: string; saida: string;
  situacao: string; referencia: string; hipotese_nula: string; pressupostos: string; limitacoes: string; afirmacao: string;
  independencia: string; natureza: string; classe_evidencia: string; resultado_atual: string; anotacoes: string[];
  versoes?: VersaoTeste[]; provas?: Prova[]; evidencia?: string; interpretacao?: string | null; impacto_votos?: string; metodo_versao?: number;
  pre_especificacao?: string; revisoes?: string[]; mudancas?: Mudanca[];
};
export type VersaoTeste = { versao: string; rodada: number; data: string; git_tag?: string; commit?: string; metodo_versao: number; situacao: string; classe_evidencia: string; natureza: string; resultado: string; evidencia?: string; interpretacao?: string | null; nota?: string; mudancas?: Mudanca[] };
export type Mudanca = { campo: string; causa: string; origem: string; justificativa: string };
export type Prova = { data: string; rodada: number; tipo: string; alvo?: string; descricao: string; resultado: 'resistiu' | 'caiu' | 'ajustado' | 'em_andamento' | 'em_revisao' | 'inalterado' };
export type Achado = { id: string; origem: string; secao: string; titulo: string; prioridade: string; testes: string[]; classificacao: string; verificacao_interna: string; resposta: string; acoes: string[]; fase_alvo: string; situacao: string; pendente: string };
export type Revisao = { pasta: string; revisao: string; titulo: string; revisor: string; data: string; alvo: string; classificacoes: Record<string, string>; situacoes: Record<string, string>; achados: Achado[] };
export type EtapaCaminho = { id: string; titulo: string; status: string; versao: string; texto: string; link: string };
export type PerguntaF2 = { id: string; pergunta: string; distingue: string; afirmacao: string; natureza: string; teste: string; origem: string; situacao?: string; resposta?: string; testes?: string[]; resumo_claro?: string; em_votos?: string; f3?: { estado_final: string; resposta: string } };
export type ItemF3 = { id: string; origem: string; pergunta: string; o_que_a_f2_demonstrou?: string; o_que_falta?: string; hipoteses_concorrentes?: string; menor_experimento?: string; criterio_de_encerramento?: string; alcance_em_votos?: string; estado_inicial_f3: string; trabalho_na_f3: string; estado_final: string; resposta_ou_motivo: string; proxima_evidencia: string };
export type Fase = { id: string; rodada: number | null; versao?: string; titulo: string; status: 'concluida' | 'em_andamento' | 'proxima' | 'planejada' | 'pendente'; inicio?: string; fim?: string; resumo: string; etapas: { titulo: string; texto: string }[] };
export type ResumoRodada = { rodada: number; versao: string | null; estado: string | null; commit: string | null; titulo: string; data: string; placar: { testes: number; classes: Record<string, number>; situacoes: Record<string, number>; natureza: Record<string, number> }; tag: string | null; arquivos: number };
export type LinhaDoTempo = { descricao: string; situacao_atual?: string | null; caminho: EtapaCaminho[]; revisoes: Revisao[]; fase2: PerguntaF2[]; fase3?: ItemF3[]; fases: Fase[]; marcos: { data: string; hora: string; titulo: string; texto: string }[]; conclusoes_recentes?: { titulo: string; texto: string; teste?: string }[]; rodadas: ResumoRodada[]; github: string };
export type Placar = { total: number; concluidos: number; parciais: number; processando: number; exploratorios: number; confirmatorios: number; classes: Record<string, number>; situacoes: Record<string, number> };
export type Registro = { descricao: string; modelos_nulos: Record<string, string>; classes: Record<string, string>; independencia: Record<string, string>; testes: Teste[]; placar: Placar };

export type Nacional = { lula1: number; lula2: number; comp1: number; comp2: number; bn2: number; eleitores: number; votos_lula2: number; votos_adv2: number; ganho_lula: number; ganho_adv: number; virada: number; dcomp: number; virada_nacional: number };
export type UFDados = { lula1: number; lula2: number; comp1: number; comp2: number; bn2: number; eleitores: number; votos_lula2: number; votos_adv2: number; ganho_lula: number; ganho_adv: number; virada: number; dcomp: number; virada_rel: number };
export type Fluxo = { linhas: string[]; colunas: string[]; votos: number[][]; por_uf: Record<string, number[][]>; conferencia_previsto: Record<string, number>; conferencia_observado: Record<string, number> };
export type Serie = { min: number[]; urnas: number[]; pct: Record<string, (number | null)[]>; prev: Record<string, (number | null)[]>; total_urnas: number; nomes: Record<string, string> };
export type LogResumo = Record<string, number | number[] | Record<string, number>> & { urnas: number; votos_log: number; log_igual_comparecimento: number; confirmacoes_igual_total: number; urnas_com_imgbu: number; rdv_igual_boletim: number; urnas_com_rdv: number; assin_lista_ok: number; urnas_substituidas: number; assin_ok_bu: number[]; assin_ok_rdv: number[]; assin_ok_log: number[]; assin_ok_imgbu: number[]; hash_ok_imgbu: number[]; hash_ok_bu: number[]; hash_ok_rdv: number[]; hash_ok_log: number[] };
export type Home = {
  gerado_em: string; fonte: string; totais_1: Record<string, number>; urnas_1: number; totais_2: Record<string, number>; urnas_2: number;
  nomes_1: Record<string, string>; nomes_2: Record<string, string>; datas: { t1: string; t2: string }; margem_votos: number;
  nacional: Record<string, Nacional>; ufs: Record<string, Record<string, UFDados>>; fluxo: Record<string, Fluxo>;
  apuracao: { t1: Serie; t2: Serie }; logs: Record<string, { t: number[]; votos: number[] }> | null;
  curva: { hora: string[]; real: number[]; prev_mun: number[]; prev_uf: number[] }; curva_max_desvio: { noite_toda: number; depois_19h: number };
  z_hist: { bordas: number[]; contagem: number[]; n: number; acima5_lula: number; acima5_flavio: number };
  log_resumo: Record<string, LogResumo>;
  poder: { margem_real_votos: number; cenarios: number; detectados: number; maior_passou_votos: number; grupos: { grupo: string; n: number; detectados: number }[] };
  placar: Placar; klimek20: Record<string, Record<string, number[][]> | null>;
};
export type TestesDados = {
  totais_1: Record<string, number>; urnas_1: number; totais_2: Record<string, number>; urnas_2: number;
  z_hist: Home['z_hist']; curva_max_desvio: Home['curva_max_desvio']; curva: Home['curva'];
  poder: { base: Record<string, number>; limiar: Record<string, number>; margem_real_votos: number; linhas: { cenario: string; grupo: string; votos: number; pct_validos: number; detectou: (number | boolean)[]; algum: boolean }[] };
  biometria: Record<string, Record<string, number>>; log_resumo: Record<string, LogResumo>;
  bateria: Record<string, Record<string, any>>; novos: Record<string, any>;
};
export type Mapas = {
  fonte: string; nacional: Record<string, Nacional>; campos: string[]; codigos: string[]; nomes: string[]; uf: string[]; municipios: number[][];
  ufs: Record<string, Record<string, UFDados>>; fluxo: Record<string, Fluxo>; klimek20: Record<string, Record<string, number[][]> | null>;
};
export type Mapas2022 = { campos: string[]; municipios: (number[] | null)[] };
export type DocSecao = { id: string; titulo: string; html: string; texto: string };
export type Doc = { slug: string; arquivo: string; titulo: string; resumo: string; github: string; secoes: DocSecao[] };
export type Docs = { github: string; docs: Doc[] };
export type Meta = { gerado_em: string; pdf: boolean; github: string; testes: number; situacao?: string | null };
