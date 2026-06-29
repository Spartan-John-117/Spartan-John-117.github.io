#include <bitset>
#include <iostream>

void show_binary(int n)
{
  std::cout << "n = " << n << " = " << std::bitset<32>(n) << std::endl;

  const unsigned char *ptr = (const unsigned char
          *)&n; // unsigned char is important here to avoid automatic binary
                // complement if individual bytes are negative representations
  std::cout << "n[0] = " << std::bitset<8>(ptr[0]) << std::endl;
  std::cout << "n[1] = " << std::bitset<8>(ptr[1]) << std::endl;
  std::cout << "n[2] = " << std::bitset<8>(ptr[2]) << std::endl;
  std::cout << "n[3] = " << std::bitset<8>(ptr[3]) << std::endl;

  auto x =
      ptr[0] | (ptr[1] << 8) | (ptr[2] << 16) |
      (ptr[3] << 24); // even if bit order is little endian, we can still write
                      // binary operation as if we were pushing bits to the left
  std::cout << "x = " << x << " = " << std::bitset<32>(x) << std::endl;
}

void show_complement(int n)
{
  std::cout << "n = " << n << " = " << std::bitset<32>(n) << std::endl;
  std::cout << "-n = " << -n << " = " << std::bitset<32>(-n) << std::endl;

  auto two_complement = ~n + 1;
  std::cout << "~n + 1 = " << two_complement << " = "
            << std::bitset<32>(two_complement) << std::endl;
}

int main(int argc, const char *argv[])
{
  //show_binary(-127);
  //show_binary(14786528);
  show_binary(58);

  show_complement(58);
  show_complement(1278);

  show_complement(2147483647);     // The highest int32
  show_complement(2147483647 + 1); // The lowest int32

  show_complement(-1);

  std::cout << (unsigned int)-1 << std::endl;

  return 0;
}
