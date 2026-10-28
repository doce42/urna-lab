"""Leitura da SEQUÊNCIA de eventos do log da urna, eleitor por eleitor (testes T28–T31 e T33 do PROTOCOLO, emenda 1).

Para cada eleitor no dia da eleição: hora da habilitação, tipo de habilitação e hora do voto computado.
  - tipo "biometrica":   "Tipo de habilitação do eleitor [biométrica]"
  - tipo "manual":       "Solicitação de dado pessoal do eleitor para habilitação manual" (sem digital do eleitor)
  - tipo "mesario":      "Solicita digital do mesário" antes da habilitação (o mesário autoriza com a própria digital)
  - tipo "outro":        habilitado sem nenhum dos marcadores acima
Resumo por urna:
  T28 rajada no fim: habilitações sem biometria (manual/mesário/outro) nos últimos 30 min de votação x resto do dia
  T29 tempo entre habilitação e voto (s): mínimo, 1º percentil, mediana; nº de votos abaixo de 5 s; menor intervalo entre
      votos consecutivos (s)
  T30 votos computados fora do dia da eleição (testes/carga são outro dia) e no dia antes das 07h00 locais
  T31 votos computados sem habilitação desde o voto anterior
  T33 versões da aplicação, verificações de assinatura de software com e sem sucesso
"""
import re
from datetime import datetime

ETAPA = re.compile(r"Verificação de assinatura - Etapa \[\d+\]\s*$")
VERIF = re.compile(r"Verificação de assinatura.*\[(SUCESSO|[^\]]*)\]\s*$")


def _t(s):
    return datetime.strptime(s, "%d/%m/%Y %H:%M:%S")


def analisa(linhas, dia, ano="2026"):
    """linhas: linhas do log (todas as partes); dia: 'dd/mm/aaaa' da eleição. Devolve dict de colunas por urna."""
    r = {"seq_votos_dia": 0, "seq_votos_fora_dia": 0, "seq_votos_antes_7h": 0, "seq_sem_habilitacao": 0,
         "seq_hab_biometrica": 0, "seq_hab_manual": 0, "seq_hab_mesario": 0, "seq_hab_outro": 0,
         "sw_verif_ok": 0, "sw_verif_falha": 0}
    versoes, duracoes, votos = set(), [], []
    tipos = []  # (hora do voto, tipo) para a análise do fim do dia
    hab_t, tipo, pend_manual, pend_mesario = None, None, False, False
    for l in linhas:
        p = l.split("\t")
        if len(p) < 5:
            continue
        msg = p[4]
        if msg.startswith("Versão da aplicação:"):
            versoes.add(msg.split(":", 1)[1].strip())
            continue
        if ano == "2022" and ETAPA.match(msg):  # 2022: "Verificação de assinatura - Etapa [N]" é só andamento, não resultado
            continue
        if msg.startswith("Verificação de assinatura"):
            m = VERIF.search(msg)
            if m and m.group(1) == "SUCESSO":
                r["sw_verif_ok"] += 1
            else:
                r["sw_verif_falha"] += 1
            continue
        if not p[0].startswith(dia):
            if msg.startswith("O voto do eleitor foi computado"):
                r["seq_votos_fora_dia"] += 1
            continue
        if msg.startswith("Aguardando digitação do identificador") or (ano == "2022" and msg.startswith("Aguardando digitação do título")):
            pend_manual = pend_mesario = False
            tipo = None
        elif msg.startswith("Solicitação de dado pessoal do eleitor para habilitação manual"):
            pend_manual = True
        elif msg.startswith("Solicita digital do mesário"):
            pend_mesario = True
        elif msg.startswith("Tipo de habilitação do eleitor [biométrica]"):
            tipo = "biometrica"
        elif msg.startswith("Eleitor foi habilitado"):
            hab_t = p[0]
            if tipo is None:
                tipo = "mesario" if pend_mesario else "manual" if pend_manual else "outro"
        elif msg.startswith("O voto do eleitor foi computado"):
            r["seq_votos_dia"] += 1
            t = _t(p[0])
            if t.hour < 7:
                r["seq_votos_antes_7h"] += 1
            if hab_t is None:
                r["seq_sem_habilitacao"] += 1
                tipos.append((t, "sem"))
            else:
                duracoes.append((t - _t(hab_t)).total_seconds())
                r[f"seq_hab_{tipo}"] += 1
                tipos.append((t, tipo))
            votos.append(t)
            hab_t, tipo, pend_manual, pend_mesario = None, None, False, False
    r["sw_versoes"] = "|".join(sorted(versoes))
    if duracoes:
        d = sorted(duracoes)
        r["seq_dur_min"] = d[0]
        r["seq_dur_p01"] = d[int(0.01 * (len(d) - 1))]
        r["seq_dur_mediana"] = d[len(d) // 2]
        r["seq_dur_abaixo_5s"] = sum(x < 5 for x in d)
    if len(votos) > 1:
        r["seq_intervalo_min"] = min((b - a).total_seconds() for a, b in zip(votos, votos[1:]))
    if tipos:
        fim = tipos[-1][0]
        ult = [k for t, k in tipos if (fim - t).total_seconds() <= 1800]
        resto = [k for t, k in tipos if (fim - t).total_seconds() > 1800]
        r["seq_ult30_votos"] = len(ult)
        r["seq_ult30_sem_biometria"] = sum(k != "biometrica" for k in ult)
        r["seq_resto_votos"] = len(resto)
        r["seq_resto_sem_biometria"] = sum(k != "biometrica" for k in resto)
    return r
