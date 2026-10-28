"""T60b (complemento): testes unitários negativos e positivo do verificador Ed521 do projeto, com chave e assinatura reais de uma urna."""
import hashlib, json, sys, zipfile, os
os.environ["ANO"] = "2026"
R = "."; sys.path.insert(0, R + "/analise"); sys.path.insert(0, R + "/operacao_veracidade/scripts")
import der, ed521, processar_brutos as PB, cadeia  # noqa: E402
pacote, _ = PB.fonte(2, "AC"); z = zipfile.ZipFile(pacote)
n = next(x for x in z.namelist() if x.endswith("-vota.vsc")); raiz, _ = der.ler(z.read(n))
ue = next(b for b in raiz["f"] if b["k"] and len(b["f"]) >= 5 and b["f"][2]["k"] and b["f"][2]["f"][0]["f"][0]["v"][:4].upper() == b"UEAO")
info = cadeia.analisa_cert(ue["f"][4]["v"], cadeia.carrega_acs()); pub = info["pub"]
h = ue["f"][2]["f"][3]["f"][1]["v"]; sig = ue["f"][2]["f"][3]["f"][2]["v"]
L = int(ed521.L); S = int.from_bytes(sig[66:], "little")
neutro = (1).to_bytes(66, "little")                       # ponto neutro (x = 0, y = 1)
casos = {"0_controle_genuino": (pub, sig, h, True),
         "1_hash_diferente": (pub, sig, hashlib.sha512(h).digest(), False),
         "2_bit_alterado_em_R": (pub, bytes([sig[0] ^ 1]) + sig[1:], h, False),
         "3_bit_alterado_em_S": (pub, sig[:66] + bytes([sig[66] ^ 1]) + sig[67:], h, False),
         "4_S_mais_L_(nao_canonica)": (pub, sig[:66] + ((S + L) % (1 << 528)).to_bytes(66, "little"), h, False),
         "5_assinatura_truncada": (pub, sig[:-1], h, False),
         "6_chave_neutra_com_R_neutro_e_S_zero": (neutro, neutro + (0).to_bytes(66, "little"), h, False),
         "7_chave_de_outra_urna": (cadeia.carrega_acs()["AC UE2020"][1], sig, h, False),
         "8_chave_vazia": (b"", sig, h, False)}
out = {}
for k, (p, s, hh, esperado) in casos.items():
    try: r = bool(ed521.verifica(p, s, hh))
    except Exception as e: r = f"excecao: {type(e).__name__}"
    out[k] = {"resultado": r, "esperado": esperado, "ok": r is esperado}
out["todos_conforme_esperado"] = all(v["ok"] for v in out.values() if isinstance(v, dict))
json.dump(out, open(f"{R}/operacao_veracidade/resultados/ed521_unitarios.json", "w"), ensure_ascii=False, indent=1); print(json.dumps(out, ensure_ascii=False, indent=1))
