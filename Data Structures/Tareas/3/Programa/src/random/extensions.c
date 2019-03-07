#include "extensions.h"

/** Generates a random double in the interval [0, bound] */
uint64_t get_random()
{
		uint64_t random = ((uint64_t)pcg32_random() << 32) + pcg32_random();
		return random;
}

/** Sets an integer as random seed */
void   random_seed(int seed)
{
	pcg32_srandom((0x853c49e6748fea9bULL ^ seed) | 1, 0xda3e39cb94b95bdbULL);
}
