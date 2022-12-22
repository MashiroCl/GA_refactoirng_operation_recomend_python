import unittest


class MyTestCase(unittest.TestCase):
    def test_something(self):
        dictionary = ["cat","catt","rat"]
        trie = {}
        for word in dictionary:
            cur = trie
            for c in word:
                # print("c",c)
                # print("before_trie", trie)
                if c not in cur:
                    cur[c] = {}
                    # print("cur",cur)
                # print("cur", cur)
                print("after_trie", trie)
                # print("before：",id(cur))
                # print(id(trie))
                cur = cur[c]
                # print(id(cur))
                print("cur",cur)
                # print("trie", trie)
            cur['#'] = {}

        # d = {1:1,2:2,3:3}
        # c=d
        # c[4]=4
        # c=c[4]
        # print(c)
        # print(d)


if __name__ == '__main__':
    unittest.main()
