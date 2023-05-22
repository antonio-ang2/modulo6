# Importações de bibliotecas:

import csv
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from collections import deque
from tf_transformations import euler_from_quaternion

# csv: Biblioteca para trabalhar com arquivos CSV.
# rclpy: Biblioteca do ROS 2 para desenvolver aplicativos em Python para robôs.
# Node da biblioteca rclpy.node: Classe base para criar um nó no ROS 2.
# Twist e Odometry do pacote geometry_msgs.msg e nav_msgs.msg, respectivamente: Mensagens do ROS 2 que contêm informações de pose e velocidade para o controle do robô.
# deque da biblioteca collections: Estrutura de dados de fila.
# euler_from_quaternion da biblioteca tf_transformations: Função para converter uma representação de orientação quaternion em ângulos de Euler.

MAX_DIFF = 0.1
#Constante definida com o valor de 0.1, usada para verificar a igualdade entre poses.Como dito no vídeo, nenhum sensor é 100% preciso, aqui estamos setando o erro aceitável de diferença entre posições.



class Pose:
    def __init__(self, x=0.0, y=0.0, theta=0.0):
        self.x = x
        self.y = y
        self.theta = theta

    def __repr__(self):
        return f"(x={self.x:.2f}, y={self.y:.2f}, theta={self.theta:.2f})"

    def __add__(self, other):
        return Pose(self.x + other.x, self.y + other.y, self.theta + other.theta)

    def __sub__(self, other):
        return Pose(self.x - other.x, self.y - other.y, self.theta - other.theta)

    def __eq__(self, other):
        return abs(self.x - other.x) < MAX_DIFF and abs(self.y - other.y) < MAX_DIFF

#A classe Pose é definida para representar uma pose no espaço 2D. Ela possui atributos para coordenadas x, y e ângulo theta. A classe também implementa métodos especiais para representação de string, adição e subtração de poses e comparação de igualdade.

class MissionControl(deque):
    def __init__(self, csv_file="pontos.csv"):
        super().__init__()
        with open(csv_file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            for row in csv_reader:
                new_pose = Pose()
                new_pose.x, new_pose.y = [float(x) for x in row]
                self.append(new_pose)

#A classe MissionControl é definida como uma subclasse de deque. Ela é responsável por ler um arquivo CSV contendo os pontos da missão e armazená-los em uma fila. A classe possui um construtor que lê o arquivo CSV e adiciona cada ponto como uma instância da classe Pose na fila.


class TurtleController(Node):
    def __init__(self, mission_control, control_period=0.02):
        super().__init__('turtle_controller')
        self.pose = Pose(x=-40.0)
        self.setpoint = Pose(x=-40.0)
        self.mission_control = mission_control
        self.publisher = self.create_publisher(Twist, "/cmd_vel", qos_profile=10)
        self.subscription = self.create_subscription(Odometry, "/odom", self.pose_callback, qos_profile=10)
        self.control_timer = self.create_timer(control_period, self.control_callback)
#A classe TurtleController é responsável por controlar o robô simulado para seguir os pontos da missão. A classe possui um construtor que recebe uma instância de MissionControl e um período de controle (control_period). No construtor, são criados um publicador para o tópico "/cmd_vel" (usado para enviar comandos de velocidade para a tartaruga) e uma subscrição para o tópico "/odom" (usado para receber informações de odometria da tartaruga). Também é criado um temporizador que chama a função control_callback a cada período de controle.


    def control_callback(self):
        if self.pose.x == -40.0:
            self.get_logger().info("Aguardando primeira pose...")
            return
        msg = Twist()
        x_diff = self.setpoint.x - self.pose.x
        y_diff = self.setpoint.y - self.pose.y
        if self.pose == self.setpoint:
            msg.linear.x, msg.linear.y = 0.0, 0.0
            self.update_setpoint()
        if abs(y_diff) > MAX_DIFF:
            msg.linear.y = 0.5 if y_diff > 0 else -0.5
        else:
            msg.linear.y = 0.0
        if abs(x_diff) > MAX_DIFF:
            msg.linear.x = 0.5 if x_diff > 0 else -0.5
        else:
            msg.linear.x = 0.0
        self.publisher.publish(msg)

    def update_setpoint(self):
        try:
            self.setpoint = self.pose + self.mission_control.popleft()
            self.get_logger().info(f"Chegou em {self.pose}, indo para {self.setpoint}")
        except IndexError:
            self.get_logger().info("Fim da jornada!")
            exit()

    def pose_callback(self, msg: Odometry):
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        _, _, theta = euler_from_quaternion([msg.pose.pose.orientation.x, msg.pose.pose.orientation.y, msg.pose.pose.orientation.z, msg.pose.pose.orientation.w])
        self.pose = Pose(x=x, y=y, theta=theta)
        if self.setpoint.x == -40.0:
            self.update_setpoint()
#O método control_callback é chamado a cada período de controle. Ele calcula a diferença entre a pose atual do robô simulado e o ponto de referência. Se a pose atual for igual ao setpoint, um novo setpoint é atualizado e enviado para o robô. Caso contrário, são definidos os comandos de velocidade linear (msg.linear.x) e linear (msg.linear.y) com base nas diferenças de coordenadas x e y. Os comandos de velocidade são publicados no tópico "/cmd_vel".

#O método pose_callback é chamado sempre que uma nova mensagem de odometria é recebida no tópico "/odom". Ele extrai as coordenadas x, y e o ângulo theta da mensagem de odometria e atualiza a pose atual da tartaruga. Se o setpoint atual for igual a -40.0 (valor inicial), o método update_setpoint é chamado para definir o primeiro setpoint.


def main(args=None):
    rclpy.init(args=args)
    mc = MissionControl()
    tc = TurtleController(mc)
    rclpy.spin(tc)
    tc.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
