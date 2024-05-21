# ekf_module.py
import numpy as np
from filterpy.kalman import ExtendedKalmanFilter as EKF

def H_jacobian(x):
    return np.eye(len(x))

def hx(x):
    return x

def fx(x, dt):
    return x  # Örneğinizi ve dinamik modelinizi buraya uygulayın

class EKFDataFusion:
    def __init__(self, initial_state, P=None, R=None, Q=None, dt=1.0):
        self.ekf = EKF(dim_x=len(initial_state), dim_z=len(initial_state))
        self.ekf.x = np.array(initial_state)  # Başlangıç durumu
        
        # Hata kovaryans matrisleri
        self.ekf.P = np.eye(len(initial_state)) * 500 if P is None else P
        self.ekf.R = np.eye(len(initial_state)) * 5 if R is None else R
        self.ekf.Q = np.eye(len(initial_state)) if Q is None else Q
        
        self.dt = dt
    
    def update(self, measurement):
        self.ekf.predict_update(measurement, HJacobian=H_jacobian, Hx=hx, args=(self.dt,), Fx=fx)
        return self.ekf.x, self.ekf.P

# End of ekf_module.py
