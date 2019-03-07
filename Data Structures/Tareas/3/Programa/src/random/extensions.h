#pragma once

#include "pcg_basic.h"

/** Generates a random double in the interval [0, bound] */
uint64_t get_random();

/** Sets an integer as random seed */
void random_seed(int seed);
