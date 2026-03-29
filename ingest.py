import sys
from long_memory import LongTermMemory

def main():
    if len(sys.argv) < 2:
        print("Penggunaan: python ingest.py \"teks memori yang ingin ditambahkan\"")
        print("Atau: python ingest.py --file path/to/file.txt")
        return

    ltm = LongTermMemory()

    if sys.argv[1] == "--file" and len(sys.argv) == 3:
        filepath = sys.argv[2]
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                # Split by double newline to add as separate chunks if necessary
                chunks = [c.strip() for c in content.split("\n\n") if c.strip()]
                for chunk in chunks:
                    ltm.add_memory(chunk)
                print(f"Berhasil menambahkan {len(chunks)} memori dari file {filepath}.")
        except Exception as e:
            print(f"Gagal membaca file: {e}")
    else:
        text = " ".join(sys.argv[1:])
        ltm.add_memory(text)
        print("Berhasil menambahkan memori baru.")

if __name__ == "__main__":
    main()
