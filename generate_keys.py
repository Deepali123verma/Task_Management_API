from Crypto.PublicKey import RSA

# Generate 2048-bit RSA key pair
key = RSA.generate(2048)

private_key = key.export_key()
with open("private.pem", "wb") as f:
    f.write(private_key)

public_key = key.publickey().export_key()
with open("public.pem", "wb") as f:
    f.write(public_key)

print("Public and Private keys generated successfully.")
