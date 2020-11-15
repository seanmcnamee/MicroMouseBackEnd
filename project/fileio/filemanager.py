import pandas as pd
import numpy as np

PORT_FILE = 'project//movement//userports.csv'
STRAIGHT_CONTROL_FILE_FRAME = 'project//movement//ML//straightdata//'
NEURAL_NETWORK_DATA = 'project//movement//ML//neuralnetworkdata//weightsandbias.csv'
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

    def get_raw_data(self):
        """Get a dataframe with all the data in the csv datafile

        Returns:
            Pandas DataFrame: can be accessed/manipulated/stored back quickly
        """
        return pd.read_csv(self.list_tuple_file)

    def store_raw_data(self, tuple_list):
        """Append the list of 9 tuples used in this run to the CSV file

        Args:
            tuple_list (list of 9-tuples): follows structure of STRAIGHT_CONTROL_STRUCT
        """
        data = pd.DataFrame.from_records(tuple_list, columns=STRAIGHT_CONTROL_STRUCT)
        data.to_csv(self.list_tuple_file, mode='a')
    
def store_weights_and_biases(layersetweights, layersetbiases, sizingTuple):
    """Replace the entire neural network data file with these weights and biases

    Args:
        layersetweights (list of matrices of weights): from all layers
        layersetbiases (list of matrices of biases): from all layers
    """
    weightsmatrix = np.concatenate(layersetweights, axis=1)
    bias_matrix = np.concatenate(layersetbiases, axis=1)
    weights_bias_matrix = np.concatenate((weightsmatrix, bias_matrix), 0)

    data_frame = pd.DataFrame.from_records(weights_bias_matrix.transpose())
    print("Data Frame: ", data_frame)
    store_raw_data(data_frame)
    #TODO make it so that VARYING size weights+biases get added incrementally to the file
    
def store_raw_data(data_frame):
    """Replace the neural network data file with this dataframe

    Args:
        matrix: set of NN weights and biases from each layer
    """
    data_frame.to_csv(NEURAL_NETWORK_DATA)

def retrieve_weights():
    """Get the NN weights and biases stored

    Returns:
        tuple of (weights, biases): entire networks' weights and biases
    """
    full_matrix = np.delete(pd.read_csv(NEURAL_NETWORK_DATA).to_numpy(), 0, axis=1)
    num_of_weights = full_matrix.shape[1]-1
    weights_biases = np.hsplit(full_matrix, np.array([num_of_weights, num_of_weights+1]))
    return (weights_biases[0], weights_biases[1])