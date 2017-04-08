from Model import Model

size = 100
empty_ratio = 0.2
similarity = 0.5
step = 20

def run_without_pause():
    # chay 20 step xong dung va hien thi ket qua
    for i in range(step):
        if not model.is_happy():
            model.step()
    model.plot_grid()

def run():
    # chay va hien thi ket qua tung step
    for i in range(step):
        if not model.is_happy():
            model.step()
            raw_input("Press Enter to continue...")
            model.plot_grid()

def run_with_save():
    # lam theo yeu cau cua bai tap giao su cho:
    # Your simulation runs as follows:
    # Plot the initial grid as a heat-map.
    # Plot the initial distribution of the happiness in your city.
    # Iterate over 4) 20 times
    # Calculate happiness for each agent. Relocate an unhappy agent to a random empty cell.
    # Plot the final grid as a heat-map.
    # Plot the final distribution of the happiness in your city.

    model.plot_grid(True, "initial.png") # plot initial
    model.plot_happiness("happiness.png") # Plot the initial distribution of the happiness in your city.
    for i in range(step): # Iterate over 4) 20 times
        if not model.is_happy():
            model.step()
    model.plot_grid(True, "after20.png") # Plot the final grid as a heat-map.
    model.plot_happiness("after20h.png") # Plot the final distribution of the happiness in your city.


'''MAIN'''
model = Model(size, size, 1 - empty_ratio, similarity)

#run_without_pause()
#run()
run_with_save()

