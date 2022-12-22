def get_command(algorithm, repo_name, iteration, platform):
    return f"nohup python3 {algorithm}.py {repo_name} {iteration} {platform} >search_log/{repo_name}_{algorithm}.out 2>&1 &"


# run all algorithms for a repository by setting repo_name, platform, iteration number
def all_ga(repo_name, iteration, platform):
    algorithms = ["Nsga3RE", "Nsga3NRE", "NsgaiiRE", "NsgaiiNRE", "RandomSearchRE"]
    res = []
    for each in algorithms:
        res.append(get_command(each, repo_name, iteration, platform))
    return res


# run all algorithms for a repository for 5 times by setting repo_name, platform, iteration number
def five_runs(repo_name, iteration, platform):
    command = f"nohup python3 command.py -m search -n {repo_name} -i {iteration} -p {platform} >command_log/{repo_name}.out 2>&1 &"
    return command


def search_titan(repo_name, iteration, output_num):
    command = f"nohup python3 command.py -m search_titan -n {repo_name} -i {iteration} -p titan -d {output_num} >command_log/{repo_name}{output_num}.out 2>&1 &"
    return command


def search_thor(repo_name, iteration, output_num):
    command = f"nohup python3 command.py -m search_thor -n {repo_name} -i {iteration} -p thor -d {output_num} >command_log/{repo_name}{output_num}.out 2>&1 &"
    return command


def scp_command(repo_name):
    command = f'scp -r "/Users/leichen/experiement_result/MORCoRE2/1st_test_output/{repo_name}" "chenlei@titan:/home/chenlei/MORCoRE/dataset/{repo_name}"'
    return command


def scp_command_thor(repo_name):
    # command = f'scp -r "/home/salab/chenlei/project/MORCoRE/dataset/{repo_name}" "/Users/leichen/experiement_result/MORCoRE2/1st_test_output/{repo_name}" '
    command = f'scp -r  "/Users/leichen/experiement_result/MORCoRE2/1st_test_output/{repo_name}" "chenlei@thor:/home/salab/chenlei/project/MORCoRE/dataset/{repo_name}"'
    return command


def scp_download(repo_name, platform, output_num):
    local_store_path = "/Users/leichen/experiement_result/MORCoRE2/output/"
    if platform == "thor":
        command = f'scp "chenlei@thor:/home/salab/chenlei/project/MORCoRE/dataset/{repo_name}/output{output_num}/{repo_name}/*" "{local_store_path}{repo_name}/output{output_num}"'
    elif platform == "valkyrie":
        command = f'scp "chenlei@valkyrie:/home/chenlei/projects/master_thesis/dataset/mailmapBuilt/{repo_name}/MORCoRE/output{output_num}/{repo_name}/*" "{local_store_path}{repo_name}/output{output_num}"'
    elif platform == "titan":
        command = f'scp "chenlei@titan:/home/chenlei/MORCoRE/dataset/{repo_name}/output{output_num}/{repo_name}/*" "{local_store_path}{repo_name}/output{output_num}"'
    return command


if __name__ == "__main__":
    # #all_ga
    # repo_name = "titan"
    # platform = "valkyrie"
    # iteration = 120000
    # res = all_ga(repo_name,iteration, platform)
    # for each in res:
    #     print(each)

    repo_iteration_dict = {
        'UltimateRecyclerView': 45000,
        'auto': 25000,
        'HikariCP': 20000,
        'dagger': 22000,
        'fresco': 110000,
        'quasar': 89000,
        'guice': 82000,
        'ActionBarSherlock': 48000,
        'AndroidAsync': 46000,
        'mockito': 80000
    }
    # for each in repo_iteration_dict.keys():
    # # run_five
    #     print(five_runs(each, repo_iteration_dict[each], "valkyrie"))
        # search_titan/ thor
        # for output_num in range(1,6):
            # print(search_titan(each,int(repo_iteration_dict[each]/2),output_num))
            # print(search_thor(each,int(repo_iteration_dict[each]/2),output_num))

    # repos = ['UltimateRecyclerView', 'ActiveAndroid', 'auto', 'HikariCP',
    #          'dagger', 'fresco', 'quasar', 'guice', 'ActionBarSherlock',
    #          'AndroidAsync', 'mockito']
    #
    # # 11/29 16:50 valkyrie
    # repos = ['HikariCP', 'dagger', 'ActionBarSherlock', 'AndroidAsync', 'mockito']
    #
    # # 11/29 20:56 valkyrie
    # repos2 = ['auto']
    #
    # # 11/30 9:16 titan
    # repos2 = ['UltimateRecyclerView']
    #
    # # 11/30 9:22 valkyrie
    # repos2 = ['guice']
    #
    # # 12/1 10:34 titan
    # repos2 = ['quasar']
    #
    # # 12/1 14:11 thor
    repos2 = ['auto']
    # # scp
    for each in repos2:
        # print(scp_command_thor(each))
        for i in range(1, 6):
            print(scp_download(each, "thor", i))
