import tkinter
import zmq

class connexion_ssh(self) :

    def __init__(self) :
        #ConnectionSSH
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.ipadresse = "tcp://192.168.246.2/9999"
        self.ip = "192.168.246.2"
        self.New_IP = tkinter.StringVar()
        self.New_Port = tkinter.StringVar()

    def Communication(self, command_name, value, clefs) :
        try:
            self.socket.send({"command" : command_name, "val" : value})
            self.socket.setsockopt(zmq.RCVTIMEO, 500)
            self.socket.setsockopt(zmq.LINGER, 0)
            mess = self.socket.recv()
        except zmq.ZMQError as e:
            mess = ""
            print("ERROR : ssh not connected")
            return bool
            #self.button_Connect.configure(text="Not Connected", fg_color='orange')
            print("Err2")
            self.IsConnected = False
            if e.errno == zmq.EAGAIN:
                pass  # no message was ready (yet!)
        # Message reçu de la Rpi pour s'assurer de la connection avec l'arduino
        print(mess)