"""F3 / R2: curva divulgada (capturas do Internet Archive do JSON nacional oficial de Presidente) × curva reconstruída pela
hora de recebimento dos boletins (DT_BU_RECEBIDO). Escopo de busca fixo (fase3/PREREG_RESPOSTAS.md, R2): uma consulta CDX por
eleição + o download de cada captura. Saídas: fase3/resultados/r2_curva_publica.json e fase3/externos/wayback_capturas/ (brutos)."""
import base64, gzip, hashlib, json, os, time, urllib.request, zlib
import numpy as np, pandas as pd

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."); OUTD = RAIZ + "/fase3/externos/wayback_capturas"; os.makedirs(OUTD, exist_ok=True)
EL = {"2022_1T": ("resultados.tse.jus.br/oficial/ele2022/544/dados-simplificados/br/br-c0001-e000544-r", "20221002190000", "20221003060000", "2022", 1),
      "2022_2T": ("resultados.tse.jus.br/oficial/ele2022/545/dados-simplificados/br/br-c0001-e000545-r", "20221030190000", "20221031060000", "2022", 2),
      "2026_1T": ("resultados.tse.jus.br/oficial/ele2026/6257/dados/br/br-c0001-e006257-u", "20261004190000", "20261005060000", "2026", 1),
      "2026_2T": ("resultados.tse.jus.br/oficial/ele2026/6258/dados/br/br-c0001-e006258-u", "20261025190000", "20261026060000", "2026", 2)}


def get(url, tent=3):
    """baixa por curl (o urllib do ambiente teve conexão recusada na 1ª execução: correção operacional declarada)"""
    import subprocess
    for i in range(tent):
        r = subprocess.run(["curl", "-s", "-f", "-m", "60", "-A", "urna-lab pesquisa (reproducao)", url], capture_output=True)
        if r.returncode == 0 and r.stdout: return r.stdout
        time.sleep(3 * (i + 1))
    raise RuntimeError(f"falha ao baixar {url}")


def decodifica(b):
    for f in (lambda x: x, gzip.decompress, lambda x: zlib.decompress(x, -15)):
        try: t = f(b)
        except Exception: continue
        t = t.strip()
        if t[:1] == b"{": return json.loads(t)
        if t.count(b".") == 2:   # JWS compacto: cabeçalho.payload.assinatura
            p = t.split(b".")[1]; p += b"=" * (-len(p) % 4)
            try: return json.loads(base64.urlsafe_b64decode(p))
            except Exception: pass
    return None


def extrai(d):
    cand = {}
    def walk(x):
        if isinstance(x, dict):
            if "n" in x and "vap" in x and str(x.get("n", "")).isdigit() and len(str(x["n"])) == 2: cand[int(x["n"])] = int(x["vap"] or 0)
            for v in x.values(): walk(v)
        elif isinstance(x, list):
            for v in x: walk(v)
    walk(d)
    st = d.get("st") if "st" in d else (d.get("s") or {}).get("st"); s = d.get("s") if isinstance(d.get("s"), str) else (d.get("s") or {}).get("ts")
    return {"dg": d.get("dg"), "hg": d.get("hg"), "st": int(str(st).replace(".", "")) if st not in (None, "") else None,
            "s": int(str(s)) if s not in (None, "") and str(s).isdigit() else None, "v13": cand.get(13), "v22": cand.get(22)}


R = {"pergunta": "R2", "desvios": "1ª execução: urllib com conexão recusada (trocado por curl, correção); 2ª: uma captura falhou e interrompeu (3ª execução tolera falha por captura; acima do orçamento, declarado)", "fonte": "Internet Archive (web.archive.org), capturas do JSON oficial do TSE; escopo fixo no pré-registro", "eleicoes": {}}
for nome, (pref, de, ate, ano, t) in EL.items():
    cdx = f"http://web.archive.org/cdx/search/cdx?url={pref}&matchType=prefix&output=json&fl=timestamp,original,digest&from={de}&to={ate}&filter=statuscode:200&limit=5000"
    try: lst = json.loads(get(cdx))[1:]
    except Exception as e:   # archive.org passou a recusar conexões: usa só as capturas já guardadas (sem rede), registrando o bloqueio
        cache = sorted(f for f in os.listdir(OUTD) if f.startswith(nome + "_"))
        lst = [(f.split("_")[2], "cache:" + f, f.split("_")[3][:-4]) for f in cache]
        R.setdefault("bloqueios", {})[nome] = f"índice do Internet Archive inacessível ({e}); usadas {len(cache)} capturas guardadas"
    vistos = set(); caps = []
    for ts, orig, dig in lst:
        if dig in vistos: continue
        vistos.add(dig)
        # desvio declarado (acima do orçamento): captura que falha é registrada e pulada; capturas já baixadas são reaproveitadas
        ja = [f for f in os.listdir(OUTD) if f.startswith(f"{nome}_{ts}_")]
        if ja: raw = open(f"{OUTD}/{ja[0]}", "rb").read(); fn = f"{OUTD}/{ja[0]}"
        else:
            try: raw = get(f"http://web.archive.org/web/{ts}id_/{orig}")
            except Exception as e:
                caps.append({"ts": ts, "erro": f"download falhou: {e}"}); continue
            fn = f"{OUTD}/{nome}_{ts}_{hashlib.sha256(raw).hexdigest()[:12]}.bin"; open(fn, "wb").write(raw)
        d = decodifica(raw)
        if not d: caps.append({"ts": ts, "erro": "não decodificado", "arquivo": os.path.basename(fn)}); continue
        e = extrai(d); e.update({"ts": ts, "url": orig, "sha256": hashlib.sha256(raw).hexdigest(), "arquivo": os.path.basename(fn)}); caps.append(e)
        time.sleep(2)
    ok = sorted([c for c in caps if c.get("v13") is not None and c.get("hg")], key=lambda c: (c["dg"], c["hg"], c["st"] or 0))
    # reconstrução pela hora de recebimento
    b = pd.read_parquet(f"{RAIZ}/analise/base.parquet" if ano == "2026" else f"{RAIZ}/analise/base_{ano}.parquet")
    b = b[b[f"total_{t}"].notna() & b[f"DT_BU_RECEBIDO_{t}"].notna()].sort_values(f"DT_BU_RECEBIDO_{t}").reset_index(drop=True)
    L, A = b[f"v13_{t}"].fillna(0).cumsum().values, b[f"v22_{t}"].fillna(0).cumsum().values; tr = pd.to_datetime(b[f"DT_BU_RECEBIDO_{t}"]).values
    Ls, As = np.sort(b[f"v13_{t}"].fillna(0).values), np.sort(b[f"v22_{t}"].fillna(0).values)
    LT, AT = float(b[f"v13_{t}"].sum()), float(b[f"v22_{t}"].sum())
    linhas = []
    for c in ok:
        pub_share = c["v13"] / (c["v13"] + c["v22"]); st = c["st"] or 0
        i = min(max(st, 1), len(L)) - 1; rec_share_st = L[i] / (L[i] + A[i])
        hora = pd.Timestamp(f"{c['dg'][6:10]}-{c['dg'][3:5]}-{c['dg'][0:2]} {c['hg']}")
        j = int(np.searchsorted(tr, np.datetime64(hora), side="right")) - 1
        rec_share_t = (L[j] / (L[j] + A[j])) if j >= 0 else None
        viavel = (Ls[:st].sum() <= c["v13"] <= Ls[::-1][:st].sum()) if st else None
        linhas.append({"data": c["dg"], "hora": c["hg"], "secoes_totalizadas": st, "lula": c["v13"], "adversario": c["v22"], "pct_lula_publicado": round(100 * pub_share, 3),
                       "pct_lula_reconstrucao_mesmas_secoes": round(100 * rec_share_st, 3), "dif_pp_secoes": round(100 * (pub_share - rec_share_st), 3),
                       "secoes_recebidas_ate_a_hora": j + 1, "pct_lula_reconstrucao_mesma_hora": None if rec_share_t is None else round(100 * rec_share_t, 3),
                       "lider_publicado": "Lula" if c["v13"] > c["v22"] else "adversário", "lider_reconstrucao": "Lula" if rec_share_st > 0.5 else "adversário",
                       "votos_lula_viaveis_com_st_secoes": viavel, "arquivo": c["arquivo"], "sha256": c["sha256"]})
    mono = all(linhas[k + 1]["lula"] >= linhas[k]["lula"] and linhas[k + 1]["adversario"] >= linhas[k]["adversario"] for k in range(len(linhas) - 1))
    trocas_pub = sum(1 for k in range(len(linhas) - 1) if linhas[k]["lider_publicado"] != linhas[k + 1]["lider_publicado"])
    final = [x for x in linhas if x["secoes_totalizadas"] and x["secoes_totalizadas"] >= 0.999 * len(L)]
    # defasagem recebimento → divulgação que melhor ajusta (validação/sensibilidade), 0 a 180 min
    lag = {}
    for dmin in range(0, 181, 5):
        errs = []
        for x in linhas:
            hora = pd.Timestamp(f"{x['data'][6:10]}-{x['data'][3:5]}-{x['data'][0:2]} {x['hora']}") - pd.Timedelta(minutes=dmin)
            j = int(np.searchsorted(tr, np.datetime64(hora), side="right")) - 1
            if j >= 0: errs.append(abs(x["secoes_totalizadas"] - (j + 1)))
        if errs: lag[dmin] = float(np.median(errs))
    R["eleicoes"][nome] = {"capturas_no_indice": len(lst), "capturas_unicas": len(caps), "capturas_lidas": len(linhas), "nao_decodificadas": [c for c in caps if "erro" in c],
                           "sequencia": linhas, "votos_nunca_diminuem": mono, "trocas_de_lider_entre_capturas": trocas_pub,
                           "consistentes_criterio_0_1pp_e_mesmo_lider": sum(1 for x in linhas if abs(x["dif_pp_secoes"]) < 0.1 and x["lider_publicado"] == x["lider_reconstrucao"]),
                           "max_abs_dif_pp_secoes": max([abs(x["dif_pp_secoes"]) for x in linhas], default=None),
                           "fora_do_intervalo_viavel": [x["hora"] for x in linhas if x["votos_lula_viaveis_com_st_secoes"] is False],
                           "captura_final_igual_ao_total": [{"hora": x["hora"], "lula_igual": x["lula"] == LT, "adv_igual": x["adversario"] == AT} for x in final],
                           "defasagem_mediana_secoes_por_minutos": lag, "melhor_defasagem_min": min(lag, key=lag.get) if lag else None}
    print(nome, {k: v for k, v in R["eleicoes"][nome].items() if k not in ("sequencia", "defasagem_mediana_secoes_por_minutos")}, flush=True)
json.dump(R, open(f"{RAIZ}/fase3/resultados/r2_curva_publica.json", "w"), ensure_ascii=False, indent=1, default=str)
