import random


class DataEnv(object):
    def __init__(self, filepath):
        self._filepath = filepath
        self._ent2id = {}
        self._rel2id = {}
        self._storage = set()
        self._cur_draw = None

        self._load()
        self._id2ent = {v: k for k, v in self._ent2id.items()}
        self._id2rel = {v: k for k, v in self._rel2id.items()}

    def _load(self):
        with open(self._filepath) as fin:
            for line in fin.readlines():
                head, rel, tail = line.strip().split('\t')
                hid = self._ent2id.setdefault(head, len(self._ent2id))
                rid = self._rel2id.setdefault(rel, len(self._rel2id))
                tid = self._ent2id.setdefault(tail, len(self._ent2id))
                self._storage.add((hid, rid, tid))

    def observe(self, k=1):
        self._cur_draw = random.sample(self._storage, k)
        heads, rels, _ = zip(*self._cur_draw)
        n_rest = len(self._storage)
        return heads, rels, n_rest

    def _hit(self, head, rel, t_li):
        for t in t_li:
            if (head, rel, t) in self._storage:
                return t
        return None

    def act(self, decisions, t_lists):
        rewards, results = [], []
        heads, rels, tails = zip(*self._cur_draw)
        for dec, head, rel, tail, t_li in zip(decisions, heads, rels, tails, t_lists):
            if dec == 'FLIP':
                results.append(tail)
                rewards.append(0.)
                self._storage.remove((head, rel, tail))
            elif dec == 'BET':
                t = self._hit(head, rel, t_li)
                results.append(t)
                if t is None:
                    rewards.append(-1.)
                else:
                    rewards.append(1.)
                    self._storage.remove((head, rel, t))
            elif dec == 'RETURN':
                results.append(None)
                rewards.append(0.)
            elif dec == 'DISCARD':
                results.append(None)
                rewards.append(0.)
            else:
                raise ValueError('{} is a wrong decision'.format(dec))
        self._cur_draw = None
        return rewards, results


if __name__ == '__main__':
    data_env = DataEnv('data/WN/data')
    print(data_env.observe(k=4))
    print(data_env.act(['FLIP', 'FLIP', 'FLIP', 'BET'], [[],[],[],[4,5,6,7]]))