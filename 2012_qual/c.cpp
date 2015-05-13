#include <iostream>
#include <vector>
#include <algorithm>

using uint64 = unsigned long long;

class CountRecycled {
public:
	CountRecycled(uint64 A, uint64 B) : mA{A}, mB{B}
	{
		pow10 = 1;
		length = 1;
		uint64 x = mA;
		while ( x >= 10 ) {
			x /= 10;
			pow10 *= 10;
			++length;
		}
	}

	uint64 count_recycled(const uint64 n)
	{
		uint64 m = n;
		buffer.clear();
		for (int i = 0; i < length; ++i) {
			m = (m / 10) + pow10 * (m % 10); // Rotate m
			// m could have a leading zero, but then "n < m" is false...
			if ( n < m and m <= mB ) { buffer.push_back(m); }
		}
		uint64 count = static_cast<uint64>(buffer.size());
		if ( count <= 1 ) { return count; }
		std::sort(buffer.begin(), buffer.end());
		auto front = buffer.begin();
		auto back = front + 1;
		while ( back != buffer.end() ) {
			if ( *front == *back ) { --count; }
			++front; ++back;
		}
		return count;
	}

	uint64 count()
	{
		uint64 count = 0;
		for (uint64 n = mA; n < mB; ++n) {
			count += count_recycled(n);
		}
		return count;
	}
private:
	uint64 mA, mB, pow10;
	int length;
	std::vector<uint64> buffer;
};

int main()
{
	int num_cases;
	std::cin >> num_cases;
	for (int cas = 1; cas <= num_cases; ++cas) {
		uint64 A, B;
		std::cin >> A >> B;
		uint64 output = CountRecycled(A, B).count();
		std::cout << "Case #" << cas << ": " << output << std::endl;
	}
}
