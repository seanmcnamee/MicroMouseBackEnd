import pandas as pd

PORT_FILE = 'project//movement//userports.csv'
STRAIGHT_CONTROL_FILE_FRAME = 'project//movement//ML//straightdata//'
NEURAL_NETWORK_DATA = 'project//movement//ML//straightdata//weightsandbiasfile.csv'
STRAIGHT_CONTROL_STRUCT = ['left', 'front-left', 'front', 'front-right', 'right', 'back-right', \
                            'back', 'back-left', 'leftMotor', 'rightMotor']
DATA_FILE_HEADER = "rawdatafile"


class FileManager:
    """Deals with the reading/writing to files
    """

    def __init__(self, user='SeanPC', robot_name='FA-20'):
        self.set_user_port_and_files(user, robot_name)


    def set_user_port_and_files(self, user='SeanPC', robot_name='FA-20'):
        """Get the bluetooth port and datafile for the given user and robot

        Args:
            user (str, optional): Who/What machine. Defaults to 'SeanPC'.
            robot_name (str, optional): FA-20 or FA-83. Defaults to 'FA-20'.
        """
        user_ports = pd.read_csv(PORT_FILE)
        self.port = user_ports.loc[user, robot_name]
        self.list_tuple_file = STRAIGHT_CONTROL_FILE_FRAME + str(user_ports.loc[user, DATA_FILE_HEADER])

    def saveToCSV(self, tuple_list):
        """Append the list of 9 tuples used in this run to the CSV file

        Args:
            tuple_list (list of 9-tuples): follows structure of STRAIGHT_CONTROL_STRUCT
        """
        data = pd.DataFrame.from_records(tuple_list, columns=STRAIGHT_CONTROL_STRUCT)
        data.to_csv(self.list_tuple_file, mode='a')
    

def store_weights(layers):
    #Get current records
    perceptron_weights = []
    for i in range(len(layers)):
        perceptron_weights.append(layers[i])
    current_weights = pd.DataFrame.from_records(perceptron_weights)

    
    previous_weights = retrieve_weights()
    previous_weights.update(current_weights)

def retrieve_weights():
    return pd.read_csv(NEURAL_NETWORK_DATA)