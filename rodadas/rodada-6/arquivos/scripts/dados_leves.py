"""Gera o pacote de dados leves (dados_leves/): o que é preciso para repetir boa parte das análises sem baixar os ~405 GB do TSE.
Tudo é derivado dos arquivos oficiais pelo código deste repositório; a correspondência com os brutos é garantida pelo manifesto
(dados/listas/MANIFESTO.csv) e por SHA256SUMS. PRELIMINAR: atualizado a cada versão; ver dados_leves/LEIAME.md.
Uso: python scripts/dados_leves.py   (publicado como anexo do release no GitHub, não no git)"""
import glob, hashlib, json, os, shutil, subprocess, zipfile
import pandas as pd

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."); AN = os.path.join(RAIZ, "analise"); OUT = os.path.join(RAIZ, "dados_leves")
os.makedirs(OUT, exist_ok=True)
versao = json.load(open(os.path.join(RAIZ, "rodadas", "linha_do_tempo.json")))["situacao_atual"]
arquivos = {}


def salva(df, nome, csv=False):
    p = os.path.join(OUT, nome + ".parquet"); df.to_parquet(p, index=False, compression="zstd"); arquivos[nome + ".parquet"] = (len(df), list(df.columns))
    if csv: df.to_csv(os.path.join(OUT, nome + ".csv.gz"), index=False, compression="gzip"); arquivos[nome + ".csv.gz"] = (len(df), None)


# 1. resultado por seção (tabela BU na Web do TSE, 1º e 2º turnos numa linha)
for ano, f in (("2026", "base.parquet"), ("2022", "base_2022.parquet")):
    salva(pd.read_parquet(os.path.join(AN, f)), f"secoes_{ano}", csv=True)
# 2. resumo por urna lido dos arquivos das urnas (boletim, RDV, imagem, log, assinaturas)
for ano, t, pas in (("2026", 1, "1t"), ("2026", 2, "2t"), ("2022", 1, "2022_1t"), ("2022", 2, "2022_2t")):
    fs = sorted(glob.glob(os.path.join(AN, "brutos", pas, "urnas_*.parquet")))
    if fs: salva(pd.concat([pd.read_parquet(x) for x in fs], ignore_index=True), f"urnas_{ano}_{t}t")
    fm = sorted(glob.glob(os.path.join(AN, "brutos", pas, "minutos_*.parquet")))
    if fm: salva(pd.concat([pd.read_parquet(x) for x in fm], ignore_index=True), f"votos_por_minuto_{ano}_{t}t")
# 3. perfil do eleitorado por seção (proporções), 2026 e 2022
for ano, pasta in (("2026", "dados/perfil_eleitorado"), ("2022", "dados/2022/perfil_eleitorado")):
    partes = []
    for z in sorted(glob.glob(os.path.join(RAIZ, pasta, f"perfil_eleitor_secao_{ano}_*.zip"))):
        zf = zipfile.ZipFile(z); nome = [n for n in zf.namelist() if n.endswith(".csv")][0]
        col = "QT_ELEITORES" if ano == "2026" else "QT_ELEITORES_PERFIL"
        pf = pd.read_csv(zf.open(nome), sep=";", encoding="latin-1", usecols=["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO", "CD_GENERO", "CD_FAIXA_ETARIA", "CD_GRAU_ESCOLARIDADE", col])
        k = ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"]; tot = pf.groupby(k)[col].sum()
        d = pd.DataFrame({"eleitores": tot, "fem": pf[pf.CD_GENERO == 4].groupby(k)[col].sum() / tot})
        for c in sorted(pf.CD_GRAU_ESCOLARIDADE.unique()):
            if c > 0: d[f"esc_{c}"] = pf[pf.CD_GRAU_ESCOLARIDADE == c].groupby(k)[col].sum() / tot
        idade = pf.CD_FAIXA_ETARIA // 100
        for nome_f, (lo, hi) in {"ate24": (0, 24), "25a34": (25, 34), "35a44": (35, 44), "45a59": (45, 59), "60mais": (60, 200)}.items():
            d[f"idade_{nome_f}"] = pf[(idade >= lo) & (idade <= hi)].groupby(k)[col].sum() / tot
        partes.append(d.fillna(0).reset_index())
    if partes: salva(pd.concat(partes, ignore_index=True), f"perfil_por_secao_{ano}")
# 4. resultados das investigações (pequenos) e capturas da divulgação ao vivo
dst = os.path.join(OUT, "resultados"); os.makedirs(dst, exist_ok=True)
for f in glob.glob(os.path.join(RAIZ, "fase3", "resultados", "*.json")) + glob.glob(os.path.join(RAIZ, "fase3", "resultados", "*.csv")) + glob.glob(os.path.join(AN, "resultado_*.json")):
    shutil.copy2(f, dst)
shutil.copy2(os.path.join(RAIZ, "fase3", "veredito_2026.json"), OUT); shutil.copy2(os.path.join(RAIZ, "fase3", "respostas_f3.json"), OUT)
shutil.copytree(os.path.join(RAIZ, "fase3", "externos", "wayback_capturas"), os.path.join(OUT, "capturas_divulgacao_ao_vivo"), dirs_exist_ok=True)
shutil.copy2(os.path.join(RAIZ, "dados", "listas", "MANIFESTO.csv"), OUT)
# SHA256SUMS
linhas = []
for r, _, fs in os.walk(OUT):
    for f in sorted(fs):
        if f in ("SHA256SUMS", "LEIAME.md", "DICIONARIO.md"): continue
        p = os.path.join(r, f); linhas.append(f"{hashlib.sha256(open(p, 'rb').read()).hexdigest()}  {os.path.relpath(p, OUT)}")
open(os.path.join(OUT, "SHA256SUMS"), "w").write("\n".join(sorted(linhas, key=lambda x: x.split('  ')[1])) + "\n")
commit = subprocess.run(["git", "-C", os.path.join(RAIZ, "..", "urna-lab-publico"), "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
json.dump({"gerado_com": versao, "commit_publico": commit, "arquivos": {k: {"linhas": v[0], "colunas": v[1]} for k, v in arquivos.items()}}, open(os.path.join(OUT, "conteudo.json"), "w"), ensure_ascii=False, indent=1)
tam = sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(OUT) for f in fs)
print(f"dados_leves: {len(linhas)} arquivos, {tam / 1e6:.0f} MB")
