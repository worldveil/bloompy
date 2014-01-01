bloompy
====

Bloom filter written in 45 lines of Python code.

Currently only works with strings and numeric types. I built this on a car ride.

## Dependencies
* [mmh3](https://github.com/hajimes/mmh3) (C++ Murmur hash Python wrapper)

## Usage

To create a bloom filter, choose an approximate capacity and an acceptable error rate.

```python
>>> from bloompy import BloomFilter
>>> import random, math
>>> bf = BloomFilter(capacity=10000, error_rate=0.0001)
```

 Based on these preferences, `bloompy` will choose the optimal number of hash functions (`k`) and bit vector size (`m`): 

```python
>>> print bf
<BloomFilter n=10000, k=13, m=191701, p=0.0001>
```

Congrats! You now have an empty bloom filter. You can treat it like a Python `set`, with the exception that you cannot retrieve the keys. 

```python
>>> print "apple" in bf
False
>>> bf.add("apple")
>>> bf.add(9)
>>> bf.add("orange")
>>> print "apple" in bf and 9 in bf and "orange" in bf
True
```

## Implementation

For a given approximate number of elements (`n`) and a desired false positive probability (`p`), there exists an [optimal setting](http://en.wikipedia.org/wiki/Bloom_filter#Optimal_number_of_hash_functions) of:

* length of bit vector (`m`)
* number of hash functions (`k`)

in order to minimize the space required while still maintaining `p` under condition of `n` elements or less. These optimal settings are found through the equation for `m`:

    m* = -n * ln(p) / ln(2)^2
    
and for `k`:
    
    k = ln(2) * m / n

Instead of using a family of hash functions, I simply use `k` random salts (created upon instantiation) for the Murmur hash algorithm, which has phenomenal speed and key distribution. Each item to be added undergoes `k` hashings, each with a salt. Each 128 bit hash output is pulverized modulo the size of the bit vector (`m`), and that bit in the bit vector is set to 1.

Testing for membership simply involves hashing the item into a bit vector of size `m` with at most `k` set bits. This bit vector is `AND` with the bloom filter's vector, and then tested for equality with the original bit vector from hashing that element. 

## Performance

Speed: not so great, error adherence: right on.

```
[*] Now testing with 100000 unique strings and desired error rate of 0.001
[*] Performance results: 
pybloom: 1.711986 seconds with error rate = 0.001050
pybloomfilter: 0.303201 seconds with error rate = 0.000360
bloompy: 62.798033 seconds with error rate = 0.000990
```

As my implementation code is only 45 lines and I use the built-in Python `int` for the bitstring, that's not too surprising. 

As you can see the math works and the error rate is maintained quite well. `pybloomfilter` is really quite masterfully done, being quite fast and keeping the error rate lower than desired. 