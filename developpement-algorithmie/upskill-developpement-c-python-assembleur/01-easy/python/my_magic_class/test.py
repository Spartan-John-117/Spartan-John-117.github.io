# Code de test
if __name__ == "__main__":
    # Cas 1
    test1 = Dummy(a=12, b="test")
    print("Cas 1:")
    print(f"test1.desc = {test1.desc}")  # "instance magic"
    print(f"test1.a = {test1.a}")  # 12
    print(f"test1.b = {test1.b}")  # "test"
    
    # Cas 2
    test2 = Dummy(unicorn="pink invisible", desc="le constructeur est magic")
    print("\nCas 2:")
    print(f"test2.desc = {test2.desc}")  # "le constructeur est magic"
    print(f"test2.unicorn = {test2.unicorn}")  # "pink invisible"
    
    # Cas 3
    test3 = Dummy(1, 2, 3, 4, desc="non vraiment")
    print("\nCas 3:")
    print(f"test3[0] = {test3[0]}")  # 1
    print(f"test3[1] = {test3[1]}")  # 2
    print(f"test3[2] = {test3[2]}")  # 3
    print(f"test3[3] = {test3[3]}")  # 4
    print(f"test3.desc = {test3.desc}")  # "non vraiment"
