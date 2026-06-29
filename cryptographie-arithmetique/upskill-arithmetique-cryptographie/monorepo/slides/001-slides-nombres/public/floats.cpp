#include <bitset>
#include <iomanip>
#include <iostream>

void show_binary(float n)
{
  const unsigned char *ptr = (const unsigned char
          *)&n; // unsigned char is important here to avoid automatic binary
                // complement if individual bytes are negative representations
  std::cout << "n[0] = " << std::bitset<8>(ptr[0]) << std::endl;
  std::cout << "n[1] = " << std::bitset<8>(ptr[1]) << std::endl;
  std::cout << "n[2] = " << std::bitset<8>(ptr[2]) << std::endl;
  std::cout << "n[3] = " << std::bitset<8>(ptr[3]) << std::endl;

  auto mem = ptr[0] | (ptr[1] << 8) | (ptr[2] << 16) | (ptr[3] << 24);

  float x = *(const float *)&mem;
  std::cout << "x = " << x << std::endl;
  int sign = ptr[3] >> 7;
  std::cout << "sign = " << sign << std::endl;
  unsigned char biased_expo = ((ptr[3] << 1) | (ptr[2] >> 7));
  char expo = biased_expo - 127;
  std::cout << "biased_expo = " << int(biased_expo) << " "
            << std::bitset<8>(biased_expo) << std::endl;
  std::cout << "expo = " << int(expo) << " " << std::bitset<8>(expo)
            << std::endl;
  uint32_t mantissa =
      ptr[0] | (ptr[1] << 8) | (((uint8_t)(ptr[2] << 1) >> 1) << 16);
  std::cout << "mantissa = " << mantissa << " " << std::bitset<24>(mantissa)
            << std::endl;

  std::cout << "n = "
            << "(-1)**" << sign << " * 2**" << int(expo) << " * (1 + "
            << mantissa << " / 2**23)" << std::endl;
  float f = (sign == 0 ? 1 : -1) * (1 << int(expo)) *
            (1 + mantissa / (float)(1 << 23));
  std::cout << "f = " << f << std::endl;
}

int main(int argc, const char *argv[])
{
  std::cout << std::setprecision(32);

  show_binary(-118.625);
  show_binary(-478.081);
  show_binary(+0.0);
  show_binary(-0.0);

  show_binary(8388609.0f);

  std::cout << 4194304.0f << std::endl;
  std::cout << 4194304.25f << std::endl; // equal to 4194304.0f
  std::cout << 4194304.5f << std::endl;

  std::cout << 8388609.0f << std::endl;
  std::cout << 8388609.5f << std::endl; // equal to 8388610.0f
  std::cout << 8388610.0f << std::endl;

  std::cout << 16777216.0f << std::endl;
  std::cout << 16777217.0f << std::endl; // equal to 16777216.0f
  std::cout << 16777218.0f << std::endl;

  return 0;
}
