import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt
import pickle

def run(episodes, is_training=True, render=False):

    env = gym.make('FrozenLake-v1', map_name="8x8", is_slippery=True, render_mode='human' if render else None)

    if(is_training):
         q = ...#________ Inicializujte prázdnou tabulku se všemi states a možnými akcemi (64 x 4)
    else:
        f = open('frozen_lake8x8.pkl', 'rb')
        q = pickle.load(f)
        f.close()

    learning_rate_a = 0.9 # Alpha / Learning Rate
    discount_factor_g = 0.9 # Gamma / Discount Rate. Near 0: Větší focus na přítomnosti. Near 1: Předpovídání budoucí cesty.
    epsilon =  ...        # 1 = 100% Náhodné Akce, 0 = jede kompletně jen z QTablu
    epsilon_decay_rate = ...        # Decay rate epsilonu --> Zmenšování náhodnosti každou episodu. 1/0.0001 = 10,000
    rng = ...   # Inicializujte numpy random generator s default rng

    rewards_per_episode = np.zeros(episodes)

    for i in range(episodes):
        state = env.reset()[0]  # states: 0 to 63, 0=vlevo nahoře,63=vpravo dole
        terminated = False      # True když spadne do díry nebo vyhraje
        truncated = False       # True když actions > 200

        while(not terminated and not truncated):
            if is_training and rng.random() < epsilon:
                action = env.action_space.sample() # Akce: 0=vlevo,1=dolu,2=doprava,3=nahoru
            else:
                action = np.argmax(q[state,:])

            ... = env.step(action) #vyvoříte nové proměné new_state,reward,terminated,truncated,_ z env.step(action) --> vaše akce

            if is_training:
                q[state,action] = q[state,action] + learning_rate_a * (
                    reward + discount_factor_g * np.max(q[new_state,:]) - q[state,action]
                )

            state = ... #setnutí nového state do state proměné

        epsilon = ... #decay epsilonu kalkulace

        if(epsilon==0):
            learning_rate_a = 0.0001


        #pokud reward bude 1, označí to rewards_per_episode[i] na 1 (aka: Odmění episodu)
        ...

    env.close()

    sum_rewards = np.zeros(episodes)
    for t in range(episodes):
        sum_rewards[t] = np.sum(rewards_per_episode[max(0, t-100):(t+1)])
    plt.plot(sum_rewards)
    plt.savefig('frozen_lake8x8.png')

    if is_training:
        f = open("frozen_lake8x8.pkl","wb")
        pickle.dump(q, f)
        f.close()

if __name__ == '__main__':
    # Rozjedte funkci
