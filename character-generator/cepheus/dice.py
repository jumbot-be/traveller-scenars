import random


class Rng:
    """Seeded dice roller. Every roll is drawn from one random.Random so a
    whole character is reproducible from its seed."""

    def __init__(self, seed=None):
        if seed is None:
            seed = random.SystemRandom().randrange(2 ** 63)
        self.seed = int(seed)
        self._r = random.Random(self.seed)

    def d6(self, n=1):
        return [self._r.randint(1, 6) for _ in range(n)]

    def d6_sum(self, n=1):
        return sum(self.d6(n))

    def choice(self, seq):
        return self._r.choice(seq)

    def randint(self, a, b):
        return self._r.randint(a, b)

    def shuffle(self, seq):
        seq = list(seq)
        self._r.shuffle(seq)
        return seq

    def random(self):
        return self._r.random()
