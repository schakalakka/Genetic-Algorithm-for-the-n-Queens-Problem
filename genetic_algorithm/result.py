from genetic_algorithm import main


def result():
    time = 0
    for i in [0, 50]:
        main();
        time += main[1]
    time = time/i
    print(time)
    return time
