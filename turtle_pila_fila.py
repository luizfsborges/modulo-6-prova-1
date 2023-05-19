import queue
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from math import radians
from time import sleep

global fila_coordenadas

fila_coordenadas = queue.Queue()

fila_coordenadas.put((0.0, 0.5))
fila_coordenadas.put((0.5, 0.0))
fila_coordenadas.put((0.0, 0.5))
fila_coordenadas.put((0.5, 0.0))
fila_coordenadas.put((0.0, 1.0))
fila_coordenadas.put((1.0, 0.0))

while not fila_coordenadas.empty():
    print(fila_coordenadas.get())
   
class TurtleController(Node):
    def __init__(self):
        print("1")
        super().__init__('turtle_controller')
        print("2")
        self.publisher_ = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)
        print("3")
        #self.timer_ = self.create_timer(0.1, self.move_2_coordinates)
        self.move_2_coordinates(fila_coordenadas)
        print("4")
        self.move_forward = Twist()
        print("5")
        self.move_forward.linear.x = 1.0
        print("6")

        self.move_forward.angular.z = 0.0
        print("7")
        self.start_coodinates = (0.0, 0.0)



    def calculate_distance(self, x, y):
        # Cálculo da distância entre dois pontos
        x_inicial = self.start_coodinates[0]
        y_inicial = self.start_coodinates[1]
        distancia = ((x - x_inicial)**2 + (y - y_inicial)**2)**0.5

        return distancia
    
    def move_frente(self, distancia):
        # Move a tartaruga para frente
        self.move_forward.linear.x = 1.0
        self.publisher_.publish(self.move_forward)
        sleep(distancia)
        self.move_forward.linear.x = 0.0
        self.publisher_.publish(self.move_forward)
        print("Indo pra frente")

    # Itera sobre a fila de coordenadas e move a tartaruga para cada coordenada
    def move_2_coordinates(self, fila_coordenadas):
        print("UIII")
        while not fila_coordenadas.empty():
            print("HU<<<<")
            coordenadas = fila_coordenadas.get()
            distancia = self.calculate_distance(coordenadas[0], coordenadas[1])
            self.move_frente(5)
            print("UI")
            self.turnar(coordenadas[0], coordenadas[1])
            self.start_coodinates = coordenadas
            print("Ha")
       

# Função principal
def main(args=None):
    rclpy.init()
    print("A")
    turtle_controller = TurtleController()
    print("B")
    rclpy.spin(turtle_controller)
    print("C")
    turtle_controller.destroy_node()
    print("D")
    rclpy.shutdown()
    print("E")


if __name__ == '__main__':
    main()







