from filterpy.kalman import ExtendedKalmanFilter
import numpy as np

class kalmanfilter:
    def __init__(self):
        #initialize the ekf object
        self.ekf = ExtendedKalmanFilter(dim_x=4, dim_z=2)
        #initialize the state transition matrix
        self.ekf.F = np.array([[1., 1., 0., 0.],
                               [0., 1., 0., 0.],
                               [0., 0., 1., 1.],
                               [0., 0., 0., 1.]])
        #initialize the measurement function
        self.ekf.H = np.array([[1., 0., 0., 0.],
                               [0., 0., 1., 0.]])
        #initialize the process noise covariance
        self.ekf.Q *= 0.01
        #initialize the measurement noise covariance
        self.ekf.R = np.array([[5., 0.],
                               [0., 5.]])
        #initialize the state covariance
        self.ekf.P *= 1000.
        #initialize the state
        self.ekf.x = np.array([[0., 0., 0., 0.]]).T

    def update(self, z):
        self.ekf.update(z)

    def predict(self):
        self.ekf.predict()

    def get_state(self):
        return self.ekf.x

    def set_state(self, x):
        self.ekf.x = x

    def set_state_covariance(self, P):
        self.ekf.P = P

    def get_state_covariance(self):
        return self.ekf.P

    def set_process_noise_covariance(self, Q):
        self.ekf.Q = Q

    def get_process_noise_covariance(self):
        return self.ekf.Q

    def set_measurement_noise_covariance(self, R):
        self.ekf.R = R

    def get_measurement_noise_covariance(self):
        return self.ekf.R

    def set_state_transition_matrix(self, F):
        self.ekf.F = F

    def get_state_transition_matrix(self):
        return self.ekf.F

    def set_measurement_function(self, H):
        self.ekf.H = H

    def get_measurement_function(self):
        return self.ekf.H