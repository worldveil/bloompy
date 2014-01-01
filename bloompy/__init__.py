import mmh3, random, math

class BloomFilter():
    SALT_SIZE = 5
    def __init__(self, capacity, error_rate):
        self.p, self.n, self.vector, self.salts = error_rate, int(capacity), 0, set()
        self.m = int(-self.n * math.log(self.p) / math.log(2)**2)
        self.k = int(math.log(2) * self.m / self.n)
        while len(self.salts) < self.k:
            salt = ""
            for j in range(BloomFilter.SALT_SIZE):
                salt += chr(random.randint(0, 255))
            self.salts.add(salt)
            
    def _hash(self, item):
        bloom = 0
        for salt in self.salts:
            bloom |= (1L << (mmh3.hash128(salt + str(item)) % self.m))
        return bloom

    def add(self, item):
        self.vector |= self._hash(item)

    def __contains__(self, item):
        h = self._hash(item)
        return ((h & self.vector) == h)
        
    def __repr__(self):
        return "<BloomFilter n=%d, k=%d, m=%d, p=%f>" % (self.n, self.k, self.m, self.p)