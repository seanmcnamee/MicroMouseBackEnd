import pandas as pd
import numpy as np

PORT_FILE = 'project//movement//userports.csv'
STRAIGHT_CONTROL_FILE_FRAME = 'project//movement//ML//straightdata//'
NEURAL_NETWORK_DATA = 'project//movement//ML//neuralnetworkdata//weightsandbias.csv'
SENSOR_MAX_FILE = 'project//movement//ML//neuralnetworkdata//maxreadings.csv'
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
    
def store_weights_and_biases(layersetweights, layersetbiases):
    """Replace the entire neural network data file with these weights and biases

    Args:
        layersetweights (list of matrices of weights): from all layers
        layersetbiases (list of matrices of biases): from all layers
    """
    #weightsmatrix = np.concatenate(layersetweights, axis=1)
    #bias_matrix = np.concatenate(layersetbiases, axis=1)
    #weights_bias_matrix = np.concatenate((weightsmatrix, bias_matrix), 0)
    
    for i in range(0, len(layersetweights)):
        weights_bias_matrix = np.concatenate((layersetweights[i], layersetbiases[i]), 0)
        data_frame = pd.DataFrame.from_records(weights_bias_matrix.transpose())
        print("Data Frame", i, ": ", data_frame)
        store_raw_data(data_frame, first=i==0)
    #TODO make it so that VARYING size weights+biases get added incrementally to the file
    
def store_raw_data(data_frame, first=False):
    """Replace the neural network data file with this dataframe

    Args:
        matrix: set of NN weights and biases from each layer
    """
    data_frame.to_csv(NEURAL_NETWORK_DATA, mode='w' if first else 'a')

def retrieve_weights(sizingTuple):
    """Get the NN weights and biases stored

    Returns:
        tuple of (weights, biases): entire networks' weights and biases
    """

    '''
    full_matrix = np.delete(pd.read_csv(NEURAL_NETWORK_DATA).to_numpy(), 0, axis=1)
    num_of_weights = full_matrix.shape[1]-1
    weights_biases = np.hsplit(full_matrix, np.array([num_of_weights, num_of_weights+1]))'''
    full_nparr = np.delete(pd.read_csv(NEURAL_NETWORK_DATA).to_numpy(), 0, axis=1)
    weights = []
    biases = []
    rowStart = 0
    for i in range(len(sizingTuple)):
        single_layer = full_nparr[rowStart:rowStart+sizingTuple[i][1]]
        single_layer = np.hsplit(single_layer, np.array([sizingTuple[i][0], sizingTuple[i][0]+1]))
        weights.append(single_layer[0].transpose())
        biases.append(single_layer[1].transpose())
        rowStart += sizingTuple[i][1] + 1
    return (weights, biases)
    #return (weights_biases[0], weights_biases[1])

def retrieve_highest_sensors():
    return tuple(pd.read_csv(SENSOR_MAX_FILE).to_numpy()[0][1:])

def store_highest_data(tuple_list):
    current_largest = retrieve_highest_sensors()
    largest_tuple = (max(tuple_list[i], current_largest[i]) for i in range(len(tuple_list)))


    data = pd.DataFrame.from_records([largest_tuple], columns=STRAIGHT_CONTROL_STRUCT[:-2])
    data.to_csv(SENSOR_MAX_FILE, mode='w')
