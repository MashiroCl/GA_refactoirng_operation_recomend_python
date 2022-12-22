import unittest
from collaboration.collaboration import get_pr_history, get_collaboration_score
from collaboration.graph import Graph
import collaboration.pullrequest as pullrequest
import utils.csv as csv


class MyTestCase(unittest.TestCase):
    def test_get_pullrequest_comments(self):
        pr_str = {'url': 'https://api.github.com/repos/bennidi/mbassador/pulls/167',
                  'state': 'open',
                  'user': {'login': 'FlorianKirmaier'},
                  'comments_url': 'https://api.github.com/repos/bennidi/mbassador/issues/167/comments'
                  }
        pr = pullrequest.Pullrequest(pr_str)
        comments = pr.get_comments()
        self.assertTrue(len(comments) == 3)

    def test_write_pullrequest2csv(self):
        pr_str = {'url': 'https://api.github.com/repos/bennidi/mbassador/pulls/167',
                  'state': 'open',
                  'user': {'login': 'FlorianKirmaier'},
                  'comments_url': 'https://api.github.com/repos/bennidi/mbassador/issues/167/comments'
                  }
        pr = pullrequest.Pullrequest(pr_str)
        pr.get_comments()
        with open("./pullrequest.csv", "a") as f:
            csv.pullrequest2csv([pr], f)

    def test_get_pullrequests(self):
        get_pr_history("https://github.com/bennidi/mbassador", "./pullrequest.csv")

    def test_graph(self):
        g = Graph()
        csv_path = "./pullrequest.csv"
        res = g.build_from_csv(csv_path)
        print(res)

    def test_graph_calc(self):
        import json
        d = {'FlorianKirmaier': {'bennidi': 1.6183970271856054},
             'bennidi': {'FlorianKirmaier': 1.6183970271856054, 'manish364824': 1.1480539800508507,
                         'dependabot[bot]': 1.1480539800508507, 'kolybelkin': 1.4769064053761005,
                         'chriskingnet': 1.0421847193323623, 'kashike': 2.0552818750635637,
                         'leif81': 2.2180536162534716, 'yaronyam': 2.639931144985578,
                         'ToddCostella': 0.5999413260316839, 'arne-vandamme': 0.3159006454136515,
                         'georgekankava': 0.6498141991003324, 'nikoliazekter': 0.7222014735771562,
                         'cpw': 0.8821239976530413, 'davidsowerby': 3.4675909720320757,
                         'cyberoblivion': 1.0392333268140037, 'dorkbox': 3.939993283964354,
                         'bdavisx': 0.5072853510659104, 'durron597': 3.9819284177586542,
                         'Rossi1337': 0.8137070438490125, 'wkritzinger': 0.432231566594954,
                         'staale': 0.40925092900449833, 'bigbear3001': 0.37869157050655194,
                         'o-nix': 0.40558380598474475, 'lennartj': 0.7756448269117935, 'spadge4711': 0.5953060825347154,
                         'KenFromNN': 0.14539878740465484, 'merjadok': 0.5813612360649325},
             'manish364824': {'bennidi': 1.1480539800508507}, 'dependabot[bot]': {'bennidi': 1.1480539800508507},
             'kolybelkin': {'bennidi': 1.4769064053761005}, 'eduardoestrella': {},
             'kashike': {'bennidi': 2.0552818750635637}, 'Ktar5': {}, 'chriskingnet': {'bennidi': 1.0421847193323623},
             'toukovk': {}, 'bryant1410': {}, 'bgroenks96': {}, 'leif81': {'bennidi': 2.2180536162534716},
             'yaronyam': {'bennidi': 2.639931144985578, 'bwzhang2011': 0.007892089313757029},
             'bwzhang2011': {'yaronyam': 0.007892089313757029}, 'ToddCostella': {'bennidi': 0.5999413260316839},
             'arne-vandamme': {'dnault': 0.6642382163113631, 'bennidi': 0.3159006454136515},
             'dnault': {'arne-vandamme': 0.6642382163113631}, 'georgekankava': {'bennidi': 0.6498141991003324},
             'nikoliazekter': {'bennidi': 0.7222014735771562, 'tbee': 0.1677173009974575},
             'tbee': {'nikoliazekter': 0.1677173009974575}, 'cpw': {'bennidi': 0.8821239976530413},
             'davidsowerby': {'bennidi': 3.4675909720320757, 'ghost': 0.5627811460981811},
             'cyberoblivion': {'bennidi': 1.0392333268140037}, 'dorkbox': {'bennidi': 3.939993283964354},
             'ghost': {'davidsowerby': 0.5627811460981811}, 'bdavisx': {'bennidi': 0.5072853510659104},
             'durron597': {'bennidi': 3.9819284177586542}, 'Rossi1337': {'bennidi': 0.8137070438490125},
             'wkritzinger': {'bennidi': 0.432231566594954}, 'staale': {'bennidi': 0.40925092900449833},
             'bigbear3001': {'bennidi': 0.37869157050655194}, 'o-nix': {'bennidi': 0.40558380598474475},
             'lennartj': {'bennidi': 0.7756448269117935}, 'spadge4711': {'bennidi': 0.5953060825347154},
             'KenFromNN': {'md-5': 0.3549775083121455, 'bennidi': 0.14539878740465484},
             'md-5': {'KenFromNN': 0.3549775083121455}, 'merjadok': {'bennidi': 0.5813612360649325}}
        for a in d.keys():
            for b in d[a]:
                if d[a][b] != d[b][a]:
                    print(a, b)
        res = json.dumps(d)
        print(res)

    def test_get_collaboration_score_normal(self):
        g = Graph()
        g.vertices = {"A": {"B": 1.0, "C": 2.0, "D": 3.0}, "B": {"A": 1.0, "D": 4.0}, "C": {"A": 2.0, "D": 5.0},
                      "D": {"A": 3.0, "B": 4.0, "C": 5.0,}}
        res = get_collaboration_score(g, ["A", "B", "C", "D"])
        self.assertEqual(res, 15.0)


if __name__ == '__main__':
    unittest.main()
