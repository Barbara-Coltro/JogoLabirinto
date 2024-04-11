import matplotlib.pyplot as plt
import numpy as np
import threading
import time
import random
import tkinter as tk
from tkinter import messagebox

GAME_SIZE = 10
SCORE_MAX = 2000
SIZE_RANDOM = 100
score = 0

# Criando a matriz tridimensional com valores aleatórios
matrix = np.random.randint(-SIZE_RANDOM*2, SIZE_RANDOM+1, size=(GAME_SIZE, GAME_SIZE, GAME_SIZE))

matrix[0,0,0] = 0

# Posição inicial do cubo principal
cube_position = [0, 0, 0]

# Configuração para desativar todas as teclas de atalho do Matplotlib
plt.rcParams['toolbar'] = 'None'

# Cria a figura inicial
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Configurações da plotagem inicial
ax.set_xlim(0, GAME_SIZE)
ax.set_ylim(0, GAME_SIZE)
ax.set_zlim(0, GAME_SIZE)
ax.xaxis.set_ticklabels([])
ax.yaxis.set_ticklabels([])
ax.zaxis.set_ticklabels([])
ax.set_xticks(range(0, GAME_SIZE))
ax.set_yticks(range(0, GAME_SIZE))
ax.set_zticks(range(0, GAME_SIZE))
data = np.zeros((GAME_SIZE, GAME_SIZE, GAME_SIZE), dtype=np.bool_)
voxel = ax.voxels(data)

# Posição inicial do cubo aleatório (vermelho)
random_cube_position = [random.randint(0, GAME_SIZE - 1),
                        random.randint(0, GAME_SIZE - 1),
                        random.randint(0, GAME_SIZE - 1)]

# Lista de posições visitadas
visited_positions = []

# Função para desenhar os cubos
def draw_cubes():
    global visited_positions
    ax.clear()
    
    # Configurações da plotagem
    ax.set_xlim(0, GAME_SIZE)
    ax.set_ylim(0, GAME_SIZE)
    ax.set_zlim(0, GAME_SIZE)
    ax.xaxis.set_ticklabels([])
    ax.yaxis.set_ticklabels([])
    ax.zaxis.set_ticklabels([])
    ax.set_xticks(range(0, GAME_SIZE))
    ax.set_yticks(range(0, GAME_SIZE))
    ax.set_zticks(range(0, GAME_SIZE))
    
    # Criação do voxel do cubo aleatório (vermelho)
    random_cube_data = np.zeros((GAME_SIZE, GAME_SIZE, GAME_SIZE), dtype=np.bool_)
    random_cube_data[random_cube_position[0], random_cube_position[1], random_cube_position[2]] = True
    ax.voxels(random_cube_data, facecolors='red')
    
    # Criação do voxel do cubo principal
    data = np.zeros((GAME_SIZE, GAME_SIZE, GAME_SIZE), dtype=np.bool_)
    for position in visited_positions:
        data[position[0], position[1], position[2]] = True
    ax.voxels(data, facecolors='lightblue')

    # Destaca a posição atual do cubo principal
    current_position_data = np.zeros((GAME_SIZE, GAME_SIZE, GAME_SIZE), dtype=np.bool_)
    current_position_data[cube_position[0], cube_position[1], cube_position[2]] = True
    ax.voxels(current_position_data, facecolors='blue')

    # Atualiza a plotagem
    plt.draw()

# Função para verificar se uma jogada é válida
def is_valid_move(new_position):
    return all(0 <= coord < GAME_SIZE for coord in new_position)

def generate_greedy_move():
    global cube_position, visited_positions, score
    
    # Lista de possíveis movimentos
    possible_moves = []
    
    # Verifica todas as posições vizinhas
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            for dz in [-1, 0, 1]:
                # Ignora o movimento que mantém a posição atual
                if dx == dy == dz == 0:
                    continue
                new_position = [cube_position[0] + dx, cube_position[1] + dy, cube_position[2] + dz]
                # Verifica se o movimento é válido e se a nova posição já foi visitada
                if is_valid_move(new_position) and new_position not in visited_positions:
                    possible_moves.append((new_position, matrix[new_position[0], new_position[1], new_position[2]]))
    
    # Se não houver movimentos possíveis, retorna para a posição inicial
    if not possible_moves:
        new_position = [0, 0, 0]
    else:
        # Escolhe o próximo movimento baseado na pontuação
        new_position = max(possible_moves, key=lambda x: x[1])[0]
    
    # Atualiza a posição do cubo principal e registra a nova posição visitada
    cube_position = new_position
    visited_positions.append(cube_position)
    
    score += matrix[new_position[0], new_position[1], new_position[2]]
    
    draw_cubes()

last_position = cube_position.copy()

def generate_backtrack_move():
    global cube_position, visited_positions, score, last_position

    # Lista de possíveis movimentos
    possible_moves = []

    # Verifica todas as posições vizinhas
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            for dz in [-1, 0, 1]:
                new_position = [cube_position[0] + dx, cube_position[1] + dy, cube_position[2] + dz]
                # Verifica se o movimento é válido e se a nova posição já foi visitada
                if is_valid_move(new_position) and new_position not in visited_positions:
                    possible_moves.append((new_position, matrix[new_position[0], new_position[1], new_position[2]]))

    # Se não houver movimentos possíveis, retorna para a posição inicial
    if not possible_moves:
        new_position = [0, 0, 0]
    else:
        # Escolhe aleatoriamente um dos movimentos possíveis
        new_position = random.choice(possible_moves)[0]

    # Atualiza a posição do cubo principal e registra a nova posição visitada
    cube_position = new_position
    visited_positions.append(last_position)
    last_position = new_position

    score += matrix[new_position[0], new_position[1], new_position[2]]

    draw_cubes()

# Função para verificar se o cubo principal encontrou o cubo aleatório
def check_if_cube_found():
    if score >= SCORE_MAX:
        messagebox.showinfo("Parabéns!", "Você atingiu mais que {}.".format(SCORE_MAX))
        plt.close()  # Fecha a janela da plotagem
    elif score <= -SCORE_MAX:
        messagebox.showinfo("Perdeu!", "Sua pontuação é menor que {}.".format(-SCORE_MAX))
        plt.close()  # Fecha a janela da plotagem
    elif cube_position == random_cube_position:
        messagebox.showinfo("Parabéns!", "Você encontrou o cubo vermelho.")
        plt.close()  # Fecha a janela da plotagem

# Função para gerar movimentos aleatórios em intervalos de tempo
def generate_moves():
    while True:
        generate_greedy_move()
        #generate_backtrack_move()
        check_if_cube_found()
        time.sleep(0.75)  # Ajuste o intervalo de tempo conforme necessário

def score_board():
    root = tk.Tk()
    root.title("Score")
    score_label = tk.Label(root, text="Score: 0")
    score_label.pack()
    while True:
        score_label.config(text="Score: {}".format(score))
        root.update()
        time.sleep(0.5)

# Inicia a thread para gerar movimentos aleatórios
thread = threading.Thread(target=generate_moves)
thread.daemon = True  # Permite que a thread seja encerrada quando o programa principal terminar
thread.start()

thread2 = threading.Thread(target=score_board)
thread2.daemon = True  # Permite que a thread seja encerrada quando o programa principal terminar
thread2.start()

# Inicializa a plotagem com os cubos na posição inicial
draw_cubes()

# Mantém o programa principal em execução
plt.show()
