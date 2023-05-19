#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from math import radians
from time import sleep
import queue

global fila_coordenadas

fila_coordenadas = queue.Queue()

fila_coordenadas.put((0.0, 0.5))
fila_coordenadas.put((0.5, 0.0))
fila_coordenadas.put((0.0, 0.5))
fila_coordenadas.put((0.5, 0.0))
fila_coordenadas.put((0.0, 1.0))
fila_coordenadas.put((1.0, 0.0))

class TurtleController(Node):
    def __init__(self):
        super().__init__('turtle_controller')
        self.publisher_ = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)
        self.timer_ = self.create_timer(0.1, self.move_turtle)
        self.move_forward = Twist() # responsável por fazer a tartagura ir para frente
        self.turn = Twist() # responsável por fazer a tartaruga virar
        self.start_coodinates = (0.0, 0.0)

        self.fila_coordenadas = queue.Queue()

    def calculate_distance(self, x, y):
        # Cálculo da distância entre dois pontos
        x_inicial = self.start_coodinates[0]
        y_inicial = self.start_coodinates[1]
        distancia = ((x - x_inicial)**2 + (y - y_inicial)**2)**0.5

        return distancia
    
    def move_turtle(self):
        self.move_forward.linear.x = 0.2 # parâmetro do avanço da tartatura
        self.turn.linear.x = 0.0 # parâmetro nulo para o giro da tartaruga
        self.turn.angular.z = radians(45) # definição de grandeza angular para o giro da tartaruga

        while True:
            # Laço de repetição que faz a tartagura visitar as coordenadas da fila
            while not fila_coordenadas.empty():
    
                coordenadas = fila_coordenadas.get()
                distancia = self.calculate_distance(coordenadas[0], coordenadas[1])

                self.publisher_.publish(self.move_forward)
                print(distancia[0])
                sleep(int(distancia[0]))

                self.publisher_.publish(self.turn)

                self.publisher_.publish(self.move_forward)
                sleep(int(distancia[1]))

# Função principal
def main(args=None):
    rclpy.init()
    turtle_controller = TurtleController()
    rclpy.spin(turtle_controller)
    turtle_controller.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()