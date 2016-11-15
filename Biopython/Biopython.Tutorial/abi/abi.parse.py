from Bio import SeqIO

abi_list = ["k18_2_U.ab1", "k18_2_L.ab1", "w18_2_U.ab1", "w18_2_L.ab1"]
for abi_file in abi_list:
    handle = open("w18_2_U.ab1", "rb")
for record in SeqIO.parse(handle, "abi"):
    print(dir(record))
    print("ID:", record.id)
    print("description", record.description)
    print(record.annotations.keys())
    print(record.annotations['abif_raw'].keys())
    print("annotations", record.annotations)
    print("features", record.features)
    print("seq", record.seq)
    handle.close()

with open("w18_2_U.ab1", 'rb') as ABI:
    for line in ABI:
        print(line)