from search_technique.SearchTechnique import SearchTechnique



class ClassCounter():
    def __init__(self):
        self.st = SearchTechnique()

    def count(self, json_file):
        jClist = self.st.load_repository(json_file, exclude_test=True, exclude_anonymous=True)
        print(f"{json_file.split('/')[-3]} {len(jClist)}")
        return len(jClist)


if __name__ == "__main__":
    cc = ClassCounter()
    repos = ['UltimateRecyclerView', 'ActiveAndroid', 'auto', 'HikariCP',
             'dagger', 'fresco', 'quasar', 'guice', 'ActionBarSherlock',
             'AndroidAsync', 'mockito']
    json_root = "/Users/leichen/experiement_result/MORCoRE2/RQ1/"
    class_num = []
    for each in repos:
       class_num.append(cc.count(f"{json_root}{each}/csv/abs.json"))
    print(sorted(class_num))