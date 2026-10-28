import json, sys, numpy as np, collections
d = json.load(open(sys.argv[1]))
for ano, a in d["anos"].items():
    print("==", ano, "seed", a["seed"], "gamma", a["gamma"])
    if "reproducao_c06" in a: print(" reprodução C06:", a["reproducao_c06"])
    g = collections.defaultdict(list)
    for r in a["adversarial"]: g[r["cenario"]].append(r)
    for c, rs in g.items():
        f = lambda k, i: np.array([x[k][i] for x in rs])
        el = f("abs_lula", 1) - f("abs_lula", 0); ea = f("abs_adv", 1) - f("abs_adv", 0)
        rz = f("razao_abs", 1); rt = f("razao_abs", 0)
        print(f" {c:3} verdade Abs→L {f('abs_lula',0).mean():.4f} est {f('abs_lula',1).mean():.4f} (erro {el.mean():+.4f}, max|e| {np.abs(el).max():.4f}) | Abs→A verd {f('abs_adv',0).mean():.4f} est {f('abs_adv',1).mean():.4f} (erro {ea.mean():+.4f}) | razão verd {rt.mean():.2f} est {rz.mean():.2f} [{rz.min():.2f},{rz.max():.2f}] | EAM36 {np.mean([x['eam_36'] for x in rs]):.4f} | err.total Lula 2T {np.mean([abs(x['erro_total_2t_lula_rel']) for x in rs]):.2e} | nconv {sum(x['nao_convergiu'] for x in rs)}")
    if "contabilidade" in a: print(json.dumps(a["contabilidade"], indent=0, ensure_ascii=False)[:2600])
