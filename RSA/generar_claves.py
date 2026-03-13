from Crypto.PublicKey import RSA

def generar_par_claves(bits: int = 3072):
    # genera el par
    key = RSA.generate(bits)

    # extraer del par las llaves
    public_key = key.publickey().export_key()
    private_key = key.export_key()

    with open("public_key.pem", "wb") as f:
        f.write(public_key)

    with open("private_key.pem", "wb") as f:
        f.write(private_key)

if __name__ == '__main__':
    generar_par_claves(3072)
    print("Claves generadas: private_key.pem y public_key.pem")